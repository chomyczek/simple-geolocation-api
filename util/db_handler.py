from typing import Type, Union

from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from model.geolocation import Geolocation
from model.table_base import TableBase
from util.db_engine import DbEngine


class DbHandler:
    """
    The class is used to perform simple operations on the database.
    """

    engine: Engine = None

    def __init__(self):
        self.engine = DbEngine().engine

    def add_geolocation(self, geolocation: Geolocation):
        """
        The function adds a geolocation object to the database.
        :param geolocation: Object to be placed in the database. After the function is executed, the object will be
        updated with the primary key from the database.
        :return: Returns True if the insertion was successful.
        """
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(geolocation)
            try:
                session.commit()
                return True
            except OperationalError:
                session.rollback()
                return False

    def read_geolocation(self, value: str, is_ip: bool = True) -> Union[None, Geolocation, list[Type[Geolocation]]]:
        """
        Retrieves records from the Geolocation table based on either an IP address or a URL.
        :param value: IP or URL required for executing function.
        :param is_ip: Set to True if IP was provided as value.
        :return: todo
        """
        with Session(self.engine) as session:
            if is_ip:
                return session.query(Geolocation).filter_by(ip=value).first()
            else:
                result = session.query(Geolocation).filter_by(url=value).all()  # todo: always will be one
                return result if result else None

    def delete_geolocation(self, value: str, is_ip: bool = True) -> bool:
        """
        Deletes records from the Geolocation table based on an IP address or a URL.
        :param value: IP or URL required for executing function.
        :param is_ip: Set to True if IP was provided as value.
        :return: Returns True if the deletion was successful.
        """
        geolocation = self.read_geolocation(value, is_ip)
        if not geolocation:
            return False
        with Session(self.engine) as session:
            if is_ip:
                session.delete(geolocation)
            else:
                for g in geolocation:
                    session.delete(g)
            try:
                session.commit()
            except OperationalError:
                session.rollback()
                return False
        return True

    def update_geolocation_url(self, geolocation: Geolocation, new_url: str) -> bool:
        """
        Updates the url attribute of a Geolocation record.
        :param geolocation: Object to be updated.
        :param new_url: New value of the URL.
        :return: Returns True if the update was successful.
        """
        with Session(self.engine) as session:
            session.query(Geolocation).filter_by(id=geolocation.id).update({"url": new_url})
            try:
                session.commit()
                return True
            except OperationalError:
                session.rollback()
                return False

    def prepare_db_tables(self):
        """
        Creates the necessary database tables. Handles the OperationalError exception if the database is locked.
        """
        base = TableBase()
        try:
            base.metadata.create_all(self.engine)
        except OperationalError:
            raise ConnectionError("The database is locked, please try again later or close unnecessary connections.")
        except Exception as e:
            raise RuntimeError(f"Error creating tables: {str(e)}")
