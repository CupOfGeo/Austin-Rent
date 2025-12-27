"""Data Access Object for scrape extractions.

Handles database operations for storing structured rental unit data
extracted from scrape responses.
"""

from typing import List

import structlog

from scraper.db.scrape_extraction.extraction_model import ScrapeExtractionModel
from scraper.db.sql_connect import get_db_session

logger = structlog.get_logger()


class ScrapeExtractionDAO:
    """Data Access Object for scrape_extractions table."""

    async def add_extraction(self, extraction: ScrapeExtractionModel):
        """Add a single extraction record to the database.

        Args:
            extraction: The extraction model to persist.

        Returns:
            The extraction_id of the inserted record.
        """
        async for session in get_db_session():
            async with session.begin():
                session.add(extraction)
                logger.debug(
                    "Adding Extraction", extraction_id=extraction.scrape_extraction_id
                )
                return extraction.scrape_extraction_id

    async def add_extractions(self, extractions: List[ScrapeExtractionModel]):
        """Add multiple extraction records to the database in a single transaction.

        Args:
            extractions: List of extraction models to persist.

        Raises:
            Exception: If the transaction fails, rolls back and re-raises.
        """
        async for session in get_db_session():
            async with session.begin():
                try:
                    for extraction in extractions:
                        session.add(extraction)
                    await session.commit()
                    logger.debug(
                        "Adding Extraction",
                        scrape_extraction_id=extraction.scrape_extraction_id,
                    )
                except Exception as e:
                    logger.error(
                        "Failed to save scrape response to database rolling back commit.",
                        error=str(e),
                    )
                    await session.rollback()
                    raise e
