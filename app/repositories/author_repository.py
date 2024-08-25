from typing import Optional, List
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
        
        # Cache the newly created author in Redis
        redis_client.set(f"author:{db_author.id}", json.dumps(db_author.to_dict()))
        return db_author

    def get_author(self, author_id: int) -> Optional[Author]:
        cache_key = f"author:{author_id}"
        
        # Try to get the author from Redis cache
        cached_author = redis_client.get(cache_key)
        if cached_author:
            return Author(**json.loads(cached_author))
        
        # If not found in cache, get it from the database
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if author:
            # Cache the author data in Redis
            redis_client.set(cache_key, json.dumps(author.to_dict()))
        return author

    def get_authors(self, skip: int = 0, limit: int = 10) -> List[Author]:
        cache_key = f"authors:{skip}:{limit}"
        
        # Try to get the list of authors from Redis cache
        cached_authors = redis_client.get(cache_key)
        if cached_authors:
            author_dicts = json.loads(cached_authors)
            return [Author(**author_dict) for author_dict in author_dicts]
        
        # If not found in cache, get the data from the database
        authors = self.db.query(Author).offset(skip).limit(limit).all()
        
        # Cache the list of authors in Redis
        redis_client.set(cache_key, json.dumps([author.to_dict() for author in authors]))
        
        return authors

    def count_authors(self) -> int:
        return self.db.query(Author).count()

    def update_author(self, author_id: int, author_update: AuthorUpdate) -> Optional[Author]:
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if author:
            for key, value in author_update.model_dump().items():
                setattr(author, key, value)
            self.db.commit()
            
            # Update the cache with the new data
            redis_client.set(f"author:{author.id}", json.dumps(author.to_dict()))
            
        return author

    def delete_author(self, author_id: int) -> Optional[Author]:
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if author:
            self.db.delete(author)
            self.db.commit()
            
            # Remove the author from the Redis cache
            redis_client.delete(f"author:{author_id}")
            
        return author
    
    def get_books_by_author(self, author_id: int) -> List[dict]:
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if author:
            # Convert the books to a list of dictionaries
            return [book.to_dict() for book in author.books]
        return []

    def _invalidate_authors_cache(self):
        # Invalidate cache by deleting all keys that match the authors pattern
        for key in redis_client.scan_iter("authors:*"):
            redis_client.delete(key)
