from geoalchemy2 import Geometry

from database import Base
from sqlalchemy import Column, Integer, Float


class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    zone_coordinates = Column(Geometry("POLYGON"))
    # zone_coordinates = Column(Float)
    currier = Column(Integer, nullable=True)


