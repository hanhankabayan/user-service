from datetime import datetime

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: int | None = Field(serialization_alias="_id", default=None)
    name: str
    logo: str | None = None
    alias: str | None = None
    started_at: datetime | None = Field(
        serialization_alias="periode_from", default=None
    )
    ends_at: datetime | None = Field(serialization_alias="periode_to", default=None)
    subscribe_type: int | None = Field(serialization_alias="display_tipe", default=None)
    features: dict | None = None
