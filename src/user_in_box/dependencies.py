from fastapi import HTTPException

from src.models import Box, User, UserBox, RandPresenter
from src.box.utils import read_json_dependence


def userbox_by_user_by_box(user: User, box: Box) -> UserBox | None:
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
    if not box_dependence:
        return
    if box_dependence[user.username]:
        raise HTTPException(
            status_code=400,
            detail='Сначала удалите пользователя из жеребьевки'
        )
    
def rand_presenter_by_user_by_box(box: Box, user: User) -> RandPresenter | None:
    rand_presenter = RandPresenter.query.filter(
        RandPresenter.box_id == box.id
        ).filter(RandPresenter.presenter == user.username).first()
    return rand_presenter


def check_rand_presenter_box_dependence(box: Box, user: User) -> None:
    rand_presenter = rand_presenter_by_user_by_box(box=box, user=user)
    
    if rand_presenter:
        raise HTTPException(
            status_code=400,
            detail='Сначала удалите пользователя из жеребьевки'
        )