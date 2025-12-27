"""
Routes for the scraper.

For now out of convenient and speed well just do the extraction here.
It should go to extractor in the future -
    This will enable reprocessing of the data
    and also allow us to have different scrapers if we wanted to start using vendors
"""

import json

import structlog
import uuid6
from bs4 import BeautifulSoup
from crawlee.crawlers import BeautifulSoupCrawlingContext
from crawlee.router import Router
from google.cloud import storage  # type: ignore[attr-defined]

from scraper.db.scrape_extraction.extraction_dao import ScrapeExtractionDAO
from scraper.db.scrape_extraction.extraction_model import ScrapeExtractionModel
from scraper.db.scrape_response.scrape_response_dao import ScrapeResponseDAO
from scraper.utils.bucket_utils import upload_string_to_gcs

logger = structlog.get_logger()
router = Router[BeautifulSoupCrawlingContext]()

storage_client = storage.Client()
bucket = storage_client.bucket("scraper-responses")
dao = ScrapeResponseDAO()
extractor_dao = ScrapeExtractionDAO()


def save_to_gcs(content, building_id):
    """Save scraped content to Google Cloud Storage bucket.

    Args:
        content: The scraped content to save (will be JSON serialized).
        building_id: The ID of the building being scraped.

    Returns:
        UUID: The generated file ID for the saved content.
    """
    file_id = uuid6.uuid8()
    filename = f"{file_id}.json"
    upload_string_to_gcs(bucket, json.dumps(content), filename, building_id)
    return file_id


async def save_scrape_response(context: BeautifulSoupCrawlingContext, cleaned_content):
    """Save scrape response metadata and content to GCS and database.

    Args:
        context: The Crawlee crawling context containing request metadata.
        cleaned_content: The cleaned content to save (HTML or JSON).

    Note:
        Does not raise exceptions on failure to prevent Crawlee retries.
    """
    building_id = context.request.user_data.get("building_id")
    scrape_response = {
        "metadata": {
            "requested_url": context.request.url,
            "loaded_url": context.request.loaded_url,
            "building_id": building_id,
            "retry_count": context.request.retry_count,
        },
        "content": cleaned_content,
    }
    try:
        file_id = save_to_gcs(scrape_response, building_id)
        await dao.add_scrape_response(scrape_response, file_id)
        logger.info(
            "Scrape response saved to GCP.",
            url={context.request.url},
            building_id=building_id,
            file_id=file_id,
        )
    except Exception as e:
        # We won't raise an error bc then crawlee will retry the request.
        logger.error(
            "Failed to save scrape response to GCP.",
            url={context.request.url},
            building_id=building_id,
            error=str(e),
        )


@router.default_handler
async def default_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    building_id = context.request.user_data.get("building_id")
    logger.info("PASSING", url={context.request.url}, building_id=building_id)


@router.handler("HTML")
async def html_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    building_id = context.request.user_data.get("building_id")
    logger.info("Handling", url={context.request.url}, building_id=building_id)
    http_response = context.http_response
    # In crawlee v1.x, http_response.read() is async
    content = await http_response.read() if http_response else None
    if content:
        try:
            content_str = content.decode("utf-8")
            # BeautifulSoup will fixes invalid HTML
            if content_str == str(BeautifulSoup(content_str, "html.parser")):
                logger.error("Invalid HTML content.")
                raise Exception("Invalid HTML content.")
            logger.debug("Valid HTML content.")
        except Exception as e:
            logger.error(
                "An error occurred while parsing HTML content.",
                error=str(e),
                url=context.request.url,
            )
            raise e
    else:
        # Not sure if none content is already handled by crawlee doesn't hurt to have it here
        logger.error("No content fetched.", url=context.request.url)
        raise Exception("No content fetched.")

    # title = await context.page.locator('.product-meta h1').text_content()
    await save_scrape_response(context, content_str)


def parse_sight_map_content(json_content, building_id) -> list:
    """Parse sight map content."""
    units = json_content.get("content").get("data").get("units")
    extractions = []
    for unit in units:
        extraction = ScrapeExtractionModel(
            building_id=building_id,
            scrape_page_id=unit.get("id"),
            unit_number=unit.get("name"),
            bed_count=unit.get("bedrooms"),
            bath_count=unit.get("bathrooms"),
            sqft=unit.get("sqft"),
            base_rent=unit.get("rent"),
            available=unit.get("availability"),
            additional_attributes=unit,
        )
        extractions.append(extraction)
    return extractions


@router.handler("JSON")
async def json_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    building_id = context.request.user_data.get("building_id")
    logger.info("Handling", url={context.request.url}, building_id=building_id)
    http_response = context.http_response
    try:
        # In crawlee v1.x, http_response.read() is async
        response_bytes = await http_response.read()
        response_text = response_bytes.decode("utf-8")
        json_content = json.loads(response_text)
    except json.JSONDecodeError:
        json_content = None
        logger.error("Invalid JSON content.", url=context.request.url)
    # We should save invalid page for debugging?
    # They get saved in the logs maybe future we pump them to a bad_responses bucket?
    await save_scrape_response(context, json_content)

    # atm all json extractions are sight map
    extractions = parse_sight_map_content(json_content, building_id)
    await extractor_dao.add_extractions(extractions)
    logger.info(
        "Extraction saved to database.",
    )
