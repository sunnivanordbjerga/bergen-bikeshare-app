import pytest
from legacy_csv_importer import _parse_station


@pytest.fixture
def valid_station_row():
    return {
        "start_station_id": "1",
        "start_station_name": "Høyteknologisenteret",
        "start_station_latitude": "60.382216",
        "start_station_longitude": "5.332288",
        "start_station_max_spots": "66",
    }


@pytest.fixture
def valid_user_row():
    return {"user_id": "1", "user_name": "Jane Doe", "user_phone_number": "12345789"}


@pytest.fixture
def valid_bike_row():
    return {
        "bike_id": "1",
        "bike_name": "Thea",
        "bike_station_id": "",
        "bike_status": "Active",
    }


@pytest.fixture
def valid_subscription_row():
    return {
        "subscription_id": "1",
        "user_id": "1",
        "subscription_start_time": "2020-09-18 17:22:27",
        "subscription_type": "Day",
    }


@pytest.fixture
def valid_trip_row():
    return {
        "trip_id": "1",
        "user_id": "1",
        "bike_id": "1",
        "start_station_id": "1",
        "end_station_id": "",
        "trip_start_time": "2020-09-18 17:22:27",
        "trip_end_time": "",
    }


class TestParseStation:
    def test_valid_station(self, valid_station_row):
        parsed = _parse_station(valid_station_row, "start_station")

        assert parsed == ("1", "Høyteknologisenteret", "60.382216", "5.332288", "66")

    def test_missing_station_id(self, valid_station_row):
        valid_station_row["start_station_id"] = ""

        assert _parse_station(valid_station_row, "start_station_id") is None

    def test_missing_station_name(self, valid_station_row):
        valid_station_row["start_station_name"] = "  "

        assert _parse_station(valid_station_row, "start_station_name") is None
