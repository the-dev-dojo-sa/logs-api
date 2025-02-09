# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Схема для создания лог-записи
class LogEntryCreate(BaseModel):
    application_name: str  # Название уже созданного приложения
    user: Optional[str] = None  # Идентификация пользователя (например, email)
    notification_text: str  # Текст уведомления для Telegram
    log_content: str  # Содержимое лог-файла


# Схема для ответа лог-записи
class LogEntryResponse(BaseModel):
    id: int
    s3_key: str
    timestamp: datetime

    class Config:
        orm_mode = True


# Схема для создания приложения
class ApplicationCreate(BaseModel):
    name: str
    telegram_chat_id: str


# Схема для ответа приложения
class ApplicationResponse(BaseModel):
    id: int
    name: str
    telegram_chat_id: str
    created_at: datetime

    class Config:
        orm_mode = True
