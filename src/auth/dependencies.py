from fastapi import HTTPException

from src.models import User

def user_by_username(username) -> User:
    return User.query.filter(User.username == username).first()


def check_user(user: User) -> None:    
    if user:
        raise HTTPException(
            status_code=400,
            detail='Такой пользователь уже есть'
        )


def check_not_user(user: User) -> None:    
    if not user:
        raise HTTPException(
            status_code=400,
            detail='Такого пользователя нет'
        )

