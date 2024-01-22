from fastapi import APIRouter, Depends

from typing import Annotated

from src.auth.schemas import UserCreate, UserAuth
from src.auth.crud import reg_user_rest, get_user_by_token
from src.auth.secure import apikey_scheme
from src.auth.tokens import cr_token


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/process-reg', status_code=201)
def process_reg_rest(user_data: UserCreate):
    reg_user_rest(user_data=user_data)


@router.post('/token', status_code=201)
def create_token(user_data: UserAuth):
    cr_token(user_data=user_data)


@router.get('/self')
def get_user(access_token: Annotated[str, Depends(apikey_scheme)]):
    return get_user_by_token(access_token=access_token)
