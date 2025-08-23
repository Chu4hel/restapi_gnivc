"""
Главный файл приложения FastAPI.

Отвечает за создание экземпляра FastAPI, настройку,
подключение роутеров и запуск фоновых задач.
"""
from fastapi import FastAPI
from app.api.v1.endpoints import checks
from app.db.session import engine, Base


async def create_tables():
    """
    Создает все таблицы в базе данных на основе моделей SQLAlchemy.

    Эту функцию следует использовать для первоначальной настройки БД.
    В производственной среде для управления миграциями схемы данных
    рекомендуется использовать Alembic.
    """
    async with engine.begin() as conn:
        # В продакшене лучше использовать Alembic для миграций,
        # но для разработки это самый простой способ.
        await conn.run_sync(Base.metadata.create_all)


# Создаем экземпляр FastAPI
app = FastAPI(
    title="Receipts API",
    description="API для чтения чеков.",
    version="0.1.0"
)


# Регистрируем событие, которое выполнится при старте приложения
@app.on_event("startup")
async def on_startup():
    """
    Выполняется при старте приложения.

    Создает таблицы в базе данных.
    """
    await create_tables()


# Подключаем роутер с нашими эндпоинтами
app.include_router(
    checks.router,
    prefix="/api/v1",
    tags=["Checks"]
)


# Корневой эндпоинт для проверки, что API работает
@app.get("/")
def read_root():
    """
    Корневой эндпоинт.

    Возвращает приветственное сообщение.
    """
    return {"message": "Welcome to Receipts API. Go to /docs to see the documentation."}
