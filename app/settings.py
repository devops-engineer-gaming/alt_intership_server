import os

DB_HOST = os.environ["DB_HOST"]

DB_USER = os.environ["DB_USER"]

DB_PASS = os.environ["DB_PASS"]

DB_NAME = os.environ["DB_NAME"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

origins = [
    "http://localhost.tiangolo.com",
    "https://frontend-service",
    "http://localhost:8000",
    "http://todo.com",
    "http://frontend-service:3000",
    "http://localhost:3000",
]
