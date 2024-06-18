from app.services.admin_service import execute_ssh_command_async, connect_to_ssh


async def high_load_processes():
    ssh_connect = await connect_to_ssh()
    data = await execute_ssh_command_async(ssh_connect, "ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6")
    data = data.split('\n')
    correct_data = []
    for element in data:
        if element.strip():
            parts = element.split()
            if len(parts) == 3:
                pid, command, cpu = parts
                correct_data.append({"PID": pid, "COMMAND": command, "%CPU": cpu})
    return correct_data[1:]


async def get_system_load_data():
    ssh_connect = await connect_to_ssh()
    data = await execute_ssh_command_async(ssh_connect, "uptime")
    load_average = data.split('average:')[1].strip()
    load_average_list = [float(avg.strip()) for avg in load_average.split(',')]
    return {
        "load_average": load_average_list,
    }