import json

import structlog
import uuid6
from bs4 import BeautifulSoup
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
from crawlee.router import Router
from google.cloud import storage

from scraper.db.scrape_response.scrape_response_dao import ScrapeResponseDAO
from scraper.utils.bucket_utils import upload_string_to_gcs  # , get_bucket

logger = structlog.get_logger()
router = Router[BeautifulSoupCrawlingContext]()
storage_client = storage.Client()
bucket = storage_client.bucket("scraper-responses")
dao = ScrapeResponseDAO()


def save_to_gcs(content, building_id):
    # get_bucket = storage_client.bucket("scraper-responses")
    file_id = uuid6.uuid8()
    filename = f"{file_id}.json"
    upload_string_to_gcs(bucket, json.dumps(content), filename, building_id)
    return file_id


async def save_scrape_response(context: BeautifulSoupCrawlingContext, cleaned_content):
    building_id = context.request.user_data.model_extra.get("building_id")
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


# @router.default_handler()
@router.handler("HTML")
async def html_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    building_id = context.request.user_data.model_extra.get("building_id")
    logger.info("Processing", url={context.request.url}, building_id=building_id)
    http_response = context.http_response
    content = http_response.read() if http_response else None
    if content:
        try:
            content_str = content.decode("utf-8")
            # BeautifulSoup will fixes invalid HTML
            if content_str == str(BeautifulSoup(content_str, "html.parser")):
                logger.error("Invalid HTML content.")
                raise Exception("Invalid HTML content.")
            else:
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

    await save_scrape_response(context, content_str)


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
    # They get saved in the logs maybe future we pump them to a bad_responses bucket?
    await save_scrape_response(context, json_content)


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
