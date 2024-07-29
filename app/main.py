import datetime
import time
from typing import List, Optional
from fastapi import FastAPI ,Response, status,HTTPException, Depends
import psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import  models
# from models import Author, Book
from .database import SessionLocal, engine , get_db



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author_id: int
    publication_year: Optional[int] = None
    genre: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


@app.post("/authors/", response_model=models.Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/authors/", response_model=List[Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors

@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(
        title=book.title, 
        author_id=book.author_id, 
        publication_year=book.publication_year, 
        genre=book.genre
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

