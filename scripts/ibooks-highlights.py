#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


if __name__ == '__main__':
    cli(obj={})
