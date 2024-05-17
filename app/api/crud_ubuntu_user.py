from select import select

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.models.schemas import UbuntuUserCreate, UbuntuUserRead, UbuntuUserUpdate
from app.models.user import User
from app.db.base import get_ubuntu_user_db
from app.services.auth_service import get_user_manager
from app.services.crud_ub_user_service import add_ub_user, delete_ub_user, update_ub_user
from app.utils.auth_config import auth_backend

crud_ubuntu_user_router = APIRouter(prefix='/crud-ubuntu-user', tags=["Crud_ubuntu_user"])
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_active_user = fastapi_users.current_user(active=True)


@crud_ubuntu_user_router.post('/create-ub-user')
async def create_ubuntu_user(
        ubuntu_user_create: UbuntuUserCreate,
        user_db: SQLAlchemyUserDatabase = Depends(get_ubuntu_user_db),
        user_check: User = Depends(current_superuser)):
    user_to_create = await user_db.get_by_name(ubuntu_user_create.username)
    if user_check:
        if not user_to_create:
            await add_ub_user(ubuntu_user_create.username, ubuntu_user_create.password)
            new_ubuntu_user = await user_db.create(ubuntu_user_create.dict())

            return {"message": "UbuntuUser created successfully",
                    "username": new_ubuntu_user.username,
                    "user_id": new_ubuntu_user.id
                    }
        else:
            return {"user": f"{ubuntu_user_create.username} already created"}
    else:
        return {"You are not super"}


@crud_ubuntu_user_router.delete('/delete-ub-user')
async def delete_ubuntu_user(
        ubuntu_user_read: UbuntuUserRead,
        user_db: SQLAlchemyUserDatabase = Depends(get_ubuntu_user_db),
        user_check: User = Depends(current_superuser)):
    if user_check:
        user_to_delete = await user_db.get_by_name(ubuntu_user_read.username)
        if user_to_delete:
            await delete_ub_user(ubuntu_user_read.username)
            await user_db.delete(user_to_delete)
            return {"message": f"{ubuntu_user_read.username} deleted"}
        else:
            return {"message": "User not found"}
    else:
        return {"message": "Permission denied"}


@crud_ubuntu_user_router.patch('/update-ub-user')
async def update_ubuntu_user(
        ubuntu_user_update: UbuntuUserUpdate,
        user_db: SQLAlchemyUserDatabase = Depends(get_ubuntu_user_db),
        user_check: User = Depends(current_superuser)):
    if user_check:
        user_to_update = await user_db.get_by_name(ubuntu_user_update.username)
        if user_to_update:
            await update_ub_user(
                ubuntu_user_update.username,
                ubuntu_user_update.new_username,
                ubuntu_user_update.new_password,
            )
            update_data = {
                "username": ubuntu_user_update.new_username,
                "password": ubuntu_user_update.new_password,
            }

            await user_db.update(user_to_update, update_dict=update_data)
            return {"message": f"{ubuntu_user_update.username} updated"}
        else:
            return {"message": "User not found"}
    else:
        return {"message": "Permission denied"}


@crud_ubuntu_user_router.get("/get_all_users")
async def get_all_users(
        user_db: SQLAlchemyUserDatabase = Depends(get_ubuntu_user_db),
        user_check: User = Depends(current_superuser)):
    if user_check:
        users = await user_db.get_all_users()
        return users
    else:
        return {"message": "Permission denied"}

