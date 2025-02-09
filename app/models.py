# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    telegram_chat_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship("LogEntry", back_populates="application")


class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    user = Column(String, nullable=True)  # Идентификация пользователя (например, email)
    notification_text = Column(Text, nullable=False)
    s3_key = Column(String, unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="logs")
