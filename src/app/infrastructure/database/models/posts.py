from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models.base import BaseModel
from app.infrastructure.database.types.postgres import INT_PRIMARY_KEY


class Post(BaseModel):
    __tablename__ = 'posts'

    id: Mapped[INT_PRIMARY_KEY]
    title: Mapped[str] = mapped_column(String(64))
    text: Mapped[str] = mapped_column(String(64))
    author: Mapped[str] = mapped_column(String(64))
