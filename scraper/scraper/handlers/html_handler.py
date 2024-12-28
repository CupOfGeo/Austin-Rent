import structlog
from bs4 import BeautifulSoup
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
from scraper.db.scrape_extraction.extraction_model import ScrapeExtractionModel

logger = structlog.get_logger()

async def html_validate(context: BeautifulSoupCrawlingContext, building_id: int) -> str:
    logger.info("Validating", url={context.request.url}, building_id=building_id)
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

    return content_str


async def html_extract(context: BeautifulSoupCrawlingContext, scrape_response_id:int, building_id: int) -> ScrapeExtractionModel:
    logger.info("Extracting", scrape_response_id=scrape_response_id, building_id=building_id)
    building_id = context.request.user_data.model_extra.get("building_id")
    # these are hardcoded rules but if you wanted to scale to do more page types
    # we would implement a rule bases system. {css_selector, regex, ....} as a db row 
    # then manage a db of rules over changing code.
    title = await context.page.locator('.product-meta h1').text_content()
    return [ScrapeExtractionModel(scrape_response_id, title)]
    