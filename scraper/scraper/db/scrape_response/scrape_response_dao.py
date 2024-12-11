import structlog

from scraper.db.scrape_response.scrape_response_model import ScrapeResponse
from scraper.db.sql_connect import get_db_session

logger = structlog.get_logger()


class ScrapeResponseDAO:

    async def add_scrape_response(self, scrape_response, file_id):
        async for session in get_db_session():
            new_scrape_response = ScrapeResponse(
                file_id=file_id,
                requested_url=scrape_response["metadata"]["requested_url"],
                loaded_url=scrape_response["metadata"]["loaded_url"],
                building_id=scrape_response["metadata"]["building_id"],
                retry_count=scrape_response["metadata"]["retry_count"],
            )
            session.add(new_scrape_response)
