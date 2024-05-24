from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from app.models.user import User
from app.services.auth_service import get_user_manager
from app.utils.auth_config import auth_backend

from app.services.monitoring_service import high_load_processes, monitor_resources_activity

process_ub_router = APIRouter(prefix='/process_ubuntu', tags=["Process_ubuntu"])
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)


@process_ub_router.get("/get_high_load_processes")
async def get_high_load_processes():
    return await high_load_processes()


@process_ub_router.get("/get_resources_activity")
async def get_resources_activity():
    return await monitor_resources_activity()

