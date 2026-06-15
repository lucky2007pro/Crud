from fastapi import FastAPI
from book.router import router as book_router



app = FastAPI()

app.include_router(book_router, prefix='')


