# Book and Author API

This is a FastAPI-based application that allows you to manage authors and books with support for pagination, search, and caching using Redis. It also provides Swagger documentation for easy API exploration and `pytest` for testing.

## Features

- Create, retrieve, update, and delete authors and books.
- Pagination and search functionality.
- In-memory caching using Redis.
- Swagger documentation for API exploration.
- Automated testing using `pytest`.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8+
- Redis
- MySQL (or another supported database)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/wahyuutomoputra/books-api
    cd yourrepository
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv env

    # For Linux
    source env/bin/activate

    # For Windows
    .\env\Scripts\activate.bat
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    - **Create a MySQL database:**
      Create a new MySQL database for this application. You can use tools like MySQL Workbench or SQL commands in the terminal to create the database.

    - **Update the database connection URL:**
      After creating the database, update the database connection URL in the `app/core/config.py` file:

      ```python
      SQLALCHEMY_DATABASE_URL = "mysql://myuser:mypassword@localhost:3306/mydatabase"
      ```

    - **Configure the test database:**
      For testing purposes, you'll need a separate test database. Update the test database configuration in `tests/conftest.py`:

      ```python
      SQLALCHEMY_DATABASE_URL_WITHOUT_DB = "mysql+pymysql://user:password@localhost"
      DATABASE_NAME = "test_db"
      SQLALCHEMY_DATABASE_URL = f"{SQLALCHEMY_DATABASE_URL_WITHOUT_DB}/{DATABASE_NAME}"
      ```

5. **Install and configure Redis:**

    Ensure Redis is installed and running on your machine. The application uses Redis for caching, which can be configured in the `app/core/config.py` file:

    ```python
    REDIS_URL = "redis://localhost:6379"
    ```

## Running the Application

1. **Start the FastAPI server:**

    ```bash
    uvicorn app.main:app --reload
    ```

2. **Access the API:**

    - **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
    - **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

3. **Access the Redis server (optional):**

    You can access your Redis server via the command line:

    ```bash
    redis-cli
    ```

## API Endpoints

- **Authors:**
  - `POST /authors/`: Create a new author.
  - `GET /authors/{author_id}`: Retrieve an author by ID.
  - `GET /authors/`: List authors with pagination and search.
  - `PUT /authors/{author_id}`: Update an existing author.
  - `DELETE /authors/{author_id}`: Delete an author.

- **Books:**
  - `POST /books/`: Create a new book.
  - `GET /books/{book_id}`: Retrieve a book by ID.
  - `GET /books/`: List books with pagination and search.
  - `PUT /books/{book_id}`: Update an existing book.
  - `DELETE /books/{book_id}`: Delete a book.

- **Associations:**
  - `GET /authors/{author_id}/books`: Retrieve all books by a specific author.

## Testing

To run tests using `pytest`, follow these steps:

1. **Install `pytest` and other testing dependencies:**

    ```bash
    pip install -r requirements-test.txt
    ```

2. **Configure the test database:**

    Update the test database configuration in `tests/conftest.py` as described in the [Set up the database](#set-up-the-database) section.

3. **Run the tests:**

    ```bash
    pytest
    ```

    The tests will run, and you'll see the results in your terminal.

## Deployment

To deploy the application, you can use any ASGI server such as `uvicorn` or `gunicorn`. You can also deploy it using Docker or any cloud service like AWS, GCP, or Azure.

## Docker Deployment

If you prefer to run the application using Docker:

1. **Build the Docker image:**

    ```bash
    docker build -t book-author-api .
    ```

2. **Run the Docker container:**

    ```bash
    docker run -d -p 8000:8000 book-author-api
    ```

3. **Access the application:**

    The application will be available at `http://localhost:8000`.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
