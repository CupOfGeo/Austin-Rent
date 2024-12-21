from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
from crawlee.configuration import Configuration

from scraper.Buildings import buildings
from scraper.config.logging import configure_logging
from scraper.config.settings import settings
from scraper.db.sql_connect import test_connect
from scraper.routes import router


async def main() -> None:
    """The crawler entry point."""
    configure_logging()
    await test_connect()
    configuration = Configuration(verbose_log=True) #persist_storage=False, write_metadata=False, 
    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_requests_per_crawl=None,
        configuration=configuration,
    )

    if settings.debug_building_limit:
        buildings_to_run = buildings[: settings.debug_building_limit]
    else:
        buildings_to_run = buildings
    await crawler.run(buildings_to_run)
