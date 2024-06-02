from crontab import CronTab
import asyncssh
from app.services.admin_service import connect_to_ssh, execute_ssh_sudo_command_async


def generate_backup_script(backup_folders: list[str], backup_dir: str) -> str:
    script_content = f"""
import os
import tarfile
from datetime import datetime

BACKUP_FOLDERS = {backup_folders}
BACKUP_DIR = '{backup_dir}'

def create_backup():
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
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


async def cron_schedule_backup(script_path, minute, hour, day, month, day_of_week):
    command = f"/usr/bin/python3 {script_path}"

    try:
        conn = await connect_to_ssh()
        current_crontab = await execute_ssh_sudo_command_async(conn, "crontab -l")
        cron = CronTab(tab=current_crontab)

        existing_jobs = cron.find_command(command)
        if not existing_jobs:
            job = cron.new(command=command)
            job.setall(minute, hour, day, month, day_of_week)

            updated_crontab = str(cron)

            temp_cron_path = "/tmp/temp_cron"
            async with conn.start_sftp_client() as sftp:
                async with sftp.open(temp_cron_path, 'w') as temp_cron_file:
                    await temp_cron_file.write(updated_crontab)

            await execute_ssh_sudo_command_async(conn, f"crontab {temp_cron_path}")
            await execute_ssh_sudo_command_async(conn, f"rm {temp_cron_path}")

            return {
                "schedule": f'{minute} {hour} {day} {month} {day_of_week} {command}',
                "status": "GOOD"
            }
        else:
            return {
                "schedule": f'{minute} {hour} {day} {month} {day_of_week} {command}',
                "status": "ALREADY_EXISTS"
            }
    except asyncssh.Error as e:
        raise Exception(f"SSH connection or command execution failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")





