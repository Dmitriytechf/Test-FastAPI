from sqlalchemy import create_engine, MetaData
from databases import Database
from te_fast.core.config import settings


# Создаем metadata отдельно
metadata = MetaData()

# Синхронный движок только для создания таблиц
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

# Асинхронный клиент БД
database = Database(settings.database_url)

async def init_db():
    """Инициализация базы данных"""
    # Создаем таблицы
    metadata.create_all(bind=engine)
    
    # Подключаемся к БД
    await database.connect()
    
    # Добавляем начальные данные
    try:
        from te_fast.models.books import books_table
        await database.execute(
            books_table.insert().values([
                {"title": "Книга 1", "author": "Автор 1"},
                {"title": "Книга 2", "author": "Автор 2"},
            ])
        )
    except Exception:
        pass  # Данные уже есть или ошибка
    
    print("Database ready ✅")


async def close_db():
    """Закрытие соединения с БД"""
    await database.disconnect()
