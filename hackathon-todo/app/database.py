"""
Database connection and session management.
"""
from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Create database engine with SQLite support
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args=connect_args,
)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
