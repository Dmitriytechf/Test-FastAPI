from fastapi import FastAPI
from .database import init_db, close_db
from .routers import books, users, other, git_users


app = FastAPI(
    title="My API",
    description="Test FastAPI",
)

# Подключаем роутеры
app.include_router(books.router)
app.include_router(users.router)
app.include_router(git_users.router)
app.include_router(other.router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db()


@app.get("/", summary="Главная")
def main():
    return {"Hello": "World"}
