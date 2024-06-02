from config import SUDO_PASSWORD, SSH_HOST, SSH_USER, SSH_KEY
import asyncssh


async def connect_to_ssh():
    return await asyncssh.connect(SSH_HOST, username=SSH_USER, client_keys=[SSH_KEY], password=SUDO_PASSWORD)


async def execute_ssh_sudo_command_async(conn, command) -> str:
    try:
        full_command = f"echo {SUDO_PASSWORD} | sudo -S {command}"
        result = await conn.run(full_command, check=True)
        return result.stdout
    except asyncssh.Error as e:
        raise Exception(f"Command execution failed: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")
