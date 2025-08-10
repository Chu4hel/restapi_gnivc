from pydantic_settings import BaseSettings, SettingsConfigDict


"""
Модуль для управления конфигурацией приложения.

Этот модуль определяет класс `Settings`, который использует Pydantic для
загрузки и валидации настроек из переменных окружения (или .env файла).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения, которые загружаются из переменных окружения.

    Атрибуты:
        POSTGRES_SERVER (str): Адрес сервера PostgreSQL.
        POSTGRES_USER (str): Имя пользователя для подключения к PostgreSQL.
        POSTGRES_PASSWORD (str): Пароль для подключения к PostgreSQL.
        POSTGRES_DB (str): Название базы данных в PostgreSQL.
        POSTGRES_PORT (int): Порт для подключения к PostgreSQL.
    """
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        """
        Формирует полный URL для подключения к базе данных.
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Указываем Pydantic, что нужно читать переменные из файла .env
    model_config = SettingsConfigDict(env_file=".env")


# Создаем единственный экземпляр настроек, который будем использовать во всем приложении
settings = Settings()
