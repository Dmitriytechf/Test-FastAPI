from fastapi import APIRouter, HTTPException
from ..models.users import UserModel, UsersList, UserResponse, remove_none_fields


router = APIRouter(prefix="/users", tags=["Пользователи"])

# Временное хранилище
users_storage = []


@router.post("/",
             summary="Добавление пользователя")
def create_user(user: UserModel):
    user_id = len(users_storage) + 1
    user_data = remove_none_fields({
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "country": user.country,
        "bio": user.bio,
        "groupBlood": user.groupBlood,
        "isHappy": user.isHappy,
        "phone": user.phone,
        "githubUsername": user.githubUsername
    })
    users_storage.append(user_data)
    return {
        "success": True,
        "message": "Пользователь создан",
        "user": user_data
    }


@router.delete("/{user_id}", summary="Удаление пользователя")
def delete_user(user_id: int):
    global users_storage

    for index, user in enumerate(users_storage):
        if user["id"] == user_id:
            deleted_user = users_storage.pop(index)
            return {
                "success": True,
                "message": f"Пользователь {deleted_user['username']} удален",
                "deleted_user": deleted_user
            }

    raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.get("/{user_id}", summary="Получить пользователя")
def get_user_profile(user_id: int):
    for user in users_storage:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.get("/",
            summary="Все пользователи",
            response_model=UsersList,
            response_model_exclude_none=True)
def get_all_users():
    users_all = [remove_none_fields(user) for user in users_storage]
    return UsersList(
        users=users_all,
        total=len(users_all)
    )
