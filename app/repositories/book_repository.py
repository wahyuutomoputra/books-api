from sqlalchemy.orm import Session
from app.models.book_model import Book
from app.schemas.book_schema import BookCreate, BookUpdate
from app.core.redis import redis_client
import json
from typing import Optional, List

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookCreate) -> Book:
        db_book = Book(**book.model_dump())  # Use dict() to convert Pydantic model to a dictionary
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        redis_client.set(f"book:{db_book.id}", json.dumps(db_book.to_dict()))  # Use to_dict() to serialize the SQLAlchemy model
        return db_book

    def get_book(self, book_id: int) -> Optional[Book]:
        cache_key = f"book:{book_id}"
        cached_book = redis_client.get(cache_key)
        if cached_book:
            return json.loads(cached_book)

        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            redis_client.set(cache_key, json.dumps(book.to_dict()))  # Use to_dict() to serialize the SQLAlchemy model
        return book

    def get_books(self, skip: int = 0, limit: int = 10) -> List[Book]:
        return self.db.query(Book).offset(skip).limit(limit).all()

    def count_books(self) -> int:
        return self.db.query(Book).count()

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            for key, value in book_update.model_dump().items():  # Use dict() to convert Pydantic model to a dictionary
                setattr(book, key, value)
            self.db.commit()
            redis_client.set(f"book:{book.id}", json.dumps(book.to_dict()))  # Use to_dict() to serialize the SQLAlchemy model
        return book

    def delete_book(self, book_id: int) -> Optional[Book]:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            self.db.delete(book)
            self.db.commit()
            redis_client.delete(f"book:{book_id}")
        return book
