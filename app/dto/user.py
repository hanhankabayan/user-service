from datetime import datetime

from app.dto.common import BaseRequestModel, BaseResponseModel, Pagination
from app.enums.common import SortOrderEnum
from app.enums.user import UserRoleEnum, UserSortByEnum
from fastapi import Query


# --- requests ---
class UserBaseFilter(BaseRequestModel):
    roles: str = Query(
        default=None,
        description=f"Available values: `{[f'{item.name}:{item.value}' for item in UserRoleEnum]}`. --Separate multiple IDs with commas. --Example: 2,3",
    )
    search: str = Query(default=None, description="Search by name or username")


class UserFilter(UserBaseFilter):
    page: int = 1
    items: int = 10
    sort_by: UserSortByEnum = UserSortByEnum.CREATED_AT.value
    sort_order: SortOrderEnum = SortOrderEnum.DESC.value


class UserCreate(BaseRequestModel):
    name: str
    username: str
    password: str
    role: UserRoleEnum
    email: str | None = None
    phone_number: str | None = None


class UserUpdate(BaseRequestModel):
    name: str
    username: str
    role: UserRoleEnum | None = None
    email: str | None = None
    phone_number: str | None = None


class UserPasswordUpdate(BaseRequestModel):
    old_password: str
    new_password: str


# --- responses ---
class UserAccessibilityResponse(BaseResponseModel):
    data_cleansing: str | None = None
    instagram_comment: str | None = None
    tiktok_comment: str | None = None
    youtube_comment: str | None = None


class UserProjectResponse(BaseResponseModel):
    id: int
    name: str
    logo: str | None = None
    alias: str
    started_at: datetime | None = None
    ends_at: datetime | None = None
    subscribe_type: int | None = None
    features: dict | None = dict


class UserResponse(BaseResponseModel):
    id: str
    name: str
    username: str
    role: int = UserRoleEnum.ADMIN.value
    email: str | None = None
    phone_number: str | None = None
    created_at: datetime | None = None


class UserPaginationResponse(BaseResponseModel):
    users: list[UserResponse]
    pagination: Pagination


class UserDetailResponse(UserResponse):
    accessibility: UserAccessibilityResponse | None = None
    project: UserProjectResponse
