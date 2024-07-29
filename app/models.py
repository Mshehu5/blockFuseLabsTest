from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship
from .database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    bio = Column(String, index=True)

    items = relationship("Book", back_populates="owner")


class Book(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    publication_year = Column(Integer)
    genre = Column(String)
    # created_at = Column(DateTime, server_default=func.now())
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("Author", back_populates="items")