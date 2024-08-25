import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text
from app.main import app
from app.core.database import Base, get_db

# URL untuk MySQL (tanpa nama database untuk membuat database)
SQLALCHEMY_DATABASE_URL_WITHOUT_DB = "mysql://root:@localhost"
DATABASE_NAME = "test_db"

# URL dengan nama database untuk melakukan koneksi setelah database dibuat
SQLALCHEMY_DATABASE_URL = f"{SQLALCHEMY_DATABASE_URL_WITHOUT_DB}/{DATABASE_NAME}"

# Engine untuk membuat database
engine_without_db = create_engine(SQLALCHEMY_DATABASE_URL_WITHOUT_DB)

# Engine setelah database dibuat
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Membuat database jika belum ada
def create_test_database():
    try:
        with engine_without_db.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))
    except ProgrammingError as e:
        print(f"Error creating database: {e}")

# Hapus database setelah pengujian selesai
def drop_test_database():
    try:
        with engine_without_db.connect() as conn:
            conn.execute(text(f"DROP DATABASE IF EXISTS {DATABASE_NAME}"))
    except ProgrammingError as e:
        print(f"Error dropping database: {e}")

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the database and the tables
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Membuat database sebelum tes
    create_test_database()
    Base.metadata.create_all(bind=engine)

    yield  # Semua pengujian berjalan di sini

    # Hapus database setelah tes
    Base.metadata.drop_all(bind=engine)
    drop_test_database()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()
