from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    publish_date: date
    author_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True

class BookListResponse(BaseModel):
    total: int
    books: List[BookResponse]

    class Config:
        from_attributes = True
