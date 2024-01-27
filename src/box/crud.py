from typing import List, Dict

from src.db import db_session
from src.models import Box, UserBox, User
from src.auth.schemas import UserRead
from src.box.schemas import BoxCreate, BoxRead
from src.box.utils import test_random, create_json_dependence
from src.box.dependencies import box_by_name, check_creator


def get_boxes(user: UserRead, skip: int = 0, limit: int = 100) -> List[Box]:
    all_boxes = Box.query.filter(Box.creator_id == user.id).offset(skip).limit(limit).all()
    return all_boxes


def get_box_by_name(user: UserRead, boxname: str) -> BoxRead:
    box = box_by_name(boxname=boxname)
    check_creator(box=box, user=user)
    return box


def cr_rand_list(user: UserRead, boxname: str) -> Dict[str, str]:
    box = box_by_name(boxname=boxname)
    check_creator(box=box, user=user)
    box_list = UserBox.query.filter(UserBox.box_id == box.id).all()
    users = [User.query.filter(User.id == userbox.user_id).first() for userbox in box_list]
    
    dependence = test_random(users)
    create_json_dependence(filename=f'{box.boxname}', person_dict=dependence)
    return dependence


def create_box(box: BoxCreate, user: UserRead) -> None:
    new_box = Box(boxname=box.boxname, creator_id=user.id)
    db_session.add(new_box)
    db_session.commit()


def update_box(user: UserRead, box: BoxCreate, new_boxname: str) -> None:
    box = box_by_name(boxname=box.boxname)
    check_creator(box=box, user=user)
    box.boxname = new_boxname
    db_session.commit()


def delete_box(user: UserRead, boxname: str) -> None:
    box = box_by_name(boxname=boxname)
    check_creator(box=box, user=user)
    db_session.delete(box)
    db_session.commit()
