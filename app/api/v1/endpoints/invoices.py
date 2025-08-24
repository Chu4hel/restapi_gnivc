"""
Эндпоинты для работы с накладными.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.crud import crud_invoice
from app.db.session import get_db
from app.schemas.check import Invoice, InvoiceCreate, InvoiceWithChecks, User

router = APIRouter()


@router.post(
    "/invoices/",
    response_model=Invoice,
    status_code=status.HTTP_201_CREATED,
    summary="Создание новой накладной",
    responses={401: {"description": "Не авторизован"}}
)
async def create_invoice(
        invoice: InvoiceCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создать новую накладную."""
    return await crud_invoice.create_invoice(db=db, invoice=invoice)


@router.get(
    "/invoices/",
    response_model=List[Invoice],
    summary="Получение списка накладных",
    responses={401: {"description": "Не авторизован"}}
)
async def read_invoices(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить список накладных."""
    invoices = await crud_invoice.get_invoices(db, skip=skip, limit=limit)
    return invoices


@router.get(
    "/invoices/{invoice_id}",
    response_model=Invoice,
    summary="Получение накладной по ID",
    responses={401: {"description": "Не авторизован"}, 404: {"description": "Накладная не найдена"}}
)
async def read_invoice(
        invoice_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить накладную по ID."""
    db_invoice = await crud_invoice.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Накладная не найдена")
    return db_invoice


@router.get(
    "/invoices/{invoice_id}/checks",
    response_model=InvoiceWithChecks,
    summary="Получение накладной с привязанными чеками",
    responses={401: {"description": "Не авторизован"}, 404: {"description": "Накладная не найдена"}}
)
async def read_invoice_with_checks(
        invoice_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить накладную с привязанными чеками."""
    db_invoice = await crud_invoice.get_invoice_with_checks(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Накладная не найдена")
    return db_invoice
