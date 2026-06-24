from fastapi import APIRouter, Depends
from db import get_db
import book.crud as crud
import book.schema as schema
from sqlalchemy.orm import Session
from service import check_token
from permission import is_admin, is_owner, is_owner_or_readonly, is_owner_or_admin, get_current_user
from user.models import User


router = APIRouter(dependencies=[Depends(check_token)])


@router.post('/create-author', dependencies=[Depends(is_admin)])
def create_author_router(data:schema.CreateAuthorSchema , session: Session = Depends(get_db)):
    return crud.create_author(session, data)

@router.get('/detail-author/{author_id}')
def detail_author_router(author_id:int, session: Session = Depends(get_db)):
    return crud.author_detail(session, author_id)

@router.get('/list-author/')
def list_author_router(session: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return crud.author_list(session, limit, offset)

@router.patch('/update-author/{author_id}', dependencies=[Depends(is_admin)])
def update_author_router(author_id:int, data: schema.UpdateAuthorSchema ,session: Session = Depends(get_db)):
    return crud.update_author(session, data, author_id)

@router.delete('/delete-author/{author_id}', dependencies=[Depends(is_admin)])
def delete_author_router(author_id:int, session: Session = Depends(get_db)):
    return crud.author_delete(session, author_id)


#CATEGORY
@router.post('/create-category', dependencies=[Depends(is_admin)])
def create_category_router(data:schema.CreateCategorySchema , session: Session = Depends(get_db)):
    return crud.create_category(session, data)

@router.get('/detail-category/{category_id}')
def detail_category_router(category_id:int, session: Session = Depends(get_db)):
    return crud.category_detail(session, category_id)

@router.get('/list-category/')
def list_category_router(session: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return crud.category_list(session, limit, offset)

@router.patch('/update-category/{category_id}', dependencies=[Depends(is_admin)])
def update_category_router(category_id:int, data: schema.UpdateCategorySchema ,session: Session = Depends(get_db)):
    return crud.update_category(session, data, category_id)

@router.delete('/delete-category/{category_id}', dependencies=[Depends(is_admin)])
def delete_category_router(category_id:int, session: Session = Depends(get_db)):
    return crud.category_delete(session, category_id)


#BOOK
@router.post('/create-book', dependencies=[Depends(is_admin)])
def create_book_router(data:schema.CreateBookSchema , session: Session = Depends(get_db)):
    return crud.create_book(session, data)

@router.get('/detail-book/{book_id}')
def detail_book_router(book_id:int, session: Session = Depends(get_db)):
    return crud.book_detail(session, book_id)

@router.get('/list-book/')
def list_book_router(session: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return crud.book_list(session, limit, offset)

@router.get('/filter-book/')
def filter_book_router(title: str = None, desc: str = None, session: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return crud.filter_book(session, title, desc, limit, offset)

@router.get('/search-book/')
def search_book_router(query_str: str = None, session: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return crud.search_book(session, query_str, limit, offset)

@router.patch('/update-book/{book_id}', dependencies=[Depends(is_admin)])
def update_book_router(book_id:int, data: schema.UpdateBookSchema ,session: Session = Depends(get_db)):
    return crud.update_book(session, data, book_id)

@router.delete('/delete-book/{book_id}', dependencies=[Depends(is_admin)])
def delete_book_router(book_id:int, session: Session = Depends(get_db)):
    return crud.book_delete(session, book_id)


#COMMENT
@router.post('/create-comment')
def create_comment_router(data:schema.CreateCommentSchema , session: Session = Depends(get_db)):
    return crud.create_comment(session, data)

@router.get('/detail-comment/{comment_id}', dependencies=[Depends(is_owner_or_readonly)])
def detail_comment_router(comment_id:int, session: Session = Depends(get_db)):
    return crud.comment_detail(session, comment_id)

@router.get('/list-comment/')
def list_comment_router(session: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return crud.comment_list(session, limit, offset)

@router.patch('/update-comment/{comment_id}', dependencies=[Depends(is_owner)])
def update_comment_router(comment_id:int, data: schema.UpdateCommentSchema ,session: Session = Depends(get_db)):
    return crud.update_comment(session, data, comment_id)

@router.delete('/delete-comment/{comment_id}', dependencies=[Depends(is_owner_or_admin)])
def delete_comment_router(comment_id:int, session: Session = Depends(get_db)):
    return crud.comment_delete(session, comment_id)


#SAVED
@router.post('/create-saved')
def create_saved_router(data:schema.CreateSavedSchema , session: Session = Depends(get_db)):
    return crud.create_saved(session, data)

@router.get('/detail-saved/{saved_id}', dependencies=[Depends(is_owner)])
def detail_saved_router(saved_id:int, session: Session = Depends(get_db)):
    return crud.saved_detail(session, saved_id)

@router.get('/list-saved/')
def list_saved_router(session: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return crud.saved_list(session, limit, offset)

@router.patch('/update-saved/{saved_id}', dependencies=[Depends(is_owner)])
def update_saved_router(saved_id:int, data: schema.UpdateSavedSchema ,session: Session = Depends(get_db)):
    return crud.update_saved(session, data, saved_id)

@router.delete('/delete-saved/{saved_id}', dependencies=[Depends(is_owner_or_admin)])
def delete_saved_router(saved_id:int, session: Session = Depends(get_db)):
    return crud.saved_delete(session, saved_id)


#CART AND ORDER
@router.post('/create-cart')
def create_cart_router(data: schema.CreateCartSchema, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_cart(session, data, current_user.id)

@router.patch('/update-cart/{cart_id}', dependencies=[Depends(is_owner)])
def update_cart_router(cart_id: int, data: schema.UpdateCartSchema, session: Session = Depends(get_db)):
    return crud.update_cart(session, data, cart_id)

@router.delete('/delete-cart/{cart_id}', dependencies=[Depends(is_owner)])
def delete_cart_router(cart_id: int, session: Session = Depends(get_db)):
    return crud.delete_cart(session, cart_id)

@router.get('/my-cart/')
def list_cart_router(session: Session = Depends(get_db), current_user: User = Depends(get_current_user), limit: int = 10, offset: int = 0):
    return crud.cart_list(session, current_user, limit, offset)

@router.post('/checkout/')
def checkout_router(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.checkout(session, current_user)

@router.get('/my-orders/')
def list_orders_router(session: Session = Depends(get_db), current_user: User = Depends(get_current_user), limit: int = 10, offset: int = 0):
    return crud.order_list(session, current_user, limit, offset)
