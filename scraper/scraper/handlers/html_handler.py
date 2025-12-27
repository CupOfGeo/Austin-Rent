"""HTML handler for validating and extracting data from HTML responses."""

import structlog
from bs4 import BeautifulSoup
from crawlee.crawlers import BeautifulSoupCrawlingContext

from scraper.db.scrape_extraction.extraction_model import ScrapeExtractionModel

logger = structlog.get_logger()


async def html_validate(context: BeautifulSoupCrawlingContext, building_id: int) -> str:
    """Validate HTML content from the HTTP response.

    Args:
        context: The crawling context containing the HTTP response.
        building_id: The building ID for logging.

    Returns:
        The validated HTML content as a string.

    Raises:
        Exception: If no content is fetched or HTML is invalid.
    """
    logger.info("Validating", url={context.request.url}, building_id=building_id)
    http_response = context.http_response
    # In crawlee v1.x, http_response.read() is async
    content = await http_response.read() if http_response else None
    if content:
        try:
            content_str = content.decode("utf-8")
            # BeautifulSoup will fixes invalid HTML
            if content_str == str(BeautifulSoup(content_str, "html.parser")):
                logger.error("Invalid HTML content.")
                raise ValueError("Invalid HTML content.")
            logger.debug("Valid HTML content.")
        except Exception as e:
            logger.error(
                "An error occurred while parsing HTML content.",
                error=str(e),
                url=context.request.url,
            )
            raise e
        return content_str
    # Not sure if none content is already handled by crawlee doesn't hurt to have it here
    logger.error("No content fetched.", url=context.request.url)
    raise RuntimeError("No content fetched.")


async def html_extract(
    context: BeautifulSoupCrawlingContext, scrape_response_id: int, building_id: int
) -> list[ScrapeExtractionModel]:
    """Extract structured data from HTML content.

    Args:
        context: The crawling context containing the parsed HTML.
        scrape_response_id: The ID of the saved scrape response.
        building_id: The building ID for the extraction.

    Returns:
        List of ScrapeExtractionModel objects with extracted data.
    """
    logger.info(
        "Extracting", scrape_response_id=scrape_response_id, building_id=building_id
    )
    # TODO: Implement actual HTML extraction logic.
    # These are hardcoded rules but if you wanted to scale to do more page types
    # we would implement a rule based system. {css_selector, regex, ....} as a db row
    # then manage a db of rules over changing code.
    soup = context.soup
    title_tag = soup.select_one(".product-meta h1")
    title = title_tag.get_text() if title_tag else None
    logger.debug("Extracted title", title=title)
    return [
        ScrapeExtractionModel(
            building_id=building_id,
            scrape_response_id=scrape_response_id,
            unit_number=title,
        )
    ]
