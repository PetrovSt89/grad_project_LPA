from fastapi import Depends, FastAPI
from src.auth.crud import get_user_by_token

from src.auth.router import router as auth_router
from src.box.router import router as box_router

from typing import Annotated


app = FastAPI(
    title='Project App'
)


@app.get('/')
def index():
    page_title = 'Нечто'
    current_user = None
    return {
        "page_title": page_title,
        "current_user": current_user
        }


app.include_router(auth_router)
app.include_router(box_router)
