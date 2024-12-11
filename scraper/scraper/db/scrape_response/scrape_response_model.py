from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from scraper.db.base import Base


class ScrapeResponse(Base):
    __tablename__ = "scrape_responses"

    scrape_page_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(UUID, nullable=False)
    requested_url = Column(String, nullable=False)
    loaded_url = Column(String, nullable=False)
    building_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    retry_count = Column(Integer, nullable=False)
