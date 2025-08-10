"""
Модуль для настройки подключения к базе данных.

Здесь создается асинхронный "движок" (engine) SQLAlchemy,
фабрика сессий (AsyncSessionLocal) и базовая декларативная модель (Base).
Также определяется функция-зависимость `get_db` для использования в эндпоинтах FastAPI.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Создаем асинхронный "движок". `echo=True` полезно для отладки, т.к. выводит SQL-запросы в консоль.
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Фабрика для создания асинхронных сессий
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Базовый класс для всех наших SQLAlchemy моделей
Base = declarative_base()


async def get_db():
    """
    Зависимость FastAPI для получения асинхронной сессии базы данных.

    Создает новую сессию `AsyncSession` для каждого запроса и гарантирует
    ее закрытие после завершения запроса.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with AsyncSessionLocal() as session:
        yield session
