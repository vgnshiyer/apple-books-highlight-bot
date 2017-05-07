import datetime as dt
import os
import re
from glob import glob

import frontmatter
from dateutil import parser as duparser
from slugify import slugify

from ibooks_highlights.util import (
    cmp_to_key, query_compare_no_asset_id, TEMPLATE_ENVIRONMENT, NS_TIME_INTERVAL_SINCE_1970)



class Annotation(object):

    def __init__(self, location, selected_text=None, note=None,
        represent_text=None, chapter=None, style=None, modified_date=None):

        if (selected_text is None) and (note is None):
            raise ValueError('specify either selected_text or note')

        self.location = location
        self.selected_text = selected_text

        if represent_text is not None:
            represent_text = represent_text.strip()
        self.represent_text = represent_text

        self.chapter = chapter
        self.style = style
        self.note = note
        self.modified_date = modified_date

    def __getitem__(self, key):
        return getattr(self, key)


class Book(object):

    def __init__(self, asset_id=None, filename=None):

        args_present = asset_id is not None
        file_present = filename is not None

        if args_present == file_present:
            raise ValueError('specify either asset_id or filename')

        self._modified_date = None
        self._annotations = []

        if args_present:
            self._asset_id = asset_id
            self._author = None
            self._title = None
            self._prev_content = None

        if file_present:
            self._process_file(filename)

    def _process_file(self, filename):

        self._filename = os.path.split(filename)[-1]

        book = frontmatter.load(filename)
        self._asset_id = book['asset_id']
        self._author = book['author']
        self._title = book['title']

        if 'modified_date' in book.keys():
            self._modified_date = duparser.parse(book['modified_date'])

        self._prev_content = book.content

    def __str__(self):
        mod = ' '
        if self.is_modified:
            mod = '*'
        return '{asset_id} {mod} {len}\t{title}'.format(
            asset_id=self._asset_id.ljust(32),
            mod=mod,
            len=self.num_annotations,
            title=self._title,
        )

    def _yaml_str(cls, txt):
        exp = '[^A-Za-z0-9 ]+'
        return re.sub(exp, '', txt)

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if value is None:
            value = 'Unknown'
        self._author = self._yaml_str(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value is None:
            value = 'Unknown'
        self._title = self._yaml_str(value)
        self._filename = '{slug}-{asset_id}.md'.format(
            slug=slugify(value),
            asset_id=self._asset_id[:5].lower()
        )

    @property
    def asset_id(self):
        return self._asset_id

    @property
    def is_modified(self):
        if self._modified_date is None:
            if self.num_annotations > 0:
                return True
            else:
                return False

        anno_max = max([
            anno.modified_date
            for anno in self._annotations
        ])
        return anno_max > self._modified_date

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
            highlights=self.annotations,
        )
        return md

    def write(self, path):

        mod_date = max([
            anno.modified_date
            for anno in self._annotations
        ])
        mod_date = mod_date.isoformat()

        fmpost = frontmatter.Post(
            self.content,
            asset_id=self._asset_id,
            title=self.title,
            author=self.author,
            modified_date=mod_date
        )

        fn = os.path.join(path, self._filename)
        with open(fn, 'w') as f:
            frontmatter.dump(fmpost, f)


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

    def _get_create_book(self, asset_id):

        if asset_id not in self.books:
            book = Book(asset_id=asset_id)
            self.books[asset_id] = book

        return self.books[asset_id]

    def populate_annotations(self, annos):

        res = [
            r
            for r in annos
            if r['asset_id'] is not None and
            ((r['selected_text'] is not None) or (r['note'] is not None))
        ]

        for r in res:
            book = self._get_create_book(r['asset_id'])
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
                style=r['style'],
                modified_date=dt.datetime.fromtimestamp(
                    NS_TIME_INTERVAL_SINCE_1970 + r['modified_date']),
            )
            anno_group[asset_id].append(anno)

        for asset_id, anno in anno_group.items():
            self.books[asset_id].annotations = anno

    def write_modified(self, path=None):

        if path == None:
            path = self._path

        if not os.path.exists(path):
            os.makedirs(path)

        for book in self.books.values():
            if not book.is_modified:
               continue
            print('updating', book.title)
            book.write(path)

