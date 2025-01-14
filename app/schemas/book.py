from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None
    summary: str | None = None  # Thêm trường summary

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: str

    class Config:
        from_attributes = True