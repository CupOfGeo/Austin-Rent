from typing import AsyncGenerator

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from scraper.config.settings import settings

logger = structlog.get_logger()
logger.info("Creating database engine", url=str(settings.db_url))
engine = create_async_engine(str(settings.db_url),
            echo=settings.db_echo)

session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def test_connect():
    """
    Test database connection.
    """
    async with session_factory() as session:
        await session.execute(select(1))
        logger.info("Successfully connected to the database")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :yield: database session.
    """
    session: AsyncSession = session_factory()

    try:
        yield session
    finally:
        try:
            await session.commit()
        except Exception as e:
            logger.error(
                "Failed to save scrape response to database rolling back commit.",
                error=str(e),
            )
            await session.rollback()
            raise e
        await session.close()
