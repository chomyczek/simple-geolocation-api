from flask import request, jsonify

from model.response import Response
from util.db_handler import DbHandler
from util.route_util import decode_input_json, value_is_ip_check


def delete():
    response = Response()
    req_data = request.get_json()

    value = decode_input_json(req_data)

    if not value:
        response.message = "Incorrect input JSON. Expected input contains 'input' key."
        return jsonify(response.serialize())
    is_ip = value_is_ip_check(value)

    db = DbHandler()
    result = db.delete_geolocation(value, is_ip)

    if result:
        response.message = "Value dropped from database successfully."
    else:
        response.message = "Value was not deleted from the database."

    return jsonify(response.serialize())
