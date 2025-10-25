import re
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, HttpUrl


class BloodGroup(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class UserModel(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=120,
        description="Имя пользователя",
        example="Martin"
    )
    email: EmailStr = Field(
        ...,
        description="Email пользователя", 
        example="user@example.com"
    )
    age: int = Field(
        ...,
        ge=1,
        le=120,
        description="Возраст пользователя"
    )
    country: Optional[str] = Field(
        None,
        min_length=3,
        max_length=150,
        description="Страна проживания"
    )
    bio: Optional[str] = Field(
        None,
        max_length=5000,
        description="Биография пользователя"
    )
    groupBlood: Optional[BloodGroup] = Field(
        None,
        description="Группа крови"
    )
    isHappy: Optional[bool] = Field(
        None,
        description="Счастлив ли пользователь",
        example=True
    )
    phone: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{1,14}$",
        description="Номер телефона"
    )
    githubUsername: Optional[str] = Field(
        None,
        description="Аккаунт GitHub"
    )

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Можно только буквы (a-z, A-Z), цифры (0-9), _ и -')
        return v

    @field_validator('githubUsername')
    @classmethod
    def github_username_format(cls, v):
        if v and not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$', v):
            raise ValueError('Неверный формат GitHub username')
        return v


class UserResponse(UserModel):
    id: int


class UsersList(BaseModel):
    users: List[UserResponse]
    total: int


class ProfileGit(UserModel):
    githubUsername: str = Field(
        ...,
        min_length=3,
        max_length=39,
        description="Аккаунт GitHub",
        example="satoshi"
    )
    developer: bool = Field(
        ...,
        description="Вы разрабочтик?",
        example=True
    )
    avatar: Optional[HttpUrl] = Field(
        None,
        description="URL аватара пользователя",
        example="https://example.com/avatars/user123.jpg"
    )

    @field_validator('githubUsername')
    @classmethod
    def validate_github_username(cls, v):
        cleaned = v.replace('-', '').replace('_', '')
        if not cleaned.isalnum():
            raise ValueError(
                'GitHub username может содержать только буквы, цифры, дефисы и подчеркивания'
            )
        return v


class GitUsersList(BaseModel):
    users: List[ProfileGit]
    total: int


def remove_none_fields(data: dict):
    """Удаляет поля со значением None из словаря"""
    return {key: value for key, value in data.items() if value is not None}
