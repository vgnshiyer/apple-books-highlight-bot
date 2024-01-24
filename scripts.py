from py_apple_books import PyAppleBooks
import json, pathlib, logging
from templates import book_schema
from utils import object_to_dict

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

    def _remove_empty_highlights(self, book_data: dict):
        book_data["highlights"] = [h for h in book_data["highlights"] if h["selected_text"] != None]
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
            book_data = self._remove_empty_highlights(book_data)

            book_has_highlights = len(book_data["highlights"]) > 0
            if not book_has_highlights:
                logger.debug(f"Skipping {book.title} because it has no highlights")
            else:
                with open(book_path, "w") as f:
                    json.dump(book_data, f, indent=4)
                    logger.info(f"Exported {book.title} to {book_path}")
            