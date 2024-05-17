from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr

# Register schemas:


class UserRead(schemas.BaseUser[int]):
    name: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(UserRead):
    password: str


class UserUpdate(UserCreate):
    pass


# UbuntuUser schemas:


class UbuntuUserRead(BaseModel):
    username: str


class UbuntuUserCreate(UbuntuUserRead):
    password: str


class UbuntuUserUpdate(UbuntuUserRead):
    new_username: str
    new_password: str

