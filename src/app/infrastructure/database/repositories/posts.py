from sqlalchemy import select

from app.infrastructure.database.models import PostModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository):
    async def get(self, id: int) -> PostModel:
        statement = select(PostModel).where(PostModel.id == id)
        return await self.session.scalar(statement)
