"""
Главный файл приложения FastAPI.

Отвечает за создание экземпляра FastAPI, настройку,
подключение роутеров и запуск фоновых задач.
"""
import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import checks, users, organizations, invoices, login, health
from app.core.logging import setup_logging

# Настраиваем логирование
setup_logging()

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Receipts API",
    description="API для чтения чеков.",
    version="0.1.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware для логирования HTTP-запросов."""
    start_time = time.time()
    logging.info(f"Запрос: {request.method} {request.url}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"Ответ: {response.status_code} (обработано за {process_time:.2f}с)")
    return response


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    """Обработчик для логирования необработанных исключений."""
    logging.error(f"Необработанное исключение: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"},
    )


# Подключаем роутеры с нашими эндпоинтами
app.include_router(checks.router, prefix="/api/v1", tags=["Чеки"])
app.include_router(users.router, prefix="/api/v1", tags=["Пользователи"])
app.include_router(organizations.router, prefix="/api/v1", tags=["Организации"])
app.include_router(invoices.router, prefix="/api/v1", tags=["Накладные"])
app.include_router(login.router, prefix="/api/v1", tags=["Аутентификация"])
app.include_router(health.router, tags=["Служебные"])


# Корневой эндпоинт для проверки, что API работает
@app.get("/")
def read_root():
    """
    Корневой эндпоинт.

    Возвращает приветственное сообщение.
    """
    return {"message": "Welcome to Receipts API. Go to /docs to see the documentation."}
