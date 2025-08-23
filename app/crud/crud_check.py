"""
Модуль с CRUD (Create, Read, Update, Delete) операциями для моделей.

Здесь содержатся функции для взаимодействия с базой данных.
"""
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import date

from app.models.receipt import Check, Item, User, Organization, Invoice, CheckInvoice
from app.schemas.check import CheckCreate, UserCreate, OrganizationCreate, InvoiceCreate


# CRUD для Чека
async def get_check(db: AsyncSession, check_id: int):
    """Получить чек по ID."""
    result = await db.execute(
        select(Check).options(selectinload(Check.items), selectinload(Check.user), selectinload(Check.organization),
                              selectinload(Check.invoices)).where(Check.check_id == check_id)
    )
    return result.scalars().first()


async def get_checks(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список чеков."""
    result = await db.execute(
        select(Check).options(selectinload(Check.items), selectinload(Check.user), selectinload(Check.organization),
                              selectinload(Check.invoices)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_check(db: AsyncSession, check: CheckCreate):
    """Создать новый чек."""
    db_check = Check(check_sum=check.check_sum, user_id=check.user_id, org_id=check.org_id)
    db.add(db_check)
    await db.flush()

    for item_data in check.items:
        db_item = Item(**item_data.model_dump(), check_id=db_check.check_id)
        db.add(db_item)

    await db.commit()
    await db.refresh(db_check)
    return db_check


async def link_check_to_invoice(db: AsyncSession, check_id: int, invoice_id: int):
    """Связать чек с накладной."""
    db_check_invoice = CheckInvoice(check_id=check_id, invoice_id=invoice_id)
    db.add(db_check_invoice)
    await db.commit()
    return db_check_invoice


# CRUD для Пользователя
async def get_user(db: AsyncSession, user_id: int):
    """Получить пользователя по ID."""
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список пользователей."""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate):
    """Создать нового пользователя."""
    db_user = User(username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# CRUD для Организации
async def get_organization(db: AsyncSession, org_id: int):
    """Получить организацию по ID."""
    result = await db.execute(select(Organization).where(Organization.org_id == org_id))
    return result.scalars().first()


async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список организаций."""
    result = await db.execute(select(Organization).offset(skip).limit(limit))
    return result.scalars().all()


async def create_organization(db: AsyncSession, organization: OrganizationCreate):
    """Создать новую организацию."""
    db_org = Organization(org_name=organization.org_name, legal_form=organization.legal_form)
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org


# CRUD для Накладной
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


# Аналитика
async def get_sales_by_organization(db: AsyncSession):
    """Получить аналитику по продажам в разрезе организаций."""
    query = text("""
                 SELECT o.org_name,
                        o.legal_form,
                        COUNT(DISTINCT c.check_id) as total_checks,
                        SUM(c.check_sum)           as total_revenue,
                        AVG(c.check_sum)           as avg_check_amount
                 FROM organizations o
                          JOIN checks c ON o.org_id = c.org_id
                 GROUP BY o.org_id, o.org_name, o.legal_form
                 ORDER BY total_revenue DESC;
                 """)
    result = await db.execute(query)
    return result.all()


async def get_checks_by_user_for_period(db: AsyncSession, user_id: int, start_date: date, end_date: date):
    """Получить чеки пользователя за определенный период."""
    query = text("""
                 SELECT c.check_id,
                        c.created_at,
                        c.check_sum,
                        o.org_name,
                        o.legal_form,
                        STRING_AGG(i.item_name, ', ') as items
                 FROM checks c
                          JOIN organizations o ON c.org_id = o.org_id
                          JOIN items i ON c.check_id = i.check_id
                 WHERE c.user_id = :user_id
                   AND c.created_at BETWEEN :start_date AND :end_date
                 GROUP BY c.check_id, o.org_name, o.legal_form
                 ORDER BY c.created_at DESC;
                 """)
    result = await db.execute(query, {"user_id": user_id, "start_date": start_date, "end_date": end_date})
    return result.all()


async def get_items_by_category(db: AsyncSession):
    """Получить аналитику по товарам в разрезе категорий."""
    query = text("""
                 SELECT CASE
                            WHEN i.item_type BETWEEN 1 AND 5 THEN 'Food'
                            WHEN i.item_type BETWEEN 12 AND 17 THEN 'Services'
                            WHEN i.item_type = 26 THEN 'Alcohol'
                            ELSE 'Other'
                            END              as category,
                        COUNT(*)             as items_sold,
                        SUM(i.item_quantity) as total_quantity,
                        SUM(i.item_sum)      as total_revenue
                 FROM items i
                 GROUP BY category
                 ORDER BY total_revenue DESC;
                 """)
    result = await db.execute(query)
    return result.all()
