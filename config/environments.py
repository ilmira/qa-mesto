import json
from pathlib import Path

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from typing import Dict, Literal


class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        return {"dev": "Dev", "stage": "Stage"}[self.value]


class UserCredentials(BaseModel):
    """Модель учётных данных пользователя."""
    email: str
    password: str


class EnvironmentConfig(BaseSettings):
    """Конфигурация для конкретного окружения (загружается из .env.dev или .env.stage)."""

    url: str
    default_user: Literal["user", "admin"] = "user"
    users: Dict[str, UserCredentials] = Field(default_factory=dict)

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("users", mode="before")
    @classmethod
    def parse_users_json(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON for USERS: {v}")
        return v

    def get_user_credentials(self, user_type: str = None) -> UserCredentials:
        """Возвращает учётные данные для указанного типа пользователя (user/admin) или default_user."""
        key = user_type or self.default_user
        if key not in self.users:
            raise KeyError(f"User type '{key}' not found in USERS. Available: {list(self.users.keys())}")
        return self.users[key]

    def __str__(self):
        return f"- URL: {self.url}, default user: {self.default_user}"


def load_config(env: Environment = Environment.DEV) -> EnvironmentConfig:
    """Загружает конфигурацию из .env.<env>"""
    base_dir = Path(__file__).parent.parent
    env_file = base_dir / f".env.{env.value}"
    return EnvironmentConfig(_env_file=env_file)


def print_environment_info(env_name: str, user_type: str = None):
    """Выводит краткую сводку по тестовому окружению с выбранным пользователем."""
    env = Environment(env_name)
    config = load_config(env)
    creds = config.get_user_credentials(user_type)

    print()
    print(f"Окружение:    {env.value.upper()}")
    print(f"URL:          {config.url}")
    print(f"Пользователь: {creds.email}")
    print(f"Пароль:       {creds.password}")
    print()
