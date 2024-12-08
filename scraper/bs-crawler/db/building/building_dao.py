import structlog

from ...db.building.building_model import Building
from ...db.sql_connect import get_db_session

logger = structlog.get_logger()


class BuildingDAO:
    async def add_building(self, address, building_name, url, is_active=True):
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
        async for session in get_db_session():
            return session.query(Building).filter(Building.is_active == True).all()
