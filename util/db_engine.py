from sqlalchemy import Engine, create_engine

from meta.singleton_meta import SingletonMeta
from util import app_config


class DbEngine(metaclass=SingletonMeta):
    """
    The class is used to store a single instance of the engine responsible for connecting to the database.
    """

    engine: Engine = None

    def __init__(self):
        if not app_config.DB_URL:
            raise ValueError("Please provide app_config.DB_URL value.")
        self.engine = create_engine(app_config.DB_URL)
