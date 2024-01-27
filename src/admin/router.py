from fastapi import APIRouter, Depends

from typing import Annotated, List

from src.admin.crud import get_users
from src.auth.crud import get_user_by_token
from src.auth.secure import apikey_scheme
from src.auth.schemas import UserRead


router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.get('/users', response_model=List[UserRead])
def users(
        access_token: Annotated[str, Depends(apikey_scheme)],
        skip: int = 0,
        limit: int = 100
        ) -> List[UserRead]:
    auth_user = get_user_by_token(access_token=access_token)
    
    users: List[UserRead] = get_users(auth_user=auth_user, skip=skip, limit=limit)

    return users

