from app.schemas.book_schema import BookCreate, BookResponse
from app.models.book_model import Book
from app.models.author_model import Author

def test_create_book(client, db_session):
    # Create an author first
    author = Author(name="Author Name", bio="Author Bio", birth_date="1970-01-01")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    response = client.post("/books/", json={"title": "Book Title", "description": "Book Description", "publish_date": "2022-01-01", "author_id": author.id})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["title"] == "Book Title"

def test_get_book(client, db_session):
    # Create an author
    author = Author(name="Author Name", bio="Author Bio", birth_date="1970-01-01")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    # Create a book
    book = Book(title="Test Book", description="Description", publish_date="2022-01-01", author_id=author.id)
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    response = client.get(f"/books/{book.id}")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["title"] == "Test Book"

def test_update_book(client, db_session):
    # Create an author
    author = Author(name="Author Name", bio="Author Bio", birth_date="1970-01-01")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    # Create a book
    book = Book(title="Old Title", description="Description", publish_date="2022-01-01", author_id=author.id)
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    response = client.put(f"/books/{book.id}", json={"title": "Updated Title", "description": "Updated Description", "publish_date": "2022-01-01", "author_id": author.id})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["title"] == "Updated Title"

def test_delete_book(client, db_session):
    # Create an author
    author = Author(name="Author Name", bio="Author Bio", birth_date="1970-01-01")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    # Create a book
    book = Book(title="Delete Me", description="Description", publish_date="2022-01-01", author_id=author.id)
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    response = client.delete(f"/books/{book.id}")
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Check if book was really deleted
    response = client.get(f"/books/{book.id}")
    assert response.status_code == 404
