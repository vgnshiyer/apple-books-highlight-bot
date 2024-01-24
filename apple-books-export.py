import click, pathlib, logging, datetime
from scripts import Exporter

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"./logs/apple-books-export.log", mode="w")
        ],
    )
logger = logging.getLogger(__name__)


@click.group()
@click.option(
    "--export-dir",
    "-e",
    type=click.Path(),
    envvar="APPLE_BOOKS_EXPORT_DIR",
    default="./highlights_data",
)
@click.pass_context
def cli(ctx: click.Context, export_dir: str):
    logger.info(f"Exporting to {export_dir}")
    # create directory if it doesn't exist
    p = pathlib.Path(export_dir)
    logger.debug(f"Creating directory {p}")
    p.mkdir(parents=True, exist_ok=True)
    ctx.obj["EXPORTER"] = Exporter(export_dir)


@cli.command()
@click.pass_context
def list(ctx: click.Context):
    exporter = ctx.obj["EXPORTER"]
    books = exporter.list_books()
    logger.info(f"Found {len(books)} books")
    logger.debug("Sorting books by title")
    books = sorted(books, key=lambda b: b.title)
    for book in books:
        print(f"{book.id} - {book.title}")


@cli.command()
@click.pass_context
def sync(ctx: click.Context):
    logger.info("Syncing highlights" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    exporter = ctx.obj["EXPORTER"]
    exporter.write_modified()


if __name__ == "__main__":
    cli(obj={})
