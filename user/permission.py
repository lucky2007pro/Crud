from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth2 import AuthJWT
from db import get_db
from user.models import User

def check_admin(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
        current_username = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.username == current_username).first()
        
        if not user:
            raise HTTPException(
                detail={'message': "User not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
            
        if not user.is_staff:
            raise HTTPException(
                detail={'message': "Sizda ushbu amalni bajarish uchun ruxsat yo'q (Faqat adminlar uchun)"},
                status_code=status.HTTP_403_FORBIDDEN
            )
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            detail={'message': "Invalid or expired token"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )