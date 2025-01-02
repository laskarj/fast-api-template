from abc import ABC, abstractmethod

from app.application.posts.schemas import PostCreateSchema, PostUpdate


class IPostsService(ABC):
    @abstractmethod
    async def get_post_detail(self, post_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_posts_feed(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create_post(self, post: PostCreateSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_post(self, post_id: int, post: PostUpdate) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_post(self, post_id: int) -> None:
        raise NotImplementedError
