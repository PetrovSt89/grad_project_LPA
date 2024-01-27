import uuid
from fastapi import HTTPException

from src.auth.schemas import UserCreate
from src.models import Token, User
from src.auth.secure import Hasher
from src.auth.dependencies import user_by_username, check_not_user
from src.db import db_session


def cr_token(user: UserCreate) -> None:
    find_user = user_by_username(username=user.username)
    check_not_user(user=find_user)
    
    if not Hasher.verify_password(user.password, find_user.hashed_password):
        raise HTTPException(status_code=400, detail='Неверный пароль')

    if find_user.tokens:
        raise HTTPException(
            status_code=400, detail='Токен для этого пользователя уже создан')
    
    token: Token = Token(user_id=find_user.id, access_token=str(uuid.uuid4()))
    db_session.add(token)
    db_session.commit()