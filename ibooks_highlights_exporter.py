#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import datetime
import argparse
import re
import frontmatter

from glob import glob
from jinja2 import Environment, FileSystemLoader


PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=True,
    lstrip_blocks=False)


ANNOTATION_DB_PATH = (
    "~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/")
BOOK_DB_PATH = (
    "~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/")


ATTACH_BOOKS_QUERY = """
attach database ? as books
"""


BOOK_LIST_QUERY = """
select 
ZANNOTATIONASSETID, 
count(ZANNOTATIONSELECTEDTEXT), 
books.ZBKLIBRARYASSET.ZTITLE, 
books.ZBKLIBRARYASSET.ZAUTHOR 

from ZAEANNOTATION

left join books.ZBKLIBRARYASSET
on ZAEANNOTATION.ZANNOTATIONASSETID = books.ZBKLIBRARYASSET.ZASSETID

group by 1
"""


NOTE_LIST_QUERY = """
select 
ZANNOTATIONASSETID as assetid, 
ZANNOTATIONREPRESENTATIVETEXT as represent_text, 
ZANNOTATIONSELECTEDTEXT as selected_text, 
ZFUTUREPROOFING5 as chapter, 
ZANNOTATIONSTYLE as style, 
ZANNOTATIONLOCATION as location,
ZANNOTATIONNOTE as note,
books.ZBKLIBRARYASSET.ZTITLE as title, 
books.ZBKLIBRARYASSET.ZAUTHOR as author

from ZAEANNOTATION

left join books.ZBKLIBRARYASSET
on ZAEANNOTATION.ZANNOTATIONASSETID = books.ZBKLIBRARYASSET.ZASSETID

where ZANNOTATIONDELETED = 0

order by ZANNOTATIONASSETID, ZPLLOCATIONRANGESTART;
"""

def get_ibooks_database(_cache=[]):

    if len(_cache) > 0:
        return _cache[0]

    asset_title_tab = {}
    anno_db_path = os.path.expanduser(ANNOTATION_DB_PATH)
    sqlite_file = glob(anno_db_path + "*.sqlite")

    if not sqlite_file:
        print("Couldn't find the iBooks database. Exiting.")
        exit()
    else:
        sqlite_file = sqlite_file[0]

    book_db_path = os.path.expanduser(BOOK_DB_PATH)
    assets_file = glob(book_db_path + "*.sqlite")

    if not assets_file:
        print("Couldn't find the iBooks assets database. Exiting.")
        exit()
    else:
        assets_file = assets_file[0]

    db1 = sqlite3.connect(sqlite_file, check_same_thread=False)
    cursor = db1.cursor()
    cursor.execute(
        ATTACH_BOOKS_QUERY,
        (assets_file,)
    )

    _cache.append(cursor)
    return cursor


def parse_epubcfi(raw):

    if raw is None:
        return []

    parts = raw[8:-1].split(',')
    cfistart = parts[0] + parts[1]

    parts = cfistart.split(':')

    path = parts[0]
    offsets = [ 
        int(x[1:]) 
        for x in re.findall('(/\d+)', path) 
    ]

    if len(parts) > 1:
        offsets.append(int(parts[1]))

    return offsets


def epubcfi_compare(x, y):
    depth = min( len(x), len(y) )
    for d in range(depth):
        if x[d] == y[d]:
            continue
        else:
            return x[d] - y[d]

    return len(x) - len(y)


def query_compare(x, y):
    if x['assetid'] > y['assetid']:
        return 1
    elif x['assetid'] < y['assetid']:
        return -1
    return epubcfi_compare(
        parse_epubcfi(x['location']), 
        parse_epubcfi(y['location'])
    )


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def do_book_list(args):

    #only prints a list of books with highlights and exists
    cur = get_ibooks_database()
    res = cur.execute(BOOK_LIST_QUERY)
    res = sorted(res, key=lambda x: x[1])
    for assetid, count, title, author in res:
        if count > 0:
            print(assetid.ljust(32), count, '\t', title, ',', author)


def do_note_list(args):

    fields = [
        'assetid', 
        'represent_text', 
        'selected_text', 
        'chapter', 
        'style', 
        'location',
        'note',
        'title', 
        'author'
    ]

    cur = get_ibooks_database()
    res = cur.execute(NOTE_LIST_QUERY)
    res = res.fetchall()
    res = [dict(zip(fields, r)) for r in res]

    template = TEMPLATE_ENVIRONMENT.get_template("markdown_template.md")

    books = {}
    for r in res:
        if r['selected_text'] is None:
            continue
        assetid = r['assetid']
        if r['represent_text'] is not None:
            r['represent_text'] = r['represent_text'].strip()
        if assetid not in books:
            books[assetid] = []
        books[assetid].append(r)

    for book in books.values():

        book.sort(key=cmp_to_key(query_compare))

        md = template.render(
            title=book[0]['title'],
            author=book[0]['author'],
            highlights=book,
        )

        fmpost = frontmatter.Post(md, asset_id=book[0]['assetid'])
        fmpost_txt = frontmatter.dumps(fmpost)

        fn = '{}/{}.md'.format(args.dname, book[0]['title'])
        with open(fn, 'wb') as f:
            f.write(fmpost_txt.encode('utf-8'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='iBooks Highlights Exporter')
    parser.add_argument('-o', action="store", default="books", dest="dname",
            help="Specify output directory (default: books)")
    parser.add_argument('--list', action="store_true", help="Lists a books having highlights.")
    args = parser.parse_args()


    if args.list:
        do_book_list(args)

    else:
        if not os.path.exists(args.dname):
            os.makedirs(args.dname)
        do_note_list(args)
