from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None

    class Config:
        from_attributes = True
