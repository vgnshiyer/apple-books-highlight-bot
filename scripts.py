from py_apple_books import PyAppleBooks
import json, pathlib, logging, book_schema
from utils import object_to_dict, replace_unicode_characters

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Exporter:
    def __init__(self, export_dir: str):
        self.export_dir = export_dir
        self.api = PyAppleBooks()

    def list_books(self, include_annotations: bool = False):
        logger.debug("Fetching books")
        return self.api.list_books(include_annotations=include_annotations)

    def _format_book_data(self, book: any):
        book_dict = object_to_dict(book)
        book_obj = book_schema.Book(**book_dict)
        return book_obj.model_dump()

    def _remove_empty_highlights_and_underlines(self, book_data: dict):
        book_data["highlights"] = [h for h in book_data["highlights"] if h["selected_text"] != None]
        book_data["highlights"] = [h for h in book_data["highlights"] if h["representative_text"] != None]
        book_data["underlines"] = [u for u in book_data["underlines"] if u["selected_text"] != None]
        return book_data

    def _preprocess_text_fields(self, book_data: dict):
        for h in book_data["highlights"]:
            h["representative_text"] = replace_unicode_characters(h["representative_text"])
            h["selected_text"] = replace_unicode_characters(h["selected_text"])
            if h["note"] != None:
                h["note"] = replace_unicode_characters(h["note"])
        for u in book_data["underlines"]:
            u["selected_text"] = replace_unicode_characters(u["selected_text"])
            if u["note"] != None:
                u["note"] = replace_unicode_characters(u["note"])
        book_data["title"] = replace_unicode_characters(book_data["title"])
        book_data["author"] = replace_unicode_characters(book_data["author"])
        return book_data

    def write_modified(self):
        logger.info("Writing modified books")
        books = self.list_books(include_annotations=True)
        for book in books:
            logger.debug(f"Checking {book.title}")

            try:
                book_data = self._format_book_data(book)
            except Exception as e:
                logger.warning(f"Error parsing book {book.title}: {e}")
                logger.debug(f"Book: {book.title} \n highlights: {book.highlights}")
                continue

            book_path = pathlib.Path(self.export_dir) / f"{book.id}.json"
            book_data = self._remove_empty_highlights_and_underlines(book_data)
            book_data = self._preprocess_text_fields(book_data)

            book_has_highlights = len(book_data["highlights"]) > 0
            if not book_has_highlights:
                logger.debug(f"Skipping {book.title} because it has no highlights")
            else:
                with open(book_path, "w") as f:
                    json.dump(book_data, f, indent=4)
                    logger.info(f"Exported {book.title} to {book_path}")
