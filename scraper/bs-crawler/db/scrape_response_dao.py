from sqlalchemy.ext.asyncio import AsyncSession
from ..db.scrape_response_model import ScrapeResponse
from ..db.sql_connect import get_db_session
from ..db.dummy_model import DummyModel
import structlog

logger = structlog.get_logger()

class ScrapeResponseDAO:
    # def __init__(self, session: AsyncSession = get_db_session()):
    #     self.session = session

    async def add_scrape_response(self, scrape_response, file_id):
        async for session in get_db_session():
            session.add(DummyModel(name="new test"))
            return
            new_scrape_response = ScrapeResponse(
                file_id=file_id,
                requested_url=scrape_response['metadata']['requested_url'],
                loaded_url=scrape_response['metadata']['loaded_url'],
                building_id=scrape_response['metadata']['building_id'],
                handled_at=scrape_response['metadata']['handled_at'],
                retry_count=scrape_response['metadata']['retry_count'],
            )
            session.add(new_scrape_response)
            logger.debug("Scrape response saved to database.", scrape_response=new_scrape_response)
