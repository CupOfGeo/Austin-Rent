import asyncio
import multiprocessing

from crawlee import Request
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
from crawlee.configuration import Configuration

from .config.logging import configure_logging
from .routes import router
from .utils.simple_webserver import run_simple_webserver

from .db.sql_connect import get_db_session

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

    await crawler.run(
        [
            Request.from_url(
                url="https://sightmap.com/app/api/v1/8epml7q1v6d/sightmaps/80524",
                label="JSON",
                user_data={"building_id": 1},
            ),
            # Request.from_url(
            #     url="https://sightmap.com/app/api/v1/60p7q39nw7n/sightmaps/397",
            #     label="JSON",
            #     user_data={"building_id": 2},
            # ),
            # Request.from_url(
            #     url="https://www.windsorcommunities.com/properties/windsor-on-the-lake/floorplans/",
            #     label="HTML",
            #     user_data={"building_id": 3},
            # ),
        ]
    )

    # Sleep for an extra minute to keep the application running for health check
    await asyncio.sleep(60)
    simple_webserver.terminate()
