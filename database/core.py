from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from settings.loader import PG_CONNECTION_URL


engine = create_async_engine(PG_CONNECTION_URL)


AsyncSessionManager = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
