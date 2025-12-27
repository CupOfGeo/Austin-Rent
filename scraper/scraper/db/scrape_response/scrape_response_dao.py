"""Data Access Object for scrape response metadata.

Handles database operations for storing raw scrape response metadata and
linking to GCS-stored content.
"""

from typing import cast

import structlog

from scraper.db.scrape_response.scrape_response_model import ScrapeResponseModel
from scraper.db.sql_connect import get_db_session

logger = structlog.get_logger()


class ScrapeResponseDAO:
    """Data Access Object for scrape_responses table."""

    async def add_scrape_response(self, scrape_response, file_id) -> int:
        """Add a scrape response metadata record to the database.

        Args:
            scrape_response: Dictionary containing metadata and content.
            file_id: UUID of the file saved to GCS.

        Returns:
            int: The scrape_response_id of the inserted record, or -1 on failure.
        """
        async for session in get_db_session():
            try:
                new_scrape_response = ScrapeResponseModel(
                    file_id=file_id,
                    requested_url=scrape_response["metadata"]["requested_url"],
                    loaded_url=scrape_response["metadata"]["loaded_url"],
                    building_id=scrape_response["metadata"]["building_id"],
                    retry_count=scrape_response["metadata"]["retry_count"],
                )
                session.add(new_scrape_response)
                await session.commit()
                # await session.refresh(new_scrape_response)
                return cast(int, new_scrape_response.scrape_response_id)
            except Exception as e:
                logger.error(
                    "Failed to save scrape response to database rolling back commit.",
                    error=str(e),
                )
                await session.rollback()
                # raise e dont raise will cause scrape to retry
        return -1
