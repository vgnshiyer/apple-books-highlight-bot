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
from slugify import slugify


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

NOTE_LIST_FIELDS = [
    'asset_id', 
    'title', 
    'author',
    'location',
    'selected_text', 
    'note',
    'represent_text', 
    'chapter', 
    'style', 
]

NOTE_LIST_QUERY = """
select 
ZANNOTATIONASSETID as assetid, 
books.ZBKLIBRARYASSET.ZTITLE as title, 
books.ZBKLIBRARYASSET.ZAUTHOR as author,
ZANNOTATIONLOCATION as location,
ZANNOTATIONSELECTEDTEXT as selected_text, 
ZANNOTATIONNOTE as note,
ZANNOTATIONREPRESENTATIVETEXT as represent_text, 
ZFUTUREPROOFING5 as chapter, 
ZANNOTATIONSTYLE as style

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
    if x['asset_id'] > y['asset_id']:
        return 1
    elif x['asset_id'] < y['asset_id']:
        return -1
    return epubcfi_compare(
        parse_epubcfi(x['location']), 
        parse_epubcfi(y['location'])
    )


def query_compare_no_asset_id(x, y):
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


class Annotation(object):

    def __init__(self, location, selected_text=None, note=None,
        represent_text=None, chapter=None, style=None):

        if (selected_text is None) and (note is None):
            print(location)
            print(selected_text)
            print(note)
            print(represent_text)
            print(chapter)
            print(style)
            raise ValueError('specify either selected_text or note')

        self.location = location
        self.selected_text = selected_text
        
        if represent_text is not None:
            represent_text = represent_text.strip()
        self.represent_text = represent_text

        self.chapter = chapter
        self.style = style
        self.note = note

    def __getitem__(self, key):
        return getattr(self, key)


class Book(object):

    def __init__(self, asset_id=None, filename=None):

        args_present = asset_id is not None
        file_present = filename is not None

        if args_present == file_present:
            raise ValueError('specify either asset_id or filename')

        self._annotations = []

        if args_present:
            self._asset_id = asset_id
            self.author = None
            self.title = None
            self._prev_content = None

        if file_present:
            self._process_file(filename)

    def _process_file(self, filename):
        book = frontmatter.load(filename)
        self._asset_id = book['asset_id']
        self.author = book['author']
        self.title = book['title']

        self._prev_content = book.content

    def __str__(self):
        return '{asset_id} {len}\t{title}, {author}'.format(
            asset_id=self._asset_id.ljust(32),
            len=self.num_annotations, 
            title=self.title,
            author=self.author
        )

    @property
    def asset_id(self):
        return self._asset_id

    @property
    def annotations(self):
        return self._annotations

    @annotations.setter
    def annotations(self, anno):
        self._annotations = anno
        self._annotations.sort(key=cmp_to_key(query_compare_no_asset_id))

    @property
    def num_annotations(self):
        return len(self._annotations)

    @property
    def prev_content(self):
        return self._prev_content

    @property
    def content(self):
        template = TEMPLATE_ENVIRONMENT.get_template("markdown_template.md")

        md = template.render(
            title=self._title,
            author=self._author,
            highlights=book,
        )
        return md


class BookList(object):

    def __init__(self, path):

        self._path = path
        self.books = {}

        if os.path.exists(self._path):
            self.books = self._load_books(self._path)

    def _load_books(self, path):
        book_glob  = os.path.join(path, '*.md')
        book_files = glob(book_glob)

        md_books = {}
        for bf in book_files:
            book = Book(filename=bf)
            md_books[book.asset_id] = book

        return md_books

    def get_create_book(self, asset_id):

        if asset_id not in self.books:
            book = Book(asset_id=asset_id)
            self.books[asset_id] = book

        return self.books[asset_id]


def load_markdown_books(args):

    book_glob  = os.path.join(args.dname, '*.md')
    book_files = glob(book_glob)

    md_books = {}
    for bf in book_files:
        book = Book(filename=bf)
        md_books[book.asset_id] = book

    return md_books


def print_book_list(args):

    book_list = BookList(args.dname)

    # only prints a list of books with highlights and exists
    print('=== ibooks database ===')
    cur = get_ibooks_database()
    res = cur.execute(BOOK_LIST_QUERY)
    res = sorted(res, key=lambda x: x[1])
    for assetid, count, title, author in res:
        if count > 0:
            print(assetid.ljust(32), count, '\t', title, ',', author)

    print('\n\n=== filesystem ===')
    for book in book_list.books.values():
        print(book)


def print_book_list_2(args):

    book_list = BookList(args.dname)

    cur = get_ibooks_database()
    res = cur.execute(NOTE_LIST_QUERY)
    res = res.fetchall()
    res = [dict(zip(NOTE_LIST_FIELDS, r)) for r in res]

    res = [
        r
        for r in res
        if r['asset_id'] is not None and
        ((r['selected_text'] is not None) or (r['note'] is not None))
    ]

    for r in res:
        book = book_list.get_create_book(r['asset_id'])
        if book.title is None:
            book.title = r['title']
        if book.author is None:
            book.author = r['author']

    anno_group = {}
    for r in res:
        asset_id = r['asset_id']
        if asset_id not in anno_group:
            anno_group[asset_id] = []

        anno = Annotation(
            location=r['location'], 
            selected_text=r['selected_text'],
            note=r['note'],
            represent_text=r['represent_text'],
            chapter=r['chapter'],
            style=r['style']
        )
        anno_group[asset_id].append(anno)

    for asset_id, anno in anno_group.items():
        book_list.books[asset_id].annotations = anno

    for book in book_list.books.values():
        print(book)


def do_note_list(args):

    fields = [
        'asset_id', 
        'title', 
        'author',
        'location',
        'selected_text', 
        'note',
        'represent_text', 
        'chapter', 
        'style', 
    ]

    cur = get_ibooks_database()
    res = cur.execute(NOTE_LIST_QUERY)
    res = res.fetchall()
    res = [dict(zip(fields, r)) for r in res]

    template = TEMPLATE_ENVIRONMENT.get_template("markdown_template.md")

    books = {}
    for r in res:
        if r['selected_text'] is None and r['note'] is None:
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
        print_book_list_2(args)

    else:
        if not os.path.exists(args.dname):
            os.makedirs(args.dname)
        do_note_list(args)
