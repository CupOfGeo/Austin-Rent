import json
import structlog
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
from scraper.db.scrape_extraction.extraction_model import ScrapeExtractionModel

logger = structlog.get_logger()


async def json_validate(context: BeautifulSoupCrawlingContext) -> dict:
    """json_validate and return json content."""
    building_id = context.request.user_data.model_extra.get("building_id")
    logger.info("Handling", url={context.request.url}, building_id=building_id)
    http_response = context.http_response
    try:
        json_content = json.load(http_response)
    except json.JSONDecodeError:
        json_content = None
        logger.error("Invalid JSON content.", url=context.request.url)

    return json_content

async def json_extract(json_content, building_id, scrape_response_id) -> list:
    """Parse sight map content."""
    floor_plans = {floor_plan.get('id'): floor_plan for floor_plan in json_content.get("data").get("floor_plans")}

    units = json_content.get("data").get("units")
    extractions = []
    for unit in units:
        extraction = ScrapeExtractionModel(
            building_id=building_id,
            scrape_response_id=scrape_response_id,
            unit_number=unit.get("unit_number"),
            bed_count=floor_plans.get(unit.get("floor_plan_id")).get("bedroom_count"),
            bath_count=floor_plans.get(unit.get("floor_plan_id")).get("bathroom_count"),
            sqft=unit.get("area"),
            base_rent=unit.get("price"),
            # available=unit.get("available_on"),
            img_url=floor_plans.get(unit.get("floor_plan_id")).get("image_url"),
            # additional_attributes=unit
        )
        extractions.append(extraction)
    return extractions
