from typing import AsyncGenerator
from sqlalchemy import create_engine, MetaData
from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from te_fast.core.config import settings


engine = create_engine(
    settings.database_url,  # ПРОСТО как есть
    connect_args={"check_same_thread": False}
)

# Для асинхронных операций - правильно преобразуем
async_db_url = settings.database_url.replace("sqlite://", "sqlite+aiosqlite://")
async_engine = create_async_engine(
    async_db_url,
    echo=settings.debug,
    future=True
)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# База для моделей SQLAlchemy
Base = declarative_base()
metadata = MetaData()

# Database для queries
database = Database(settings.database_url)

# Dependency для получения сессии
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Простая инициализация"""
    from te_fast.models.books import books_table
    # Создаем все таблицы из metadata
    metadata.create_all(bind=engine)
    # Подключаемся
    await database.connect()
    print("Database ready ✅")


async def close_db():
    """Закрытие соединения с БД"""
    await database.disconnect()
