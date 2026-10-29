from datetime import datetime

from pydantic import BaseModel, Field


class UserAccessibility(BaseModel):
    data_cleansing: str | None = Field(
        serialization_alias="datacleansing", default=None
    )
    instagram_comment: str | None = None
    tiktok_comment: str | None = None
    youtube_comment: str | None = None


class User(BaseModel):
    id: str | None = Field(serialization_alias="_id", default=None)
    project_id: int = Field(serialization_alias="id_project")
    name: str = Field(serialization_alias="nama")
    username: str
    password: str
    email: str | None = None
    phone_number: str | None = Field(serialization_alias="phone", default=None)
    role: int
    accessibility: UserAccessibility | None = Field(
        serialization_alias="capabilities", default=None
    )
    created_at: datetime | None = None
    created_by: str | None = None
    updated_at: datetime | None = None
    updated_by: str | None = None
