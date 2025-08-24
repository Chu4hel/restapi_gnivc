"""
Модули базы данных SQLAlchemy для чеков и товаров.

Определяет структуру таблиц `checks`, `items`, `users`, `organizations`, 
`invoices` и их взаимосвязи.
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, func, Numeric, SMALLINT, VARCHAR
)
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    """
    Модель SQLAlchemy, представляющая пользователя.
    """
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    checks = relationship("Check", back_populates="user")


class Organization(Base):
    """
    Модель SQLAlchemy, представляющая организацию.
    """
    __tablename__ = "organizations"

    org_id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String, nullable=False)
    legal_form = Column(VARCHAR(10))

    checks = relationship("Check", back_populates="organization")


class Invoice(Base):
    """
    Модель SQLAlchemy, представляющая накладную.
    """
    __tablename__ = "invoices"

    invoice_id = Column(Integer, primary_key=True, index=True)
    invoice_sum = Column(Numeric(10, 2), nullable=False)
    invoice_type = Column(SMALLINT)
    payment_type = Column(VARCHAR(10))

    checks = relationship("Check", secondary="check_invoices", back_populates="invoices")


class CheckInvoice(Base):
    """
    Ассоциативная таблица для связи многие-ко-многим между чеками и накладными.
    """
    __tablename__ = 'check_invoices'
    check_id = Column(Integer, ForeignKey('checks.check_id'), primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.invoice_id'), primary_key=True)


class Check(Base):
    """
    Модель SQLAlchemy, представляющая чек в базе данных.
    """
    __tablename__ = "checks"

    check_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    check_sum = Column(Numeric(10, 2), nullable=False)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="checks")

    org_id = Column(Integer, ForeignKey("organizations.org_id"), nullable=False)
    organization = relationship("Organization", back_populates="checks")

    items = relationship("Item", back_populates="check", cascade="all, delete-orphan")
    invoices = relationship("Invoice", secondary="check_invoices", back_populates="checks")


class Item(Base):
    """
    Модель SQLAlchemy, представляющая товар в чеке.
    """
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(VARCHAR(255), nullable=False)
    item_price = Column(Numeric(10, 2))
    item_type = Column(SMALLINT)
    item_quantity = Column(Numeric(8, 3))
    item_sum = Column(Numeric(10, 2))

    check_id = Column(Integer, ForeignKey("checks.check_id"), nullable=False)
    check = relationship("Check", back_populates="items")
