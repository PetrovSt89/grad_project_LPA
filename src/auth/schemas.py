from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException


class TunedModel(BaseModel):
    class Config:
        from_attributes = True

    # model_config = ConfigDict(from_attributes=True)


class RoleBase(TunedModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int


class UserAuth(TunedModel):
    username: str
    password: str


class UserBase(TunedModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str

    @validator('username')
    def validate_username(cls, value):
        if not value:
            raise HTTPException(
                status_code=422, detail='Это имя не подходит'
            )
        return value


class UserRead(UserBase):
    id: int
    role_id: Role
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class Token(TunedModel):
    access_token: str
