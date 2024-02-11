from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для будущих моделей."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()

    # Во все таблицы будет добавлено поле ID.
    id: Mapped[int] = mapped_column(primary_key=True)


# создание асинхронного движка.
engine = create_async_engine(settings.database_url)

# создание объектов асинхронной сессии.
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# Асинхронный генератор сессий.
async def get_async_session():
    # Через асинхронный контекстный менеджер и async_sessionmaker
    # открывается сессия.
    async with AsyncSessionLocal() as async_session:
        # Генератор с сессией передается в вызывающую функцию.
        yield async_session
        # Когда HTTP-запрос отработает - выполнение кода вернётся сюда,
        # и при выходе из контекстного менеджера сессия будет закрыта.
