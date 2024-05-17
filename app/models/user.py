from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP
from datetime import datetime

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


class UbuntuUser(Base):

    __tablename__ = "ubuntu_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    added_at = Column(TIMESTAMP, default=datetime.utcnow)
    password = Column(String(length=1024), nullable=False)
