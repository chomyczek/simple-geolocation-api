from sqlalchemy import DECIMAL, Column, Integer, String
from sqlalchemy.orm import declarative_base

base = declarative_base()


class Geolocation(base):
    """
    Geolocation class model used to store data in the database.
    """

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

    def __init__(self, ip, continent_name, country_name, region_name, city, zip_, latitude, longitude, radius):
        self.ip = ip
        self.continent_name = continent_name
        self.country_name = country_name
        self.region_name = region_name
        self.city = city
        self.zip = zip_
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
