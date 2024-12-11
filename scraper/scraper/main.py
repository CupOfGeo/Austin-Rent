import asyncio
import multiprocessing

from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
from crawlee.configuration import Configuration

from scraper.Buildings import buildings
from scraper.config.logging import configure_logging
from scraper.config.settings import settings
from scraper.routes import router
from scraper.utils.simple_webserver import run_simple_webserver


async def main() -> None:
    """The crawler entry point."""
    configure_logging()
    # Create thread and start health check endpoint
    simple_webserver = multiprocessing.Process(target=run_simple_webserver)
    simple_webserver.start()

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

    # Sleep for an extra minute to keep the application running for health check
    await asyncio.sleep(60)
    simple_webserver.terminate()
