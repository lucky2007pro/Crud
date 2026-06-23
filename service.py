from fastapi_jwt_auth2 import AuthJWT
from sqlalchemy.orm import Session
from user.models import BlackListToken
from fastapi import HTTPException, status, Depends
from db import get_db

def check_token(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()['jti']
        token = db.query(BlackListToken).filter(BlackListToken.jti == jti).first()
        if token:
            raise HTTPException(
                detail={
                    'message': "Token has been revoked",
                },
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            detail={
                'message': "Invalid or expired token",
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )