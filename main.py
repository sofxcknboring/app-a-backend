from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from app.api.admin import admin_router
from app.api.crud_ubuntu_user import crud_ubuntu_user_router

from fastapi.middleware.cors import CORSMiddleware
from app.db.base import User
from app.models.schemas import UserRead, UserCreate
from app.services.auth_service import get_user_manager
from app.utils.auth_config import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(admin_router)
app.include_router(crud_ubuntu_user_router)


# CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
'''