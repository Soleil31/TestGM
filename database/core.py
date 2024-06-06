from sqlalchemy.ext.asyncio import create_async_engine

from settings.loader import PG_CONNECTION_URL


engine = create_async_engine(
    PG_CONNECTION_URL,
    echo=True
)
