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

