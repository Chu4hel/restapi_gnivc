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
        TEST_POSTGRES_SERVER (str): Адрес тестового сервера PostgreSQL.
        TEST_POSTGRES_USER (str): Имя пользователя для подключения к тестовому PostgreSQL.
        TEST_POSTGRES_PASSWORD (str): Пароль для подключения к тестовому PostgreSQL.
        TEST_POSTGRES_DB (str): Название тестовой базы данных в PostgreSQL.
        TEST_POSTGRES_PORT (int): Порт для подключения к тестовому PostgreSQL.
        SECRET_KEY (str): Секретный ключ для подписи JWT-токенов.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Время жизни токена доступа в минутах.
        TESTING (bool): Флаг, указывающий, запущено ли приложение в режиме тестирования.
    """
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_PORT: int
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    TESTING: bool = False

    @property
    def DATABASE_URL(self) -> str:
        """
        Формирует полный URL для подключения к базе данных.
        """
        if self.TESTING:
            return (
                f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@"
                f"{self.TEST_POSTGRES_SERVER}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
            )
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Указываем Pydantic, что нужно читать переменные из файла .env
    model_config = SettingsConfigDict(env_file=".env")


# Создаем единственный экземпляр настроек, который будем использовать во всем приложении
settings = Settings()
