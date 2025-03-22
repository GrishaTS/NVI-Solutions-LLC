from functools import cached_property
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    '''Настройки приложения.'''

    APP_MODE: Literal['DEV', 'PROD']
    BACKEND_HOST: str
    BACKEND_PORT: int
    FRONTEND_HOST: str
    FRONTEND_PORT: int
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    @cached_property
    def FRONTEND_URL(self) -> str:
        '''Возвращает URL фронтенда.'''
        return f'http://{self.FRONTEND_HOST}:{self.FRONTEND_PORT}'

    @cached_property
    def BACKEND_URL(self) -> str:
        '''Возвращает URL бэкенда.'''
        return f'http://{self.BACKEND_HOST}:{self.BACKEND_PORT}'

    @cached_property
    def POSTGRES_URL(self) -> str:
        '''Возвращает URL подключения к PostgreSQL.'''
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )


settings = Settings()