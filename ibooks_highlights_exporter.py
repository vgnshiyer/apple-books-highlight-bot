#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import datetime
import argparse
import re

from glob import glob
from jinja2 import Environment, FileSystemLoader


PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=True,
    lstrip_blocks=False)


asset_title_tab = {}
base1 = "~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/"
base1 = os.path.expanduser(base1)
sqlite_file = glob(base1 + "*.sqlite")

if not sqlite_file:
    print("Couldn't find the iBooks database. Exiting.")
    exit()
else:
    sqlite_file = sqlite_file[0]

base2 = "~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/"
base2 = os.path.expanduser(base2)
assets_file = glob(base2 + "*.sqlite")

if not assets_file:
    print("Couldn't find the iBooks assets database. Exiting.")
    exit()
else:
    assets_file = assets_file[0]

db1 = sqlite3.connect(sqlite_file, check_same_thread=False)
cur1 = db1.cursor()
cur1.execute("""
    attach database ? as books
    """,
    (assets_file,)
)

db2 = sqlite3.connect(assets_file, check_same_thread=False)
cur2 = db2.cursor()


def uniquify(lst):
    return list(set(list))


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
    if x[0] > y[0]:
        return 1
    elif x[0] < y[0]:
        return -1
    return epubcfi_compare(
        parse_epubcfi(x[5]), 
        parse_epubcfi(y[5])
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
    res2 = cur1.execute("""
        select 
        ZANNOTATIONASSETID, 
        count(ZANNOTATIONSELECTEDTEXT), 
        books.ZBKLIBRARYASSET.ZTITLE, 
        books.ZBKLIBRARYASSET.ZAUTHOR 

        from ZAEANNOTATION

        left join books.ZBKLIBRARYASSET
        on ZAEANNOTATION.ZANNOTATIONASSETID = books.ZBKLIBRARYASSET.ZASSETID

        group by 1
    """)
    res2 = sorted(res2, key=lambda x: x[1])
    for assetid, count, title, author in res2:
        if count > 0:
            print(assetid.ljust(32), count, '\t', title, ',', author)
    print()
    for assetid, count, title, author in res2:
        if count == 0 and title is not None:
            print(assetid.ljust(32), count, '\t', title, ',', author)


def do_note_list(args):

    res1 = cur1.execute("""
        select 
        ZANNOTATIONASSETID, 
        ZANNOTATIONREPRESENTATIVETEXT, 
        ZANNOTATIONSELECTEDTEXT, 
        ZFUTUREPROOFING5, 
        ZANNOTATIONSTYLE, 
        ZANNOTATIONLOCATION,
        ZANNOTATIONNOTE,
        books.ZBKLIBRARYASSET.ZTITLE, 
        books.ZBKLIBRARYASSET.ZAUTHOR

        from ZAEANNOTATION

        left join books.ZBKLIBRARYASSET
        on ZAEANNOTATION.ZANNOTATIONASSETID = books.ZBKLIBRARYASSET.ZASSETID
        
        order by ZANNOTATIONASSETID, ZPLLOCATIONRANGESTART;
    """)
    res1 = res1.fetchall()
    res1 = [list(r) for r in res1]

    template = TEMPLATE_ENVIRONMENT.get_template("markdown_template.md")

    books = {}
    for r in res1:
        if r[2] is None:
            continue
        assetid = r[0]
        r[1] = r[1].strip()
        if assetid not in books:
            books[assetid] = []
        books[assetid].append(r)

    for book in books.values():

        book.sort(key=cmp_to_key(query_compare))

        md = template.render(
            title=book[0][7],
            author=book[0][8],
            last="###", 
            highlights=book
        )

        fn = '{}/{}.md'.format(args.dname, book[0][7])
        with open(fn, 'wb') as f:
            f.write(md.encode('utf-8'))


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
