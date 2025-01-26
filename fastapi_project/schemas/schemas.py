from pydantic import BaseModel, EmailStr, validator, Field
from typing import List

# Исправленная модель NewUser  с валидацией
class NewUser (BaseModel):
    """Данные для создания нового пользователя"""
    name: str
    last_name: str
    phone: str = Field(..., pattern=r"^\+7\d{10}$")
    email: EmailStr


class ErrorModel(BaseModel):
    """Модель ошибки"""
    error_message: str

class GetUser (NewUser ):
    """Возвращает пользователя"""
    id: int
    role: str

class GetAllUsers(BaseModel):
    """Возвращает всех пользователей"""
    users: List[GetUser ]

class GetRole(BaseModel):
    """Возвращает роль"""
    id: int
    role: str
    user: str
    description: str

class GetAllRoles(BaseModel):
    """Возвращает все роли"""
    roles: List[GetRole]

class NewRole(BaseModel):
    """Даннеы создания роли"""
    name: str
    description: str

class NewRoleResult(NewRole):
    """Возвращает созданную роль"""
    id: int
