from pydantic import BaseModel, EmailStr, ConfigDict
from fastapi import Path

from typing import Annotated


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoleBase(TunedModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int


class UserBase(TunedModel):
    pass
    

class Creator(UserBase):
    username: str
    id: int


class UserAuth(UserBase):
    username: str
    password: str
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: str
    

class UserRead(UserBase):
    id: int
    username: str
    email: EmailStr
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class Token(TunedModel):
    access_token: Annotated[str, Path(ge=1, lt=40)]


class ResponseOk(TunedModel):
    message: str = 'ok'
    
