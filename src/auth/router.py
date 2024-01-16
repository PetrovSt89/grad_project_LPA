from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from typing import Annotated

from src.auth.forms import RegistrationForm, LoginForm, UserException,\
EmailException, PassException
from src.auth.models import User as AuthUser
from src.auth.schemas import UserCreate
from src.auth.crud import get_users, reg_user, get_user_by_token
from src.auth.secure import apikey_scheme
from src.auth.tokens import cr_token
from src.db import db_session

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

templates = Jinja2Templates(directory='src/templates')


# получение всех юзеров, может понадобиться для админки
@router.get('/users')
def users(skip: int = 0, limit: int = 100):
    users = get_users(skip=skip, limit=limit)
    return users


# пароль с хешом, сделаный через passlib
@router.post('/pr-reg', status_code=201)
def register_user(user_data: UserCreate):
    reg_user(user_data=user_data)


# аутентификация через токен
@router.post('/token', status_code=201)
def create_token(user_data: UserCreate):
    cr_token(user_data=user_data)


# получение данных аутентифицированного пользователя
@router.get('/self')
def get_user(access_token: Annotated[str, Depends(apikey_scheme)]):
    return get_user_by_token(access_token=access_token)


@router.get('/register')
def register(request: Request):
    page_title = 'Регистрация'
    # reg_form = RegistrationForm() # не доделано, просто прокинуто в шаблон
    return templates.TemplateResponse(name='user/registration.html',
                                      request=request,
                                      context={"page_title": page_title}
                                      )


@router.post('/process-reg')
def process_reg(username: Annotated[str, Form()], email: Annotated[str, Form()], 
             password: Annotated[str, Form()], password2: Annotated[str, Form()]):
    
    form = RegistrationForm(
        username=username,email=email,password=password,password2=password2)
    try:
        if not any((form.validate_username(),
                form.validate_email(),
                form.pas_not_mistake())):
    
        
            new_user = AuthUser(
                username=username, email=email, role_id=1, hashed_password=password,
                is_active = True, is_superuser = False, is_verified = False)
            db_session.add(new_user)
            db_session.commit()
            # flash('Вы успешно зарегистрировались')
            return RedirectResponse(url='/')
        
        else:
            return RedirectResponse(url='user.register')
    except UserException:
        return {'ошибка':'Пользователь с таким именем уже существует'}
    except EmailException:
        return {'ошибка': 'Пользователь с такой почтой уже существует'}
    except PassException:
        return {'ошибка': 'введены разные пароли'}



@router.get('/login')
def login(request: Request):
    page_title = 'Авторизация'
    
    return templates.TemplateResponse(name='user/login.html',
                                      request=request,
                                      context={"page_title": page_title}
                                      )


@router.post('/process_login')
def process_login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    
    form = LoginForm(
        username=username,password=password)
    user = AuthUser.query.filter(AuthUser.username == form.username).first()
    if user and user.password == form.password:
        return RedirectResponse(url='/')
    return RedirectResponse(url='/register')
