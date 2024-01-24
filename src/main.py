from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.admin.router import router as admin_router
from src.box.router import router as box_router
from src.user_in_box.router import router as userbox_router


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
app.include_router(admin_router)
app.include_router(box_router)
app.include_router(userbox_router)
