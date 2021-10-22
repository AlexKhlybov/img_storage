import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models.database import Base, get_db

test_name_db = 'test.db'
SQLALCHEMY_DATABASE_URL = f'sqlite:///./tests/{test_name_db}'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def drop_db():
    os.remove(f'tests/{test_name_db}')

