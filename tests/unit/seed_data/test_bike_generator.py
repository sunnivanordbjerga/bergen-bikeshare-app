import pytest

from seed_data.generators.bike_generator import generate_bikes

STATION_IDS = [1, 2, 3, 4]
ACTIVITY_STATUS_IDS = [5, 6, 7, 8]


def test_generate_bikes_returns_correct_amount():
    bikes = generate_bikes(5, STATION_IDS, ACTIVITY_STATUS_IDS)
    assert len(bikes) == 5


def test_generate_zero_bikes_returns_empty_list():
    bikes = generate_bikes(0, STATION_IDS, ACTIVITY_STATUS_IDS)
    assert bikes == []


def test_generate_negative_bikes_raises_value_error():
    with pytest.raises(ValueError):
        generate_bikes(-1, STATION_IDS, ACTIVITY_STATUS_IDS)


def test_generated_bikes_use_existing_ids():
    bikes = generate_bikes(10, STATION_IDS, ACTIVITY_STATUS_IDS)
    for bike in bikes:
        assert bike.last_station_id in STATION_IDS
        assert bike.activity_status_id in ACTIVITY_STATUS_IDS
