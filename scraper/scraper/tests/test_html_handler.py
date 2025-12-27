"""Tests for HTML handler routing."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
from crawlee import Request

# Mock the storage.Client initialization
with patch("google.cloud.storage.Client", new=Mock()):
    from scraper.routes import router as my_router


class MockHttpResponse:
    """Mock HTTP response for testing.

    In crawlee v1.x, http_response.read() is async.
    """

    @property
    def http_version(self) -> str:
        """Return the HTTP version string."""
        return "HTTP/1.1"

    @property
    def status_code(self) -> int:
        """Return the HTTP status code."""
        return 200

    @property
    def headers(self) -> dict:
        """Return the HTTP response headers."""
        return {"Content-Type": "text/html"}

    async def read(self) -> bytes:
        """Read the response body (async in crawlee v1.x)."""
        return b"<html>bad >"


def create_mock_context(label: str | None = None, building_id: int = 1) -> Mock:
    """Create a mock BeautifulSoupCrawlingContext for testing.

    Args:
        label: The request label (e.g., 'HTML', 'JSON').
        building_id: The building ID for user_data.

    Returns:
        A Mock object with the necessary context attributes.
    """
    mock_context = Mock()
    mock_context.request = Request.from_url(
        url="https://example.com/",
        label=label,
        user_data={"building_id": building_id},
    )
    mock_context.http_response = MockHttpResponse()
    mock_context.soup = Mock()
    return mock_context


@pytest.mark.asyncio
async def test_router_specific_handler_invoked() -> None:
    """Test that the router invokes the correct handler based on label."""
    context = create_mock_context(label="HTML", building_id=1)
    await my_router(context)
