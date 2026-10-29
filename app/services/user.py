from app.core.exception import (
    DataNotFoundException,
    ForbiddenAccessException,
    InternalServerException,
    InvalidOldPasswordException,
    UsernameExistException,
)
from app.dto.user import UserCreate, UserFilter, UserPasswordUpdate, UserUpdate
from app.enums.user import UserRoleEnum
from app.middlewares.context import AuthClaims
from app.models.project import Project
from app.models.user import User
from app.repositories.project import AbstractProjectRepository
from app.repositories.user import AbstractUserRepository
from app.utils.common import get_current_datetime
from app.utils.filter_mapper import mapping_user_base_filter
from werkzeug.security import check_password_hash, generate_password_hash


class UserService:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        project_repo: AbstractProjectRepository,
    ):
        # repositories
        self._user_repo = user_repo
        self._project_repo = project_repo

    async def get_users(
        self, filter: UserFilter, auth_user: AuthClaims
    ) -> tuple[list[User], int]:
        new_filter = mapping_user_base_filter(filter)

        # mapping specific filters
        new_filter.project_id = auth_user.project_id
        new_filter.page = filter.page
        new_filter.items = filter.items
        new_filter.sort_by = filter.sort_by
        new_filter.sort_order = filter.sort_order

        # retrieve data
        users, total = await self._user_repo.find_all(new_filter)

        return users, total

    async def get_user(
        self, user_id: str, auth_user: AuthClaims
    ) -> tuple[User, Project]:
        # retrieve data
        user = await self._user_repo.find_by_id(auth_user.project_id, user_id)
        if not user:
            raise DataNotFoundException(message="User not founds!")

        # check user project
        project = await self._project_repo.find_by_id(auth_user.project_id)
        if not project:
            raise DataNotFoundException(message="Project not founds!")

        # normalize project features
        if project.features:
            for key, value in project.features.items():
                if isinstance(value, dict):
                    project.features[key] = bool(value.get("status", False))
                else:
                    project.features[key] = bool(value)

        return user, project

    async def create_user(self, data: UserCreate, auth_user: AuthClaims) -> str:
        # validate access
        if auth_user.role != UserRoleEnum.ADMIN:
            raise ForbiddenAccessException()

        # check existing username
        exist_user = await self._user_repo.find_by_username(
            auth_user.project_id, data.username
        )
        if exist_user:
            raise UsernameExistException()

        current_datetime = get_current_datetime()

        # formatting password to hash
        formatted_hash_password = f"{data.password}-{auth_user.project_id}-{current_datetime.strftime('%Y%m%d%H%I%S')}"

        # mapping new data
        user = User(
            project_id=auth_user.project_id,
            name=data.name,
            username=data.username,
            password=generate_password_hash(formatted_hash_password),
            role=data.role.value,
            email=data.email,
            phone_number=data.phone_number,
            created_at=current_datetime,
            created_by=auth_user.id,
            updated_at=current_datetime,
            updated_by=auth_user.id,
        )

        # create data
        inserted_id = await self._user_repo.create(user)
        if not inserted_id:
            raise InternalServerException()

        return inserted_id

    async def update_user(
        self, user_id: str, data: UserUpdate, auth_user: AuthClaims
    ) -> bool:
        # validate access
        if user_id != auth_user.id and auth_user.role != UserRoleEnum.ADMIN:
            raise ForbiddenAccessException()

        # check existing data
        user = await self._user_repo.find_by_id(auth_user.project_id, user_id)
        if not user:
            raise DataNotFoundException(message="User not founds!")

        # check existing username
        if data.username != user.username:
            exist_username = await self._user_repo.find_by_username(
                auth_user.project_id, data.username
            )
            if exist_username:
                raise UsernameExistException()

        # mapping update data
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        update_data["updated_by"] = auth_user.id

        # update data
        if not await self._user_repo.update_by_id(user_id, update_data):
            raise InternalServerException()

        return True

    async def delete_user(self, user_id: str, auth_user: AuthClaims) -> bool:
        # validate access
        if auth_user.role != UserRoleEnum.ADMIN:
            raise ForbiddenAccessException()

        # check existing data
        if not await self._user_repo.find_by_id(auth_user.project_id, user_id):
            raise DataNotFoundException(message="User not founds!")

        # delete data
        if not await self._user_repo.delete_by_id(user_id):
            raise InternalServerException()

        return True

    async def change_password(
        self, data: UserPasswordUpdate, auth_user: AuthClaims
    ) -> bool:
        # check existing data
        user = await self._user_repo.find_by_id(auth_user.project_id, auth_user.id)
        if not user:
            raise DataNotFoundException(message="User not founds!")

        # formatting password to hash
        formatted_hash_old_password = f"{data.old_password}-{user.project_id}-{user.created_at.strftime('%Y%m%d%H%I%S')}"
        formatted_hash_new_password = f"{data.new_password}-{user.project_id}-{user.created_at.strftime('%Y%m%d%H%I%S')}"

        # compare old password with existing
        if not check_password_hash(user.password, formatted_hash_old_password):
            raise InvalidOldPasswordException()

        update_data = {
            "password": generate_password_hash(formatted_hash_new_password),
            "updated_by": auth_user.id,
        }
        if not await self._user_repo.update_by_id(auth_user.id, update_data):
            raise InternalServerException()

        return True
