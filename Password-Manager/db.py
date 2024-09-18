from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models import Base

DATABASE_URL = "sqlite:///password_manager.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_session():
    """Provide a session context for interacting with the database."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Create the tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)