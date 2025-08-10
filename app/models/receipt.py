"""
Модули базы данных SQLAlchemy для чеков и товаров.

Определяет структуру таблиц `receipts` и `items` и их взаимосвязи.
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, func
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class Receipt(Base):
    """
    Модель SQLAlchemy, представляющая чек в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор чека.
        user_id (int): Идентификатор пользователя, которому принадлежит чек.
        created_at (datetime): Дата и время создания чека.
        items (relationship): Связь с товарами, принадлежащими этому чеку.
    """
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связь "один-ко-многим": один чек может иметь много товаров
    # cascade="all, delete-orphan" означает, что при удалении чека удалятся и все связанные с ним товары.
    items = relationship("Item", back_populates="receipt", cascade="all, delete-orphan")


class Item(Base):
    """
    Модель SQLAlchemy, представляющая товар в чеке.

    Атрибуты:
        id (int): Уникальный идентификатор товара.
        name (str): Наименование товара.
        price (int): Цена за единицу товара.
        quantity (float): Количество товара.
        sum (int): Общая стоимость товара.
        invoice_type (int, optional): Тип накладной.
        invoice_sum (int, optional): Сумма по накладной.
        product_type (int, optional): Тип продукта.
        payment_type (int, optional): Тип оплаты.
        receipt_id (int): Внешний ключ, связывающий товар с чеком.
        receipt (relationship): Обратная связь с объектом чека.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer)
    quantity = Column(Float)
    sum = Column(Integer)

    # Опциональные поля
    invoice_type = Column(Integer, nullable=True)
    invoice_sum = Column(Integer, nullable=True)
    product_type = Column(Integer, nullable=True)
    payment_type = Column(Integer, nullable=True)

    # Внешний ключ для связи с таблицей чеков
    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=False)

    # Обратная связь для удобного доступа к объекту чека из товара
    receipt = relationship("Receipt", back_populates="items")
