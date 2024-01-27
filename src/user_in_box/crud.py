from fastapi import HTTPException
from typing import List, Tuple

from src.db import db_session
from src.models import Box, UserBox, User
from src.auth.schemas import UserRead
from src.box.schemas import BoxCreate, BoxRead
from src.box.utils import read_json_dependence
from src.box.crud import get_boxes, get_box_by_name


def reg_useer_in_box(box: BoxCreate, user: UserRead, wishes: str) -> None:
    box = Box.query.filter(Box.boxname == box.boxname).first()
    if not box:
        raise HTTPException(
            status_code=400,
            detail='Такой коробки нет'
        )
    is_user_in_box = UserBox.query.filter(
        UserBox.user_id == user.id).filter(UserBox.box_id == box.id).first()
    if is_user_in_box:
        raise HTTPException(
            status_code=400,
            detail='Пользователь уже зарегистрирован'
        )
    new_user_box = UserBox(box_id=box.id, user_id=user.id, wishes=wishes)
    db_session.add(new_user_box)
    db_session.commit()


def reg_useer_by_creator(
        box: BoxCreate,
        user: UserRead,
        username: str,
        wishes: str
        ) -> None:
    box = Box.query.filter(Box.boxname == box.boxname).first()
    if not box:
        raise HTTPException(
            status_code=400,
            detail='Такой коробки нет'
        )
    if box.creator_id != user.id:
        raise HTTPException(
            status_code=400,
            detail='Вы не создатель этой таблицы'
        )
    reg_user = User.query.filter(User.username == username).first()
    if not reg_user:
        raise HTTPException(
            status_code=400,
            detail='Такого пользователя нет'
        )
    is_user_in_box = UserBox.query.filter(
        UserBox.user_id == reg_user.id).filter(UserBox.box_id == box.id).first()
    if is_user_in_box:
        raise HTTPException(
            status_code=400,
            detail='Пользователь уже зарегистрирован'
        )
    new_user_box = UserBox(box_id=box.id, user_id=reg_user.id, wishes=wishes)
    db_session.add(new_user_box)
    db_session.commit()


def get_useers_in_box(
        boxname: str
        ) -> List[Tuple[UserRead, str]]:
    
    box_input = Box.query.filter(Box.boxname == boxname).first()

    if not box_input:
        raise HTTPException(
            status_code=400,
            detail='Такой коробки нет'
        )
    userbox_models = UserBox.query.filter(
        UserBox.box_id == box_input.id
        ).all()
    list_user_wishes = []
    for model in userbox_models:
        list_user_wishes.append(
            (User.query.filter(User.id == model.user_id).first(),
             model.wishes)
             )

    return list_user_wishes


def get_list_boxes_with_wishes(
        user: UserRead,
        skip: int = 0,
        limit: int = 100
        ) -> List[BoxRead]:
    
    boxes = get_boxes(user=user, skip=skip, limit=limit)

    return [{
        'id': box.id,
        'boxname': box.boxname,
        'list_participants': get_useers_in_box(boxname=box.boxname),
        'creator': {'username': box.creator.username, 'id': box.creator.id},
             } for box in boxes]


def get_box_with_wishes(
        user: UserRead,
        boxname: str,
        ) -> BoxRead:
    
    box = get_box_by_name(user=user, boxname=boxname)

    return {
        'id': box.id,
        'boxname': box.boxname,
        'list_participants': get_useers_in_box(boxname=box.boxname),
        'creator': {'username': box.creator.username, 'id': box.creator.id},
             }


def get_user_recipient(user: UserRead, boxname: str) -> str:
    box_input = Box.query.filter(Box.boxname == boxname).first()
    if not box_input:
        raise HTTPException(
            status_code=400,
            detail='Такой коробки нет'
        )
    box_dependence = read_json_dependence(filename=box_input.boxname)
    return box_dependence[user.username]


def delete_users_in_box(user: UserRead, boxname: str) -> None:
    box_input = Box.query.filter(Box.boxname == boxname).first()
    if not box_input:
        raise HTTPException(
            status_code=400,
            detail='Такой коробки нет'
        )
    userbox = UserBox.query.filter(
        UserBox.user_id == user.id
        ).filter(UserBox.box_id == box_input.id).first()
    if not userbox:
        raise HTTPException(
            status_code=400,
            detail='Вы не зарегистрированы в коробку'
        )
    db_session.delete(userbox)
    db_session.commit()


def delete_users_by_creator(user: UserRead, boxname: str, username: str) -> None:
    box_input = Box.query.filter(Box.boxname == boxname).first()
    if not box_input:
        raise HTTPException(
            status_code=400,
            detail='Такой коробки нет'
        )
    if box_input.creator_id != user.id:
        raise HTTPException(
            status_code=400,
            detail='Вы не создатель этой таблицы'
        )
    del_user = User.query.filter(User.username == username).first()
    if not del_user:
        raise HTTPException(
            status_code=400,
            detail='Такого пользователя нет'
        )
    userbox = UserBox.query.filter(
        UserBox.user_id == del_user.id
        ).filter(UserBox.box_id == box_input.id).first()
    if not userbox:
        raise HTTPException(
            status_code=400,
            detail='Пользователь не зарегистрирован в коробку'
        )
    db_session.delete(userbox)
    db_session.commit()    
