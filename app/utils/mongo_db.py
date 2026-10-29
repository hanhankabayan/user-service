from datetime import datetime

from app.enums.common import SortOrderEnum
from bson import ObjectId


def mongo_db_serializer(data: dict) -> dict:
    result = {}

    if isinstance(data, ObjectId):
        return str(data)

    if isinstance(data, datetime):
        return data.isoformat()

    if isinstance(data, list):
        return [mongo_db_serializer(item) for item in data]

    if isinstance(data, dict):
        result = {}

        for key, value in data.items():
            serialized_key = "id" if key == "_id" else key
            result[serialized_key] = mongo_db_serializer(value)

        return result

    return data


def get_mongo_db_sort_order(sort_order: SortOrderEnum):
    return -1 if sort_order == SortOrderEnum.DESC.value else 1
