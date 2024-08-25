from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from app.core.exception_handlers import general_exception_handler, http_exception_handler
from app.core.database import engine, Base
from app.routers import author_route, book_router

app = FastAPI(
    title="Book and Author API",
    description="An API for managing authors and books, with support for pagination, search, and caching using Redis.",
    version="1.0.0",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Book and Author API",
        version="1.0.0",
        description="An API for managing authors and books, with support for pagination, search, and caching using Redis.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Daftarkan handler pengecualian
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(author_route.router)
app.include_router(book_router.router)

# Membuat tabel database saat aplikasi berjalan
Base.metadata.create_all(bind=engine)
