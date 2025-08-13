"""
Модуль с CRUD (Create, Read, Update, Delete) операциями для модели чека (Receipt).

Здесь содержатся функции для взаимодействия с базой данных:
- получение одного чека по ID
- получение списка чеков
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.receipt import Receipt, Item
from app.schemas.receipt import ReceiptCreate


async def get_receipt(db: AsyncSession, receipt_id: int):
    """
    Получает один чек из базы данных по его ID.

    "Жадно" загружает связанные с чеком товары (items) для повышения производительности.

    Args:
        db (AsyncSession): Сессия базы данных.
        receipt_id (int): ID чека, который нужно найти.

    Returns:
        Optional[Receipt]: Объект чека с загруженными товарами или None, если чек не найден.
    """
    # `selectinload(Receipt.items)` "жадно" загружает связанные товары одним запросом,
    # что гораздо эффективнее, чем делать отдельный запрос для товаров.
    result = await db.execute(
        select(Receipt).options(selectinload(Receipt.items)).where(Receipt.id == receipt_id)
    )
    return result.scalars().first()


async def get_receipts(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Получает список чеков из базы данных с пагинацией.

    "Жадно" загружает связанные с каждым чеком товары (items).

    Args:
        db (AsyncSession): Сессия базы данных.
        skip (int): Количество записей, которые нужно пропустить.
        limit (int): Максимальное количество записей для возврата.

    Returns:
        List[Receipt]: Список объектов чеков.
    """
    result = await db.execute(
        select(Receipt).options(selectinload(Receipt.items)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_receipt(db: AsyncSession, receipt: ReceiptCreate):
    """
    Создает новый чек в базе данных.

    Args:
        db (AsyncSession): Сессия базы данных.
        receipt (ReceiptCreate): Данные для создания нового чека.

    Returns:
        Receipt: Созданный объект чека.
    """
    db_receipt = Receipt(user_id=receipt.user_id)
    db.add(db_receipt)
    await db.flush()

    for item_data in receipt.items:
        db_item = Item(**item_data.model_dump(), receipt_id=db_receipt.id)
        db.add(db_item)

    await db.commit()
    await db.refresh(db_receipt)
    return db_receipt
