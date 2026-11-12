from fastapi import APIRouter, Query

from routers.deps import ActorId
from schemas import (
    UserCreate,
    UserProfileResponse,
    UserResponse,
    UserUpdate,
)
from services import (
    create_user,
    delete_user,
    get_profile,
    get_user,
    list_users,
    update_user,
)
from storage import store

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_users_route(
    q: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
) -> list:
    return list_users(store, q, limit)


@router.post("", response_model=UserResponse, status_code=201)
def create_user_route(payload: UserCreate):
    return create_user(store, payload)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int):
    return get_user(store, user_id)


@router.get("/{user_id}/profile", response_model=UserProfileResponse)
def profile_route(user_id: int):
    data = get_profile(store, user_id)
    return UserProfileResponse(
        **UserResponse.model_validate(data["user"]).model_dump(),
        completed_lessons=data["completed_lessons"],
        solved_problems=data["solved_problems"],
        accepted_submissions=data["accepted_submissions"],
    )


@router.patch("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, payload: UserUpdate, actor_id: ActorId):
    return update_user(store, user_id, payload, actor_id)


@router.delete("/{user_id}", status_code=204)
def delete_user_route(user_id: int, actor_id: ActorId) -> None:
    delete_user(store, user_id, actor_id)
