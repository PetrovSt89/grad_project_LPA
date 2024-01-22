from fastapi import APIRouter, Depends

from typing import Annotated

from src.admin.crud import get_users
from src.auth.crud import get_user_by_token
from src.auth.secure import apikey_scheme


router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.get('/users')
def users(
        access_token: Annotated[str, Depends(apikey_scheme)],
        skip: int = 0,
        limit: int = 100
        ):
    auth_user = get_user_by_token(access_token=access_token)
    
    users = get_users(auth_user=auth_user, skip=skip, limit=limit)
    return [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role_id': user.role_id,
        'is_active': user.is_active,
        'is_verified': user.is_verified,
        'is_superuser': user.is_superuser
            } for user in users]
