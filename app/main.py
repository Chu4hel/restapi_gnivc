"""
Главный файл приложения FastAPI.

Отвечает за создание экземпляра FastAPI, настройку,
подключение роутеров и запуск фоновых задач.
"""
from fastapi import FastAPI
from app.api.v1.endpoints import checks

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Receipts API",
    description="API для чтения чеков.",
    version="0.1.0"
)

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
