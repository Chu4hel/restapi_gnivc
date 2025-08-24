"""
Определяет Pydantic схемы для валидации данных запросов и сериализации ответов API.

Этот модуль содержит все модели данных, которые используются FastAPI для:
1.  Валидации JSON-объектов, поступающих в POST/PUT запросах.
2.  Сериализации объектов SQLAlchemy в JSON для ответов API.
3.  Автоматической генерации документации OpenAPI (Swagger/ReDoc).
"""

from pydantic import BaseModel, ConfigDict, PlainSerializer
from typing import List, Optional, Annotated
from datetime import datetime, date
from decimal import Decimal

# Пользовательский тип для корректной сериализации Decimal в float в Pydantic V2.
# Annotated используется для добавления метаданных (в данном случае, сериализатора) к типу.
DecimalAsFloat = Annotated[Decimal, PlainSerializer(lambda x: float(x), return_type=float)]


# ==============================================================================
# Схемы для сущности "Пользователь" (User)
# ==============================================================================

class UserBase(BaseModel):
    """Базовая схема для пользователя, содержащая общие поля."""
    username: str


class UserCreate(UserBase):
    """Схема для создания нового пользователя. Включает поле 'password'."""
    password: str


class User(UserBase):
    """Схема для возврата данных о пользователе из API. Не содержит 'password'."""
    user_id: int
    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# Схемы для сущности "Организация" (Organization)
# ==============================================================================

class OrganizationBase(BaseModel):
    """Базовая схема для организации."""
    org_name: str
    legal_form: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    """Схема для создания новой организации."""
    pass


class Organization(OrganizationBase):
    """Схема для возврата данных об организации из API."""
    org_id: int
    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# Схемы для сущности "Накладная" (Invoice)
# ==============================================================================

class InvoiceBase(BaseModel):
    """Базовая схема для накладной."""
    invoice_sum: DecimalAsFloat
    invoice_type: Optional[int] = None
    payment_type: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    """Схема для создания новой накладной."""
    pass


class Invoice(InvoiceBase):
    """Схема для возврата данных о накладной из API."""
    invoice_id: int
    model_config = ConfigDict(from_attributes=True)


class InvoiceWithChecks(Invoice):
    """Расширенная схема накладной для будущего использования (например, с деталями чеков)."""
    pass


# ==============================================================================
# Схемы для сущности "Товар/Позиция" (Item)
# ==============================================================================

class ItemBase(BaseModel):
    """Базовая схема для товарной позиции в чеке."""
    item_name: str
    item_price: Optional[DecimalAsFloat] = None
    item_type: Optional[int] = None
    item_quantity: Optional[DecimalAsFloat] = None
    item_sum: Optional[DecimalAsFloat] = None


class ItemCreate(ItemBase):
    """Схема для создания новой товарной позиции в составе чека."""
    pass


class Item(ItemBase):
    """Схема для возврата данных о товарной позиции из API."""
    item_id: int
    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# Схемы для сущности "Чек" (Check)
# ==============================================================================

class CheckBase(BaseModel):
    """Базовая схема для чека."""
    check_sum: DecimalAsFloat
    user_id: int
    org_id: int


class CheckCreate(CheckBase):
    """Схема для создания нового чека, включая список товарных позиций."""
    items: List[ItemCreate] = []


class Check(CheckBase):
    """Полная схема чека для вывода из API, включая связанные объекты."""
    check_id: int
    created_at: datetime
    items: List[Item] = []
    user: User
    organization: Organization
    model_config = ConfigDict(from_attributes=True)


class CheckUpdate(CheckBase):
    """Схема для обновления существующего чека."""
    pass


# Обновление forward-ссылок в моделях после их полного определения.
# Необходимо для разрешения циклических зависимостей, если они появятся.
InvoiceWithChecks.model_rebuild()
Check.model_rebuild()


# ==============================================================================
# Схемы для аналитических эндпоинтов
# ==============================================================================

class SalesByOrganization(BaseModel):
    """Схема для вывода аналитики по продажам в разрезе организаций."""
    org_name: str
    legal_form: Optional[str] = None
    total_checks: int
    total_revenue: DecimalAsFloat
    avg_check_amount: DecimalAsFloat
    model_config = ConfigDict(from_attributes=True)


class UserCheck(BaseModel):
    """Схема для вывода списка чеков пользователя за период."""
    check_id: int
    created_at: datetime
    check_sum: DecimalAsFloat
    org_name: str
    legal_form: Optional[str] = None
    items: str
    model_config = ConfigDict(from_attributes=True)


class ItemsByCategory(BaseModel):
    """Схема для вывода аналитики по товарам в разрезе категорий."""
    category: str
    items_sold: int
    total_quantity: DecimalAsFloat
    total_revenue: DecimalAsFloat
    model_config = ConfigDict(from_attributes=True)
