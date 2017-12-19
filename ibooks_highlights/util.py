import os
import re

from typing import (List, Dict, Optional, Union, Any, Callable)
from jinja2 import Environment, FileSystemLoader

from ibooks_highlights.models import Annotation

NS_TIME_INTERVAL_SINCE_1970 = 978307200


PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=True,
    lstrip_blocks=False)


def parse_epubcfi(raw: str) -> List[int]:

    if raw is None:
        return []

    parts = raw[8:-1].split(',')
    cfistart = parts[0] + parts[1]

    parts = cfistart.split(':')

    path = parts[0]
    offsets = [
        int(x[1:])
        for x in re.findall('(/\d+)', path)
    ]

    if len(parts) > 1:
        offsets.append(int(parts[1]))

    return offsets


def epubcfi_compare(x: List[int], y: List[int]) -> int:
    depth = min(len(x), len(y))
    for d in range(depth):
        if x[d] == y[d]:
            continue
        else:
            return x[d] - y[d]

    return len(x) - len(y)


def query_compare_no_asset_id(x: Annotation, y: Annotation) -> int:
    return epubcfi_compare(
        parse_epubcfi(x['location']),
        parse_epubcfi(y['location'])
    )


def cmp_to_key(mycmp: Callable) -> Any:
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj: Any, *args: Any) -> None:
            self.obj = obj

        def __lt__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other: Any) -> Any:
            return mycmp(self.obj, other.obj) != 0
    return K
