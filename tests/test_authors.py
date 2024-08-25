from app.schemas.author_schema import AuthorCreate, AuthorResponse
from app.models.author_model import Author

def test_create_author(client):
    response = client.post("/authors/", json={"name": "John Doe", "bio": "Author Bio", "birth_date": "1980-01-01"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["name"] == "John Doe"

def test_get_author(client, db_session):
    # Create an author in the database
    author = Author(name="Jane Doe", bio="Another Bio", birth_date="1990-01-01")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    response = client.get(f"/authors/{author.id}")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["name"] == "Jane Doe"

def test_update_author(client, db_session):
    # Create an author
    author = Author(name="Old Name", bio="Bio", birth_date="1980-01-01")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    response = client.put(f"/authors/{author.id}", json={"name": "New Name", "bio": "Updated Bio", "birth_date": "1980-01-01"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["name"] == "New Name"

def test_delete_author(client, db_session):
    # Create an author
    author = Author(name="Delete Me", bio="Bio", birth_date="1980-01-01")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    response = client.delete(f"/authors/{author.id}")
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Check if author was really deleted
    response = client.get(f"/authors/{author.id}")
    assert response.status_code == 404
