from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


from src.db import db_session
from src.models import User, Token
from src.auth.schemas import UserCreate
from src.auth.secure import apikey_scheme, Hasher
from src.auth.errors import HTTPExceptionUser, HTTPExceptionToken, \
HTTPExceptionPass, HTTPExceptionAuth, HTTPExceptionEmail, HTTPExceptionRepUser


def reg_user_rest(user_data: UserCreate):
    if db_session.scalar(select(User).where(User.username == user_data.username)):
        raise HTTPExceptionRepUser(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким именем уже существует'
        )
    if db_session.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPExceptionEmail(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Пользователь с такой почтой уже существует'
        )
    user = User(email=user_data.email, username=user_data.username, role_id=1,
                is_active=True, is_superuser=False, is_verified=False)
    user.hashed_password = Hasher.get_password_hash(user_data.password)
    db_session.add(user)
    db_session.commit()
    

def get_user_by_token(access_token: str):
    token = db_session.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        return token.user
    else:
        raise HTTPExceptionAuth(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Пользователь не авторизован'
        )
    

def log_user_token(username: str,token: str):
    user = User.query.filter(User.username == username).first()
    if not user:
        raise HTTPExceptionUser(
            status_code=400,
            detail='Такого пользователя нет'
        )
    
    if not user.tokens == token:
        raise HTTPExceptionToken(
            status_code=400,
            detail='Неверный токен'
        )
    
    return user


def log_user_pass(username: str,password: str):
    user = User.query.filter(User.username == username).first()
    if not user:
        raise HTTPExceptionUser(
            status_code=400,
            detail='Такого пользователя нет'
        )

    if not Hasher.verify_password(password, user.hashed_password):
        raise HTTPExceptionPass(
            status_code=400,
            detail='Неверный пароль'
        )
    return user


def check_token(access_token: Annotated[str, Depends(apikey_scheme)]):
        return access_token