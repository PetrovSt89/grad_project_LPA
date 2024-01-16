import uuid
from fastapi import HTTPException
from sqlalchemy import select
from starlette.status import HTTP_404_NOT_FOUND

from src.auth.schemas import UserCreate
from src.auth.models import Token, User
from src.auth.secure import pwd_context
from src.db import db_session


def cr_token(user_data: UserCreate):
    user: User = db_session.scalar(select(User).where(User.username == user_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    if not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Неверный пароль')
    
    token: Token = Token(user_id=user.id, access_token=str(uuid.uuid4()))
    db_session.add(token)
    db_session.commit()