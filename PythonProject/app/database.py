from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = "postgres"
DB_PASSWORD = "port5432"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "book_contacts"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@db:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
