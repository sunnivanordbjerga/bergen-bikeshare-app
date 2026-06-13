import pytest
from legacy_csv_importer import _parse_station, _parse_user, _parse_bike, _parse_subscription


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
    return {"user_id": "1", "user_name": "Jane Doe", "user_phone_number": "12345678"}


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
    def test_valid_station_returns_correct_values(self, valid_station_row):
        parsed = _parse_station(valid_station_row, "start_station")

        assert parsed == ("1", "Høyteknologisenteret", "60.382216", "5.332288", "66")

    def test_missing_station_id_returns_none(self, valid_station_row):
        valid_station_row["start_station_id"] = ""

        assert _parse_station(valid_station_row, "start_station") is None

    def test_missing_station_name_returns_none(self, valid_station_row):
        valid_station_row["start_station_name"] = "  "

        assert _parse_station(valid_station_row, "start_station") is None

    def test_missing_latitude_returns_none(self, valid_station_row):
        valid_station_row["start_station_latitude"] = ""

        assert _parse_station(valid_station_row, "start_station") is None

    def test_missing_longitude_returns_none(self, valid_station_row):
        valid_station_row["start_station_longitude"] = ""

        assert _parse_station(valid_station_row, "start_station") is None

    def test_missing_max_capacity_returns_none(self, valid_station_row):
        valid_station_row["start_station_max_spots"] = ""

        assert _parse_station(valid_station_row, "start_station") is None


class TestParseUser:
    def test_valid_user_returns_correct_values(self, valid_user_row):
        parsed = _parse_user(valid_user_row)

        assert parsed == ("1", "Jane", "Doe", "12345678", None, None)

    def test_missing_user_id_returns_none(self, valid_user_row):
        valid_user_row["user_id"] = ""

        assert _parse_user(valid_user_row) is None

    def test_blank_name_returns_none(self, valid_user_row):
        valid_user_row["user_name"] = "  "

        assert _parse_user(valid_user_row) is None

    def test_single_name_returns_empty_last_name(self, valid_user_row):
        valid_user_row["user_name"] = "Jane"

        parsed = _parse_user(valid_user_row)

        assert parsed == ("1", "Jane", "", "12345678", None, None)

    def test_missing_phone_number_returns_none(self, valid_user_row):
        valid_user_row["user_phone_number"] = "  "

        assert _parse_user(valid_user_row) is None


class TestParseBike:
    activity_statuses = {"Parked": 1, "Active": 2, "Missing": 3, "Service": 4}

    def test_valid_bike_returns_correct_values(self, valid_bike_row):
        parsed = _parse_bike(valid_bike_row, self.activity_statuses)

        assert parsed == ("1", "Thea", None, 2)

    def test_missing_bike_id_returns_none(self, valid_bike_row):
        valid_bike_row["bike_id"] = ""

        assert _parse_bike(valid_bike_row, self.activity_statuses) is None

    def test_missing_bike_name_returns_none(self, valid_bike_row):
        valid_bike_row["bike_name"] = "  "

        assert _parse_bike(valid_bike_row, self.activity_statuses) is None

    def test_missing_bike_status_returns_none(self, valid_bike_row):
        valid_bike_row["bike_status"] = "  "

        assert _parse_bike(valid_bike_row, self.activity_statuses) is None

    def test_invalid_bike_status_returns_none(self, valid_bike_row):
        valid_bike_row["bike_status"] = "Flying"

        assert _parse_bike(valid_bike_row, self.activity_statuses) is None


class TestParseSubscription:
    sub_types = {"Day": 1, "Week": 2, "Month": 3, "Year": 4}

    def test_valid_subscription_returns_correct_values(self, valid_subscription_row):
        parsed = _parse_subscription(valid_subscription_row, self.sub_types)

        assert parsed == ("1", "1", "2020-09-18 17:22:27", 1)

    def test_missing_subscription_id_returns_none(self, valid_subscription_row):
        valid_subscription_row["subscription_id"] = ""

        assert _parse_subscription(valid_subscription_row, self.sub_types) is None

    def test_missing_subscription_user_id_returns_none(self, valid_subscription_row):
        valid_subscription_row["user_id"] = ""

        assert _parse_subscription(valid_subscription_row, self.sub_types) is None

    def test_missing_subscription_date_returns_none(self, valid_subscription_row):
        valid_subscription_row["subscription_start_time"] = ""

        assert _parse_subscription(valid_subscription_row, self.sub_types) is None

    def test_missing_subscription_type_returns_none(self, valid_subscription_row):
        valid_subscription_row["subscription_type"] = " "

        assert _parse_subscription(valid_subscription_row, self.sub_types) is None

    def test_invalid_subscription_type_returns_none(self, valid_subscription_row):
        valid_subscription_row["subscription_type"] = "Minute"

        assert _parse_subscription(valid_subscription_row, self.sub_types) is None
