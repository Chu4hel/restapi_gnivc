"""
Эндпоинты для работы с накладными.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.crud import crud_invoice
from app.db.session import get_db
from app.schemas.check import Invoice, InvoiceCreate, InvoiceWithChecks
from app.schemas.check import User

router = APIRouter()


@router.post("/invoices/", response_model=Invoice, status_code=status.HTTP_201_CREATED)
async def create_invoice_endpoint(
        invoice: InvoiceCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создать новую накладную."""
    return await crud_invoice.create_invoice(db=db, invoice=invoice)


@router.get("/invoices/", response_model=List[Invoice])
async def read_invoices_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить список накладных."""
    invoices = await crud_invoice.get_invoices(db, skip=skip, limit=limit)
    return invoices


@router.get("/invoices/{invoice_id}", response_model=Invoice)
async def read_invoice_endpoint(
        invoice_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить накладную по ID."""
    db_invoice = await crud_invoice.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Накладная не найдена")
    return db_invoice


@router.get("/invoices/{invoice_id}/checks", response_model=InvoiceWithChecks)
async def read_invoice_with_checks_endpoint(
        invoice_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить накладную с привязанными чеками."""
    db_invoice = await crud_invoice.get_invoice_with_checks(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Накладная не найдена")
    return db_invoice
