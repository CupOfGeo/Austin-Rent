"""
Handles JSON content validation and extraction for the scraper.
"""

import json
from typing import Any, Optional

import structlog
from crawlee.crawlers import BeautifulSoupCrawlingContext

from scraper.db.scrape_extraction.extraction_model import ScrapeExtractionModel

logger = structlog.get_logger()


async def json_validate(
    context: BeautifulSoupCrawlingContext,
) -> Optional[dict[str, Any]]:
    """Validate and return json content from the HTTP response.

    Args:
        context: The crawling context containing the HTTP response.

    Returns:
        The parsed JSON content as a dict, or None if parsing fails.
    """
    building_id = context.request.user_data.get("building_id")
    logger.info("Handling", url={context.request.url}, building_id=building_id)

    try:
        # In crawlee v1.x, http_response.read() is async
        response_bytes = await context.http_response.read()
        response_text = response_bytes.decode("utf-8")
        json_content: dict[str, Any] = json.loads(response_text)
        return json_content
    except json.JSONDecodeError:
        logger.error("Invalid JSON content.", url=context.request.url)
        return None


async def json_extract(json_content, building_id, scrape_response_id) -> list:
    """Parse sight map content."""
    floor_plans = {
        floor_plan.get("id"): floor_plan
        for floor_plan in json_content.get("data").get("floor_plans")
    }

    units = json_content.get("data").get("units")
    extractions = []
    for unit in units:
        floor_plan = floor_plans.get(unit.get("floor_plan_id"))
        bed_count = None
        bath_count = None
        img_url = None
        if floor_plan:
            bed_count = floor_plan.get("bedroom_count")
            bath_count = floor_plan.get("bathroom_count")
            img_url = floor_plan.get("image_url")
        extraction = ScrapeExtractionModel(
            building_id=building_id,
            scrape_response_id=scrape_response_id,
            unit_number=unit.get("unit_number"),
            bed_count=bed_count,
            bath_count=bath_count,
            sqft=unit.get("area"),
            base_rent=unit.get("price"),
            # available=unit.get("available_on"),
            img_url=img_url,
            # additional_attributes=unit
        )
        extractions.append(extraction)
    return extractions
