"""
Модуль со схемами Pydantic для валидации данных чеков и товаров.

Эти схемы используются FastAPI для валидации входящих JSON-запросов
и для форматирования исходящих JSON-ответов.
"""

from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


# --- Схемы для Товара (Item) ---

class ItemBase(BaseModel):
    """Базовая схема для товара, содержащая общие поля."""
    name: str
    price: Optional[int] = None
    quantity: Optional[float] = None
    sum: Optional[int] = None
    invoice_type: Optional[int] = None
    invoice_sum: Optional[int] = None
    product_type: Optional[int] = None
    payment_type: Optional[int] = None


class ItemCreate(ItemBase):
    """Схема для создания нового товара. Наследуется от ItemBase."""
    pass


class Item(ItemBase):
    """Схема для представления товара в ответе API. Включает ID."""
    id: int

    # Позволяет Pydantic читать данные из объектов SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


# --- Схемы для Чека (Receipt) ---

class ReceiptBase(BaseModel):
    """Базовая схема для чека."""
    user_id: int


class Receipt(ReceiptBase):
    """Схема для представления чека в ответе API. Включает ID, дату создания и список товаров."""
    id: int
    created_at: datetime
    items: List[Item] = []

    model_config = ConfigDict(from_attributes=True)


class ReceiptCreate(ReceiptBase):
    """Схема для создания нового чека."""
    items: List[ItemCreate] = []
