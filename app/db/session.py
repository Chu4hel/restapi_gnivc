"""
Модуль для настройки подключения к базе данных.

Здесь создается асинхронный "движок" (engine) SQLAlchemy,
фабрика сессий (AsyncSessionLocal) и базовая декларативная модель (Base).
Также определяется функция-зависимость `get_db` для использования в эндпоинтах FastAPI.
"""
import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from tenacity import retry, stop_after_attempt, wait_fixed

from app.core.config import settings

logger = logging.getLogger(__name__)

# Создаем асинхронный "движок"
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Фабрика для создания асинхронных сессий
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Базовый класс для всех наших SQLAlchemy моделей
Base = declarative_base()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость FastAPI для получения асинхронной сессии базы данных.

    Создает новую сессию `AsyncSession` для каждого запроса и гарантирует
    ее закрытие после завершения запроса.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise


async def check_db_connection():
    """Проверяет доступность базы данных."""
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False
