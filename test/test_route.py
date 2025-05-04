import pytest

from app import app_setup
from model.geolocation import Geolocation
from util import app_config
from util.db_handler import DbHandler
from util.ip_to_geolocation import Ip2Geolocation


class TestRoute:
    def _get_geolocation_object(self):
        return Geolocation(
            ip="127.0.0.0",
            continent_name="continent_name",
            country_name="country_name",
            region_name="region_name",
            city="city",
            zip="zip",
            latitude=0,
            longitude=0,
            radius=0,
        )

    @pytest.fixture
    def setup_db(self):
        app_config.set_db_url(True)
        DbHandler().prepare_db_tables()
        yield
        DbHandler().delete_geolocation(self._get_geolocation_object().ip)

    @pytest.fixture
    def app(self):
        app = app_setup()
        app.config.update({"TESTING": True, })
        yield app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_add_incorrect_input(self, client):
        result = client.post("/add", json={
            "query": 123,
        })

        assert result.json["message"] == "Incorrect input JSON. Expected input contains 'input' key."
        assert result.json["result"] is None

    def test_add_already_in_db(self, client, setup_db):
        geo = self._get_geolocation_object()
        DbHandler().add_geolocation(geo)

        result = client.post("/add", json={
            "input": geo.ip,
        })

        assert result.json["message"] == "Value already in database."
        assert result.json["result"]["ip"] == geo.ip

    def test_add_ipstack_failed(self, mocker, client, setup_db):
        mocker.patch.object(Ip2Geolocation, "get", return_value=None)
        geo = self._get_geolocation_object()

        result = client.post("/add", json={
            "input": geo.ip,
        })

        assert result.json["message"] == "There was problem related to ipstack service."
        assert result.json["result"] is None

    def test_add_update_url(self, client, setup_db, mocker):
        url = "www.super-url.com"
        geo = self._get_geolocation_object()
        mocker.patch.object(Ip2Geolocation, "get", return_value=geo)
        DbHandler().add_geolocation(geo)

        result = client.post("/add", json={
            "input": url,
        })

        assert result.json["message"] == "The URL has been updated to an existing record in the database."
        assert result.json["result"]["ip"] == geo.ip
        assert result.json["result"]["url"] == geo.url

    def test_add_db_success(self, client, setup_db, mocker):
        geo = self._get_geolocation_object()
        mocker.patch.object(Ip2Geolocation, "get", return_value=geo)
        mocker.patch.object(DbHandler, "add_geolocation", return_value=False)

        result = client.post("/add", json={
            "input": geo.ip,
        })

        assert result.json["message"] == "Failed to add value to database."
        assert result.json["result"] is None

    def test_add_db_fail(self):
        raise NotImplementedError()

    def test_delete(self):
        raise NotImplementedError()

    def test_get(self):
        raise NotImplementedError()
