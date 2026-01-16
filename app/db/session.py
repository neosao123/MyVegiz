from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.core.config import DATABASE_URL

# Create database engine & session
# Open DB → do work → close DB

# Creates a connection bridge between FastAPI and PostgreSQL
engine = create_engine(DATABASE_URL)


# creates DB sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

