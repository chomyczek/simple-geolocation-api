from flask import json, jsonify

from model.response import Response


def index() -> json:
    """
    Index page of the application.
    :return: The JSON response.
    """
    response = Response()
    response.message = (
        "In case of problems or doubts please visit the documentation available on github "
        "https://github.com/chomyczek/simple-geolocation-api"
    )

    return jsonify(response.serialize())
