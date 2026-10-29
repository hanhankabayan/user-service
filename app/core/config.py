import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        # service name (required)
        self.SERVICE_NAME: str = "Medmon User Service"

        # medmon db
        self.MEDMON_DB_URI: str = os.getenv("MEDMON_DB_URI")
        self.MEDMON_DB_NAME: str = os.getenv("MEDMON_DB_NAME")

        # auth
        self.AUTH_SECRET_KEY: str = os.getenv("AUTH_SECRET_KEY")
        self.AUTH_TOKEN_URL: str = os.getenv("AUTH_TOKEN_URL")

        # telegram logs
        self.TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
        self.TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")
        self.TELEGRAM_MESSAGE_THREAD_ID: str = os.getenv("TELEGRAM_MESSAGE_THREAD_ID")

        # whitelist domain
        self.ORIGINS: list[str] = [
            item.strip() for item in os.getenv("ORIGINS").split(",")
        ]


config = Config()
