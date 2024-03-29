from pydantic import BaseModel, ConfigDict

from src.auth.schemas import UserRead, Creator


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BoxBase(TunedModel):
    boxname: str


class BoxCreate(BoxBase):
    pass


class BoxRead(BoxBase):
    id: int
    creator: Creator
    list_participants: list[tuple[UserRead, str]] | None

