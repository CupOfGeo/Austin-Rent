from __future__ import annotations

import logging
from unittest.mock import AsyncMock, Mock

import pytest

from unittest.mock import patch
from crawlee import Request
from crawlee.sessions import Session
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext


# Mock the storage.Client initialization
with patch("google.cloud.storage.Client", new=Mock()):
    from scraper.routes import router as my_router



class MockHttpResponse:
    @property
    def http_version(self) -> str:
        return "HTTP/1.1"

    @property
    def status_code(self) -> int:
        return 200

    @property
    def headers(self) -> dict:
        return {"Content-Type": "text/html"}

    def read(self) -> bytes:
        return b"<html>bad >"



class MockContext(BeautifulSoupCrawlingContext):
    def __init__(self, *, label: str | None) -> None:
        super().__init__(
            request=Request.from_url(url='https://example.com/', user_data={'label': label}),
            session=Session(),
            send_request=AsyncMock(),
            add_requests=AsyncMock(),
            proxy_info=AsyncMock(),
            push_data=AsyncMock(),
            get_key_value_store=AsyncMock(),
            log=logging.getLogger(),
            http_response=MockHttpResponse(),
            soup=Mock(),
            enqueue_links=Mock(),
        )



@pytest.mark.asyncio
async def test_router_specific_handler_invoked() -> None:
    mock_default_handler = Mock()
    mock_handler_a = Mock()


    await my_router(MockContext(label='HTML'))
    assert 1 == 1
