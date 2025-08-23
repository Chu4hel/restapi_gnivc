"""
Модуль со схемами Pydantic для валидации данных.

Эти схемы используются FastAPI для валидации входящих JSON-запросов
и для форматирования исходящих JSON-ответов.
"""

from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# --- Схемы для Пользователя (User) ---

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Схемы для Организации (Organization) ---

class OrganizationBase(BaseModel):
    org_name: str
    legal_form: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    org_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Схемы для Накладной (Invoice) ---

class InvoiceBase(BaseModel):
    invoice_sum: Decimal
    invoice_type: Optional[int] = None
    payment_type: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    invoice_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Схемы для Товара (Item) ---

class ItemBase(BaseModel):
    item_name: str
    item_price: Optional[Decimal] = None
    item_type: Optional[int] = None
    item_quantity: Optional[Decimal] = None
    item_sum: Optional[Decimal] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Схемы для Чека (Check) ---

class CheckBase(BaseModel):
    check_sum: Decimal
    user_id: int
    org_id: int

class CheckCreate(CheckBase):
    items: List[ItemCreate] = []

class Check(CheckBase):
    check_id: int
    created_at: datetime
    items: List[Item] = []
    user: User
    organization: Organization
    invoices: List[Invoice] = []

    model_config = ConfigDict(from_attributes=True)


class CheckUpdate(CheckBase):
    pass