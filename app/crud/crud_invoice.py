"""
Модуль с CRUD-операциями для модели Invoice.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.receipt import Invoice
from app.schemas.check import InvoiceCreate


async def get_invoice(db: AsyncSession, invoice_id: int):
    """Получить накладную по ID."""
    result = await db.execute(select(Invoice).where(Invoice.invoice_id == invoice_id))
    return result.scalars().first()


async def get_invoice_with_checks(db: AsyncSession, invoice_id: int):
    """Получить накладную с привязанными чеками."""
    result = await db.execute(
        select(Invoice).options(selectinload(Invoice.checks)).where(Invoice.invoice_id == invoice_id)
    )
    return result.scalars().first()


async def get_invoices(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список накладных."""
    result = await db.execute(select(Invoice).offset(skip).limit(limit))
    return result.scalars().all()


async def create_invoice(db: AsyncSession, invoice: InvoiceCreate):
    """Создать новую накладную."""
    db_invoice = Invoice(invoice_sum=invoice.invoice_sum, invoice_type=invoice.invoice_type,
                         payment_type=invoice.payment_type)
    db.add(db_invoice)
    await db.commit()
    await db.refresh(db_invoice)
    return db_invoice
