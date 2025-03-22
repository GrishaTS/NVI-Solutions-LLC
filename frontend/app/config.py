from functools import cached_property
from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс конфигурации настроек приложения.
    """

    FRONTEND_HOST: str
    FRONTEND_PORT: int
    BACKEND_HOST: str
    BACKEND_PORT: int
    
    @cached_property
    def BACKEND_URL(self) -> str:
        """
        Генерирует URL для бэкенда.

        :return: Строка с URL бэкенда.
        """
        return f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}"


settings = Settings()