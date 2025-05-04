from flask import json, jsonify, request

from model.response import Response
from util.db_handler import DbHandler
from util.ip_to_geolocation import Ip2Geolocation
from util.route_util import decode_input_json, value_is_ip_check


def add() -> json:
    """
    This path is used to add a new value to the database if it does not already exist. It takes POST method with a JSON
    value in the form of the 'input' key and a value in the form of an IP or URL, e.g. {"input":"ipstack.com"}
    :return: The JSON response.
    """
    response = Response()
    req_data = request.get_json()

    value = decode_input_json(req_data)

    if not value:
        response.message = "Incorrect input JSON. Expected input contains 'input' key."
        return jsonify(response.serialize())
    is_ip = value_is_ip_check(value)

    db = DbHandler()
    geo = db.read_geolocation(value, is_ip)

    if geo:
        response.message = "Value already in database."
        response.result = geo
        return jsonify(response.serialize())

    geo = Ip2Geolocation().get(value, is_ip)
    if not geo:
        response.message = "There was problem related to ipstack service."
        return jsonify(response.serialize())
    if not is_ip:
        geo_rel = db.read_geolocation(geo.ip)
        if geo_rel:
            result = db.update_geolocation_url(geo_rel, value)
            if result:
                response.message = "The URL has been updated to an existing record in the database."
                response.result = geo_rel
                return jsonify(response.serialize())
    result = db.add_geolocation(geo)
    if result:
        response.message = "Value added to database successfully."
        response.result = geo
    else:
        response.message = "Failed to add value to database."

    return jsonify(response.serialize())
