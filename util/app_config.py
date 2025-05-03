DB_URL = ""


def set_db_url(temporary: bool = False):
    """
    Set url to connect to database.
    :param temporary: If true, db file will not be created - used for unit tests
    """
    location = ":memory:" if temporary else "database.sqlite"
    global DB_URL
    DB_URL = f"sqlite+pysqlite:///{location}"
