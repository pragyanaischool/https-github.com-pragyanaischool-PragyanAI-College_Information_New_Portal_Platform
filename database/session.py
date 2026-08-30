from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL
from database.models import Base

# Configure SQLAlchemy Engine for SQLite (with thread safety check disabled for Streamlit multi-threading)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes and creates all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)
