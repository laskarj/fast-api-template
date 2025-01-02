from app.application.common.pagination import PaginatedItems
from app.application.posts.interfaces import IPostsService
from app.application.posts.schemas import (
    PostCreateSchema,
    PostDeleteSchema,
    PostDetailSchema,
    PostFeedSchema,
    PostUpdate,
)
from app.infrastructure.database.repositories import PostsRepository


class PostsService(IPostsService):
    def __init__(self, session) -> None:
        self._session = session
        self._posts_repository = PostsRepository(session)

    async def get_post_detail(self, post_id: int) -> PostDetailSchema:
        post_model = await self._posts_repository.get(post_id)
        post_schema = PostDetailSchema.from_orm(post_model)
        return post_schema

    def get_posts_feed(self) -> PaginatedItems[PostFeedSchema]: ...

    def create_post(self, post: PostCreateSchema) -> PostFeedSchema: ...

    def update_post(self, post_id: int, post: PostUpdate) -> PostDetailSchema: ...

    def delete_post(self, post_id: int) -> PostDeleteSchema: ...
