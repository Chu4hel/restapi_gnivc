"""
Схемы для JWT-токенов.
"""
from pydantic import BaseModel


class Token(BaseModel):
    """Схема для токена доступа."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Схема для данных, закодированных в токене."""
    username: str | None = None
