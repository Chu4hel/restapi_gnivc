import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app

# Устанавливаем флаг тестирования
settings.TESTING = True


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    """
    Создает и удаляет саму тестовую базу данных один раз за сессию.
    Эта фикстура не создает движок, она только подготавливает "холст".
    """
    default_db_url = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/postgres"
    engine = create_async_engine(default_db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {settings.TEST_POSTGRES_DB} WITH (FORCE)"))
        await conn.execute(text(f"CREATE DATABASE {settings.TEST_POSTGRES_DB}"))
    await engine.dispose()

    yield

    # После всех тестов удаляем БД
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {settings.TEST_POSTGRES_DB} WITH (FORCE)"))
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Для КАЖДОГО теста:
    1. Создает новый движок (engine), привязанный к циклу этого теста.
    2. Создает таблицы.
    3. Создает сессию и переопределяет зависимость.
    4. После теста откатывает все изменения, удаляет таблицы и закрывает движок.
    """
    test_db_url = f"postgresql+asyncpg://{settings.TEST_POSTGRES_USER}:{settings.TEST_POSTGRES_PASSWORD}@{settings.TEST_POSTGRES_SERVER}:{settings.TEST_POSTGRES_PORT}/{settings.TEST_POSTGRES_DB}"

    # 1. Создаем НОВЫЙ движок для этого конкретного теста
    engine = create_async_engine(test_db_url)

    # 2. Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 3. Создаем фабрику сессий и переопределяем зависимость
    TestingSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    # Передаем саму сессию, чтобы можно было подготовить данные перед тестом
    async with TestingSessionLocal() as session:
        yield session

    # --- Очистка после КАЖДОГО теста ---
    # 4. Удаляем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # 5. Полностью закрываем движок и его пул соединений
    await engine.dispose()

    # 6. Удаляем переопределение
    del app.dependency_overrides[get_db]


@pytest_asyncio.fixture(scope="function")
async def client() -> httpx.AsyncClient:
    """Создает HTTP-клиент для тестирования API."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
