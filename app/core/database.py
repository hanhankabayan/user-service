from app.core.config import config
from app.core.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = get_logger(__name__)


class Database:
    def __init__(self):
        self._medmon_db_client: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        # open medmon db connection
        logger.info(f"[MongoDB] Connecting to Database ({config.MEDMON_DB_NAME})...")

        self._medmon_db_client = AsyncIOMotorClient(config.MEDMON_DB_URI)

        logger.info(
            f"[MongoDB] Database ({config.MEDMON_DB_NAME}) is connected successfully!"
        )

    async def close(self) -> None:
        # close apps db connection
        if self._medmon_db_client:
            logger.info(
                f"[MongoDB] Closing Database connection ({config.MEDMON_DB_NAME})..."
            )

            self._medmon_db_client.close()
            self._medmon_db_client = None

            logger.info(
                f"[MongoDB] Database ({config.MEDMON_DB_NAME}) connection closed!"
            )

    def get_medmon_db(self) -> AsyncIOMotorDatabase:
        if not self._medmon_db_client:
            raise RuntimeError(
                f"[MongoDB] Database client for {config.MEDMON_DB_NAME} not initialized"
            )

        return self._medmon_db_client[config.MEDMON_DB_NAME]


database = Database()
