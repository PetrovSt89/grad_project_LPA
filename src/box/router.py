from fastapi import APIRouter, Depends

from typing import Annotated, Dict

from src.box.schemas import BoxCreate, BoxRead
from src.box.crud import create_box, update_box, delete_box, cr_rand_dict
from src.user_in_box.crud import get_list_boxes_with_wishes, get_box_with_wishes
from src.auth.router import get_user_by_token
from src.auth.secure import apikey_scheme


router = APIRouter(
    prefix='/box',
    tags=['Box']
)


@router.get('/', response_model=list[BoxRead])
def read_boxes_by_creator(
        access_token: Annotated[str, Depends(apikey_scheme)],
        skip: int = 0,
        limit: int = 100,
          ) -> list[BoxRead] | None:
    user = get_user_by_token(access_token=access_token)

    list_boxes = get_list_boxes_with_wishes(user=user, skip=skip, limit=limit)

    return list_boxes


@router.get('/{boxname}', response_model = BoxRead)
def read_box_by_boxname(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str
        ) -> BoxRead | None:
    user = get_user_by_token(access_token=access_token)

    box_with_wishes = get_box_with_wishes(user=user, boxname=boxname)

    return box_with_wishes


@router.post('/rand/{boxname}')
def create_random_dict(
        access_token: Annotated[str, Depends(apikey_scheme)],
        boxname: str
        ) -> Dict[str, str]:
    user = get_user_by_token(access_token=access_token)
    random_dict = cr_rand_dict(user=user, boxname=boxname)
    return random_dict


@router.post('/')
def cr_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate
        ) -> Dict[str, str]:
    user = get_user_by_token(access_token=access_token)
    create_box(user=user, box=box)
    return {'message': 'ок'}


@router.patch('/{new_boxname}')
def change_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate,
        new_boxname: str
               ) -> Dict[str, str]:
    user = get_user_by_token(access_token=access_token)
    update_box(user=user, box=box, new_boxname=new_boxname)
    return {'message': 'ок'}


@router.delete('/{boxname}')
def del_box(
        access_token: Annotated[str, Depends(apikey_scheme)],
        box: BoxCreate,
        ) -> Dict[str, str]:
    user = get_user_by_token(access_token=access_token)
    delete_box(user=user, boxname=box.boxname)
    return {'message': 'ок'}
