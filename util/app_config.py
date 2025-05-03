DB_URL = ""
API_TOKEN = ""


def set_db_url(temporary: bool = False):
    """
    Set url to connect to database.
    :param temporary: If true, db file will not be created - used for unit tests
    """
    location = ":memory:" if temporary else "database.sqlite"
    global DB_URL
    DB_URL = f"sqlite+pysqlite:///{location}"


def set_token(token: str):
    """
    Set token required to connect to ipstack.com.
    :param token: Token generated from service
    """
    if not token:
        raise ValueError("ipstack token is required to start the server. Please start app with -t parameter.")
    global API_TOKEN
    API_TOKEN = token
