"""Конфигурация Flask-приложения «Мои задачи»."""

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE_PATH = INSTANCE_DIR / "todo.db"

# Переменные из .env (если файл существует) загружаются раньше чтения настроек.
load_dotenv(BASE_DIR / ".env")


class Config:
    """Настройки по умолчанию для локальной разработки и продакшена."""

    # В продакшене обязательно задайте SECRET_KEY через переменную окружения.
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{DATABASE_PATH.as_posix()}"
    )
    # Heroku и некоторые другие платформы до сих пор отдают схему postgres://.
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
