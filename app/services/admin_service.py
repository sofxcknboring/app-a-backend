from config import SUDO_PASSWORD
import asyncio


async def execute_sudo_command_async(command):
    full_command = f"echo {SUDO_PASSWORD} | sudo -S {command}"
    process = await asyncio.create_subprocess_shell(
        full_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command '{command}' failed with error: {stderr.decode()}")
    return stdout.decode()


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

