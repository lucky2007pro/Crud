from fastapi import FastAPI
from book.router import router as book_router
from user.router import router as user_router
from user.schema import Settings
from fastapi_jwt_auth2 import AuthJWT


app = FastAPI()

app.include_router(book_router, prefix='')
app.include_router(user_router, prefix='')

@AuthJWT.load_config
def get_config():
    return Settings()