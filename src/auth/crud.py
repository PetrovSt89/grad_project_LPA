from fastapi import HTTPException
from sqlalchemy import select

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src.db import db_session
from src.auth.models import User, Token
from src.auth.schemas import UserCreate
from src.auth.secure import pwd_context


def get_users(skip: int = 0, limit: int = 100):
    return db_session.query(User).offset(skip).limit(limit).all()


def reg_user(user_data: UserCreate):
    if db_session.scalar(select(User).where(User.username == user_data.username)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким именем уже существует'
        )
    if db_session.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Пользователь с такой почтой уже существует'
        )
    user = User(email=user_data.email, username=user_data.username, role_id=1,
                is_active=True, is_superuser=False, is_verified=False)
    user.hashed_password = pwd_context.hash(user_data.password)
    db_session.add(user)
    db_session.commit()
    

def get_user_by_token(access_token: str):
    token = db_session.scalar(select(Token).where(Token.access_token == access_token))
    if token:
        return token.user
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Пользователь не авторизован'
        )