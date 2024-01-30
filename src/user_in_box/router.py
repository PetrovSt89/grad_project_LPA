from fastapi import APIRouter, Depends

from typing import Annotated

from src.auth.schemas import ResponseOk
from src.box.schemas import BoxCreate, BoxRead
from src.user_in_box.schemas import UserBox
from src.user_in_box.crud import reg_useer_in_box, reg_useer_by_creator, get_box_with_wishes,\
delete_users_in_box, delete_users_by_creator, get_user_recipient
from src.auth.router import get_user_by_token
from src.auth.secure import apikey_scheme


router = APIRouter(
    prefix='/user-in-box',
    tags=['User in box']
)


@router.post('/')
def reg_in_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate,
        wishes: str
        ) -> ResponseOk:
    user = get_user_by_token(access_token=access_token)
    reg_useer_in_box(user=user, box=box, wishes= wishes)
    return ResponseOk


@router.post('/{username}/{wishes}')
def reg_users_by_creator(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate,
        username: str,
        wishes: str
        ) -> ResponseOk:
    user = get_user_by_token(access_token=access_token)
    reg_useer_by_creator(user=user, box=box, username=username, wishes=wishes)
    return ResponseOk


@router.get('/{boxname}', response_model = BoxRead)
def read_users_in_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str
          ) -> BoxRead | None:
    user = get_user_by_token(access_token=access_token)
    box_with_wishes = get_box_with_wishes(user=user, boxname=boxname)

    return box_with_wishes


@router.get('/recipient/{boxname}', response_model = UserBox)
def read_user_recipient(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str,
          ) -> UserBox | None:
    user = get_user_by_token(access_token=access_token)
    recipient = get_user_recipient(user=user, boxname=boxname)
    return UserBox(recipient=recipient)


@router.delete('/{boxname}')
def del_reg_user(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str,
        ) -> ResponseOk:
    user = get_user_by_token(access_token=access_token)
    delete_users_in_box(user=user, boxname=boxname)
    return ResponseOk


@router.delete('/{boxname}/{username}')
def del_users_by_creator(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str,
        username: str
        ) -> ResponseOk:
    user = get_user_by_token(access_token=access_token)
    delete_users_by_creator(user=user, boxname=boxname, username=username)
    return ResponseOk


