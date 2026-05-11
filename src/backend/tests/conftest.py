import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base # Import your Base to create tables

# Use a separate test database or SQLite for safety
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_maki.db"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine) # Create tables for testing
    yield engine
    Base.metadata.drop_all(bind=engine) # Clean up after tests

@pytest.fixture
def db_session(db_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()