from pydantic import BaseModel
from typing import List, Optional

class Highlight(BaseModel):
    id: int
    is_deleted: Optional[bool]
    representative_text: Optional[str]
    selected_text: Optional[str]
    color: Optional[str]
    note: Optional[str]
    chapter: Optional[str]

class Underline(BaseModel):
    id: int
    is_deleted: Optional[bool]
    representative_text: Optional[str]
    selected_text: Optional[str]
    note: Optional[str]
    chapter: Optional[str]

class Book(BaseModel):
    asset_id: str
    title: str
    author: str
    highlights: List[Highlight]
    underlines: List[Underline]
