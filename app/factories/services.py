from app.core.database import database
from app.repositories.mongo.project import MongoProjectRepository
from app.repositories.mongo.user import MongoUserRepository
from app.repositories.project import AbstractProjectRepository
from app.repositories.user import AbstractUserRepository
from app.services.user import UserService


def create_user_service(
    user_repo: AbstractUserRepository | None = None,
    project_repo: AbstractProjectRepository | None = None,
) -> UserService:
    if user_repo is None:
        user_repo = MongoUserRepository(database.get_medmon_db())

    if project_repo is None:
        project_repo = MongoProjectRepository(database.get_medmon_db())

    return UserService(
        user_repo=user_repo,
        project_repo=project_repo,
    )
