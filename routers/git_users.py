from fastapi import APIRouter, HTTPException
from ..models.users import ProfileGit, GitUsersList


router = APIRouter(prefix="/git_users", tags=["Git Пользователи"])

# Временное хранилище
git_users_storage = []


@router.get("/",
            summary="Все пользователи Git",
            response_model=GitUsersList)
def get_all_gitusers():
    return GitUsersList(
        users=git_users_storage,
        total=len(git_users_storage)
    )


@router.post("/",
            summary="Создание Git")
def create_gituser(git_user: ProfileGit):
    git_user_id = len(git_users_storage) + 1
    user_data = {
        "id": git_user_id,
        "githubUsername": git_user.githubUsername,
        "developer": git_user.developer,
        "avatar": git_user.avatar,
    }
    git_users_storage.append(user_data)
    return {
        "success": True,
        "message": "Пользователь создан",
        "user": user_data
    }


@router.get("/{user_id}",
            summary="Получить пользователя")
def get_git_profile(user_id: int):
    for git in git_users_storage:
        if git["id"] == user_id:
            return git

    raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.delete("/{user_id}", 
               summary="Удаление пользователя")
def delete_git_user(user_id: int):
    global git_users_storage

    for idx, usr in enumerate(git_users_storage):
        if usr["id"] == user_id:
            delete_usr = git_users_storage.pop(idx)
            return {
                "success": True,
                "message": f"Пользователь {delete_usr['githubUsername']} удален",
                "deleted_user": delete_usr
            }

    raise HTTPException(status_code=404, detail="Пользователь не найден")
