from app.services.admin_service import execute_sudo_command_async


async def add_ub_user(username, password):
    await execute_sudo_command_async(f"useradd -N {username}")
    await execute_sudo_command_async(f"echo {username}:{password} | sudo chpasswd")
    return f"User {username} added successfully"


async def delete_ub_user(username):
    await execute_sudo_command_async(f"userdel -r {username}")
    return f"User {username} deleted"


async def update_ub_user(username, new_username, new_password):
    await execute_sudo_command_async(f"sudo usermod -l {new_username} {username}")
    await execute_sudo_command_async(f"echo {new_username}:{new_password} | sudo chpasswd")
    return f"User {username} updated successfully"

