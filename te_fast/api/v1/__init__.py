from fastapi import APIRouter
from . import books, users, other, git_users

api_router = APIRouter()

api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(git_users.router, prefix="/git_users", tags=["git_users"])
api_router.include_router(other.router, prefix="/other", tags=["other"])
