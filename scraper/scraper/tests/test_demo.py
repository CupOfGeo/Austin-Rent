# import pytest
# from unittest.mock import AsyncMock, MagicMock
# from bs4 import BeautifulSoup
# from crawlee import BeautifulSoupCrawlingContext

# # Import your handler and utility functions
# from scraper.routes import html_handler

# @pytest.mark.asyncio
# async def test_html_handler_invalid_html():
#     # Mock context and its properties
#     mock_context = AsyncMock(spec=BeautifulSoupCrawlingContext)
#     mock_context.request.url = "http://example.com"
#     mock_context.request.user_data.model_extra = {"building_id": 123}

#     # Simulate an invalid HTML response
#     invalid_html = b"<html><head><title>Test</title></head><body><div><div>"  # Missing closing tags
#     mock_context.http_response.read.return_value = invalid_html

#     # Call the handler
#     await html_handler(mock_context)

#     # Check logs or behavior
#     mock_context.logger.error.assert_called_with(
#         "Invalid HTML content."
#     )
