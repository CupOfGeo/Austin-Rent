"""Main crawler entry point for the scraper service.

Initializes and runs the BeautifulSoupCrawler with configured handlers to scrape
rental data from apartment buildings. Handles logging setup and database connectivity.
"""

from crawlee.configuration import Configuration
from crawlee.crawlers import BeautifulSoupCrawler

from scraper.buildings import buildings
from scraper.config.logging import configure_logging
from scraper.config.settings import settings
from scraper.db.sql_connect import test_connect
from scraper.handlers.routes import router


async def main() -> None:
    """The crawler entry point."""
    configure_logging()
    await test_connect()

    # Configure Crawlee for Cloud Run environment
    configuration = Configuration(
        log_level="DEBUG",
        purge_on_start=True,  # Clear storage on each run
    )

    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_requests_per_crawl=settings.debug_building_limit,
        configuration=configuration,
    )

    await crawler.run(buildings)
