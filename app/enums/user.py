from enum import IntEnum, StrEnum


class UserRoleEnum(IntEnum):
    ADMIN = 2
    USER = 3
    VIEWER = 4


class UserSortByEnum(StrEnum):
    CREATED_AT = "created_at"
    NAME = "name"
    USERNAME = "username"
