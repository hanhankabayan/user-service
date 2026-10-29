from datetime import datetime

import pytz
from app.core.logger import get_logger

logger = get_logger(__name__)


def get_current_datetime() -> datetime:
    to_zone = pytz.timezone("Asia/Jakarta")
    current_time = datetime.now(to_zone).replace(tzinfo=None)

    return current_time


def change_dict_to_dot_key(data: dict, parent_key: str = ""):
    result = {}

    for key, value in data.items():
        new_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict):
            result.update(change_dict_to_dot_key(value, new_key))
        else:
            result[new_key] = value

    return result


def split_to_int_list(data: str, separator: str = ",") -> list[int]:
    if not data:
        return []

    list_of_int = []
    for item in data.split(separator):
        try:
            list_of_int.append(int(item.strip()))
        except Exception as err:
            logger.error(f"Error parsing list int: {err}")
            continue

    return list_of_int
