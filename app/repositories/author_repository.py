from typing import Optional
from sqlalchemy.orm import Session
from app.models.author_model import Author
from app.schemas.author_schema import AuthorCreate, AuthorUpdate
from app.core.redis import redis_client
import json

class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_author(self, author: AuthorCreate) -> Author:
        db_author = Author(**author.model_dump())
        self.db.add(db_author)
        self.db.commit()
        self.db.refresh(db_author)
        redis_client.set(f"author:{db_author.id}", json.dumps(db_author.to_dict()))
        return db_author

    def get_author(self, author_id: int) -> Optional[Author]:
        cache_key = f"author:{author_id}"
        cached_author = redis_client.get(cache_key)
        if cached_author:
            return json.loads(cached_author)
        
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if author:
            redis_client.set(cache_key, json.dumps(author.to_dict()))
        return author

    def get_authors(self, skip: int = 0, limit: int = 10) -> list[Author]:
        return self.db.query(Author).offset(skip).limit(limit).all()

    def count_authors(self) -> int:
        return self.db.query(Author).count()

    def update_author(self, author_id: int, author_update: AuthorUpdate) -> Optional[Author]:
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if author:
            for key, value in author_update.model_dump().items():
                setattr(author, key, value)
            self.db.commit()
            redis_client.set(f"author:{author.id}", json.dumps(author.to_dict()))
        return author

    def delete_author(self, author_id: int) -> Optional[Author]:
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if author:
            self.db.delete(author)
            self.db.commit()
            redis_client.delete(f"author:{author_id}")
        return author
    
    def get_books_by_author(self, author_id: int) -> list:
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if author:
            return [book.to_dict() for book in author.books]  # Ensure books are serialized correctly
        return []
