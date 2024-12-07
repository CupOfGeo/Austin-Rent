from sqlalchemy import Column, Integer, String, Boolean
from ...db.base import Base

class Building(Base):
    __tablename__ = 'buildings'

    building_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    building_name = Column(String, nullable=True)
    url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)