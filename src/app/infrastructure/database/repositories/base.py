from typing import TypeVar

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta

from app.application.common.pagination import PagePagination

Model = TypeVar('Model', bound=DeclarativeMeta)


class SQLAlchemyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # noinspection PyMethodMayBeStatic
    def _apply_pagination(
        self, statement: Select, pagination: PagePagination, model: Model
    ) -> Select:
        if pagination.order:
            statement = statement.order_by(model.id.asc())
        else:
            statement = statement.order_by(model.id.desc())

        if pagination.offset is not None:
            statement = statement.offset(pagination.offset)

        if pagination.limit is not None:
            statement = statement.limit(pagination.limit)
        return statement
