from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./time_tracking.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required ONLY for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency for FastAPI (provides a DB session per request)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
