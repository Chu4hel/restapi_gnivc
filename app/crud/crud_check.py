"""
Модуль с CRUD (Create, Read, Update, Delete) операциями для моделей.

Здесь содержатся функции для взаимодействия с базой данных.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.receipt import Check, Item, User, Organization, Invoice
from app.schemas.check import CheckCreate, UserCreate, OrganizationCreate, InvoiceCreate


# CRUD for Check
async def get_check(db: AsyncSession, check_id: int):
    result = await db.execute(
        select(Check).options(selectinload(Check.items), selectinload(Check.user), selectinload(Check.organization), selectinload(Check.invoices)).where(Check.check_id == check_id)
    )
    return result.scalars().first()

async def get_checks(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Check).options(selectinload(Check.items), selectinload(Check.user), selectinload(Check.organization), selectinload(Check.invoices)).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_check(db: AsyncSession, check: CheckCreate):
    db_check = Check(check_sum=check.check_sum, user_id=check.user_id, org_id=check.org_id)
    db.add(db_check)
    await db.flush()

    for item_data in check.items:
        db_item = Item(**item_data.model_dump(), check_id=db_check.check_id)
        db.add(db_item)

    await db.commit()
    await db.refresh(db_check)
    return db_check


# CRUD for User
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# CRUD for Organization
async def get_organization(db: AsyncSession, org_id: int):
    result = await db.execute(select(Organization).where(Organization.org_id == org_id))
    return result.scalars().first()

async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Organization).offset(skip).limit(limit))
    return result.scalars().all()

async def create_organization(db: AsyncSession, organization: OrganizationCreate):
    db_org = Organization(org_name=organization.org_name, legal_form=organization.legal_form)
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org


# CRUD for Invoice
async def get_invoice(db: AsyncSession, invoice_id: int):
    result = await db.execute(select(Invoice).where(Invoice.invoice_id == invoice_id))
    return result.scalars().first()

async def get_invoices(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Invoice).offset(skip).limit(limit))
    return result.scalars().all()

async def create_invoice(db: AsyncSession, invoice: InvoiceCreate):
    db_invoice = Invoice(invoice_sum=invoice.invoice_sum, invoice_type=invoice.invoice_type, payment_type=invoice.payment_type)
    db.add(db_invoice)
    await db.commit()
    await db.refresh(db_invoice)
    return db_invoice
