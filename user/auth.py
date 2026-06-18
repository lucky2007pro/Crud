import re

from user.models import User
from user.schema import SignUpSchema, LoginSchema, ProfileUpdateSchema, PasswordChangeSchema
from sqlalchemy.orm import Session
from db import SessionLocal
from db import get_db
from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi_jwt_auth2 import AuthJWT
from fastapi import Depends
from werkzeug.security import generate_password_hash, check_password_hash


def check_user(db: Session, column: str, value: str):
    user = db.query(User).filter(getattr(User, column) == value).first()
    if user:
        raise HTTPException(
            detail={
                'message': f"{column} already exists",
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

def check_pass(password: str, check_password: str):
    if password and check_password and password != check_password:
        raise HTTPException(
            detail={
                'message': "Passwords do not match",
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    if not re.match(regex, password):
        raise HTTPException(
            detail={
                'message': "Password must be at least 8 characters long and contain at least one letter, one number, and one special character",
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return True

def register(user_data: SignUpSchema, session: Session):
    check_user(session, 'username', user_data.username)
    check_user(session, 'email', user_data.email)
    check_user(session, 'phone_number', user_data.phone_number)
    check_pass(user_data.password, user_data.conf_password)

    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        phone_number=user_data.phone_number,
        password=generate_password_hash(user_data.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        'message': 'User registered successfully',
        'status': status.HTTP_201_CREATED,
    }

def login(user_data: LoginSchema, db: Session, Authorize: AuthJWT):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(
            detail={
                'message': "Invalid username",
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    is_valid_password = check_password_hash(user.password, user_data.password)
    if not is_valid_password:
        raise HTTPException(
            detail={
                'message': "Invalid password",
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    refresh_token = Authorize.create_refresh_token(subject=user.username)
    access_token = Authorize.create_access_token(subject=user.username)

    return {
        'message': 'User logged in successfully',
        'status': status.HTTP_200_OK,
        'access_token': str(access_token),
        'refresh_token': str(refresh_token),
    }

def profile(db: Session, Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(
                detail={
                    'message': "User not found",
                },
                status_code=status.HTTP_404_NOT_FOUND
            )
        return {
            'message': 'User profile',
            'status': status.HTTP_200_OK,
            'data': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
            }
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            detail={
                'message': "Invalid or expired token",
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )