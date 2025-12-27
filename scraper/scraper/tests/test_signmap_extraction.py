"""Tests for Sightmap JSON extraction functionality.

Validates that the json_extract function correctly parses Sightmap API
responses into structured extraction models.
"""

import json
import os

import pytest

from scraper.handlers.json_handler import json_extract


@pytest.fixture
def json_content():
    """Load sightmap test data, returning just the content portion.

    The test resource file has a wrapper structure with 'metadata' and 'content'.
    The json_extract function expects just the 'content' part (the raw API response).
    """
    test_data_path = os.path.join(
        os.path.dirname(__file__), "resources", "sightmap.json"
    )
    with open(test_data_path, "r") as file:
        full_response = json.load(file)
        return full_response.get("content")


@pytest.mark.asyncio
async def test_parse_sight_map_content(json_content):
    """Test that json_extract correctly parses sightmap content into extractions."""
    building_id = 12345
    scrape_response_id = 67890
    extractions = await json_extract(json_content, building_id, scrape_response_id)

    assert len(extractions) == 300

    # Verify first extraction has expected values
    first = extractions[0]
    assert first.building_id == building_id
    assert first.scrape_response_id == scrape_response_id
    assert first.unit_number == "1401"
    assert first.bed_count == 1
    assert first.bath_count == 1
    assert first.sqft == 929
    assert first.base_rent == 4200
    assert (
        first.img_url
        == "https://cdn.sightmap.com/assets/8e/pm/8epmy950p6d/09/b9/09b9a53ea46242ecf61e08156eb68582.jpg"
    )
    # Note: 'available' field is not currently extracted (commented out in json_extract)
