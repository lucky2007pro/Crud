from book.models import *
from book.schema import *
from sqlalchemy.orm import Session, joinedload
from db import SessionLocal
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def get_object(session, id, model):
    obj = session.query(model).filter(model.id == id).first()
    if not obj:
        raise HTTPException(
            detail={
                'message': f"{model.__name__} not found",
            },
            status_code=status.HTTP_404_NOT_FOUND
        )
    return obj

def response_model(msg, status, data, etc = None):
    return {
        'msg': msg,
        'status': status,
        'etc': etc,
        'data': data,
    } if etc else {
        'msg': msg,
        'status': status,
        'data': data,
    }
    

#AUTHOR

def create_author(session: Session, data: CreateAuthorSchema):
    author = Author(name=data.name, year=data.year)
    session.add(author)
    session.commit()
    session.refresh(author)
    
    return response_model('Author created', status.HTTP_201_CREATED, author)


def update_author(session: Session, data: UpdateAuthorSchema, author_id: int):
    author = get_object(session, author_id, Author)
    
    data = data.model_dump(exclude_unset=True)
    
    for key, value in data.items():
        setattr(author, key, value)
    
    session.commit()
    session.refresh(author)
    
    return response_model('Author updated', status.HTTP_200_OK, author)


def author_detail(session: Session, author_id: int):
    author = get_object(session, author_id, Author)
    return response_model('Author', status.HTTP_200_OK, {'author': author, 'books': author.books})


def author_list(session: Session, limit: int = 10, offset: int = 0):
    authors = session.query(Author).order_by(Author.id.desc()).offset(offset).limit(limit).all()
    return response_model('Author', status.HTTP_200_OK, authors)

def author_delete(session: Session, author_id: int):
    author = get_object(session, author_id, Author)
    session.delete(author)
    session.commit()
    return response_model('Author deleted', status.HTTP_204_NO_CONTENT, data=None)



#CATEGORY
def create_category(session: Session, data: CreateCategorySchema):
    category = Category(title=data.title)
    session.add(category)
    session.commit()
    session.refresh(category)
        
    return response_model('Category created', status.HTTP_201_CREATED, category)

def update_category(session: Session, data: UpdateCategorySchema, category_id: int):
    category = get_object(session, category_id, Category)
    
    data = data.model_dump(exclude_unset=True)
    
    for key, value in data.items():
        setattr(category, key, value)
    
    session.commit()
    session.refresh(category)
    
    return response_model('Category updated', status.HTTP_200_OK, category)


def category_detail(session: Session, category_id: int):
    category = get_object(session, category_id, Category)
    return response_model('category', status.HTTP_200_OK, {'category': category, 'books': category.books})

def category_delete(session: Session, category_id:int):
    category = get_object(session, category_id, Category)
    session.delete(category)
    session.commit()
    return response_model('category deleted', status.HTTP_204_NO_CONTENT, data=None)


def category_list(session: Session, limit: int = 10, offset: int = 0):
    categories = session.query(Category).order_by(Category.id.desc()).offset(offset).limit(limit).all()
    return response_model('category', status.HTTP_200_OK, categories)


#BOOK

def create_book(session: Session, data: CreateBookSchema):
    book = Book(**data.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
        
    return response_model('book created', status.HTTP_201_CREATED, book)

def update_book(session: Session, data: UpdateBookSchema, book_id: int):
    book = get_object(session, book_id, Book)
    
    data = data.model_dump(exclude_unset=True)
    
    for key, value in data.items():
        setattr(book, key, value)
    
    session.commit()
    session.refresh(book)
    
    return response_model('book updated', status.HTTP_200_OK, book)


def book_detail(session: Session, book_id: int):
    
    book = (
        session.query(Book)
        .options(
            joinedload(Book.author),
            joinedload(Book.category),
            joinedload(Book.comments)
        )
        .filter(Book.id == book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )

    return {
        'id': book.id,
        'title': book.title,
        'year': book.year,
        'price': float(book.price),
        'desc': book.desc,
        'is_published': book.is_published,
        'created_at': book.created_at,

        'author': {
            'id': book.author.id,
            'name': book.author.name,
            'year': book.author.year,
        },

        'category': {
            'id': book.category.id,
            'title': book.category.title,
        },

        'comments':  book.comments
        
    }

def book_delete(session: Session, book_id:int):
    book = get_object(session, book_id, Book)
    session.delete(book)
    session.commit()
    return response_model('book deleted', status.HTTP_204_NO_CONTENT, data=None)


def book_list(session: Session, limit: int = 10, offset: int = 0):
    books = session.query(Book).options(joinedload(Book.author)).order_by(Book.id.desc()).offset(offset).limit(limit).all()
    return response_model('book', status.HTTP_200_OK, books)

def filter_book(session: Session, title: str = None, desc: str = None, limit: int = 10, offset: int = 0):
    query = session.query(Book).options(joinedload(Book.author), joinedload(Book.category))
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if desc:
        query = query.filter(Book.desc.ilike(f"%{desc}%"))
    books = query.order_by(Book.id.desc()).offset(offset).limit(limit).all()
    return response_model('Filtered books', status.HTTP_200_OK, books)

def search_book(session: Session, query_str: str = None, limit: int = 10, offset: int = 0):
    from sqlalchemy import or_
    query = session.query(Book).options(joinedload(Book.author), joinedload(Book.category))
    if query_str:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{query_str}%"),
                Book.desc.ilike(f"%{query_str}%")
            )
        )
    books = query.order_by(Book.id.desc()).offset(offset).limit(limit).all()
    return response_model('Search results', status.HTTP_200_OK, books)



