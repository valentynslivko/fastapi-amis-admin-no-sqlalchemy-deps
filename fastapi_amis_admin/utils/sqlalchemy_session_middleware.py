from typing import Any

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


class SQLAlchemySessionMiddleware:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def __call__(self, request: Request, call_next) -> Any:
        async with self.async_session() as session:
            async with session.begin():
                request.state.async_session = session
        return await call_next(request)
