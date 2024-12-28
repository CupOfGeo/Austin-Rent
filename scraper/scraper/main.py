from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
from crawlee.configuration import Configuration

from scraper.Buildings import buildings
from scraper.config.logging import configure_logging
from scraper.config.settings import settings
from scraper.db.sql_connect import test_connect
from scraper.handlers.routes import router


async def main() -> None:
    """The crawler entry point."""
    configure_logging()
    await test_connect()
    configuration = Configuration(
        verbose_log=False,
    )  # persist_storage=False, write_metadata=False,
    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_requests_per_crawl=settings.debug_building_limit,
        configuration=configuration,
    )

    await crawler.run(buildings)
