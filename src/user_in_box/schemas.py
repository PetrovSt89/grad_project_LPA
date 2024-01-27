from pydantic import BaseModel, ConfigDict


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBoxBase(TunedModel):
    pass


class UserBox(UserBoxBase):
    recipient: str
