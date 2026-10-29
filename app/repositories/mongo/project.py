from app.core.logger import get_logger
from app.models.project import Project
from app.repositories.project import AbstractProjectRepository
from app.utils.mongo_db import mongo_db_serializer
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = get_logger(__name__)


class MongoProjectRepository(AbstractProjectRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db["projects"]

    def _to_model(self, data: dict | None) -> Project | None:
        if not data:
            return None

        new_data = data.copy()
        new_data["id"] = str(new_data.pop("_id"))
        new_data["started_at"] = new_data.pop("periode_from")
        new_data["ends_at"] = new_data.pop("periode_to")
        new_data["subscribe_type"] = new_data.pop("display_tipe")

        serialized_data = mongo_db_serializer(new_data)

        return Project(**serialized_data)

    async def find_by_id(self, project_id: int) -> Project | None:
        project = await self._collection.find_one({"_id": project_id})

        return self._to_model(project)
