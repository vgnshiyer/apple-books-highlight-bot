import pathlib, json, logging, random

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def get_books():
    books = []
    for book in pathlib.Path("../../highlights_data").iterdir():
        if book.is_file() and book.suffix == ".json":
            books.append(book)
    logger.info(f"Found {len(books)} books")
    return books

def get_random_book():
    books = get_books()
    return random.choice(books)

def get_random_highlight():
    book = get_random_book()
    logger.info(f"Getting random highlight from {book}")
    with open(book, "r") as f:
        data = json.load(f)
    highlights = data["highlights"]
    return random.choice(highlights)

def send_email(highlight: str):
    logger.info(f"Sending email with highlight: {highlight}")

if __name__ == "__main__":
    logger.info("Getting random highlight")
    highlight_of_the_day = get_random_highlight()
    send_email(highlight_of_the_day)