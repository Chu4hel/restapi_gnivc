"""
Эндпоинты для работы с чеками.
"""
from typing import List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.crud import crud_check
from app.db.session import get_db
from app.schemas import check as check_schema
from app.schemas.check import User

router = APIRouter()


@router.get("/checks/", response_model=List[check_schema.Check])
async def read_checks_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить список чеков."""
    checks = await crud_check.get_checks(db, skip=skip, limit=limit)
    return checks


@router.get("/checks/{check_id}", response_model=check_schema.Check)
async def read_check_endpoint(
        check_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить чек по ID."""
    db_check = await crud_check.get_check(db, check_id=check_id)
    if db_check is None:
        raise HTTPException(status_code=404, detail="Чек не найден")
    return db_check


@router.post("/checks/", response_model=check_schema.Check, status_code=status.HTTP_201_CREATED)
async def create_check_endpoint(
        check: check_schema.CheckCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создать новый чек."""
    return await crud_check.create_check(db=db, check=check)


@router.get("/checks/{check_id}/full", response_model=check_schema.Check)
async def read_full_check_endpoint(
        check_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Получить полную информацию о чеке.
    """
    db_check = await crud_check.get_check(db, check_id=check_id)
    if db_check is None:
        raise HTTPException(status_code=404, detail="Чек не найден")
    return db_check


@router.post("/checks/{check_id}/invoices/{invoice_id}", status_code=status.HTTP_201_CREATED)
async def link_check_to_invoice_endpoint(
        check_id: int,
        invoice_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Связать чек с накладной.
    """
    return await crud_check.link_check_to_invoice(db, check_id=check_id, invoice_id=invoice_id)


# Эндпоинты для Аналитики
@router.get("/analysis/sales_by_organization", response_model=List[check_schema.SalesByOrganization])
async def analysis_sales_by_organization_endpoint(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Анализ продаж по организациям.
    """
    sales_data = await crud_check.get_sales_by_organization(db)
    return sales_data


@router.get("/users/{user_id}/checks_by_date", response_model=List[check_schema.UserCheck])
async def analysis_checks_by_user_for_period_endpoint(
        user_id: int,
        start_date: date,
        end_date: date,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Поиск чеков по пользователю за период.
    """
    user_checks = await crud_check.get_checks_by_user_for_period(db, user_id=user_id, start_date=start_date,
                                                                 end_date=end_date)
    return user_checks


@router.get("/analysis/items_by_category", response_model=List[check_schema.ItemsByCategory])
async def analysis_items_by_category_endpoint(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Анализ товаров/услуг по категориям.
    """
    items_data = await crud_check.get_items_by_category(db)
    return items_data
