from app.core.config import config
from app.core.http_client import HttpClient
from app.core.logger import get_logger

logger = get_logger(__name__)


class TelegramClient:
    def __init__(
        self,
        bot_token: str = config.TELEGRAM_BOT_TOKEN,
    ):
        self._bot_token = bot_token
        self._base_url = f"https://api.telegram.org/bot{self._bot_token}"

    async def send_message(
        self, chat_id: str, text: str, message_thread_id: str | None = None
    ):
        url = f"{self._base_url}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }

        if message_thread_id:
            payload["message_thread_id"] = message_thread_id

        try:
            response = await HttpClient.client.post(url, json=payload)

            return response.json()
        except Exception as err:
            logger.error(f"[Telegram Client] Failed to send telegram message: {err}")

            raise
