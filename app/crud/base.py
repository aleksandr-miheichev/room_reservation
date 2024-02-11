from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


class CRUDBase[
    ModelType:Base,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel
]:
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> ModelType | None:
        # Получаем объект класса Result.
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        # Извлекаем из него конкретное значение.
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> list[ModelType]:
        # Получаем все объекты класса из БД.
        db_objs = await session.execute(select(self.model))
        # Преобразуем результат в список объектов класса.
        return list(db_objs.scalars().all())

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            # Добавьте опциональный параметр user.
            user: User | None = None
    ) -> ModelType:
        # Конвертируем объект класса в словарь.
        obj_in_data = obj_in.model_dump()
        # Если пользователь был передан...
        if user is not None:
            # ...то дополнить словарь для создания модели.
            obj_in_data['user_id'] = user.id
        # Создаём объект модели. В параметры передаём пары
        # "ключ=значение", для этого распаковываем словарь.
        db_obj = self.model(**obj_in_data)
        # Добавляем созданный объект в сессию.
        # Никакие действия с базой пока ещё не выполняются.
        session.add(db_obj)
        # Записываем изменения непосредственно в БД.
        # Так как сессия асинхронная, используем ключевое слово await.
        await session.commit()
        # Обновляем объект db_obj: считываем данные из БД, чтобы получить
        # его id.
        await session.refresh(db_obj)
        # Возвращаем только что созданный объект класса.
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        # Представляем объект из БД в виде словаря.
        obj_data = jsonable_encoder(db_obj)
        # Конвертируем объект с данными из запроса в словарь,
        # исключаем неустановленные пользователем поля.
        update_data = obj_in.model_dump(exclude_unset=True)

        # Перебираем все ключи словаря, сформированного из БД-объекта.
        for field in obj_data:
            # Если конкретное поле есть в словаре с данными из запроса, то...
            if field in update_data:
                # ...устанавливаем объекту БД новое значение атрибута.
                setattr(db_obj, field, update_data[field])
        # Добавляем обновленный объект в сессию.
        session.add(db_obj)
        # Фиксируем изменения.
        await session.commit()
        # Обновляем объект из БД.
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        # Удаляем объект из БД.
        await session.delete(db_obj)
        # Фиксируем изменения в БД.
        await session.commit()
        # Не обновляем объект через метод refresh(),
        # следовательно он всё ещё содержит информацию об удаляемом объекте.
        return db_obj
