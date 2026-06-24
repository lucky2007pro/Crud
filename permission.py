from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth2 import AuthJWT
from db import get_db
from user.models import User
from book.models import Comment, Saved

def get_current_user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
        current_username = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.username == current_username).first()
        
        if not user:
            raise HTTPException(
                detail={'message': "User not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        return user
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            detail={'message': "Invalid or expired token"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

def is_admin(user: User = Depends(get_current_user)):
    if not user.is_staff:
        raise HTTPException(
            detail={'message': "Sizda ushbu amalni bajarish uchun ruxsat yo'q (Faqat adminlar uchun)"},
            status_code=status.HTTP_403_FORBIDDEN
        )
    return user

def is_owner(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    comment_id = request.path_params.get('comment_id')
    saved_id = request.path_params.get('saved_id')

    if comment_id:
        comment = db.query(Comment).filter(Comment.id == int(comment_id)).first()
        if comment and comment.user != user.username:
            raise HTTPException(
                detail={'message': "Siz bu obyektning egasi emassiz"},
                status_code=status.HTTP_403_FORBIDDEN
            )
    elif saved_id:
        saved = db.query(Saved).filter(Saved.id == int(saved_id)).first()
        if saved and saved.user != user.username:
            raise HTTPException(
                detail={'message': "Siz bu obyektning egasi emassiz"},
                status_code=status.HTTP_403_FORBIDDEN
            )
    return user

def is_owner_or_readonly(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if request.method in ["GET", "HEAD", "OPTIONS"]:
        return user
    return is_owner(request, user, db)

def is_owner_or_admin(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.is_staff:
        return user
    return is_owner(request, user, db)