import re

from app.core.logger import get_logger
from app.enums.user import UserSortByEnum
from app.models.user import User
from app.repositories.user import AbstractUserRepository, UserQueryFilter
from app.utils.common import change_dict_to_dot_key, get_current_datetime
from app.utils.mongo_db import get_mongo_db_sort_order, mongo_db_serializer
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = get_logger(__name__)


class MongoUserRepository(AbstractUserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db["users"]

    def _to_model(self, data: dict | None) -> User | None:
        if not data:
            return None

        new_data = data.copy()
        new_data["id"] = str(new_data.pop("_id"))
        new_data["project_id"] = new_data.pop("id_project")
        new_data["name"] = new_data.pop("nama")

        if new_data.get("phone"):
            new_data["phone_number"] = new_data.pop("phone")

        if new_data.get("capabilities"):
            if new_data["capabilities"].get("datacleansing"):
                new_data["capabilities"]["data_cleansing"] = new_data["capabilities"][
                    "datacleansing"
                ]

            new_data["accessibility"] = new_data.pop("capabilities")

        serialized_data = mongo_db_serializer(new_data)

        return User(**serialized_data)

    def _to_mongo_dict(self, data: dict) -> dict:
        new_data = data.copy()

        if new_data.get("id"):
            new_data["id"] = ObjectId(new_data["id"])

        if new_data.get("project_id"):
            new_data["id_project"] = new_data.pop("project_id")

        if new_data.get("name"):
            new_data["nama"] = new_data.pop("name")

        if new_data.get("phone_number"):
            new_data["phone"] = new_data.pop("phone_number")

        if new_data.get("created_by"):
            new_data["created_by"] = ObjectId(new_data["created_by"])

        if new_data.get("updated_by"):
            new_data["updated_by"] = ObjectId(new_data["updated_by"])

        return new_data

    def _generate_query(self, filter: UserQueryFilter) -> dict:
        query_list = []

        if filter.project_id:
            query_list.append({"id_project": filter.project_id})

        if filter.roles:
            query_list.append({"role": {"$in": filter.roles}})

        if filter.search:
            regex_keyword = re.escape(filter.search)
            query_list.append({
                "$or": [
                    {"nama": {"$regex": regex_keyword, "$options": "i"}},
                    {"username": {"$regex": regex_keyword, "$options": "i"}},
                ]
            })

        query = {"$and": query_list} if query_list else {}

        return query

    def _get_sort_by(self, sort_by: UserSortByEnum):
        if sort_by == UserSortByEnum.NAME.value:
            return "nama"

        return sort_by.value

    async def find_all(self, filter):
        query = self._generate_query(filter)

        total = 0

        sort_by = self._get_sort_by(filter.sort_by)
        sort_order = get_mongo_db_sort_order(filter.sort_order)

        if filter.page and filter.items:
            skip = (filter.page - 1) * filter.items

            # counting total
            total = await self._collection.count_documents(query)

            # get data
            cursor = (
                self._collection
                .find(query)
                .skip(skip)
                .limit(filter.items)
                .sort([(sort_by, sort_order)])
            )
            documents = await cursor.to_list(length=filter.items)
        else:
            cursor = self._collection.find(query).sort([(sort_by, sort_order)])
            documents = await cursor.to_list(length=None)

        # mapping
        users = [self._to_model(doc) for doc in documents]

        return users, total

    async def find_by_id(self, project_id, user_id):
        user = await self._collection.find_one({
            "_id": ObjectId(user_id),
            "id_project": project_id,
        })

        return self._to_model(user)

    async def find_by_username(self, project_id, username):
        user = await self._collection.find_one({
            "username": username,
            "id_project": project_id,
        })

        return self._to_model(user)

    async def create(self, data):
        try:
            payload = data.model_dump(by_alias=True, exclude_unset=True)

            if not payload.get("created_at"):
                payload["created_at"] = get_current_datetime()

            if not payload.get("updated_at"):
                payload["updated_at"] = get_current_datetime()

            payload = self._to_mongo_dict(payload)

            result = await self._collection.insert_one(payload)

            return str(result.inserted_id)
        except Exception as err:
            logger.error(f"[MongoDB] Insert query error: {err}")

            raise

    async def update_by_id(self, user_id, payload):
        try:
            if not payload.get("updated_at"):
                payload["updated_at"] = get_current_datetime()

            payload = self._to_mongo_dict(payload)
            payload = change_dict_to_dot_key(payload)

            result = await self._collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": payload}
            )

            return result.matched_count > 0
        except Exception as err:
            logger.error(f"[MongoDB] Update query error: {err}")

            raise

    async def delete_by_id(self, user_id):
        try:
            result = await self._collection.delete_one({"_id": ObjectId(user_id)})

            return result.deleted_count > 0
        except Exception as err:
            logger.error(f"[MongoDB] Delete query error: {err}")

            raise
