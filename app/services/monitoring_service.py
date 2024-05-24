import psutil
from app.services.admin_service import execute_command


async def high_load_processes():
    data = await execute_command("ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6")
    data = data.split('\n')
    correct_data = []
    for element in data:
        if element.strip():
            parts = element.split()
            if len(parts) == 3:
                pid, command, cpu = parts
                correct_data.append({"PID": pid, "COMMAND": command, "%CPU": cpu})
    return correct_data[1:]


async def monitor_resources_activity():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return {
        '%CPU': cpu_usage,
        '%Memory': memory_usage,
        '%Disk': disk_usage,
    }

