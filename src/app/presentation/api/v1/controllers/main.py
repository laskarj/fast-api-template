from fastapi import FastAPI

from .posts import router as posts_router


def setup(app: FastAPI):
    app.include_router(posts_router)
