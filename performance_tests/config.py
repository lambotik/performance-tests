from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Импортируем вложенные модели
from performance_tests.tools.config.grpc import GRPCClientConfig
from performance_tests.tools.config.http import HTTPClientConfig
from performance_tests.tools.config.locust import LocustUserConfig

env_file = Path(__file__).parent.parent / '.env.local'

class Settings(BaseSettings):
    # Конфигурация загрузки — откуда брать переменные
    model_config = SettingsConfigDict(
        extra="allow",  # Разрешить дополнительные поля (например, неиспользуемые переменные)
        env_file=env_file,  # Указываем имя и путь до локального .env файла .env.local
        env_file_encoding="utf-8",  # Кодировка файла
        env_nested_delimiter="."  # Позволяет использовать вложенные переменные, например: LOCUST_USER.WAIT_TIME_MIN
    )

    # Вложенные секции настроек
    locust_user: LocustUserConfig  # Настройки виртуального пользователя
    gateway_http_client: HTTPClientConfig  # Настройки HTTP-клиента
    gateway_grpc_client: GRPCClientConfig  # Настройки gRPC-клиента


# Глобальный объект настроек — его можно импортировать в любом месте проекта
settings = Settings()
