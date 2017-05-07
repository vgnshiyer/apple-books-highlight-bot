# iBooks highlights export

Export your iBooks highlights and notes to markdown files.  Modified from [original][] by [shrsv][].

[original]: https://github.com/shrsv/ibooks_highlights_export
[shrsv]:    https://github.com/shrsv

## Usage

Simplest way to get your highlights:

```
$ python setup.py install
$ ibooks-highlights.py
$ ll books
```

## What it does

The scripts reads the local sqlite database that iBooks uses to track annotations.  It proceeds to
generate a markdown file corresponding to each book in the database, and populate it with the
associated highlights and notes.

It preserves each book's identifier (and some other data) in the YAML header of the markdown file.
You can actually rename the file and the next run of the script will find and update the appropriate file.

## Options

To get a list of available options, type this:

```
$ ibooks-highlights.py --help
```

## TODO

- [ ] track changes in title, renaming files appropriately
- [ ] prevent update from clobbering file contents, to allow user edits
- [ ] `¯\_(ツ)_/¯`