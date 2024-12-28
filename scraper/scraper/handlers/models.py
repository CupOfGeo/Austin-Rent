"""
Unused but thoughts on how to structure the data models.
"""
from dataclasses import dataclass


@dataclass
class ScraperResponse:
    requested_url: str
    loaded_url: str
    building_id: str
    retry_count: int
    clean_content: str

@dataclass
class ScrapeExtraction:
    building_id: int
    scrape_page_id: int
    unit_number: str
    bed_count: float
    bath_count: float
    sqft: float
    base_rent: float
    deposit: float
    available: str
    img_url: str
    additional_attributes: dict
