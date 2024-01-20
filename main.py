from py_apple_books import PyAppleBooks

class Exporter:
    def __init__(self, export_dir: str):
        self.export_dir = export_dir
        self.api = PyAppleBooks()

    def list_books(self, include_annotations: bool = False):
        return self.api.list_books(include_annotations=include_annotations)

    def write_modified():
        books = self.list_books(include_annotations=True)
        