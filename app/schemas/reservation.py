from datetime import datetime, timedelta
from typing import Annotated

from pydantic import (BaseModel,
                      Field,
                      ConfigDict,
                      field_validator,
                      model_validator)

FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec='minutes')
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: Annotated[datetime, Field(examples=[FROM_TIME])]
    to_reserve: Annotated[datetime, Field(examples=[TO_TIME])]
    # запретить пользователю передавать параметры, не описанные в схеме
    model_config = ConfigDict(extra='forbid')


class ReservationUpdate(ReservationBase):
    @field_validator("from_reserve")
    @classmethod
    def check_from_reserve_later_than_now(cls, value: datetime):
        if value < datetime.now():
            raise ValueError(
                "Время начала бронирования не может быть меньше текущего "
                "времени"
            )
        return value

    @model_validator(mode="after")
    def check_from_reserve_before_to_reserve(self):
        if self.from_reserve >= self.to_reserve:
            raise ValueError(
                "Время начала бронирования не может быть больше времени "
                "окончания"
            )
        return self


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    user_id: Annotated[int | None, Field(default=None)]
    # схема может принимать на вход объект базы данных, а не только
    # Python-словарь или JSON-объект
    model_config = ConfigDict(from_attributes=True)
