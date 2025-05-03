from sqlalchemy.orm import DeclarativeBase


class TableBase(DeclarativeBase):
    """
    Base class for Database Tables, used to automatically collect the tables needed to be generated in the database.
    """

    pass
