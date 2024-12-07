import structlog
from ..config.settings import settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

logger = structlog.get_logger()

engine = create_async_engine(settings.db_url, echo=True)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = session_factory()

    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error("Failed to save scrape response to database.", error=str(e))
        raise e
    finally:
        await session.close()
