from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    birth_date: date

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int

    class Config:
        from_attributes = True

class AuthorListResponse(BaseModel):
    total: int
    authors: List[AuthorResponse]

    class Config:
        from_attributes = True
