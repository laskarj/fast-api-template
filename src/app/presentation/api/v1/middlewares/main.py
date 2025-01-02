from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.presentation.api.v1.middlewares.request_context import RequestContextMiddleware


def setup(app: FastAPI) -> None:
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
