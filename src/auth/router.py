from fastapi import APIRouter, Depends

from typing import Annotated, Dict

from src.auth.schemas import UserCreate, UserAuth
from src.auth.crud import reg_user, get_user_by_token
from src.auth.secure import apikey_scheme
from src.auth.tokens import cr_token


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/process-reg', status_code=201)
def process_reg(user: UserAuth) -> Dict[str, str]:
    reg_user(user_data=user)
    return {'message': 'ок'}


@router.post('/token', status_code=201)
def create_token(user: UserCreate) -> Dict[str, str]:
    cr_token(user=user)
    return {'message': 'ок'}


@router.get('/self')
def get_user(access_token: Annotated[str, Depends(apikey_scheme)]):
    return get_user_by_token(access_token=access_token)
