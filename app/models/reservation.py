from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Reservation(Base):
    from_reserve: Mapped[datetime]
    to_reserve: Mapped[datetime]
    # Столбец с внешним ключом: ссылка на таблицу meetingroom.
    meetingroom_id: Mapped[int] = mapped_column(ForeignKey('meetingroom.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey(column='user.id'))

    def __repr__(self):
        return (
            f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
        )
