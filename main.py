from fastapi import FastAPI
from book.router import router as book_router
from user.router import router as user_router
from user.schema import Settings
from fastapi_jwt_auth2 import AuthJWT


app = FastAPI(title='Book Project', description='Kitoblar olami', version='1.0.0')

app.include_router(book_router, prefix='', tags=['book'])
app.include_router(user_router, prefix='/auth', tags=['auth'])

@AuthJWT.load_config
def get_config():
    return Settings()