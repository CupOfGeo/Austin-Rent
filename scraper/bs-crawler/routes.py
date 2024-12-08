import json

import structlog
import uuid6
from bs4 import BeautifulSoup
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
from crawlee.router import Router
from google.cloud import storage

from .db.scrape_response.scrape_response_dao import ScrapeResponseDAO
from .utils.bucket_utils import upload_string_to_gcs

logger = structlog.get_logger()
router = Router[BeautifulSoupCrawlingContext]()
storage_client = storage.Client()
bucket = storage_client.bucket("scraper-responses")
dao = ScrapeResponseDAO()


def save_to_gcs(content, building_id):
    file_id = uuid6.uuid8()
    filename = f"{file_id}.json"
    upload_string_to_gcs(bucket, json.dumps(content), filename, building_id)
    return file_id


@router.handler("HTML")
async def default_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    building_id = context.request.user_data.model_extra.get("building_id")
    logger.info("Processing", url={context.request.url}, building_id=building_id)
    http_response = context.http_response
    content = http_response.read() if http_response else None
    if content:
        try:
            content_str = content.decode("utf-8")
            soup = BeautifulSoup(content_str, "html.parser")
            if soup.find():
                logger.debug("Valid HTML content.")
            else:
                logger.error("Invalid HTML content.")
        except Exception as e:
            logger.error(
                "An error occurred while parsing HTML content.",
                error=str(e),
                url=context.request.url,
            )
    else:
        # Not sure if this is already handled by crawlee doesn't hurt to have it here
        logger.error("No content fetched.", url=context.request.url)
        raise Exception("No content fetched.")

    scrape_response = {
        "metadata": {
            "requested_url": context.request.url,
            "loaded_url": context.request.loaded_url,
            "building_id": building_id,
            "handled_at": context.request.handled_at,
            "retry_count": context.request.retry_count,
        },
        "content": content_str if content_str else None,
    }
    try:
        file_id = save_to_gcs(scrape_response, building_id)
        await dao.add_scrape_response(scrape_response, file_id)
    except Exception as e:
        logger.error("Failed to save scrape response to GCP.", error=str(e))


@router.handler("JSON")
async def json_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    building_id = context.request.user_data.model_extra.get("building_id")
    logger.info("Processing", url={context.request.url}, building_id=building_id)
    http_response = context.http_response
    try:
        json_content = json.load(http_response)
    except json.JSONDecodeError:
        json_content = None
        logger.error("Invalid JSON content.", url=context.request.url)
    # We should save invalid page for debugging?
    # They get saved in the logs maybe we pump them to a bad_responses bucket

    scrape_response = {
        "metadata": {
            "requested_url": context.request.url,
            "loaded_url": context.request.loaded_url,
            "building_id": building_id,
            "handled_at": context.request.handled_at,
            "retry_count": context.request.retry_count,
        },
        "content": json_content if json_content else None,
    }
    try:
        file_id = save_to_gcs(scrape_response, building_id)
        await dao.add_scrape_response(scrape_response, file_id)
    except Exception as e:
        logger.error(
            "Failed to save scrape response to GCP.",
            url={context.request.url},
            building_id=building_id,
            error=str(e),
        )
    logger.info(
        "Scrape response saved to GCP.",
        url={context.request.url},
        building_id=building_id,
        file_id=file_id,
    )


# TODO images
# @router.handler('BYTES')
# async def bytes_handler(context: BeautifulSoupCrawlingContext) -> None:
#     """Default request handler."""
#     context.log.info(f'Processing {context.request.url} ...')
#     http_response = context.http_response
#     content = http_response.read() if http_response else None

#     await context.push_data(
#         {
#             'url': context.request.loaded_url,
#             'response': content if http_response else None,
#         }
#     )

#     await context.enqueue_links()
