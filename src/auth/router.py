from fastapi import APIRouter, Depends

from typing import Annotated

from src.auth.schemas import UserCreate, UserAuth, ResponseOk
from src.auth.crud import reg_user, get_user_by_token
from src.auth.secure import apikey_scheme
from src.auth.tokens import create_new_token


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/process-reg', status_code=201)
def process_reg(user: UserAuth) -> ResponseOk:
    reg_user(user_data=user)
    return ResponseOk


@router.post('/token', status_code=201)
def create_token(user: UserCreate) -> ResponseOk:
    create_new_token(user=user)
    return ResponseOk


@router.get('/self')
def get_user(access_token: Annotated[str, Depends(apikey_scheme)]):
    return get_user_by_token(access_token=access_token)
