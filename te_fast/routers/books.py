from fastapi import APIRouter, HTTPException
from typing import List
from te_fast.database import database
from te_fast.models.books import books_table, Book, NewBook


router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("/", summary="Книги", response_model=List[Book])
async def get_books():
    query = books_table.select()
    return await database.fetch_all(query)


@router.get("/titles", summary="Только названия книг")
async def get_book_titles():
    query = "SELECT id, title FROM books"
    return await database.fetch_all(query)


@router.get("/{id}", summary="Название конкретной книги", response_model=Book)
async def get_book(id: int):
    query = books_table.select().where(books_table.c.id == id)
    book = await database.fetch_one(query)

    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    return book


@router.post("/", summary="Добавление книги")
async def create_book(new_book: NewBook):
    query = books_table.insert().values(
        title=new_book.title,
        author=new_book.author,
        year=new_book.year,
        description=new_book.description
    )
    book_id = await database.execute(query)
    
    # Возвращаем созданную книгу
    query = books_table.select().where(books_table.c.id == book_id)
    book = await database.fetch_one(query)
    return book


@router.delete("/{id}", summary="Удаление книги")
async def delete_book(id: int):
    # Сначала получаем книгу
    query = books_table.select().where(books_table.c.id == id)
    book = await database.fetch_one(query)
    
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    # Затем удаляем
    query = books_table.delete().where(books_table.c.id == id)
    await database.execute(query)

    return {
        "success": True,
        "message": f"Книга {book.title}(id: {book.id}) удалена"
    }
