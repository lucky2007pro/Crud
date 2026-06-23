from fastapi import FastAPI, Depends
from book.router import router as book_router
from user.router import router as user_router
from user.schema import Settings
from fastapi_jwt_auth2 import AuthJWT
from service import check_token

app = FastAPI(title='Book Project', description='Kitoblar olami', version='1.0.0')

app.include_router(book_router, prefix='', tags=['book'])
app.include_router(user_router, prefix='/auth', tags=['auth'])

@AuthJWT.load_config
def get_config():
    return Settings()

@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token: dict, request: Request):
    token_type = decrypted_token['type']
    if token_type != 'access':
        return False
    jti = decrypted_token['jti']
    db = SessionLocal()
    try:
        token = db.query(BlacklistToken).filter(BlacklistToken.jti == jti).first()
        if token:
            return True
        return False
    finally:
        db.close()