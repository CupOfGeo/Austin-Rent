from sqlalchemy import Boolean, Column, Integer, String

from scraper.db.base import Base


class Building(Base):
    __tablename__ = "buildings"

    building_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    building_name = Column(String, nullable=True)
    url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
