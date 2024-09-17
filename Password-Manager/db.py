from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Define the database URL (SQLite in this case, you can change to PostgreSQL, MySQL, etc.)
DATABASE_URL = "sqlite:///password_manager.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    """Get a new session for interacting with the database."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Create all the tables in the database (if they don't exist already)
Base.metadata.create_all(bind=engine)