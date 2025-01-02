from pydantic import ConfigDict

from app.application.common import Schema


class PostSchema(Schema):
    title: str
    text: str
    author: str


class PostCreateSchema(PostSchema):
    pass


class PostDeleteSchema(Schema):
    pass


class PostDetailSchema(PostSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PostUpdate(PostSchema):
    pass


class PostFeedSchema(PostSchema):
    pass
