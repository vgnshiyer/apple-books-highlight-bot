from pydantic import BaseModel, field_validator
from typing import List, Optional

class Highlight(BaseModel):
    id: int
    is_deleted: Optional[bool]
    representative_text: Optional[str]
    selected_text: Optional[str]
    color: Optional[str]
    note: Optional[str]
    chapter: Optional[str]

    # @field_validator("representative_text", mode="before")
    # def check_representative_text(cls, v):
    #     if v is None or not isinstance(v, str):
    #         return ""

    # @field_validator("note", mode="before")
    # def check_note_text(cls, v):
    #     if v is None or not isinstance(v, str):
    #         return ""

    # @field_validator("chapter", mode="before")
    # def check_chapter_text(cls, v):
    #     if v is None or not isinstance(v, str):
    #         return ""

    # @field_validator("selected_text", mode="before")
    # def check_selected_text(cls, v):
    #     if v is None or not isinstance(v, str):
    #         return ""
            

class Book(BaseModel):
    asset_id: str
    title: str
    author: str
    highlights: List[Highlight]