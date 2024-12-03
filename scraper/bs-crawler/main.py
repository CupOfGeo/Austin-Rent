import asyncio
import multiprocessing

import structlog
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler

from .config.logging import configure_logging
from .extended_request import ExtendedRequest
from .routes import router
from .utils.simple_webserver import run_simple_webserver

logger = structlog.get_logger()


async def main() -> None:
    """The crawler entry point."""
    configure_logging()
    # Create thread and start health check endpoint
    simple_webserver = multiprocessing.Process(target=run_simple_webserver)
    simple_webserver.start()

    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_requests_per_crawl=1,
    )

    await crawler.run(
        [
            ExtendedRequest.from_url(
                url="https://sightmap.com/app/api/v1/8epml7q1v6d/sightmaps/80524",
                label="JSON",
                metadata={"building_id": 1},
            ),
        ]
    )

    # Sleep for an extra minute to keep the application running for health check
    await asyncio.sleep(60)
    simple_webserver.terminate()
