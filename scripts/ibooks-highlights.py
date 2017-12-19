#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from ibooks_highlights.models import BookList
from ibooks_highlights import ibooksdb


def print_book_list(book_list: BookList) -> None:

    books = list(book_list.books.values())
    books = sorted(books, key=lambda b: b.title)

    for book in books:
        print(book)


def write_book_notes(path: str, force: bool=False) -> None:
    book_list.write_modified(path, force)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='iBooks highlights exporter')
    parser.add_argument(
        '-d', action='store', default='.', dest='bookdir',
        help='Specify output directory (default: .)')
    parser.add_argument(
        '--list', action='store_true', 
        help='Lists titles of books with highlights')
    parser.add_argument(
        '--force', action='store_true',
        help='Forces update of books')

    args = parser.parse_args()

    book_list = BookList(args.bookdir)
    annos = ibooksdb.fetch_annotations()
    book_list.populate_annotations(annos)

    if args.list:
        print_book_list(book_list)
    else:
        write_book_notes(args.bookdir, args.force)
