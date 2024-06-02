import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SSH_HOST=os.getenv("SSH_HOST")
SSH_USER=os.getenv("SSH_USER")
SSH_KEY=os.getenv("SSH_KEY")


SECRET_KEY = os.getenv("SECRET_KEY")

SUDO_PASSWORD = os.getenv("SUDO_PASSWORD")

