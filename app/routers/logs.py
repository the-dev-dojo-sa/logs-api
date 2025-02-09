# app/routers/logs.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud, s3_client, telegram
from ..database import async_session

router = APIRouter(prefix="/logs", tags=["logs"])


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


@router.post("/", response_model=schemas.LogEntryResponse)
async def create_log(log: schemas.LogEntryCreate, db: AsyncSession = Depends(get_db)):
    # По имени ищем приложение
    application = await crud.get_application_by_name(db, log.application_name)
    if not application:
        raise HTTPException(status_code=404, detail="Приложение не найдено")

    # Загружаем лог в S3
    try:
        s3_key = await s3_client.upload_log(log.log_content, log.application_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки в S3: {str(e)}")

    # Сохраняем лог в БД
    try:
        db_log = await crud.create_log_entry(db, log, s3_key, application.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения в БД: {str(e)}")

    # Отправляем уведомление в Telegram в указанный чат
    try:
        filename = s3_key.split("/")[-1]
        await telegram.send_telegram_notification(
            log.notification_text,
            log.log_content,
            filename,
            application.telegram_chat_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка отправки уведомления в Telegram: {str(e)}"
        )

    return db_log
