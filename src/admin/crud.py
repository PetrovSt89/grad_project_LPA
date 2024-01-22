from src.db import db_session
from src.models import User
from src.auth.schemas import UserRead
from src.admin.errors import HTTPExceptionAdmin


def get_users(auth_user: UserRead, skip: int = 0, limit: int = 100):
    if auth_user.role_id != 2:
        raise HTTPExceptionAdmin(
            status_code=400,
            detail='Вы не админ'
        )
    return db_session.query(User).offset(skip).limit(limit).all()