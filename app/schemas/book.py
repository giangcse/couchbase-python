from pydantic import BaseModel
from typing import List

class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None
    summary: str | None = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: str
    summary_vector: List[float] | None = None

    class Config:
        from_attributes = True
