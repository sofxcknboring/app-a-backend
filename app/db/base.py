from typing import AsyncGenerator, List, Optional
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker
from app.models.user import User, UbuntuUser
from config import DB_USER, DB_HOST, DB_NAME, DB_PORT, DB_PASSWORD

from sqlalchemy import select
from fastapi_users.models import UP

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class UserUbuntuDatabase(SQLAlchemyUserDatabase):
    async def get_by_name(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(self.user_table.username == username)
        return await self._get_user(statement)

    async def get_all_users(self) -> List[UP]:
        statement = select(self.user_table)
        results = await self.session.execute(statement)
        return results.scalars().all()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_ubuntu_user_db(session: AsyncSession = Depends(get_async_session)):
    yield UserUbuntuDatabase(session, UbuntuUser)


