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

# Метаданные для тегов Swagger
tags_metadata = [
    {
        "name": "Пользователи",
        "description": "Операции с пользователями: создание, чтение.",
    },
    {
        "name": "Аутентификация",
        "description": "Получение JWT-токена для доступа к защищенным эндпоинтам.",
    },
    {
        "name": "Чеки",
        "description": "Операции с чеками и аналитика.",
    },
    {
        "name": "Организации",
        "description": "Операции с организациями.",
    },
    {
        "name": "Накладные",
        "description": "Операции с накладными.",
    },
    {
        "name": "Служебные",
        "description": "Служебные эндпоинты, например, для проверки состояния здоровья сервиса.",
    },
]

# Создаем экземпляр FastAPI
app = FastAPI(
    title="API для Чеков",
    description="Сервис для управления чеками, пользователями, организациями и накладными.",
    version="1.0.0",
    openapi_tags=tags_metadata,
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
app.include_router(users.router, prefix="/api/v1", tags=["Пользователи"])
app.include_router(login.router, prefix="/api/v1", tags=["Аутентификация"])
app.include_router(checks.router, prefix="/api/v1", tags=["Чеки"])
app.include_router(organizations.router, prefix="/api/v1", tags=["Организации"])
app.include_router(invoices.router, prefix="/api/v1", tags=["Накладные"])
app.include_router(health.router, tags=["Служебные"])


# Корневой эндпоинт для проверки, что API работает
@app.get("/", summary="Корневой эндпоинт", tags=["Служебные"])
def read_root():
    """
    Корневой эндпоинт.

    Возвращает приветственное сообщение.
    """
    return {"message": "Welcome to Receipts API. Go to /docs to see the documentation."}
