from fastapi import APIRouter, Depends

from typing import Annotated

from src.box.schemas import BoxCreate, BoxRead
from src.user_in_box.crud import reg_useer_in_box, reg_useer_by_creator, get_useers_in_box,\
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
        ):
    user = get_user_by_token(access_token=access_token)
    reg_useer_in_box(user=user, box=box, wishes= wishes)
    return {'message': 'ок'}


@router.post('/{username}/{wishes}')
def reg_users_by_creator(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate,
        username: str,
        wishes: str
        ):
    user = get_user_by_token(access_token=access_token)
    reg_useer_by_creator(user=user, box=box, username=username, wishes=wishes)
    return {'message': 'ок'}


@router.get('/{boxname}')
def read_users_in_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str,
        skip: int = 0,
        limit: int = 100,
          ):
    user = get_user_by_token(access_token=access_token)
    list_user_wishes = get_useers_in_box(user=user, boxname=boxname, skip=skip, limit=limit)
    return [{
        'id': user.id,
        'boxname': user.email,
        'username': user.username,
        'wishes': wishes
             } for user, wishes in list_user_wishes]


@router.get('/reg-user/{boxname}')
def read_user_recipient(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str,
          ):
    user = get_user_by_token(access_token=access_token)
    recipient = get_user_recipient(user=user, boxname=boxname)
    return {'recipient': recipient}


@router.delete('/{boxname}/{username}')
def del_users_by_creator(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str,
        username: str
        ):
    user = get_user_by_token(access_token=access_token)
    delete_users_by_creator(user=user, boxname=boxname, username=username)
    return {'message': 'ок'}


@router.delete('/{boxname}')
def del_reg_user(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str,
        ):
    user = get_user_by_token(access_token=access_token)
    delete_users_in_box(user=user, boxname=boxname)
    return {'message': 'ок'}
