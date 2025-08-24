"""
Модуль с CRUD-операциями для модели User.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.models.receipt import User
from app.schemas.check import UserCreate


async def get_user(db: AsyncSession, user_id: int):
    """Получить пользователя по ID."""
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    """Получить пользователя по имени пользователя."""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список пользователей."""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate):
    """Создать нового пользователя."""
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
