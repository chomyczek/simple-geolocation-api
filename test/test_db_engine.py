import time

import pytest
from sqlalchemy.orm import Session

from model.geolocation import Geolocation
from util import app_config
from util.db_engine import DbEngine
from util.db_handler import DbHandler


class TestDb:
    @pytest.fixture
    def setup_db(self):
        app_config.set_db_url(True)
        DbHandler().prepare_db_tables()

    def _get_geolocation_object(self):
        return Geolocation(
            ip=str(time.time()),
            continent_name="continent_name",
            country_name="country_name",
            region_name="region_name",
            city="city",
            zip="zip",
            latitude=0,
            longitude=0,
            radius=0,
        )

    def _db_count(self):
        with Session(DbEngine().engine) as session:
            return session.query(Geolocation.id).count()

    def test_db_engine_init_raise_if_no_db_url(self):
        app_config.DB_URL = None
        with pytest.raises(ValueError):
            DbEngine()

    def test_add(self, setup_db):
        expected = self._db_count() + 1
        DbHandler().add_geolocation(self._get_geolocation_object())
        assert self._db_count() == expected

    @pytest.mark.parametrize("is_url", [True, False])
    def test_delete(self, setup_db, is_url):
        handler = DbHandler()
        geolocation_object = self._get_geolocation_object()
        geolocation_object.url = "www.example.com/" + str(time.time())
        handler.add_geolocation(geolocation_object)
        expected_count = self._db_count() - 1
        value = geolocation_object.url if is_url else geolocation_object.ip

        result = handler.delete_geolocation(value, is_url)

        assert result is True
        assert self._db_count() == expected_count
        assert handler.read_geolocation(value, is_url) is None

    def test_delete_multiple(self, setup_db):
        handler = DbHandler()
        geolocation_object = self._get_geolocation_object()
        geolocation_object.url = "www.example.com/" + str(time.time())
        geolocation_object_second = self._get_geolocation_object()
        geolocation_object_second.url = geolocation_object.url
        handler.add_geolocation(geolocation_object)
        handler.add_geolocation(geolocation_object_second)
        expected_count = self._db_count() - 2
        value = geolocation_object.url

        handler.delete_geolocation(value, True)

        assert self._db_count() == expected_count
        assert handler.read_geolocation(value, True) is None

    def test_read(self, setup_db):
        handler = DbHandler()
        geolocation_object = self._get_geolocation_object()
        handler.add_geolocation(geolocation_object)

        result = handler.read_geolocation(geolocation_object.ip)

        assert type(result) is Geolocation
        assert result.ip == geolocation_object.ip

    def test_read_multiple(self, setup_db):
        handler = DbHandler()
        geolocation_object = self._get_geolocation_object()
        geolocation_object.url = "www.example.com/" + str(time.time())
        geolocation_object_second = self._get_geolocation_object()
        geolocation_object_second.url = geolocation_object.url
        handler.add_geolocation(geolocation_object)
        handler.add_geolocation(geolocation_object_second)
        expected_len = 2

        result = handler.read_geolocation(geolocation_object.url, True)

        assert len(result) == expected_len

    def test_update(self, setup_db):
        handler = DbHandler()
        geolocation_object = self._get_geolocation_object()
        handler.add_geolocation(geolocation_object)
        url = "www.magic-example.com"

        handler.update_geolocation_url(geolocation_object, url)

        assert handler.read_geolocation(geolocation_object.ip).url == url

    @pytest.mark.parametrize("is_url", [True, False])
    def test_delete_not_found(self, setup_db, is_url):
        handler = DbHandler()

        result = handler.delete_geolocation("unknown_value", is_url)

        assert result is False

    @pytest.mark.parametrize("is_url", [True, False])
    def test_show_not_found(self, setup_db, is_url):
        handler = DbHandler()

        result = handler.read_geolocation("unknown_value", is_url)

        assert result is None
