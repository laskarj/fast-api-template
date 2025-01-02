from asyncio import DefaultEventLoopPolicy
import os
from typing import AsyncGenerator, Generator
from urllib.parse import urlparse

from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from fastapi import FastAPI
import pytest
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer  # type: ignore[import-untyped]

from app.infrastructure.config import AppConfig, Config, DatabaseConfig


@pytest.fixture(scope='session')
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer('postgres:15-alpine')
    if os.name == 'nt':  # Note: from testcontainers/testcontainers-python#108
        postgres.get_container_host_ip = lambda: 'localhost'
    try:
        postgres.start()
        connection_url = postgres.get_connection_url().replace('psycopg2', 'psycopg')
        yield connection_url
    finally:
        postgres.stop()


@pytest.fixture(scope='session')
def app_config() -> AppConfig:
    return AppConfig(
        secret_key='your_secret_key', host='5001', port=8000, project_name='Test Project'
    )


@pytest.fixture(scope='session')
def database_config(postgres_url: str) -> DatabaseConfig:
    parsed_url = urlparse(postgres_url)

    host = parsed_url.hostname
    port = parsed_url.port
    user = parsed_url.username
    password = parsed_url.password
    database = parsed_url.path.lstrip('/')

    return DatabaseConfig(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        echo=True,
        echo_pool=True,
    )


@pytest.fixture(scope='session')
def config(
    app_config: AppConfig,
    database_config: DatabaseConfig,
) -> Config:
    return Config(
        app_config=app_config,
        database_config=database_config,
    )


@pytest.fixture(scope='session')
async def app(config: Config) -> FastAPI:
    from app.presentation.api.v1 import init_app

    app = init_app(config)
    yield app


@pytest.fixture(scope='session')
def alembic_config(database_config: DatabaseConfig) -> AlembicConfig:
    config = AlembicConfig('alembic.ini')
    config.set_main_option('sqlalchemy.url', database_config.full_url)
    return config


@pytest.fixture(scope='session', autouse=True)
def upgrade_database_schema(
    alembic_config: AlembicConfig,
) -> Generator[None, None, None]:
    upgrade(alembic_config, 'head')
    yield
    downgrade(alembic_config, 'base')


@pytest.fixture(scope='session', params=(DefaultEventLoopPolicy(),))
def event_loop_policy(request):
    return request.param


@pytest.fixture(scope='session')
def engine(postgres_url: str) -> AsyncEngine:
    return create_async_engine(url=postgres_url)


@pytest.fixture(scope='function')
async def session(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    connection = await engine.connect()
    transaction = await connection.begin()

    session_factory = async_sessionmaker(connection, expire_on_commit=False)

    session = session_factory()

    try:
        yield session
    finally:
        await transaction.rollback()
        await session.close()
        await connection.close()
