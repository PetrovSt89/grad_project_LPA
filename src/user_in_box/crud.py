from src.db import db_session
from src.models import UserBox, User
from src.auth.schemas import UserRead
from src.auth.dependencies import user_by_username, check_not_user
from src.box.schemas import BoxCreate, BoxRead
from src.box.crud import get_boxes, get_box_by_name
from src.box.dependencies import box_by_name, check_creator
from src.user_in_box.dependencies import userbox_by_user_by_box, check_userbox,\
check_not_userbox, rand_presenter_by_user_by_box, check_rand_presenter_box_dependence


def reg_useer_in_box(box: BoxCreate, user: UserRead, wishes: str) -> None:
    box = box_by_name(boxname=box.boxname)
    userbox = userbox_by_user_by_box(user=user, box=box)
    check_userbox(userbox=userbox)
    new_user_box = UserBox(box_id=box.id, user_id=user.id, wishes=wishes)
    db_session.add(new_user_box)
    db_session.commit()


def reg_useer_by_creator(
        box: BoxCreate,
        user: UserRead,
        username: str,
        wishes: str
        ) -> None:
    box = box_by_name(boxname=box.boxname)
    check_creator(box=box, user=user)
    
    reg_user = user_by_username(username)

    check_not_user(user=reg_user)

    userbox = userbox_by_user_by_box(user=reg_user, box=box)
    check_userbox(userbox=userbox)
    new_user_box = UserBox(box_id=box.id, user_id=reg_user.id, wishes=wishes)
    db_session.add(new_user_box)
    db_session.commit()


def get_useers_in_box(
        boxname: str
        ) -> list[tuple[UserRead, str]] | None:
    
    box_input = box_by_name(boxname=boxname)    
    userbox_models = UserBox.query.filter(
        UserBox.box_id == box_input.id
        ).all()
    list_user_wishes = [(User.query.filter(User.id == model.user_id).first(),
             model.wishes) for model in userbox_models]

    return list_user_wishes


def get_list_boxes_with_wishes(
        user: UserRead,
        skip: int = 0,
        limit: int = 100
        ) -> list[BoxRead] | None:
    
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
        ) -> BoxRead | None:
    
    box = get_box_by_name(user=user, boxname=boxname)

    return {
        'id': box.id,
        'boxname': box.boxname,
        'list_participants': get_useers_in_box(boxname=box.boxname),
        'creator': {'username': box.creator.username, 'id': box.creator.id},
             }


def get_user_recipient(user: UserRead, boxname: str) -> str:
    box_input = box_by_name(boxname=boxname)
    box_dependence = rand_presenter_by_user_by_box(box=box_input, user=user).recipient

    return box_dependence


def delete_users_in_box(user: UserRead, boxname: str) -> None:
    box_input = box_by_name(boxname=boxname)
    userbox = userbox_by_user_by_box(user=user, box=box_input)
    
    check_not_userbox(userbox=userbox)

    check_rand_presenter_box_dependence(box=box_input, user=user)

    db_session.delete(userbox)
    db_session.commit()


def delete_users_by_creator(user: UserRead, boxname: str, username: str) -> None:
    box_input = box_by_name(boxname=boxname)
    check_creator(box=box_input, user=user)
    
    del_user = user_by_username(username)
    
    check_not_user(user=del_user)
    
    check_rand_presenter_box_dependence(box=box_input, user=del_user)

    userbox = userbox_by_user_by_box(user=del_user, box=box_input)
    
    check_not_userbox(userbox=userbox)
    db_session.delete(userbox)
    db_session.commit()    
