
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Locate the .env file in the main Famora folder
env_path = Path(__file__).resolve().parents[3] / ".env"

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Get database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env file")

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
Base = declarative_base()


# Database dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
