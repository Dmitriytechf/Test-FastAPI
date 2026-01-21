from sqlalchemy import create_engine, MetaData
from databases import Database
from te_fast.core.config import settings


# Создаем metadata отдельно
metadata = MetaData()

# Синхронный движок только для создания таблиц
engine = create_engine(
    settings.database_url,
    echo=True,
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
                {"title": "Хоббит, или Туда и обратно", "author": "Джон Р. Р. Толкин"},
                {"title": "Казаки", "author": "Лев Николаевич Толстой"},
            ])
        )
    except Exception:
        pass  # Данные уже есть или ошибка

    print("Database ready ✅")


async def close_db():
    """Закрытие соединения с БД"""
    await database.disconnect()
