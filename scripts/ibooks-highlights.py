#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pathlib
import click

from ibooks_highlights.models import BookList
from ibooks_highlights import ibooksdb


def get_booklist(path: pathlib.Path) -> BookList:

    book_list = BookList(path)
    annos = ibooksdb.fetch_annotations()
    book_list.populate_annotations(annos)
    return book_list


@click.group()
@click.option('--bookdir', '-b', type=click.Path(exists=True), 
              envvar='IBOOKS_HIGHLIGHT_DIRECTORY')
@click.pass_context
def cli(ctx, bookdir):
    ctx.obj['BOOKDIR'] = pathlib.Path(bookdir)


@cli.command()
@click.pass_context
def list(ctx):

    bookdir = ctx.obj['BOOKDIR']
    bl = get_booklist(bookdir)

    books = bl.books.values()
    books = sorted(books, key=lambda b: b.title)
    for book in books:
        print(book)


@cli.command()
@click.option('--force', '-f', is_flag=True)
@click.pass_context
def sync(ctx, force):

    bookdir = ctx.obj['BOOKDIR']
    bl = get_booklist(bookdir)

    bl.write_modified(bookdir, force)



# def print_book_list(book_list: BookList) -> None:

#     books = list(book_list.books.values())
#     books = sorted(books, key=lambda b: b.title)

#     for book in books:
#         print(book)


# def write_book_notes(path: pathlib.Path, force: bool=False) -> None:
#     book_list.write_modified(path, force)


if __name__ == '__main__':
    cli(obj={})

    # parser = argparse.ArgumentParser(description='iBooks highlights exporter')
    # parser.add_argument(
    #     '-d', action='store', default='.', dest='bookdir',
    #     help='Specify output directory (default: .)')
    # parser.add_argument(
    #     '--list', action='store_true', 
    #     help='Lists titles of books with highlights')
    # parser.add_argument(
    #     '--force', action='store_true',
    #     help='Forces update of books')

    # args = parser.parse_args()
    # bookdir = pathlib.Path(args.bookdir)

    # book_list = BookList(bookdir)
    # annos = ibooksdb.fetch_annotations()
    # book_list.populate_annotations(annos)

    # if args.list:
    #     print_book_list(book_list)
    # else:
    #     write_book_notes(bookdir, args.force)
