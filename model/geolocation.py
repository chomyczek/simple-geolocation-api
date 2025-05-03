from typing import Optional

from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from model.table_base import TableBase


class Geolocation(TableBase):
    """
    Geolocation class model used to store data in the database.
    """

    __tablename__ = "geolocation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ip: Mapped[str]
    url: Mapped[Optional[str]]
    continent_name: Mapped[str]
    country_name: Mapped[str]
    region_name: Mapped[str]
    city: Mapped[str]
    zip: Mapped[str]
    latitude: Mapped[float] = mapped_column(DECIMAL(17, 15))
    longitude: Mapped[float] = mapped_column(DECIMAL(18, 15))
    radius: Mapped[float] = mapped_column(DECIMAL)
