from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
from crawlee.router import Router
from bs4 import BeautifulSoup
import json
import structlog
import uuid6
from google.cloud import storage

from .utils.bucket_utils import upload_string_to_gcs

logger = structlog.get_logger()

router = Router[BeautifulSoupCrawlingContext]()
storage_client = storage.Client()
bucket = storage_client.bucket("scraper-responses")


def save_to_gcs(content):
    filename = f'{uuid6.uuid8()}.json'
    upload_string_to_gcs(bucket, json.dumps(content), filename)


@router.default_handler
async def default_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    logger.debug('Processing', url={context.request.url})
    http_response = context.http_response
    content = http_response.read() if http_response else None
    if content:
        try:
            content_str = content.decode('utf-8')
            soup = BeautifulSoup(content_str, 'html.parser')
            if soup.find():
                logger.debug('Valid HTML content.')
            else:
                logger.error('Invalid HTML content.')
        except UnicodeDecodeError as e:
            logger.error('Failed to decode content.', error=str(e), url=context.request.url)
        except Exception as e:
            logger.error('An error occurred while parsing HTML content.', error=str(e), url=context.request.url)
    else:
        logger.error('No content fetched.', url=context.request.url)

    scrape_response = {
            'url': context.request.loaded_url,
            'content': content_str if content else None,
        }

    save_to_gcs(scrape_response)

@router.handler('JSON')
async def json_handler(context: BeautifulSoupCrawlingContext) -> None:
    """Default request handler."""
    logger.debug('Processing', url={context.request.url})
    http_response = context.http_response
    try:
        json_content = json.load(http_response)
    except json.JSONDecodeError:
        json_content = None
        logger.error('Invalid JSON content.', url=context.request.url)
    
    # We should save invalid page for debugging

    scrape_response = {
        'metadata': {
            'requested_url': context.request.url,
            'loaded_url': context.request.loaded_url,
            'handled_at': context.request.handled_at,
        },
        'content': json_content if json_content else None
    }

    save_to_gcs(scrape_response)




## TODO images
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