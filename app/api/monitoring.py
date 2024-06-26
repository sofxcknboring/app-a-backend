from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from app.models.user import User
from app.services.auth_service import get_user_manager
from app.utils.auth_config import auth_backend

from app.services.monitoring_service import high_load_processes, get_system_load_data

process_ub_router = APIRouter(prefix='/process_ubuntu', tags=["Process_ubuntu"])
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


@process_ub_router.get("/get_high_load_processes")
async def get_high_load_processes(user_check: User = Depends(current_superuser)):
    if user_check:
        return await high_load_processes()


@process_ub_router.get("/get_system_load")
async def get_uptime_server(user_check: User = Depends(current_superuser)):
    if user_check:
        result = await get_system_load_data()
        return result

