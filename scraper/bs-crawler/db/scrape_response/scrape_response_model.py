from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from ...db.base import Base

class ScrapeResponse(Base):
    __tablename__ = 'scrape_responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(UUID, nullable=False)
    requested_url = Column(String, nullable=False)
    loaded_url = Column(String, nullable=False)
    building_id = Column(Integer, nullable=False)
    handled_at = Column(DateTime, nullable=False)
    retry_count = Column(Integer, nullable=False)