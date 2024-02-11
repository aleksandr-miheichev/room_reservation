from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


class CRUDMeetingRoom(
    CRUDBase[MeetingRoom, MeetingRoomCreate, MeetingRoomUpdate]
):
    async def get_room_id_by_name(
            self,
            room_name: str,
            session: AsyncSession,
    ) -> int | None:
        # Получаем объект класса Result.
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(
                MeetingRoom.name == room_name
            )
        )
        # Извлекаем из него конкретное значение.
        db_room_id = db_room_id.scalars().first()
        return db_room_id


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
