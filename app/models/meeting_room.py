from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class MeetingRoom(Base):
    # Имя переговорки должно быть не больше 100 символов,
    # уникальным и непустым.
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    # Установите связь между моделями через функцию relationship.
    reservations: Mapped[list['Reservation']] = relationship(cascade='delete')
