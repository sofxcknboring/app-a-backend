from crontab import CronTab


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
    cron = CronTab(user=True)
    command = f"/usr/bin/python3 {script_path}"
    job = cron.new(command=command)
    job.setall(f'{minute} {hour} {day} {month} {day_of_week}')
    cron.write()
    return {
        "schedule": f'{minute} {hour} {day} {month} {day_of_week} /user/bin/python3 {script_path}',
        "status": f'GOOD'}

