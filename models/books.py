from sqlalchemy import Column, Integer, String, Table, Text
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from ..database import metadata


# Определяем таблицу книг
books_table = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(200)),
    Column("author", String(100)),
    Column("year", Integer, nullable=True),
    Column("description", Text, nullable=True),
)


# Модель Pydantic для валидации
class NewBook(BaseModel):
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=200, 
        description="Название книги",
        examples=["Исповедь"]
    )
    author: str = Field(
        ..., 
        min_length=3, 
        max_length=50, 
        description="Автор книги",
        examples=["Лев Толстой"]
    )
    year: Optional[int] = Field(
        None, 
        ge=1000, 
        le=2100, 
        description="Год издания",
        examples=[1884]
    )
    description: Optional[str] = Field(
        None, 
        max_length=5000,
        description="Описание",
    )


# Модель Pydantic для ответа
class Book(NewBook):
    id: int  = Field(..., description="Уникальный идентификатор книги")

    model_config = ConfigDict(
        from_attributes=True,  # Позволяет создавать из ORM объектов
        json_schema_extra={
            'examples': [{
                'id': 1,
                'title': 'Преступление и наказание',
                'author': 'Федор Достоевский', 
                'year': 1866
            }]
        }
    )
