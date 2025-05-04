import re
from typing import Union

from flask import request, jsonify

from model.response import Response
from util.db_handler import DbHandler
from util.ip_to_geolocation import Ip2Geolocation


def add():
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

    geo=Ip2Geolocation().get(value, is_ip)
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


def decode_input_json(json: dict) -> Union[None, str]:
    if json is dict:
        return json.get("input")
    return None


def value_is_ip_check(value: str) -> bool:
    match = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value)
    return bool(match)
