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

To get a list of books:

```
$ ibooks-highlights.py --list

D36605A6   1	Bayesian Methods for Hackers
80EE27E1   27	Dune
E5875B57 * 30	Making of the Atomic Bomb
7029A581   17	Meditations - Modern Library Translation
547526C9   50	Musashi
F6C97901   77	The Idea Factory
```

To set output directory:

```
$ ibooks-highlights.py -o other-books
```

## TODO

- [ ] prevent update from clobbering file contents, to allow user edits
- [ ] `¯\_(ツ)_/¯`