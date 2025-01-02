from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.posts.interfaces import IPostsService
from app.infrastructure.implementation.posts import PostsService


def get_posts_service(session: AsyncSession = Depends()) -> IPostsService:
    return PostsService(session)
