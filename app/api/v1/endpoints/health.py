"""
Эндпоинт для проверки работоспособности приложения.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.db.session import check_db_connection

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Проверяет доступность базы данных.
    """
    if await check_db_connection():
        return {"status": "OK"}
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="База данных недоступна",
        )
