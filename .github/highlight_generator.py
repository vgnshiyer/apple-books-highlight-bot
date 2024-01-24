import pathlib, json, logging, random
from jinja2 import Template

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def get_books():
    books = []
    for book in pathlib.Path("../highlights_data").iterdir():
        if book.is_file() and book.suffix == ".json":
            books.append(book)
    logger.info(f"Found {len(books)} books")
    return books

def get_random_book():
    books = get_books()
    return random.choice(books)

def get_random_highlight(highlights):
    return random.choice(highlights)

def get_book_data(book):
    logger.info(f"Getting data for {book}")
    with open(book, "r") as f:
        data = json.load(f)
        highlight = get_random_highlight(data["highlights"])
        return {
            "title": data["title"],
            "chapter": highlight["chapter"],
            "representative_text": highlight["representative_text"],
            "selected_text": highlight["selected_text"],
            "note": highlight["note"],
            "color": highlight["color"],
        }

def generate_daily_highlights_email():
    book = get_random_book()
    book_data = get_book_data(book)
    
    logger.info(f"Generating email for {book}")
    with open("./templates/email_template.html", "r") as f:
        template = Template(f.read())
    return template.render(
        book_title=book_data["title"],
        chapter=book_data["chapter"],
        representative_text=book_data["representative_text"],
        selected_text=book_data["selected_text"],
        note=book_data["note"],
        highlight_color=book_data["color"],
    )

if __name__ == "__main__":
    logger.info("Getting random highlight")
    email = generate_daily_highlights_email()
    logger.info("Email generated")

    with open("./output.html", "w") as f:
        f.write(email)
    logger.info("Email written to file")