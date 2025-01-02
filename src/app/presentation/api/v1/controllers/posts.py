from fastapi import APIRouter, Depends

from app.application.posts.interfaces import IPostsService
from app.application.posts.schemas import PostDetailSchema

router = APIRouter(tags=['Posts'], prefix='/posts')


@router.get('/')
async def post_detail(
    post_id: int, posts_service: IPostsService = Depends()
) -> PostDetailSchema:
    return await posts_service.get_post_detail(post_id)
