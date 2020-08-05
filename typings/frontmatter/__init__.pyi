import pathlib
from typing import AnyStr, IO, Any, Union

import frontmatter

from frontmatter.default_handlers import BaseHandler


FileOrName = Union[str, IO[AnyStr], pathlib.Path]


def load(fd: FileOrName, encoding: str = ..., handler: BaseHandler = ..., **defaults: Any) -> Post:
    ...

class Post:
    content: bytes

    def __init__(self, content: AnyStr, handler: BaseHandler = ..., **metadata: Any) -> None:
        ...

    ...
