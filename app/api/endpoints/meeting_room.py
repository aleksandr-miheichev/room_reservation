from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
)
from app.schemas.reservation import ReservationDB

router = APIRouter()


@router.post(
    path='/',
    # Указываем схему ответа.
    response_model=MeetingRoomDB,
    # не возвращать поля, значения которых равны None.
    response_model_exclude_none=True,
    # Добавьте вызов зависимости при обработке запроса.
    dependencies=[Depends(current_superuser)],
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        # Указываем зависимость, предоставляющую объект сессии, как параметр
        # функции.
        session: AsyncSession = Depends(get_async_session),
) -> MeetingRoomDB:
    """Только для суперюзеров."""
    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # и обработка запроса остановится.
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    path='/',
    # Указываем схему ответа.
    response_model=list[MeetingRoomDB],
    # не возвращать поля, значения которых равны None.
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
        # Указываем зависимость, предоставляющую объект сессии, как параметр
        # функции.
        session: AsyncSession = Depends(get_async_session),
) -> list[MeetingRoomDB]:
    rooms = await meeting_room_crud.get_multi(session)
    return rooms


@router.patch(
    # ID обновляемого объекта будет передаваться path-параметром.
    path='/{meeting_room_id}',
    # Указываем схему ответа.
    response_model=MeetingRoomDB,
    # не возвращать поля, значения которых равны None.
    response_model_exclude_none=True,
    # Добавьте вызов зависимости при обработке запроса.
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        # ID обновляемого объекта.
        meeting_room_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: MeetingRoomUpdate,
        # Указываем зависимость, предоставляющую объект сессии, как параметр
        # функции.
        session: AsyncSession = Depends(get_async_session),
) -> MeetingRoomDB:
    """Только для суперюзеров."""
    # Выносим повторяющийся код в отдельную корутину.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        # Если в запросе получено поле name — проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)

    # Передаём в корутину все необходимые для обновления данные.
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    path='/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    # Добавьте вызов зависимости при обработке запроса.
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> MeetingRoomDB:
    """Только для суперюзеров."""
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room


@router.get(
    path='/{meeting_room_id}/reservations',
    response_model=list[ReservationDB],
    # Добавляем множество с полями, которые надо исключить из ответа.
    response_model_exclude={'user_id'},
)
async def get_reservations_for_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> list[ReservationDB]:
    await check_meeting_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id, session=session
    )
    return reservations
