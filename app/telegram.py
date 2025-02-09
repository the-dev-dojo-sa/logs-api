# app/telegram.py
import httpx
from .config import settings


async def send_telegram_notification(
    notification_text: str, log_content: str, filename: str, telegram_chat_id: str
):
    """
    Отправляет уведомление в Telegram с прикрепленным лог-файлом в указанный чат.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    async with httpx.AsyncClient() as client:
        files = {"document": (filename, log_content)}
        data = {"chat_id": telegram_chat_id, "caption": notification_text}
        response = await client.post(url, data=data, files=files)
        response.raise_for_status()
        return response.json()
