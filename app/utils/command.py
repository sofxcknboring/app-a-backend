import asyncio
import psutil


async def execute_command(command):
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True)

        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            return stdout.decode()
        else:
            return f"Failed to execute command: {stderr.decode()}"
    except Exception as e:
        return f"An error occurred: {e}"


async def get_ubuntu_users():
    user_list = await execute_command("cut -d: -f1 /etc/passwd")
    return user_list.split("\n")


async def monitor_resources_and_activity():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return {
        'CPU': cpu_usage,
        'Memory': memory_usage,
        'Disk': disk_usage,
    }

