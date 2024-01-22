from pydantic import BaseModel
from fastapi import HTTPException
from typing import List


class TunedModel(BaseModel):
    class Config:
        from_attributes = True

    # model_config = ConfigDict(from_attributes=True)


class BoxBase(TunedModel):
    boxname: str


class BoxCreate(BoxBase):
    pass


class BoxRead(BoxBase):
    id: int
    creator_id: int
    list_participants: List

