from pydantic import BaseModel
from pydantic import UUID4


class CreateNote(BaseModel):
    title: str
    content: str
    tag: str


class ReturnNote(BaseModel):
    owner_id: UUID4
    id: int
    title: str
    content: str
    tag: str
    is_favorite: bool
