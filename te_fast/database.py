from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "sqlite:///./books.db"
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)


async def init_db():
    """Инициализация базы данных"""
    from .models.books import books_table

    metadata.create_all(engine)
    await database.connect()
    
    # Добавляем тестовые данные если таблица пустая
    existing_books = await database.fetch_all("SELECT * FROM books")
    if not existing_books:
        await database.execute_many(
            query=books_table.insert(),
            values=[
                {
                    "title": "Невыносимая легкость бытия", 
                    "author": "Милан Кундера",
                    "year": 1984
                },
                {
                    "title": "Мечтают ли андроиды об электроовцах?", 
                    "author": "Филип К. Дик",
                    "year": 1968
                }
            ]
        )

async def close_db():
    """Закрытие соединения с БД"""
    await database.disconnect()
