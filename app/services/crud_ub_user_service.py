from app.services.admin_service import execute_ssh_sudo_command_async, connect_to_ssh


async def add_ub_user(username, password):
    ssh_connect = await connect_to_ssh()
    try:
        await (execute_ssh_sudo_command_async(
            ssh_connect,
            f"useradd -N {username} && echo '{username}:{password}' | sudo chpasswd"
        ))
    except Exception as e:
        raise Exception(f"{e}")
    return f"User {username} added successfully"


async def delete_ub_user(username):
    ssh_connect = await connect_to_ssh()
    await execute_ssh_sudo_command_async(ssh_connect, f"userdel -r {username}")
    return f"User {username} deleted"


async def update_ub_user(username, new_username, new_password):
    ssh_connect = await connect_to_ssh()
    await execute_ssh_sudo_command_async(
        ssh_connect,
        f"usermod -l {new_username} {username} && echo {new_username}:{new_password} | sudo chpasswd"
    )
    return f"User {username} updated successfully"

