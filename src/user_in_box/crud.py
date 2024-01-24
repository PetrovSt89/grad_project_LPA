from src.db import db_session
from src.models import Box, UserBox, User
from src.auth.schemas import UserRead
from src.box.schemas import BoxCreate
from src.box.utils import read_json_dependence
from src.user_in_box.errors import HTTPExceptionBoxUser, HTTPExceptionRepBoxUser


def reg_useer_in_box(box: BoxCreate, user: UserRead, wishes: str):
    box = Box.query.filter(Box.boxname == box.boxname).first()
    if not box:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Такой коробки нет'
        )
    is_user_in_box = UserBox.query.filter(UserBox.user_id == user.id).filter(UserBox.box_id == box.id).first()
    if is_user_in_box:
        raise HTTPExceptionRepBoxUser(
            status_code=400,
            detail='Пользователь уже зарегистрирован'
        )
    new_user_box = UserBox(box_id=box.id, user_id=user.id, wishes=wishes)
    db_session.add(new_user_box)
    db_session.commit()


def reg_useer_by_creator(box: BoxCreate, user: UserRead, username: str, wishes: str):
    box = Box.query.filter(Box.boxname == box.boxname).first()
    if not box:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Такой коробки нет'
        )
    if box.creator_id != user.id:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Вы не создатель этой таблицы'
        )
    reg_user = User.query.filter(User.username == username).first()
    if not reg_user:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Такого пользователя нет'
        )
    is_user_in_box = UserBox.query.filter(UserBox.user_id == reg_user.id).filter(UserBox.box_id == box.id).first()
    if is_user_in_box:
        raise HTTPExceptionRepBoxUser(
            status_code=400,
            detail='Пользователь уже зарегистрирован'
        )
    new_user_box = UserBox(box_id=box.id, user_id=reg_user.id, wishes=wishes)
    db_session.add(new_user_box)
    db_session.commit()


def get_useers_in_box(boxname: str, user: UserRead, skip: int = 0, limit: int = 100):
    box_input = Box.query.filter(Box.boxname == boxname).first()
    if not box_input:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Такой коробки нет'
        )
    userbox_models = UserBox.query.filter(
        UserBox.box_id == box_input.id
        ).offset(skip).limit(limit).all()
    list_user_wishes = []
    for model in userbox_models:
        list_user_wishes.append((User.query.filter(User.id == model.user_id).first(),model.wishes))

    return list_user_wishes


def get_user_recipient(user: UserRead, boxname: str):
    box_input = Box.query.filter(Box.boxname == boxname).first()
    if not box_input:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Такой коробки нет'
        )
    box_dependence = read_json_dependence(filename=box_input.boxname)
    return box_dependence[user.username]


def delete_users_in_box(user: UserRead, boxname: str):
    box_input = Box.query.filter(Box.boxname == boxname).first()
    if not box_input:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Такой коробки нет'
        )
    userbox = UserBox.query.filter(
        UserBox.user_id == user.id
        ).filter(UserBox.box_id == box_input.id).first()
    if not userbox:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Вы не зарегистрированы в коробку'
        )
    db_session.delete(userbox)
    db_session.commit()


def delete_users_by_creator(user: UserRead, boxname: str, username: str):
    box_input = Box.query.filter(Box.boxname == boxname).first()
    if not box_input:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Такой коробки нет'
        )
    if box_input.creator_id != user.id:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Вы не создатель этой таблицы'
        )
    del_user = User.query.filter(User.username == username).first()
    if not del_user:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Такого пользователя нет'
        )
    userbox = UserBox.query.filter(
        UserBox.user_id == del_user.id
        ).filter(UserBox.box_id == box_input.id).first()
    if not userbox:
        raise HTTPExceptionBoxUser(
            status_code=400,
            detail='Пользователь не зарегистрирован в коробку'
        )
    db_session.delete(userbox)
    db_session.commit()    
