import argparse

from flask import Flask

from route import add, delete, get, index
from util import app_config
from util.db_handler import DbHandler


def app_setup() -> Flask:
    """
    Initialize Flask application and combine routes.
    :return: The Flask application.
    """
    app = Flask(__name__)
    app.add_url_rule("/", view_func=index.index)
    app.add_url_rule("/add", methods=["POST"], view_func=add.add)
    app.add_url_rule("/get", methods=["POST"], view_func=get.get)
    app.add_url_rule("/delete", methods=["POST"], view_func=delete.delete)
    return app


if __name__ == "__main__":
    app = app_setup()
    parser = argparse.ArgumentParser(prog="simple-geolocation-api")
    parser.add_argument("-t", "--token", required=True, help="The token generated from ipstack.com service")
    parser.add_argument("-i", "--host", default="127.0.0.1", help="The hostname to listen on. Set this to '0.0.0.0' to "
                                                                  "have the server available externally")
    parser.add_argument("-p", "--port", default="5000", help="The port of the webserver")
    args = parser.parse_args()
    app_config.set_db_url()
    app_config.set_token(args.token)
    DbHandler().prepare_db_tables()
    app.run(host=args.host, port=args.port)
