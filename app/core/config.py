import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:@localhost:3306/bookstore")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
PAGINATION_LIMIT = 10
