"""SQLAlchemy model for buildings table.

Defines the database schema for building metadata. Currently not actively used
as building configuration is hardcoded in buildings.py for routing purposes.
"""

from sqlalchemy import Boolean, Column, Integer, String

from scraper.db.base import Base


class Building(Base):
    """Represents a building with its metadata and scraping configuration."""

    __tablename__ = "buildings"

    building_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    building_name = Column(String, nullable=True)
    url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
