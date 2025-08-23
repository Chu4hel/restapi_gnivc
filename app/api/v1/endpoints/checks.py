"""
Эндпоинты для работы с чеками и связанными сущностями.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas import check as check_schema
from app.crud import crud_check

router = APIRouter()


# Endpoints for Checks
@router.get("/checks/", response_model=List[check_schema.Check])
async def read_checks_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    checks = await crud_check.get_checks(db, skip=skip, limit=limit)
    return checks


@router.get("/checks/{check_id}", response_model=check_schema.Check)
async def read_check_endpoint(
        check_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_check = await crud_check.get_check(db, check_id=check_id)
    if db_check is None:
        raise HTTPException(status_code=404, detail="Check not found")
    return db_check


@router.post("/checks/", response_model=check_schema.Check, status_code=status.HTTP_201_CREATED)
async def create_check_endpoint(
        check: check_schema.CheckCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud_check.create_check(db=db, check=check)


# Endpoints for Users
@router.post("/users/", response_model=check_schema.User, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
        user: check_schema.UserCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud_check.create_user(db=db, user=user)


@router.get("/users/", response_model=List[check_schema.User])
async def read_users_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    users = await crud_check.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=check_schema.User)
async def read_user_endpoint(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_user = await crud_check.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Endpoints for Organizations
@router.post("/organizations/", response_model=check_schema.Organization, status_code=status.HTTP_201_CREATED)
async def create_organization_endpoint(
        organization: check_schema.OrganizationCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud_check.create_organization(db=db, organization=organization)


@router.get("/organizations/", response_model=List[check_schema.Organization])
async def read_organizations_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    organizations = await crud_check.get_organizations(db, skip=skip, limit=limit)
    return organizations


@router.get("/organizations/{org_id}", response_model=check_schema.Organization)
async def read_organization_endpoint(
        org_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_org = await crud_check.get_organization(db, org_id=org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org


# Endpoints for Invoices
@router.post("/invoices/", response_model=check_schema.Invoice, status_code=status.HTTP_201_CREATED)
async def create_invoice_endpoint(
        invoice: check_schema.InvoiceCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud_check.create_invoice(db=db, invoice=invoice)


@router.get("/invoices/", response_model=List[check_schema.Invoice])
async def read_invoices_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    invoices = await crud_check.get_invoices(db, skip=skip, limit=limit)
    return invoices


@router.get("/invoices/{invoice_id}", response_model=check_schema.Invoice)
async def read_invoice_endpoint(
        invoice_id: int,
        db: AsyncSession = Depends(get_db)
):
    db_invoice = await crud_check.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice
