# NOTES

## Multiple sub-directories of books

I'd like to support having multiple sub-directories of books.  There will still 
be a single root directory for all the stored books, but there may be an 
arbitrary number of sub-directories (and sub-sub-dirs) below that root where
books may be moved to.

For simplicity, new books will always be in the root location.  They can then
be moved to their desired final home.

Books need to keep track of their location relative to the root.  Currently,
that is just taken to be the filename (since depth=0 is always implied).

How best to keep track of the root?  For now I'm just passing the root to each
book upon init.  

If the book is being loaded from a file, one of 2 things happens:

1. If the root is provided, the book's filename is the path relative to the 
    root.
2. If the root is not provided, the book's filename is just the filename.

If the book is being created anew, then the filename is just computed from the
book metadata as it was previously.

Then when the book is written out, it's provided a root path, and creates a full
filename relative to that path.  I also create any sub-directories in case the
book is being written to a different path than it was read from.
