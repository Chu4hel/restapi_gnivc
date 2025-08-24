"""
Эндпоинты для работы с пользователями.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.crud import crud_user
from app.db.session import get_db
from app.schemas.check import User, UserCreate

router = APIRouter()


@router.post(
    "/users/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового пользователя",
    responses={400: {"description": "Пользователь с таким именем уже существует"}}
)
async def create_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создать нового пользователя."""
    db_user = await crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    return await crud_user.create_user(db=db, user=user)


@router.get(
    "/users/",
    response_model=List[User],
    summary="Получение списка пользователей",
    responses={401: {"description": "Не авторизован"}}
)
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить список пользователей."""
    users = await crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/users/{user_id}",
    response_model=User,
    summary="Получение пользователя по ID",
    responses={401: {"description": "Не авторизован"}, 404: {"description": "Пользователь не найден"}}
)
async def read_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить пользователя по ID."""
    db_user = await crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user
