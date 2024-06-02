import psutil
from app.services.admin_service import execute_ssh_sudo_command_async, connect_to_ssh


async def high_load_processes():
    ssh_connect = await connect_to_ssh()
    data = await execute_ssh_sudo_command_async(ssh_connect, "ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6")
    data = data.split('\n')
    correct_data = []
    for element in data:
        if element.strip():
            parts = element.split()
            if len(parts) == 3:
                pid, command, cpu = parts
                correct_data.append({"PID": pid, "COMMAND": command, "%CPU": cpu})
    return correct_data[1:]


