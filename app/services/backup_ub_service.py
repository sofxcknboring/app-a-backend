from app.services.admin_service import connect_to_ssh, execute_ssh_command_async, execute_ssh_sudo_command_async
import asyncssh
from typing import Dict
from config import SSH_USER


def generate_backup_script(folders_for_backup, dir_for_backup_file) -> str:
    script_content = f"""
import os
import tarfile
from datetime import datetime

BACKUP_FOLDERS = {folders_for_backup}
BACKUP_DIR = '{dir_for_backup_file}'

def create_backup():
    current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    backup_name = f"backup_{{current_time}}.tar.gz"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    with tarfile.open(backup_path, "w:gz") as tar:
        for folder in BACKUP_FOLDERS:
            tar.add(folder, arcname=os.path.basename(folder))

    return backup_path

if __name__ == "__main__":
    backup_path = create_backup()
    print(f"Backup created at: {{backup_path}}")
"""
    return script_content


async def all_scripts() -> Dict[int, str]:
    conn = await connect_to_ssh()
    try:
        scripts = await execute_ssh_command_async(conn, f"cd /home/{SSH_USER}/Scripts/ && ls")
        scripts_list = [elem for elem in scripts.split('\n') if "." in elem]
        if not scripts_list:
            return {1: 'Folder is empty'}
        else:
            return {idx + 1: script for idx, script in enumerate(scripts_list)}
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


async def cron_schedule_backup(minute, hour, day, month, day_of_week, script_type,script_path, comment=""):
    try:
        conn = await connect_to_ssh()
        crontab_content = await execute_ssh_command_async(conn, 'crontab -l')
        crontab_list = crontab_content.splitlines()

        if comment != "":
            crontab_list.append(f"## {comment}")
        crontab_list.append(f"{minute} {hour} {day} {month} {day_of_week} {script_type} {script_path}")

        new_crontab_content = "\n".join(crontab_list) + "\n"

        try:
            temp_cron_path = "/tmp/temp_cron"
            async with conn.start_sftp_client() as sftp:
                async with sftp.open(temp_cron_path, 'w') as temp_cron_file:
                    await temp_cron_file.write(new_crontab_content)
        except Exception as e:
            raise Exception(f"Failed to write to temporary cron file: {str(e)}")
        try:
            await execute_ssh_command_async(conn, f"sh -c 'crontab < {temp_cron_path}'")
        except Exception as e:
            raise Exception(f"Failed to update crontab: {str(e)}")
        try:
            await execute_ssh_command_async(conn, f"rm {temp_cron_path}")
        except Exception as e:
            raise Exception(f"Failed to delete temporary cron file: {str(e)}")

        return {
            "schedule": f'{minute} {hour} {day} {month} {day_of_week} {script_type} {script_path}',
            "status": "UPDATED"
        }

    except asyncssh.Error as e:
        raise Exception(f"SSH connection or command execution failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")






