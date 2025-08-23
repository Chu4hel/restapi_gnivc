"""
Скрипт для заполнения базы данных тестовыми данными.
"""
import asyncio
from datetime import datetime
from decimal import Decimal

from app.db.session import get_db
from app.crud import crud_check
from app.schemas.check import UserCreate, OrganizationCreate, InvoiceCreate, CheckCreate, ItemCreate


async def main():
    """Главная функция для заполнения базы данных."""
    print("Начинаем заполнение базы данных...")
    db = await anext(get_db())

    # --- Создание пользователей ---
    print("Создаем пользователей...")
    user1 = await crud_check.create_user(db, user=UserCreate(username="Иван Иванов"))
    user2 = await crud_check.create_user(db, user=UserCreate(username="Петр Петров"))

    # --- Создание организаций ---
    print("Создаем организации...")
    org1 = await crud_check.create_organization(db, organization=OrganizationCreate(org_name="ООО Ромашка", legal_form="ООО"))
    org2 = await crud_check.create_organization(db, organization=OrganizationCreate(org_name="ИП Сидоров", legal_form="ИП"))

    # --- Создание накладных ---
    print("Создаем накладные...")
    invoice1 = await crud_check.create_invoice(db, invoice=InvoiceCreate(invoice_sum=Decimal("1500.00"), invoice_type=1, payment_type="CARD"))
    invoice2 = await crud_check.create_invoice(db, invoice=InvoiceCreate(invoice_sum=Decimal("3500.00"), invoice_type=2, payment_type="CASH"))

    # --- Создание чеков ---
    print("Создаем чеки...")
    check1_items = [
        ItemCreate(item_name="Хлеб", item_price=Decimal("50.00"), item_quantity=Decimal("2.000"), item_sum=Decimal("100.00")),
        ItemCreate(item_name="Молоко", item_price=Decimal("80.00"), item_quantity=Decimal("1.000"), item_sum=Decimal("80.00")),
    ]
    check1 = await crud_check.create_check(db, check=CheckCreate(check_sum=Decimal("180.00"), user_id=user1.user_id, org_id=org1.org_id, items=check1_items))

    check2_items = [
        ItemCreate(item_name="Консультация юриста", item_price=Decimal("2500.00"), item_quantity=Decimal("1.000"), item_sum=Decimal("2500.00")),
    ]
    check2 = await crud_check.create_check(db, check=CheckCreate(check_sum=Decimal("2500.00"), user_id=user2.user_id, org_id=org2.org_id, items=check2_items))

    # --- Связывание чеков с накладными ---
    print("Связываем чеки с накладными...")
    await crud_check.link_check_to_invoice(db, check_id=check1.check_id, invoice_id=invoice1.invoice_id)
    await crud_check.link_check_to_invoice(db, check_id=check2.check_id, invoice_id=invoice2.invoice_id)

    print("Заполнение базы данных завершено.")


if __name__ == "__main__":
    asyncio.run(main())
