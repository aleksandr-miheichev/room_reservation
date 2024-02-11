from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Reservation, User
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation(
    CRUDBase[Reservation, ReservationCreate, ReservationUpdate]
):
    async def get_reservations_at_the_same_time(
            self,
            # Добавляем звёздочку, чтобы обозначить, что все дальнейшие
            # параметры должны передаваться по ключу. Это позволит располагать
            # параметры со значением по умолчанию перед параметрами без таких
            # значений.
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            # Добавляем новый опциональный параметр - id объекта бронирования.
            reservation_id: int | None = None,
            session: AsyncSession,
    ) -> list[Reservation]:
        """Выбрать такие объекты Reservation, где выполняются следующие
        условия: номер переговорки равен заданному и верны следующие
        условия: начало бронирования меньше конца существующего объекта
        бронирования, окончание бронирования больше начала существующего
        объекта бронирования."""

        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            (from_reserve <= Reservation.to_reserve) &
            (to_reserve >= Reservation.from_reserve)
        )

        # Если передан id бронирования...
        if reservation_id is not None:
            # ... то к выражению нужно добавить новое условие.
            select_stmt = select_stmt.where(
                # id искомых объектов не равны id обновляемого объекта.
                Reservation.id != reservation_id
            )
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return list(reservations)

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession
    ) -> list[Reservation]:
        """Выбрать все будущие бронирования для указанной переговорки."""
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return list(reservations)

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ) -> list[Reservation]:
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id
            )
        )
        return list(reservations.scalars().all())


reservation_crud = CRUDReservation(Reservation)
