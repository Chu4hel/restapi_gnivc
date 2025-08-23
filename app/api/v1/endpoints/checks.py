"""
Эндпоинты для работы с чеками и связанными сущностями.
"""
from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas import check as check_schema
from app.crud import crud_check

router = APIRouter()


# Эндпоинты для Чеков
@router.get("/checks/", response_model=List[check_schema.Check])
async def read_checks_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """Получить список чеков."""
    checks = await crud_check.get_checks(db, skip=skip, limit=limit)
    return checks


@router.get("/checks/{check_id}", response_model=check_schema.Check)
async def read_check_endpoint(
        check_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить чек по ID."""
    db_check = await crud_check.get_check(db, check_id=check_id)
    if db_check is None:
        raise HTTPException(status_code=404, detail="Чек не найден")
    return db_check


@router.post("/checks/", response_model=check_schema.Check, status_code=status.HTTP_201_CREATED)
async def create_check_endpoint(
        check: check_schema.CheckCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создать новый чек."""
    return await crud_check.create_check(db=db, check=check)


@router.get("/checks/{check_id}/full", response_model=check_schema.Check)
async def read_full_check_endpoint(
        check_id: int,
        db: AsyncSession = Depends(get_db)
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
        db: AsyncSession = Depends(get_db)
):
    """
    Связать чек с накладной.
    """
    return await crud_check.link_check_to_invoice(db, check_id=check_id, invoice_id=invoice_id)


# Эндпоинты для Пользователей
@router.post("/users/", response_model=check_schema.User, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
        user: check_schema.UserCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создать нового пользователя."""
    return await crud_check.create_user(db=db, user=user)


@router.get("/users/", response_model=List[check_schema.User])
async def read_users_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """Получить список пользователей."""
    users = await crud_check.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=check_schema.User)
async def read_user_endpoint(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить пользователя по ID."""
    db_user = await crud_check.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user


# Эндпоинты для Организаций
@router.post("/organizations/", response_model=check_schema.Organization, status_code=status.HTTP_201_CREATED)
async def create_organization_endpoint(
        organization: check_schema.OrganizationCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создать новую организацию."""
    return await crud_check.create_organization(db=db, organization=organization)


@router.get("/organizations/", response_model=List[check_schema.Organization])
async def read_organizations_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """Получить список организаций."""
    organizations = await crud_check.get_organizations(db, skip=skip, limit=limit)
    return organizations


@router.get("/organizations/{org_id}", response_model=check_schema.Organization)
async def read_organization_endpoint(
        org_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить организацию по ID."""
    db_org = await crud_check.get_organization(db, org_id=org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return db_org


# Эндпоинты для Накладных
@router.post("/invoices/", response_model=check_schema.Invoice, status_code=status.HTTP_201_CREATED)
async def create_invoice_endpoint(
        invoice: check_schema.InvoiceCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создать новую накладную."""
    return await crud_check.create_invoice(db=db, invoice=invoice)


@router.get("/invoices/", response_model=List[check_schema.Invoice])
async def read_invoices_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """Получить список накладных."""
    invoices = await crud_check.get_invoices(db, skip=skip, limit=limit)
    return invoices


@router.get("/invoices/{invoice_id}", response_model=check_schema.Invoice)
async def read_invoice_endpoint(
        invoice_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить накладную по ID."""
    db_invoice = await crud_check.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Накладная не найдена")
    return db_invoice


@router.get("/invoices/{invoice_id}/checks", response_model=check_schema.InvoiceWithChecks)
async def read_invoice_with_checks_endpoint(
        invoice_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить накладную с привязанными чеками."""
    db_invoice = await crud_check.get_invoice_with_checks(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Накладная не найдена")
    return db_invoice


# Эндпоинты для Аналитики
@router.get("/analysis/sales_by_organization", response_model=List[check_schema.SalesByOrganization])
async def analysis_sales_by_organization_endpoint(
        db: AsyncSession = Depends(get_db)
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
        db: AsyncSession = Depends(get_db)
):
    """
    Поиск чеков по пользователю за период.
    """
    user_checks = await crud_check.get_checks_by_user_for_period(db, user_id=user_id, start_date=start_date,
                                                                 end_date=end_date)
    return user_checks


@router.get("/analysis/items_by_category", response_model=List[check_schema.ItemsByCategory])
async def analysis_items_by_category_endpoint(
        db: AsyncSession = Depends(get_db)
):
    """
    Анализ товаров/услуг по категориям.
    """
    items_data = await crud_check.get_items_by_category(db)
    return items_data
