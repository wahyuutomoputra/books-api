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
        db_book = Book(**book.model_dump())  # Menggunakan model_dump() untuk mengkonversi Pydantic model ke dictionary
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        
        # Cache buku yang baru dibuat di Redis
        redis_client.set(f"book:{db_book.id}", json.dumps(db_book.to_dict()))  # Menggunakan to_dict() untuk serialisasi model SQLAlchemy
        
        return db_book

    def get_book(self, book_id: int) -> Optional[Book]:
        cache_key = f"book:{book_id}"
        
        # Mencoba mendapatkan buku dari Redis cache
        cached_book = redis_client.get(cache_key)
        if cached_book:
            return Book(**json.loads(cached_book))  # Deserialize kembali menjadi object Book

        # Jika tidak ditemukan di cache, dapatkan dari database
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            # Cache buku di Redis
            redis_client.set(cache_key, json.dumps(book.to_dict()))  # Menggunakan to_dict() untuk serialisasi model SQLAlchemy
        return book

    def get_books(self, skip: int = 0, limit: int = 10) -> List[Book]:
        cache_key = f"books:{skip}:{limit}"
        
        # Mencoba mendapatkan daftar buku dari Redis cache
        cached_books = redis_client.get(cache_key)
        if cached_books:
            book_dicts = json.loads(cached_books)
            return [Book(**book_dict) for book_dict in book_dicts]
        
        # Jika tidak ditemukan di cache, dapatkan dari database
        books = self.db.query(Book).offset(skip).limit(limit).all()
        
        # Cache daftar buku di Redis
        redis_client.set(cache_key, json.dumps([book.to_dict() for book in books]))
        
        return books

    def count_books(self) -> int:
        return self.db.query(Book).count()

    def update_book(self, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            for key, value in book_update.model_dump().items():  # Menggunakan model_dump() untuk mengkonversi Pydantic model ke dictionary
                setattr(book, key, value)
            self.db.commit()
            
            # Update cache dengan data baru
            redis_client.set(f"book:{book.id}", json.dumps(book.to_dict()))  # Menggunakan to_dict() untuk serialisasi model SQLAlchemy

        return book

    def delete_book(self, book_id: int) -> Optional[Book]:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            self.db.delete(book)
            self.db.commit()
            
            # Hapus buku dari Redis cache
            redis_client.delete(f"book:{book_id}")
          
        return book

    def _invalidate_books_cache(self):
        # Invalidate cache dengan menghapus semua kunci yang berkaitan dengan daftar buku
        for key in redis_client.scan_iter("books:*"):
            redis_client.delete(key)
