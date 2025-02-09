# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def create_application(
    db: AsyncSession, app_create: schemas.ApplicationCreate
) -> models.Application:
    db_app = models.Application(
        name=app_create.name, telegram_chat_id=app_create.telegram_chat_id
    )
    db.add(db_app)
    await db.commit()
    await db.refresh(db_app)
    return db_app


async def get_application_by_name(db: AsyncSession, name: str):
    result = await db.execute(
        select(models.Application).where(models.Application.name == name)
    )
    return result.scalars().first()


async def create_log_entry(
    db: AsyncSession, log: schemas.LogEntryCreate, s3_key: str, application_id: int
) -> models.LogEntry:
    db_log = models.LogEntry(
        application_id=application_id,
        user=log.user,
        notification_text=log.notification_text,
        s3_key=s3_key,
    )
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log
