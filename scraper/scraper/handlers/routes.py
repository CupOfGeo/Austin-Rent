"""
Routes for the scraper.

For now out of convenient and speed well just do the extraction here. It should go to extractor in the future -
    This will enable reprocessing of the data
    and also allow us to have different scrapers if we wanted to start using vendors
"""
import structlog
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
from crawlee.router import Router
from google.cloud import storage

from scraper.db.scrape_response.scrape_response_dao import ScrapeResponseDAO
from scraper.db.scrape_extraction.extraction_dao import ScrapeExtractionDAO
from scraper.handlers.html_handler import html_validate, html_extract
from scraper.handlers.json_handler import json_validate, json_extract
from scraper.handlers.handler_utils import HandlerDependencies

logger = structlog.get_logger()
router = Router[BeautifulSoupCrawlingContext]()

# thought about using a singleton and passing it around to handlers?
# class RouterSingleton:
#     _instance = None
#     @classmethod
#     def get_router(cls):
#         if cls._instance is None:
#             cls._instance = Router[BeautifulSoupCrawlingContext]()
#         return cls._instance
# router = RouterSingleton.get_router()

deps = HandlerDependencies(
    storage.Client().bucket("scraper-responses"), 
    ScrapeResponseDAO(), 
    ScrapeExtractionDAO())

@router.default_handler
async def default_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    building_id = context.request.user_data.model_extra.get("building_id")
    logger.info("PASSING", url={context.request.url}, building_id=building_id)


@router.handler("HTML")
async def html_handler(context: BeautifulSoupCrawlingContext) -> None:
    building_id = context.request.user_data.model_extra.get("building_id")
    clean_content = await html_validate(context, building_id)
    if clean_content:
        scrape_response_id = await deps.save_scrape_response(context.request, clean_content)
        if scrape_response_id:
            pass
            # extraction = await html_extract(context, scrape_response_id, building_id)
            # await deps.extractor_dao.add_extractions(extraction)


@router.handler("JSON")
async def json_handler(context: BeautifulSoupCrawlingContext) -> None:
    building_id = context.request.user_data.model_extra.get("building_id")
    clean_content = await json_validate(context)
    if clean_content:
        # We should save invalid page for debugging?
        # They get saved in the logs maybe future we pump them to a bad_responses bucket?
        scrape_response_id = await deps.save_scrape_response(context.request, clean_content)
        if scrape_response_id:
            try:
                extractions = await json_extract(clean_content, building_id, scrape_response_id)
                await deps.extractor_dao.add_extractions(extractions)
                logger.info("Extraction saved to database.", )
            except Exception as e:
                logger.error("Failed to save extractions to database.", error=str(e))
                # dont raise error or it will retry to scrape the page just log it



