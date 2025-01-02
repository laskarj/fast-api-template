from functools import partial
from typing import Callable, TypeVar

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.application.posts.interfaces import IPostsService
from app.infrastructure.config.dto import Config
from app.infrastructure.database.main import get_session, make_engine, make_session_maker
from app.presentation.api.v1.providers.posts import get_posts_service

Dependency = TypeVar('Dependency')


def register_provider(
    app: FastAPI,
    dependency: Dependency,
    provider: Callable[..., Dependency],
    *args,
    **kwargs,
) -> None:
    app.dependency_overrides[dependency] = partial(provider, *args, **kwargs)


def setup(app: FastAPI, config: Config) -> None:
    db_engine: AsyncEngine = make_engine(config.database_config)
    session_maker = make_session_maker(db_engine)

    register_provider(app, AsyncSession, get_session, session_maker)
    register_provider(app, IPostsService, get_posts_service)
