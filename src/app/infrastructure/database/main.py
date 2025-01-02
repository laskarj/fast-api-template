from contextlib import asynccontextmanager
from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.infrastructure.config.dto import DatabaseConfig


def make_engine(database_config: DatabaseConfig) -> AsyncEngine:
    engine = create_async_engine(
        url=database_config.full_url,
        echo=database_config.echo,
        echo_pool=database_config.echo_pool,
    )
    return engine


@lru_cache
def make_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_session(session_maker: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with open_db_session(session_maker) as session:
        yield session


@asynccontextmanager
async def open_db_session(
    factory: async_sessionmaker,
) -> AsyncGenerator[AsyncSession, None]:
    session = factory()

    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    else:
        await session.commit()
    finally:
        await session.close()
