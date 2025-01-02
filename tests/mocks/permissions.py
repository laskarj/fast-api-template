from fastapi import Request
from fastapi.security import HTTPBearer


class MockPermissionExample(HTTPBearer):
    async def __call__(self, request: Request) -> None: ...
