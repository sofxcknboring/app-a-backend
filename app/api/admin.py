from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from app.models.user import User
from app.services.auth_service import get_user_manager
from app.utils.auth_config import auth_backend


admin_router = APIRouter(prefix='/admin', tags=["Admin"])
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_active_user = fastapi_users.current_user(active=True)


@admin_router.get("/test-admin-route")
def protected_route(user: User = Depends(current_superuser)):
    return f"Hello, {user.email}. You are authenticated with a cookie or a JWT."
