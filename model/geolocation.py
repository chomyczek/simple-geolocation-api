from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import declarative_base

base = declarative_base()


class Geolocation(base):
    __tablename__ = "geolocation"

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    url = Column(String, nullable=True)
    continent_name = Column(String)
    country_name = Column(String)
    region_name = Column(String)
    city = Column(String)
    zip = Column(String)
    latitude = Column(DECIMAL(17, 15))
    longitude = Column(DECIMAL(18, 15))
    radius = Column(DECIMAL)
