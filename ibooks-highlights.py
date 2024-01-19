#!/usr/bin/env python

import pathlib

import click

from ibooks_highlights import ibooksdb
from ibooks_highlights.models import BookList


def get_booklist(path: pathlib.Path) -> BookList:

    book_list = BookList(path)
    annos = ibooksdb.fetch_annotations()
    book_list.populate_annotations(annos)
    return book_list


@click.group()
@click.option(
    "--export-dir",
    "-e",
    type=click.Path(),
    envvar="IBOOKS_HIGHLIGHT_DIRECTORY",
    default="./highlights_data",
)
@click.pass_context
def cli(ctx: click.Context, export_dir: str):

    # create directory if it doesn't exist
    p = pathlib.Path(export_dir)
    p.mkdir(parents=True, exist_ok=True)

    ctx.obj["BOOKDIR"] = p


@cli.command()
@click.pass_context
def list(ctx: click.Context):

    export_dir = ctx.obj["BOOKDIR"]
    bl = get_booklist(export_dir)

    books = [b for b in bl.books.values()]
    books = sorted(books, key=lambda b: b.title)
    for book in books:
        print(book)


@cli.command()
@click.option("--force", "-f", is_flag=True)
@click.pass_context
def sync(ctx: click.Context, force: bool):

    export_dir = ctx.obj["BOOKDIR"]
    bl = get_booklist(export_dir)

    bl.write_modified(export_dir, force)


if __name__ == "__main__":
    cli(obj={})
