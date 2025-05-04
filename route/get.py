from flask import json, jsonify, request

from model.response import Response
from util.db_handler import DbHandler
from util.route_util import decode_input_json, value_is_ip_check


def get() -> json:
    """
    This path is used to display records from the database if it does exist. It takes POST method with a JSON
    value in the form of the 'input' key and a value in the form of an IP or URL, e.g. {"input":"ipstack.com"}
    :return: The JSON response.
    :return:
    """
    response = Response()
    req_data = request.get_json()

    value = decode_input_json(req_data)

    if not value:
        response.message = "Incorrect input JSON. Expected input contains 'input' key."
        return jsonify(response.serialize())
    is_ip = value_is_ip_check(value)

    db = DbHandler()
    result = db.read_geolocation(value, is_ip)

    if result:
        response.message = "Value retrieved from database."
        response.result = result
    else:
        response.message = "The value is not present in the database."

    return jsonify(response.serialize())
