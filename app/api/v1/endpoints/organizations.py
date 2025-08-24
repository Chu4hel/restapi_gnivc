"""
Эндпоинты для работы с организациями.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_user
from app.crud import crud_organization
from app.db.session import get_db
from app.schemas.check import Organization, OrganizationCreate
from app.schemas.check import User

router = APIRouter()


@router.post("/organizations/", response_model=Organization, status_code=status.HTTP_201_CREATED)
async def create_organization_endpoint(
        organization: OrganizationCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Создать новую организацию."""
    return await crud_organization.create_organization(db=db, organization=organization)


@router.get("/organizations/", response_model=List[Organization])
async def read_organizations_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить список организаций."""
    organizations = await crud_organization.get_organizations(db, skip=skip, limit=limit)
    return organizations


@router.get("/organizations/{org_id}", response_model=Organization)
async def read_organization_endpoint(
        org_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Получить организацию по ID."""
    db_org = await crud_organization.get_organization(db, org_id=org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return db_org
