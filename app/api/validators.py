from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models import MeetingRoom, Reservation, User


# Корутина, проверяющая уникальность полученного имени переговорки.
async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    # Вызываем функцию проверки уникальности поля name:
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    # Если такой объект уже есть в базе - вызываем ошибку:
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail=f"Переговорка с таким именем - '{room_name}' уже "
                   f"существует!"
        )


async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> MeetingRoom:
    # Получаем объект из БД по ID.
    # В ответ ожидается либо None, либо объект класса MeetingRoom.
    meeting_room = await meeting_room_crud.get(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(
            # Для отсутствующего объекта вернем статус 404 — Not found.
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room


async def check_reservation_intersections(**kwargs) -> None:
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=f"Переговорка занята. "
                   f"Список бронирований: {str(reservations)}."
        )


async def check_reservation_before_edit(
        reservation_id: int,
        session: AsyncSession,
        user: User,
) -> Reservation:
    reservation = await reservation_crud.get(reservation_id, session)
    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail='Бронь не найдена!'
        )
    if reservation.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужую бронь!'
        )
    return reservation
