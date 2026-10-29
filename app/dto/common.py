from datetime import datetime

import pytz
from pydantic import BaseModel, ConfigDict, field_validator


class BaseRequestModel(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def strip_strings(cls, value):
        if isinstance(value, str):
            return value.strip()

        return value

    @field_validator("*", mode="after")
    @classmethod
    def normalize_datetime(cls, value):
        if not isinstance(value, datetime):
            return value

        to_zone = pytz.timezone("Asia/Jakarta")

        if value.tzinfo is not None:
            value = value.astimezone(to_zone)
        else:
            value = to_zone.localize(value)

        return value.replace(tzinfo=None).replace(microsecond=0)


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Pagination(BaseResponseModel):
    page: int
    items: int
    total: int
