from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.auth.router import router as auth_router


app = FastAPI(
    title='Project App'
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory='src/templates')


@app.get('/')
def index(request: Request):
    page_title = 'Нечто'
    return templates.TemplateResponse(name='base.html',
                                      request=request,
                                      context={"page_title": page_title})


app.include_router(auth_router)
