from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth2 import AuthJWT
from db import get_db
from user.schema import SignUpSchema, LoginSchema
from user.auth import register, login, profile

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/register")
def register_user(user_data: SignUpSchema, db: Session = Depends(get_db)):
    return register(user_data, db)

@router.post("/login")
def login_user(user_data: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return login(user_data, db, Authorize)

@router.get("/profile")
def get_user_profile(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return profile(db, Authorize)
