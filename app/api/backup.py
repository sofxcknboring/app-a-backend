from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
import aiofiles
import os
import asyncssh
from app.models.schemas import BackupRequest, CronScheduleRequest
from app.models.user import User
from app.services.auth_service import get_user_manager
from app.utils.auth_config import auth_backend

from app.services.backup_ub_service import generate_backup_script, cron_schedule_backup
from app.services.admin_service import execute_ssh_sudo_command_async, connect_to_ssh

backup_ub_router = APIRouter(prefix='/backup_ubuntu', tags=["Backup_ubuntu"])

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


@backup_ub_router.post("/create_backup_script/")
async def create_backup_script(request: BackupRequest):
    script_content = generate_backup_script(request.backup_folders, request.backup_dir)

    async with aiofiles.open(request.temp_script_path, "w") as script_file:
        await script_file.write(script_content)

    ssh_connect = await connect_to_ssh()
    try:
        await execute_ssh_sudo_command_async(ssh_connect, f"mkdir -p $(dirname {request.script_path})")
        async with ssh_connect.start_sftp_client() as sftp:
            await sftp.put(request.temp_script_path, request.script_path)
            await execute_ssh_sudo_command_async(ssh_connect, f"chmod +x {request.script_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading script to server: {str(e)}")
    finally:
        os.remove(request.temp_script_path)
    return {"script_path": request.script_path}


@backup_ub_router.post("/schedule_backup/")
async def api_schedule_backup(
    request: CronScheduleRequest,
):
    response = await cron_schedule_backup(
        request.script_path,
        request.minute,
        request.hour,
        request.day,
        request.month,
        request.day_of_week,
    )
    return response
