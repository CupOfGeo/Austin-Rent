from sqlalchemy import Numeric, Column, Integer, Date, Text, JSON

from scraper.db.base import Base


class ScrapeExtractionModel(Base):
    __tablename__ = "scrape_extractions"

    scrape_extraction_id = Column(Integer, primary_key=True, autoincrement=True)
    building_id = Column(Integer, nullable=False)
    scrape_response_id = Column(Integer, nullable=False)
    unit_number = Column(Text)
    bed_count = Column(Numeric)
    bath_count = Column(Numeric)
    sqft = Column(Numeric)
    base_rent = Column(Numeric)
    deposit = Column(Numeric)
    available = Column(Date)
    img_url = Column(Text)
    additional_attributes = Column(JSON)