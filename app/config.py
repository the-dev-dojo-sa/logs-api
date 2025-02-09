# app/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Конфигурация для S3
    S3_BUCKET: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str = "us-east-1"

    # Конфигурация для Telegram (бот используется для отправки сообщений)
    TELEGRAM_BOT_TOKEN: str

    # Database URL для асинхронного подключения (используем asyncpg)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@db:5432/logs_db"

    # API-ключ для административных операций (создания приложений)
    ADMIN_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
