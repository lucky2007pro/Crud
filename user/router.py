from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth2 import AuthJWT
from db import get_db
from user.schema import SignUpSchema, LoginSchema, ProfileUpdateSchema, PasswordChangeSchema
from user.auth import register, login, profile, profile_update, password_change, token_refresh, logout
from service import check_token
from permission import is_admin


router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register")
def register_user(user_data: SignUpSchema, db: Session = Depends(get_db)):
    return register(user_data, db)

@router.post("/login")
def login_user(user_data: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return login(user_data, db, Authorize)

@router.get("/profile", dependencies=[Depends(check_token)])
def get_user_profile(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return profile(db, Authorize)

@router.put("/profile_update", dependencies=[Depends(check_token)])
def update_user_profile(user_data: ProfileUpdateSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return profile_update(user_data, db, Authorize)

@router.put("/password_change", dependencies=[Depends(check_token)])
def change_user_password(user_data: PasswordChangeSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return password_change(user_data, db, Authorize)

@router.post("/refresh")
def refresh_token(Authorize: AuthJWT = Depends()):
    return token_refresh(Authorize)

@router.post("/logout", dependencies=[Depends(check_token)])
def logout_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return logout(Authorize, db)