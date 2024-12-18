from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
from crawlee.configuration import Configuration

from scraper.Buildings import buildings
from scraper.config.logging import configure_logging
from scraper.config.settings import settings
from scraper.routes import router


async def main() -> None:
    """The crawler entry point."""
    configure_logging()
    configuration = Configuration(persist_storage=False, write_metadata=False)
    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_requests_per_crawl=1,
        configuration=configuration,
    )

    if settings.environment == "LOCAL":
        buildings_to_run = buildings[: settings.debug_building_limit]
    else:
        buildings_to_run = buildings
    await crawler.run(buildings_to_run)
