from py_apple_books import PyAppleBooks
import json, pathlib
from templates import book_schema
from utils import object_to_dict

class Exporter:
    def __init__(self, export_dir: str):
        self.export_dir = export_dir
        self.api = PyAppleBooks()

    def list_books(self, include_annotations: bool = False):
        return self.api.list_books(include_annotations=include_annotations)

    def write_modified(self):
        books = self.list_books(include_annotations=True)
        for book in books:
            book_has_highlights = len(book.highlights) > 0
            if not book_has_highlights:
                continue
            try:
                book_obj = book_schema.Book(**object_to_dict(book))
            except Exception as e:
                print(f"Error parsing book {book.title}: {e}")
                continue
            book_path = pathlib.Path(self.export_dir) / f"{book.id}.json"
            with open(book_path, "w") as f:
                json.dump(book_obj.model_dump(), f, indent=4)
                print(f"Exported {book.title} to {book_path}")
            