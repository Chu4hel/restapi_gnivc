"""
Тесты для API.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_user, crud_organization, crud_invoice, crud_check
from app.schemas.check import UserCreate, OrganizationCreate, InvoiceCreate, CheckCreate, ItemCreate

pytestmark = pytest.mark.asyncio


async def create_user_and_get_token(client: AsyncClient, db_session: AsyncSession, username, password):
    """Вспомогательная функция для создания пользователя и получения токена."""
    user = await crud_user.create_user(db_session, UserCreate(username=username, password=password))
    login_response = await client.post(
        "/api/v1/login/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return login_response.json()["access_token"]


async def test_create_user(client: AsyncClient, db_session: AsyncSession):
    """Тест создания нового пользователя."""
    response = await client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "user_id" in data


async def test_login_for_access_token(client: AsyncClient, db_session: AsyncSession):
    """Тест получения токена доступа."""
    token = await create_user_and_get_token(client, db_session, "testuser2", "testpassword2")
    assert token


async def test_read_users(client: AsyncClient, db_session: AsyncSession):
    """Тест получения списка пользователей (требует аутентификации)."""
    token = await create_user_and_get_token(client, db_session, "testuser3", "testpassword3")
    response = await client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


async def test_read_users_unauthenticated(client: AsyncClient, db_session: AsyncSession):
    """Тест получения списка пользователей (без аутентификации)."""
    response = await client.get("/api/v1/users/")
    assert response.status_code == 401


# --- Тесты для организаций ---

async def test_create_organization(client: AsyncClient, db_session: AsyncSession):
    """Тест создания новой организации."""
    token = await create_user_and_get_token(client, db_session, "org_user", "org_password")
    response = await client.post(
        "/api/v1/organizations/",
        json={"org_name": "Test Org", "legal_form": "OOO"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["org_name"] == "Test Org"


async def test_read_organizations(client: AsyncClient, db_session: AsyncSession):
    """Тест получения списка организаций."""
    token = await create_user_and_get_token(client, db_session, "org_user_2", "org_password_2")
    await crud_organization.create_organization(db_session, OrganizationCreate(org_name="Test Org 2"))
    response = await client.get(
        "/api/v1/organizations/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


async def test_read_organization(client: AsyncClient, db_session: AsyncSession):
    """Тест получения организации по ID."""
    token = await create_user_and_get_token(client, db_session, "org_user_3", "org_password_3")
    org = await crud_organization.create_organization(db_session, OrganizationCreate(org_name="Test Org 3"))
    response = await client.get(
        f"/api/v1/organizations/{org.org_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["org_name"] == "Test Org 3"


async def test_create_organization_unauthenticated(client: AsyncClient, db_session: AsyncSession):
    """Тест создания организации без аутентификации."""
    response = await client.post(
        "/api/v1/organizations/",
        json={"org_name": "Test Org 4", "legal_form": "PAO"},
    )
    assert response.status_code == 401


# --- Тесты для накладных ---

async def test_create_invoice(client: AsyncClient, db_session: AsyncSession):
    """Тест создания новой накладной."""
    token = await create_user_and_get_token(client, db_session, "invoice_user", "invoice_password")
    response = await client.post(
        "/api/v1/invoices/",
        json={"invoice_sum": 1000, "invoice_type": 1, "payment_type": "CASH"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["invoice_sum"] == 1000


async def test_read_invoices(client: AsyncClient, db_session: AsyncSession):
    """Тест получения списка накладных."""
    token = await create_user_and_get_token(client, db_session, "invoice_user_2", "invoice_password_2")
    await crud_invoice.create_invoice(db_session, InvoiceCreate(invoice_sum=2000))
    response = await client.get(
        "/api/v1/invoices/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


async def test_read_invoice(client: AsyncClient, db_session: AsyncSession):
    """Тест получения накладной по ID."""
    token = await create_user_and_get_token(client, db_session, "invoice_user_3", "invoice_password_3")
    invoice = await crud_invoice.create_invoice(db_session, InvoiceCreate(invoice_sum=3000))
    response = await client.get(
        f"/api/v1/invoices/{invoice.invoice_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["invoice_sum"] == 3000


# --- Тесты для чеков ---

async def test_create_check(client: AsyncClient, db_session: AsyncSession):
    """Тест создания нового чека."""
    token = await create_user_and_get_token(client, db_session, "check_user", "check_password")

    # Сначала создаем пользователя и организацию
    user = await crud_user.create_user(db_session,
                                       UserCreate(username="check_test_user", password="check_test_password"))
    organization = await crud_organization.create_organization(db_session,
                                                               OrganizationCreate(org_name="Check Test Org"))

    response = await client.post(
        "/api/v1/checks/",
        json={
            "check_sum": 500,
            "user_id": user.user_id,
            "org_id": organization.org_id,
            "items": [
                {"item_name": "Test Item", "item_price": 500, "item_quantity": 1, "item_sum": 500}
            ]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["check_sum"] == 500


async def test_read_checks(client: AsyncClient, db_session: AsyncSession):
    """Тест получения списка чеков."""
    token = await create_user_and_get_token(client, db_session, "check_user_2", "check_password_2")
    user = await crud_user.create_user(db_session,
                                       UserCreate(username="check_test_user_2", password="check_test_password_2"))
    organization = await crud_organization.create_organization(db_session,
                                                               OrganizationCreate(org_name="Check Test Org 2"))
    await crud_check.create_check(db_session,
                                  CheckCreate(check_sum=1000, user_id=user.user_id, org_id=organization.org_id))
    response = await client.get(
        "/api/v1/checks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


async def test_read_check(client: AsyncClient, db_session: AsyncSession):
    """Тест получения чека по ID."""
    token = await create_user_and_get_token(client, db_session, "check_user_3", "check_password_3")
    user = await crud_user.create_user(db_session,
                                       UserCreate(username="check_test_user_3", password="check_test_password_3"))
    organization = await crud_organization.create_organization(db_session,
                                                               OrganizationCreate(org_name="Check Test Org 3"))
    check = await crud_check.create_check(db_session,
                                          CheckCreate(check_sum=1500, user_id=user.user_id, org_id=organization.org_id))
    response = await client.get(
        f"/api/v1/checks/{check.check_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["check_sum"] == 1500


# --- Тесты для фильтрации и сортировки ---

async def test_filter_checks_by_user(client: AsyncClient, db_session: AsyncSession):
    """Тест фильтрации чеков по пользователю."""
    token = await create_user_and_get_token(client, db_session, "filter_user", "filter_password")
    user1 = await crud_user.create_user(db_session, UserCreate(username="filter_user_1", password="password"))
    user2 = await crud_user.create_user(db_session, UserCreate(username="filter_user_2", password="password"))
    org = await crud_organization.create_organization(db_session, OrganizationCreate(org_name="Filter Org"))
    await crud_check.create_check(db_session, CheckCreate(check_sum=100, user_id=user1.user_id, org_id=org.org_id))
    await crud_check.create_check(db_session, CheckCreate(check_sum=200, user_id=user2.user_id, org_id=org.org_id))

    response = await client.get(
        f"/api/v1/checks/?user_id={user1.user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user1.user_id


async def test_sort_checks_by_sum(client: AsyncClient, db_session: AsyncSession):
    """Тест сортировки чеков по сумме."""
    token = await create_user_and_get_token(client, db_session, "sort_user", "sort_password")
    user = await crud_user.create_user(db_session, UserCreate(username="sort_test_user", password="password"))
    org = await crud_organization.create_organization(db_session, OrganizationCreate(org_name="Sort Org"))
    await crud_check.create_check(db_session, CheckCreate(check_sum=100, user_id=user.user_id, org_id=org.org_id))
    await crud_check.create_check(db_session, CheckCreate(check_sum=200, user_id=user.user_id, org_id=org.org_id))

    response = await client.get(
        "/api/v1/checks/?sort_by=check_sum&sort_order=desc",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["check_sum"] == 200
    assert data[1]["check_sum"] == 100
