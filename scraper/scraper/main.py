import asyncio

from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
from crawlee.configuration import Configuration

from scraper.Buildings import buildings
from scraper.config.logging import configure_logging
from scraper.config.settings import settings
from scraper.routes import router


async def main() -> None:
    """The crawler entry point."""
    configure_logging()
    # Start the simple web server in a subprocess
    webserver_process = await asyncio.create_subprocess_exec(
        "python", "-m", "scraper.utils.simple_webserver"
    )
    try:
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
    finally:
        # Sleep for an extra minute to keep the application running for health check
        await asyncio.sleep(60)
        webserver_process.terminate()
        await webserver_process.wait()
