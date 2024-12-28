import structlog
from  typing import List
from scraper.db.sql_connect import get_db_session
from scraper.db.scrape_extraction.extraction_model import ScrapeExtractionModel

logger = structlog.get_logger()

class ScrapeExtractionDAO:
    async def add_extraction(self, extraction: ScrapeExtractionModel):
        async for session in get_db_session():
            async with session.begin():
                session.add(extraction)
                logger.debug("Adding Extraction", extraction_id=extraction.extraction_id)
                return extraction.extraction_id
            

    async def add_extractions(self, extractions: List[ScrapeExtractionModel]):
        async for session in get_db_session():
            async with session.begin():
                try:
                    for extraction in extractions:
                        session.add(extraction)
                    await session.commit()
                    logger.debug("Adding Extraction", scrape_extraction_id=extraction.scrape_extraction_id)
                except Exception as e:
                    logger.error(
                        "Failed to save scrape response to database rolling back commit.",
                        error=str(e),
                    )
                    await session.rollback()
                    raise e
