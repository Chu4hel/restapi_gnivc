from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.receipt import Receipt, ReceiptCreate
from app.crud import crud_receipt

router = APIRouter()


@router.get("/", response_model=List[Receipt])
async def read_receipts_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """
    Получить список чеков.
    """
    receipts = await crud_receipt.get_receipts(db, skip=skip, limit=limit)
    return receipts


@router.get("/{receipt_id}", response_model=Receipt)
async def read_receipt_endpoint(
        receipt_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Получить чек по его ID.
    """
    db_receipt = await crud_receipt.get_receipt(db, receipt_id=receipt_id)
    if db_receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return db_receipt


@router.post("/", response_model=Receipt, status_code=status.HTTP_201_CREATED)
async def create_receipt_endpoint(
        receipt: ReceiptCreate,
        db: AsyncSession = Depends(get_db)
):
    """
    Создать новый чек.
    """
    return await crud_receipt.create_receipt(db=db, receipt=receipt)
