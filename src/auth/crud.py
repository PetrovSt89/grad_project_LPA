from sqlalchemy import select
from fastapi import Depends, HTTPException
from typing import Annotated

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


from src.db import db_session
from src.models import User, Token
from src.auth.schemas import UserAuth
from src.auth.secure import apikey_scheme, Hasher


def reg_user(user_data: UserAuth) -> None:
    
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
    user.hashed_password = Hasher.get_password_hash(user_data.password)
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


def check_token(access_token: Annotated[str, Depends(apikey_scheme)]):
        return access_token