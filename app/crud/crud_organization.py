"""
Модуль с CRUD-операциями для модели Organization.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.receipt import Organization
from app.schemas.check import OrganizationCreate


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
