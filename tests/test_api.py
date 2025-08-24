"""
Тесты для API.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_user, crud_organization
from app.schemas.check import UserCreate, OrganizationCreate

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
