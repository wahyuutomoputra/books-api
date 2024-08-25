from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.repositories.author_repository import AuthorRepository
from app.schemas.author_schema import AuthorCreate, AuthorResponse, AuthorListResponse, AuthorUpdate
from app.core.database import get_db
from app.schemas.book_schema import BookResponse
from app.schemas.response_schema import APIResponse

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/", response_model=APIResponse[AuthorListResponse])
def list_authors(
    page: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    repo = AuthorRepository(db)
    skip = page * limit
    total = repo.count_authors()
    authors = repo.get_authors(skip=skip, limit=limit)
    response = AuthorListResponse(total=total, authors=authors)
    return APIResponse(success=True, data=response)


@router.get("/{author_id}", response_model=APIResponse[AuthorResponse])
def get_author(author_id: int, db: Session = Depends(get_db)):
    repo = AuthorRepository(db)
    author = repo.get_author(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return APIResponse(success=True, data=author)


@router.post("/", response_model=APIResponse[AuthorResponse])
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    repo = AuthorRepository(db)
    db_author = repo.create_author(author)
    return APIResponse(success=True, data=db_author)


@router.put("/{author_id}", response_model=APIResponse[AuthorResponse])
def update_author(author_id: int, author_update: AuthorUpdate, db: Session = Depends(get_db)):
    repo = AuthorRepository(db)
    author = repo.update_author(author_id, author_update)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return APIResponse(success=True, data=author)


@router.delete("/{author_id}", response_model=APIResponse)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    repo = AuthorRepository(db)
    author = repo.delete_author(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return APIResponse(success=True, message="Author deleted successfully")


@router.get("/{id}/books", response_model=APIResponse[List[BookResponse]])
def get_books_by_author(id: int, db: Session = Depends(get_db)):
    try:
        repo = AuthorRepository(db)
        books = repo.get_books_by_author(id)
        if books:
            return APIResponse(success=True, data=books)
        else:
            raise HTTPException(
                status_code=404, detail="Books not found for this author")
    except Exception as e:
        return APIResponse(success=False, message=str(e))
