from fastapi import HTTPException

from src.db import db_session
from src.models import User
from src.auth.schemas import UserRead
from src.admin.enums import RoleOfUser


def get_users(auth_user: UserRead, skip: int = 0, limit: int = 100) -> list[UserRead]:
    if auth_user.role_id != RoleOfUser.admin.value:
        raise HTTPException(
            status_code=400,
            detail='Вы не админ'
        )
    return db_session.query(User).offset(skip).limit(limit).all()
