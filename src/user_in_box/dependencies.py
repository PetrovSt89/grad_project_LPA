from fastapi import HTTPException

from src.models import Box, User, UserBox
from src.box.utils import read_json_dependence


def userbox_by_user_by_box(user: User, box: Box) -> UserBox:
    userbox = UserBox.query.filter(
        UserBox.user_id == user.id).filter(UserBox.box_id == box.id).first()
    return userbox


def check_userbox(userbox: UserBox) -> None:    
    if userbox:
        raise HTTPException(
            status_code=400,
            detail='Пользователь уже зарегистрирован'
        )


def check_not_userbox(userbox: UserBox) -> None:    
    if not userbox:
        raise HTTPException(
            status_code=400,
            detail='Пользователь не зарегистрирован в коробку'
        )
    

def check_box_dependence(box: Box, user: User) -> None:
    box_dependence = read_json_dependence(filename=box.boxname)
    if box_dependence[user.username]:
        raise HTTPException(
            status_code=400,
            detail='Сначала удалите пользователя из жеребьевки'
        )