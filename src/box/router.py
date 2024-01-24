from fastapi import APIRouter, Depends

from typing import Annotated

from src.box.schemas import BoxCreate, BoxRead
from src.box.crud import get_boxes, get_box_by_name, create_box, update_box, delete_box, get_rand_list
from src.user_in_box.crud import get_useers_in_box
from src.auth.router import get_user_by_token
from src.auth.secure import apikey_scheme


router = APIRouter(
    prefix='/box',
    tags=['Box']
)


@router.get('/')
def read_boxes_by_creator(
        access_token: Annotated[str, Depends(apikey_scheme)],
        skip: int = 0,
        limit: int = 100,
          ):
    user = get_user_by_token(access_token=access_token)
    boxes = get_boxes(user=user, skip=skip, limit=limit)
    return [{
        'id': box.id,
        'boxname': box.boxname,
        'list_participants': get_useers_in_box(user=user, boxname=box.boxname),
        'creator_id': {'username': box.creator.username, 'id': box.creator.id},
             } for box in boxes]



@router.get('/{boxname}')
def read_box_by_boxname(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str
        ):
    user = get_user_by_token(access_token=access_token)
    box: BoxRead = get_box_by_name(user=user, boxname=boxname)
    return {
        'id': box.id,
        'boxname': box.boxname,
        'list_participants': get_useers_in_box(user=user, boxname=box.boxname),
        'creator_id': {'username': box.creator.username, 'id': box.creator.id},
             }


@router.get('/list/{boxname}')
def get_random_list(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str
        ):
    user = get_user_by_token(access_token=access_token)
    random_dict = get_rand_list(user=user, boxname=boxname)
    return {'result': random_dict}


@router.post('/')
def cr_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate
        ):
    user = get_user_by_token(access_token=access_token)
    create_box(user=user, box=box)
    return {'message': 'ок'}


@router.post('/{new_boxname}')
def change_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate,
        new_boxname: str
               ):
    user = get_user_by_token(access_token=access_token)
    update_box(user=user, box=box, new_boxname=new_boxname)
    return {'message': 'ок'}


@router.delete('/{boxname}')
def del_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate,
        ):
    user = get_user_by_token(access_token=access_token)
    delete_box(user=user, boxname=box.boxname)
    return {'message': 'ок'}
