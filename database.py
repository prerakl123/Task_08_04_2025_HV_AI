from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config
from models import Base

# Create database engine using the connection URI from Config
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Create a scoped session factory for managing database sessions
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    """Initialize the database by creating all tables defined in the models"""
    Base.metadata.create_all(bind=engine)
