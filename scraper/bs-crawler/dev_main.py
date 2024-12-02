import enum
from crawlee.basic_crawler import BasicCrawler
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
from crawlee import Request
from google.cloud import pubsub_v1
import asyncio
import json

from .routes import router

class Label(enum.Enum):
    HTML = 'HTML'
    JSON = 'JSON'
    BYTES = 'BYTES'

class MockMessage:
    def __init__(self, data):
        self.data = data

    def ack(self):
        print("Message acknowledged")
    

async def run_crawler(crawler: BasicCrawler, url: str, label: Label) -> None:
    """Run the crawler with the given URL."""
    # crawler.add_requests()
    await crawler.run(
        [
            Request.from_url(
                url=url,
                label=label
            ),
        ]
    )
async def create_callback(crawler: BasicCrawler) -> callable:
    async def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        """Callback function to handle incoming Pub/Sub messages."""
        data = json.loads(message.data)
        url = data.get('url')
        label = data.get('label')
        if url:
            await run_crawler(crawler, url, label)
        message.ack()
    return callback


async def main() -> None:
    """The crawler entry point."""
    crawler = BeautifulSoupCrawler(
        request_handler=router,
        max_requests_per_crawl=1,
    )
    # Create the callback with the crawler instance
    mock_data = json.dumps({
        "url": "https://raw.githubusercontent.com/python/cpython/refs/heads/main/.github/problem-matchers/gcc.json",
        "label": "JSON"
    }).encode('utf-8')

    mock_message = MockMessage(mock_data)

    # Create the callback with the crawler instance
    callback = await create_callback(crawler)

    # Trigger the callback with the mock message
    await callback(mock_message)    

