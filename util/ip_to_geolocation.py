from typing import Union

import requests

from meta.singleton_meta import SingletonMeta
from model.geolocation import Geolocation


class Ip2Geolocation(metaclass=SingletonMeta):
    """
    Class responsible for communication with the api.ipstack.com application. A token is required to communicate with
    the api. A class created with the Thread-safe Singleton pattern.
    """
    token: str = None

    def __init__(self, token: str = None):
        self.token = token

    def get(self, value: str, url_value: bool = False) -> Union[None, Geolocation]:
        """
        The function is responsible for connecting to the API and returning the retrieved value in the form of a
        Geolocation model object. If there is a problem while retrieving the data, the value None will be returned
        instead.
        :param value: The value we want to check in the service, can be IP or URL.
        :param url_value: True if the value is URL.
        :return: The Geolocation object that was downloaded, or None if there was a problem.
        """
        if not value:
            return None
        url = self.get_url(value)
        try:
            response = requests.get(url)
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.TooManyRedirects:
            return None
        except requests.exceptions.RequestException:
            return None

        if not response:
            return None

        geolocation = self._json_to_geolocation(response.json())
        if not geolocation:
            return None

        if url_value:
            geolocation.url = value

        return geolocation

    def get_url(self, value: str) -> str:
        """
        Get url for request.
        :param value: The value we want to check in the service, can be IP or URL.
        :return: Formatted URL for service request.
        """
        return f"https://api.ipstack.com/{value}?access_key={self.token}"

    def _json_to_geolocation(self, json):
        if json.get("ip") and json.get("continent_name") and json.get("country_name") and json.get("region_name") and \
                json.get("zip") and json.get("latitude") and json.get("longitude") and json.get("radius"):
            ip = json["ip"]
            continent_name = json["continent_name"]
            country_name = json["country_name"]
            region_name = json["region_name"]
            city = json["city"]
            zip_ = json["zip"]
            latitude = json["latitude"]
            longitude = json["longitude"]
            radius = json["radius"]
            return Geolocation(ip, continent_name, country_name, region_name, city, zip_, latitude, longitude, radius)
        return None
