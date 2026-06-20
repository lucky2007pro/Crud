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

    refresh_token = Authorize.create_refresh_token(subject=user.id)
    access_token = Authorize.create_access_token(subject=user.id)

    return {
        'message': 'User logged in successfully',
        'status': status.HTTP_200_OK,
        'access_token': access_token,
        'refresh_token': refresh_token
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

def profile_update(data: ProfileUpdateSchema, db: Session, Authorize: AuthJWT):
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
        if data.email and data.email != user.email:
            check_user(db, 'email', data.email)
        if data.phone_number and data.phone_number != user.phone_number:
            check_user(db, 'phone_number', data.phone_number)

        user.first_name = data.first_name or user.first_name
        user.last_name = data.last_name or user.last_name
        user.email = data.email or user.email
        user.phone_number = data.phone_number or user.phone_number

        db.commit()
        db.refresh(user)

        return {
            'message': 'User profile updated successfully',
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

def password_change(data: PasswordChangeSchema, db: Session, Authorize: AuthJWT):
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
        is_valid_password = check_password_hash(user.password, data.old_password)
        if not is_valid_password:
            raise HTTPException(
                detail={
                    'message': "Invalid old password",
                },
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        check_pass(data.new_password, data.conf_password)

        if check_password_hash(user.password, data.new_password):
            raise HTTPException(
                detail={
                    'message': "New password cannot be the same as the old password",
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user.password = generate_password_hash(data.new_password)

        db.commit()
        db.refresh(user)

        return {
            'message': 'Password changed successfully',
            'status': status.HTTP_200_OK,
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

def token_refresh(Authorize: AuthJWT):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=current_user)
        return {
            'message': 'Token refreshed successfully',
            'status': status.HTTP_200_OK,
            'access_token': new_access_token
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            detail={
                'message': "Invalid or expired refresh token",
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

def logout(Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()['jti']
        return {
            'message': 'User logged out successfully',
            'status': status.HTTP_200_OK,
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