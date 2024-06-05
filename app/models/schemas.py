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


# Other

class BackupRequest(BaseModel):
    folders_for_backup: list[str] = ['/etc', '/var', '...']
    dir_for_backup_file: str = "/home/.../backups/"
    temp_script_path: str = "/code/create_script/script.py"
    script_path: str = "/home/.../Scripts/script.py"


class CronScheduleRequest(BaseModel):
    minute: str = "*"
    hour: str = "*"
    day: str = "*"
    month: str = "*"
    day_of_week: str = "*"
    script_type: str = "python3"
    script_path: str = "/home/.../Scripts/script.py"
    comment: str = "##Comma"

