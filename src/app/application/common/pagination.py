from enum import auto, StrEnum
from typing import Generic, TypeVar

from app.application.common.schemas import Schema

Item = TypeVar('Item')


class SortOrder(StrEnum):
    DESC = auto()
    ASC = auto()


class PagePagination(Schema):
    per_page: int | None = None
    page: int | None = None
    order: SortOrder = SortOrder.ASC

    @property
    def limit(self) -> int:
        return self.per_page

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class PagePaginationResult(Schema):
    per_page: int
    page: int
    order: SortOrder
    total: int

    @classmethod
    def build_result_pagination(
        cls,
        pagination: PagePagination,
        total: int,
    ) -> 'PagePaginationResult':
        return cls(
            per_page=pagination.per_page,
            page=pagination.page,
            order=pagination.order,
            total=total,
        )


class PaginatedItems(Schema, Generic[Item]):
    pagination: PagePaginationResult
    data: list[Item]
