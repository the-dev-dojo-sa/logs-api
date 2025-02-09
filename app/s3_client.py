# app/s3_client.py
import aioboto3
import uuid
from .config import settings


async def upload_log(content: str, application_name: str) -> str:
    """
    Загружает содержимое лога в S3 и возвращает сгенерированный ключ.
    """
    key = f"logs/{application_name}/{uuid.uuid4()}.log"
    session = aioboto3.Session()
    async with session.client(
        "s3",
        endpoint_url=f"https://{settings.S3_HOST}",
        region_name=settings.S3_REGION,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    ) as s3:
        await s3.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=content)
    return key
