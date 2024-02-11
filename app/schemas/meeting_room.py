from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class MeetingRoomBase(BaseModel):
    name: Annotated[str, Field(default=None, min_length=1, max_length=100)]
    description: Annotated[str | None, Field(default=None)]


class MeetingRoomCreate(MeetingRoomBase):
    name: Annotated[str, Field(min_length=1, max_length=100)]


class MeetingRoomUpdate(MeetingRoomBase):
    pass


class MeetingRoomDB(MeetingRoomCreate):
    id: int
    # схема может принимать на вход объект базы данных, а не только
    # Python-словарь или JSON-объект
    model_config = ConfigDict(from_attributes=True)
