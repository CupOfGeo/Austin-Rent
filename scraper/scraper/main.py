from datetime import timedelta

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

    # Configure Crawlee for Cloud Run environment with limited resources
    configuration = Configuration(
        verbose_log=True,
        max_used_cpu_ratio=0.75,  # Lower threshold for Cloud Run
        max_used_memory_ratio=0.75,  # Lower threshold for Cloud Run
        max_event_loop_delay=timedelta(milliseconds=100),
        purge_on_start=True,  # Clear storage on each run
    )

    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_requests_per_crawl=settings.debug_building_limit,
        configuration=configuration,
        min_concurrency=1,  # Start with 1 concurrent task
        max_concurrency=4,  # Max 4 concurrent tasks
    )

    await crawler.run(buildings)
