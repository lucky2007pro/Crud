from db import Base
from sqlalchemy import Column, String, Integer, Numeric, Text, Boolean, \
    ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from user.models import User


class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    year = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    
    books = relationship('Book', back_populates='author')
    

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    created_at = Column(DateTime, default=func.now())

    
    books = relationship('Book', back_populates='category')


class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    year = Column(Integer)
    price = Column(Numeric(12, 2))
    desc = Column(Text, nullable=True)
    is_published = Column(Boolean, default=True)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'))
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())

    
    author = relationship('Author', back_populates='books')
    category = relationship('Category', back_populates='books')
    comments = relationship('Comment', back_populates='book')
    
    
class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    summary = Column(String(120))
    user = Column(String(50))
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())

    
    book = relationship('Book', back_populates='comments')
    
class Saved(Base):
    __tablename__ = 'saveds'
    
    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now())


    book = relationship('Book')
    
    
class Cart(Base):
    __tablename__ = 'carts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())
    total_price = Column(Numeric(12, 2))

    
    user = relationship('User')
    book = relationship('Book')



class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())
    total_price = Column(Numeric(12, 2))

    
    user = relationship('User')
    book = relationship('Book')
