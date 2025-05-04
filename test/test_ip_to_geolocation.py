import json

import pytest
import requests
import requests_mock

from model.geolocation import Geolocation
from util.ip_to_geolocation import Ip2Geolocation


class TestIpToGeolocation:
    mock_json_output = json.loads(
        """{
        "ip": "3.226.163.86",
        "hostname": "ec2-3-226-163-86.compute-1.amazonaws.com",
        "type": "ipv4",
        "continent_code": "NA",
        "continent_name": "North America",
        "country_code": "US",
        "country_name": "United States",
        "region_code": "VA",
        "region_name": "Virginia",
        "city": "Ashburn",
        "zip": "20147",
        "latitude": 39.043701171875,
        "longitude": -77.47419738769531,
        "msa": "47900",
        "dma": "511",
        "radius": "43.86505",
        "ip_routing_type": "international proxy",
        "connection_type": "tx",
        "location": {
            "geoname_id": 4744870,
            "capital": "Washington D.C.",
            "languages": [
                {
                    "code": "en",
                    "name": "English",
                    "native": "English"
                }
            ],
            "country_flag": "https://assets.ipstack.com/flags/us.svg",
            "country_flag_emoji": "🇺🇸",
            "country_flag_emoji_unicode": "U+1F1FA U+1F1F8",
            "calling_code": "1",
            "is_eu": false
        }
    }"""
    )
    test_ip = "127.0.0.1"
    test_token = "test"

    def test_get_ip(self, requests_mock):
        converter = Ip2Geolocation()
        requests_mock.get(converter.get_url(self.test_ip), json=self.mock_json_output)
        output = converter.get(self.test_ip)
        assert output is not None
        assert type(output) is Geolocation
        assert output.url is None

    def test_get_url(self, requests_mock):
        url = "www.example.com"
        converter = Ip2Geolocation()
        requests_mock.get(converter.get_url(url), json=self.mock_json_output)
        output = converter.get(url, False)
        assert output is not None
        assert type(output) is Geolocation
        assert output.url == url

    @pytest.fixture
    def mock_requests_wa(self):
        """Workaround fixture for testing connection errors"""
        with requests_mock.Mocker() as mock:
            yield mock

    def test_raise_connection(self, mock_requests_wa):
        converter = Ip2Geolocation()
        mock_requests_wa.get(converter.get_url(self.test_ip), exc=requests.exceptions.ConnectionError)
        output = converter.get(self.test_ip)
        assert output is None

    def test_get_no_value(self):
        converter = Ip2Geolocation()
        output = converter.get(None)
        assert output is None

    def test_get_part_of_json(self, requests_mock):
        converter = Ip2Geolocation()
        requests_mock.get(converter.get_url(self.test_ip), json=json.loads('{"ip":"0.0.0.0"}'))
        output = converter.get(self.test_ip)
        assert output is None
