from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.repositories.book_repository import BookRepository
from app.schemas.book_schema import BookCreate, BookResponse, BookListResponse, BookUpdate
from app.core.database import get_db
from app.schemas.response_schema import APIResponse

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", response_model=APIResponse[BookListResponse])
def list_books(
    page: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    skip = page * limit
    total = repo.count_books()
    books = repo.get_books(skip=skip, limit=limit)
    response = BookListResponse(total=total, books=books)
    return APIResponse(success=True, data=response)

@router.get("/{book_id}", response_model=APIResponse[BookResponse])
def get_book(book_id: int, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return APIResponse(success=True, data=book)

@router.post("/", response_model=APIResponse[BookResponse])
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    db_book = repo.create_book(book)
    return APIResponse(success=True, data=db_book)

@router.put("/{book_id}", response_model=APIResponse[BookResponse])
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.update_book(book_id, book_update)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return APIResponse(success=True, data=book)

@router.delete("/{book_id}", response_model=APIResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.delete_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return APIResponse(success=True, message="Book deleted successfully")