#COMMENT

def create_comment(session: Session, data: CreateCommentSchema):
    comment = Comment(summary=data.summary, book_id=data.book_id, user=data.user)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    
    return response_model('comment created', status.HTTP_201_CREATED, comment)

def update_comment(session: Session, data: UpdateCommentSchema, comment_id: int):
    comment = get_object(session, comment_id, Comment)
    
    data = data.model_dump(exclude_unset=True)
    
    for key, value in data.items():
        setattr(comment, key, value)
    
    session.commit()
    session.refresh(comment)
    
    return response_model('comment updated', status.HTTP_200_OK, comment)

def comment_detail(session: Session, comment_id: int):
    comment = get_object(session, comment_id, Comment)
    return response_model('comment detail', status.HTTP_200_OK, comment)

def comment_list(session: Session, limit: int = 10, offset: int = 0):
    comments = session.query(Comment).order_by(Comment.id.desc()).offset(offset).limit(limit).all()
    return response_model('comment list', status.HTTP_200_OK, comments)

def comment_delete(session: Session, comment_id: int):
    comment = get_object(session, comment_id, Comment)
    session.delete(comment)
    session.commit()
    return response_model('comment deleted', status.HTTP_204_NO_CONTENT, data=None)

#SAVED

def create_saved(session: Session, data: CreateSavedSchema):
    saved = Saved(book_id=data.book_id, user=data.user)
    session.add(saved)
    session.commit()
    session.refresh(saved)
    
    return response_model('saved created', status.HTTP_201_CREATED, saved)

def update_saved(session: Session, data: UpdateSavedSchema, saved_id: int):
    saved = get_object(session, saved_id, Saved)
    
    data = data.model_dump(exclude_unset=True)
    
    for key, value in data.items():
        setattr(saved, key, value)
    
    session.commit()
    session.refresh(saved)
    
    return response_model('saved updated', status.HTTP_200_OK, saved)

def saved_detail(session: Session, saved_id: int):
    saved = get_object(session, saved_id, Saved)
    return response_model('saved detail', status.HTTP_200_OK, saved)

def saved_list(session: Session, limit: int = 10, offset: int = 0):
    saveds = session.query(Saved).order_by(Saved.id.desc()).offset(offset).limit(limit).all()
    return response_model('saved list', status.HTTP_200_OK, saveds)

def saved_delete(session: Session, saved_id: int):
    saved = get_object(session, saved_id, Saved)
    session.delete(saved)
    session.commit()
    return response_model('saved deleted', status.HTTP_204_NO_CONTENT, data=None)


#CART AND ORDER

def create_cart(session: Session, data: CreateCartSchema, user_id: int):
    book = get_object(session, data.book_id, Book)
    total_price = data.quantity * book.price
    cart = Cart(user_id=user_id, book_id=data.book_id, quantity=data.quantity, total_price=total_price)
    session.add(cart)
    session.commit()
    session.refresh(cart)
    
    return response_model('cart created', status.HTTP_201_CREATED, cart)

def update_cart(session: Session, data: UpdateCartSchema, cart_id: int):
    cart = get_object(session, cart_id, Cart)
    
    data_dump = data.model_dump(exclude_unset=True)
    
    for key, value in data_dump.items():
        setattr(cart, key, value)
    
    if 'quantity' in data_dump or 'book_id' in data_dump:
        book = get_object(session, cart.book_id, Book)
        cart.total_price = cart.quantity * book.price
        
    session.commit()
    session.refresh(cart)
    
    return response_model('cart updated', status.HTTP_200_OK, cart)

def delete_cart(session: Session, cart_id: int):
    cart = get_object(session, cart_id, Cart)
    session.delete(cart)
    session.commit()
    return response_model('cart deleted', status.HTTP_204_NO_CONTENT, data=None)

def cart_list(session: Session, user, limit: int = 10, offset: int = 0):
    query = session.query(Cart).options(joinedload(Cart.book))
    if not user.is_staff:
        query = query.filter(Cart.user_id == user.id)
    carts = query.order_by(Cart.id.desc()).offset(offset).limit(limit).all()
    return response_model('cart list', status.HTTP_200_OK, carts)

def checkout(session: Session, user):
    carts = session.query(Cart).filter(Cart.user_id == user.id).all()
    if not carts:
        raise HTTPException(status_code=400, detail="Savatchangiz bo'sh")
    
    orders = []
    for cart in carts:
        order = Order(user_id=user.id, book_id=cart.book_id, quantity=cart.quantity, total_price=cart.total_price)
        session.add(order)
        orders.append(order)
        session.delete(cart)
    
    session.commit()
    return response_model('Buyurtma muvaffaqiyatli qabul qilindi', status.HTTP_201_CREATED, None)

def order_list(session: Session, user, limit: int = 10, offset: int = 0):
    query = session.query(Order).options(joinedload(Order.book))
    if not user.is_staff:
        query = query.filter(Order.user_id == user.id)
    orders = query.order_by(Order.id.desc()).offset(offset).limit(limit).all()
    return response_model('order list', status.HTTP_200_OK, orders)