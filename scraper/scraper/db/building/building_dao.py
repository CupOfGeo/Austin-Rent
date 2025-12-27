"""Data Access Object for building operations."""

import structlog

from scraper.db.building.building_model import Building
from scraper.db.sql_connect import get_db_session

logger = structlog.get_logger()


class BuildingDAO:
    """Data Access Object for managing building records in the database."""

    async def add_building(self, address, building_name, url, is_active=True):
        """Add a new building to the database.

        Args:
            address: The street address of the building.
            building_name: The name of the building.
            url: The URL for scraping the building's data.
            is_active: Whether the building should be actively scraped.
        """
        async for session in get_db_session():
            new_building = Building(
                address=address,
                building_name=building_name,
                url=url,
                is_active=is_active,
            )
            session.add(new_building)

        logger.debug("Building saved to database.", building=new_building)

    async def get_all_active_buildings(self):
        """Retrieve all active buildings from the database.

        Returns:
            List of Building objects that are marked as active.
        """
        async for session in get_db_session():
            return session.query(Building).filter(Building.is_active is True).all()
