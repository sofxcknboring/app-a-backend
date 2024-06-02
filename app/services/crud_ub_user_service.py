from app.services.admin_service import execute_ssh_sudo_command_async, connect_to_ssh


async def add_ub_user(username, password):
    ssh_connect = await connect_to_ssh()
    await execute_ssh_sudo_command_async(ssh_connect, f"useradd -N {username}")
    await execute_ssh_sudo_command_async(ssh_connect, f"echo {username}:{password} | sudo chpasswd")
    return f"User {username} added successfully"


async def delete_ub_user(username):
    ssh_connect = await connect_to_ssh()
    await execute_ssh_sudo_command_async(ssh_connect, f"userdel -r {username}")
    return f"User {username} deleted"


async def update_ub_user(username, new_username, new_password):
    ssh_connect = await connect_to_ssh()
    await execute_ssh_sudo_command_async(ssh_connect, f"sudo usermod -l {new_username} {username}")
    await execute_ssh_sudo_command_async(ssh_connect, f"echo {new_username}:{new_password} | sudo chpasswd")
    return f"User {username} updated successfully"

