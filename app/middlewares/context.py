from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class TokenTypeEnum(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthClaims(BaseModel):
    id: str
    project_id: int
    username: str
    role: int
    exp: datetime | None = None
    type: TokenTypeEnum = TokenTypeEnum.ACCESS.value


class RequestContext(BaseModel):
    ip: str | None = None
    port: int | None = None
    user_agent: str | None = None
    url: str | None = None
    method: str | None = None
