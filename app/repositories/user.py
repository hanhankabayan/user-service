from abc import ABC, abstractmethod

from app.enums.common import SortOrderEnum
from app.enums.user import UserSortByEnum
from app.models.user import User
from pydantic import BaseModel


class UserQueryFilter(BaseModel):
    project_id: int | None = None
    roles: list[int] | None = None
    search: str | None = None
    page: int | None = None
    items: int | None = None
    sort_by: UserSortByEnum | None = UserSortByEnum.CREATED_AT.value
    sort_order: SortOrderEnum | None = SortOrderEnum.DESC.value


class AbstractUserRepository(ABC):
    @abstractmethod
    async def find_all(self, filter: UserQueryFilter) -> tuple[list[User], int]:
        pass

    @abstractmethod
    async def find_by_id(self, project_id: int, user_id: str) -> User | None:
        pass

    @abstractmethod
    async def find_by_username(self, project_id: int, username: str) -> User | None:
        pass

    @abstractmethod
    async def create(self, data: User) -> str:
        pass

    @abstractmethod
    async def update_by_id(self, user_id: str, payload: dict) -> bool:
        pass

    @abstractmethod
    async def delete_by_id(self, user_id: str) -> bool:
        pass
