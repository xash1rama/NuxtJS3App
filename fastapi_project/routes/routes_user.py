from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from setup import get_session
from database.models import User,Role, select
from schemas.schemas import ErrorModel, GetUser, NewUser, GetAllUsers, GetRole, GetAllRoles, NewRole, NewRoleResult
from typing import Union

router = APIRouter(tags=["users"])

@router.post("/user/", response_model=Union[NewUser , ErrorModel])
async def create_user(new_user_data: NewUser  = Body(...), async_session: AsyncSession = Depends(get_session)):
    """Создать нового пользователя"""
    try:
        new_user = User(**new_user_data.dict())
        async_session.add(new_user)
        await async_session.commit()
        await async_session.refresh(new_user)

        role = Role(
            name="Client",
            user_id=new_user.id,
            description="A legal entity or individual who uses the services of another individual "
                        "or legal entity and enters into business relations with him."
        )
        async_session.add(role)
        await async_session.commit()

        return new_user_data

    except Exception as error:
        return ErrorModel(error_message=str(error))


@router.put("/user/{id}", response_model=Union[GetUser , ErrorModel])
async def update_user(id: int, new_user_data: NewUser  = Body(...), async_session: AsyncSession = Depends(get_session)):
    """Обновить данные пользователя с указанным ID"""
    try:
        result = await async_session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User  not found")

        for field, value in new_user_data.dict().items():
            setattr(user, field, value)

        await async_session.commit()
        await async_session.refresh(user)

        return GetUser (
            id=user.id,
            name=user.name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            role=user.roles[0].name if user.roles else "Without role"
        )

    except Exception as error:
        return ErrorModel(error_message=str(error))



@router.get("/user/", response_model=Union[GetAllUsers, ErrorModel])
async def get_all_user(async_session: AsyncSession = Depends(get_session)):
    """Пользователь может получить информацию о всех пользователях"""
    try:
        result = await async_session.execute(select(User).options(selectinload(User.roles)))
        users = result.scalars().all()
        if not users:
            raise HTTPException(status_code=404, detail="Users not found")

        return GetAllUsers(
            users=[
                GetUser (
                    id=user.id,
                    name=user.name,
                    last_name=user.last_name,
                    email=user.email,
                    phone=user.phone,
                    role=user.roles[0].name if user.roles else "Without role"
                ) for user in users
            ]
        )

    except Exception as error:
        return ErrorModel(error_message=str(error))


@router.delete("/user/{id}", response_model=Union[GetUser , ErrorModel])
async def delete_user(id: int, async_session: AsyncSession = Depends(get_session)):
    """Пользователь может удалить пользователя по его ID"""
    try:
        result = await async_session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User  not found")

        await async_session.delete(user)
        await async_session.commit()
        return GetUser (
            id=user.id,
            name=user.name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            role=user.roles[0].name if user.roles else "Without role"
        )

    except Exception as error:
        return ErrorModel(error_message=str(error))

@router.get("/user/roles", response_model=GetAllRoles)
async def get_all_roles(
        async_session: AsyncSession = Depends(get_session),
):
    """Пользователь может получить информацию о всех ролях"""
    try:
        result = await async_session.execute(select(Role).options(selectinload(Role.users)))
        roles = result.scalars().all()

        if not roles:
            return GetAllRoles(roles=[])

        response = GetAllRoles(
            roles=[
                GetRole(
                    id=role.id,
                    role=role.name,
                    user=f"{role.users.name} {role.users.last_name}" if role.users else "No user",
                    description=role.description
                ) for role in roles if role.users
            ]
        )

        if not response.roles:
            return GetAllRoles(roles=[])

        return response

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))



@router.put("/user/roles/{id}", response_model=Union[NewRoleResult, ErrorModel])
async def update_role(
    id: int,
    new_role_data: NewRole = Body(...),
    async_session: AsyncSession = Depends(get_session),
    ):
    """ Обновить данные роли пользователя с указанным ID """
    try:
        result = await async_session.execute(select(Role).where(Role.user_id == id))
        role = result.scalar_one_or_none()
        if not role:
            raise HTTPException(status_code=404,
                                detail="User not found")
        role.name = new_role_data.name
        role.description = new_role_data.description

        await async_session.commit()
        await async_session.refresh(role)

        response = NewRoleResult(
                id=role.id,
                name = role.name,
                description = role.description,
            )
        return response

    except Exception as error:
        return ErrorModel(
            error_message=str(error)
        )




