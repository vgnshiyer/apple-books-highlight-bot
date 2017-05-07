import os
import sqlite3

from glob import glob


ANNOTATION_DB_PATH = (
    "~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/")
BOOK_DB_PATH = (
    "~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/")


ATTACH_BOOKS_QUERY = """
attach database ? as books
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
    'modified_date'
]

NOTE_LIST_QUERY = """
select 
ZANNOTATIONASSETID as asset_id, 
books.ZBKLIBRARYASSET.ZTITLE as title, 
books.ZBKLIBRARYASSET.ZAUTHOR as author,
ZANNOTATIONLOCATION as location,
ZANNOTATIONSELECTEDTEXT as selected_text, 
ZANNOTATIONNOTE as note,
ZANNOTATIONREPRESENTATIVETEXT as represent_text, 
ZFUTUREPROOFING5 as chapter, 
ZANNOTATIONSTYLE as style,
ZANNOTATIONMODIFICATIONDATE as modified_date

from ZAEANNOTATION

left join books.ZBKLIBRARYASSET
on ZAEANNOTATION.ZANNOTATIONASSETID = books.ZBKLIBRARYASSET.ZASSETID

where ZANNOTATIONDELETED = 0

order by ZANNOTATIONASSETID, ZPLLOCATIONRANGESTART;
"""


def get_ibooks_database(_cache=[]):

    if len(_cache) > 0:
        return _cache[0]

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


def fetch_annotations():

    cur = get_ibooks_database()
    res = cur.execute(NOTE_LIST_QUERY)
    res = res.fetchall()
    res = [dict(zip(NOTE_LIST_FIELDS, r)) for r in res]

    return res
