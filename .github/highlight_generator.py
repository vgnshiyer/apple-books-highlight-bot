import pathlib, json, logging, random, datetime, os
from jinja2 import Template

# Create logs directory if it doesn't exist
pathlib.Path('logs').mkdir(parents=True, exist_ok=True)

print(os.listdir())

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/highlight_generator.log", mode="w")
    ]
)
logger = logging.getLogger(__name__)

def get_books():
    books = []
    for book in pathlib.Path("highlights_data").iterdir():
        if book.is_file() and book.suffix == ".json":
            books.append(book)
    logger.info(f"Found {len(books)} books")
    return books

def get_random_book():
    books = get_books()
    return random.choice(books)

def get_random_highlight(highlights):
    if not highlights:
        return None
    return random.choice(highlights)

def get_random_underline(underlines):
    if not underlines:
        return None
    return random.choice(underlines)

def get_book_data(book1, book2):
    logger.info(f"Getting random highlight for {book1}")
    res1, res2 = None, None
    with open(book1, "r") as f:
        data = json.load(f)
        highlight = get_random_highlight(data.get("highlights", []))
        if highlight:
            res1 = {
                "title": data["title"],
                "chapter": highlight["chapter"],
                "representative_text": highlight["representative_text"],
                "selected_text": highlight["selected_text"],
                "note": highlight["note"],
                "color": highlight["color"],
            }

    logger.info(f"Getting random underline for {book2}")
    with open(book2, "r") as f:
        data = json.load(f)
        underline = get_random_underline(data.get("underlines", []))
        if underline:
            res2 = {
                "title": data["title"],
                "chapter": underline["chapter"],
                "representative_text": underline["representative_text"],
                "selected_text": underline["selected_text"],
                "note": underline["note"],
            }

    return res1, res2

def generate_daily_highlights_email():
    book1 = get_random_book()
    book2 = get_random_book()
    highlight_data, underline_data = get_book_data(book1, book2)

    logger.info(f"Generating email for {book1} & {book2}")
    with open(".github/templates/email_template.html", "r") as f:
        template = Template(f.read())
    return template.render(
        book_title=highlight_data["title"] if highlight_data else None,
        chapter=highlight_data["chapter"] if highlight_data else None,
        representative_text=highlight_data["representative_text"] if highlight_data else None,
        selected_text=highlight_data["selected_text"] if highlight_data else None,
        note=highlight_data["note"] if highlight_data else None,
        highlight_color=highlight_data["color"] if highlight_data else None,
        word=underline_data["selected_text"] if underline_data else None,
        definition=underline_data["note"] if underline_data else None,
        example=underline_data["representative_text"] if underline_data else None,
    )

if __name__ == "__main__":
    os.chdir("..")
    logger.info("Getting random highlight -- " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    email = generate_daily_highlights_email()
    logger.info("Email generated")

    with open(".github/output.html", "w") as f:
        f.write(email)
    logger.info("Email written to file")
