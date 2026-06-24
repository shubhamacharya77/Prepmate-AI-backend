from sqlmodel import Session, create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=Session
)

def get_session():
    with Session(engine) as session:
        yield session


@contextmanager
def get_local_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()