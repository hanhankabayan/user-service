from app.api.dependencies.services import get_user_service
from app.dto.common import Pagination
from app.dto.user import (
    UserCreate,
    UserDetailResponse,
    UserFilter,
    UserPaginationResponse,
    UserPasswordUpdate,
    UserUpdate,
)
from app.middlewares.context import AuthClaims
from app.middlewares.main import middleware
from app.services.user import UserService
from fastapi import APIRouter, Body, Depends, Query

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=UserPaginationResponse)
async def get_users(
    filter: UserFilter = Query(),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    users, total = await user_service.get_users(filter, auth_user)

    return UserPaginationResponse(
        users=users,
        pagination=Pagination(
            page=filter.page,
            items=filter.items,
            total=total,
        ),
    )


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    user, project = await user_service.get_user(user_id, auth_user)

    return UserDetailResponse(
        **user.model_dump(),
        project=project,
    )


@router.post("")
async def create_user(
    data: UserCreate = Body(),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    user_id = await user_service.create_user(data, auth_user)

    return {
        "user_id": user_id,
        "message": "User created successfully!",
    }


@router.patch("/{user_id}")
async def update_user(
    user_id: str,
    data: UserUpdate = Body(),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    await user_service.update_user(user_id, data, auth_user)

    return {
        "message": "User updated successfully!",
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    await user_service.delete_user(user_id, auth_user)

    return {
        "message": "User deleted successfully!",
    }


@router.post("/change-password")
async def change_password(
    data: UserPasswordUpdate = Body(),
    user_service: UserService = Depends(get_user_service),
    auth_user: AuthClaims = Depends(middleware.get_auth_user),
):
    await user_service.change_password(data, auth_user)

    return {
        "message": "Password updated successfully!",
    }
