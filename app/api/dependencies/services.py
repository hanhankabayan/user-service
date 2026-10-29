from app.api.dependencies.repositories import (
    ProjectRepoDependency,
    UserRepoDependency,
)
from app.factories.services import create_user_service
from app.services.user import UserService


# --- auth ---
def get_user_service(
    user_repo: UserRepoDependency,
    project_repo: ProjectRepoDependency,
) -> UserService:
    return create_user_service(
        user_repo=user_repo,
        project_repo=project_repo,
    )
