from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
import structlog

from .config.logging import configure_logging
from .routes import router
from .extended_request import ExtendedRequest

logger = structlog.get_logger()

async def main() -> None:
    """The crawler entry point."""
    configure_logging()
    
    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_requests_per_crawl=1,
    )

    await crawler.run(
        [
            ExtendedRequest.from_url(
                url='https://sightmap.com/app/api/v1/8epml7q1v6d/sightmaps/80524',
                label='JSON',
                metadata={"building_id": 1}
            ),
        ]
    )