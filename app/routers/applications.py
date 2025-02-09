# app/routers/applications.py
import hmac

from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from .. import schemas, crud
from ..database import async_session

router = APIRouter(prefix="/applications", tags=["applications"])


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


# Простая проверка админского API-ключа
async def verify_admin(x_admin_api_key: Optional[str] = Header(None)):
    from ..config import settings

    if not hmac.compare_digest(x_admin_api_key, settings.ADMIN_API_KEY):
        raise HTTPException(status_code=403, detail="Нет доступа")
    return x_admin_api_key


@router.post(
    "/",
    response_model=schemas.ApplicationResponse,
    dependencies=[Depends(verify_admin)],
)
async def create_application(
    app_data: schemas.ApplicationCreate, db: AsyncSession = Depends(get_db)
):
    # Проверяем, существует ли приложение с таким именем
    existing = await crud.get_application_by_name(db, app_data.name)
    if existing:
        raise HTTPException(
            status_code=400, detail="Приложение с таким именем уже существует"
        )
    new_app = await crud.create_application(db, app_data)
    return new_app
