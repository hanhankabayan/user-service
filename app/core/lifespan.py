from contextlib import asynccontextmanager

from app.core.database import database
from app.core.logger import setup_logger


@asynccontextmanager
async def lifespan(app):
    setup_logger()

    # initialize infrastructure
    await database.connect()

    yield

    await database.close()
