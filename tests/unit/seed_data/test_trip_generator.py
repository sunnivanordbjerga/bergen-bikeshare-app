import pytest
import datetime as dt
from dateutil.relativedelta import relativedelta
from seed_data.generators.trip_generator import generate_trips, _generate_trip

USER_IDS = [1, 2, 3]
BIKE_IDS = [4, 5, 6]
STATION_IDS = [7, 8, 9, 10]


def test_generate_trips_returns_correct_amount():
    trips = generate_trips(5, USER_IDS, BIKE_IDS, STATION_IDS)
    assert len(trips) == 5


def test_generate_zero_trips_returns_empty_list():
    trips = generate_trips(0, USER_IDS, BIKE_IDS, STATION_IDS)
    assert trips == []


def test_generate_negative_trips_raises_value_error():
    with pytest.raises(ValueError):
        generate_trips(-1, USER_IDS, BIKE_IDS, STATION_IDS)


def test_generated_trips_use_existing_ids():
    trips = generate_trips(10, USER_IDS, BIKE_IDS, STATION_IDS)

    for trip in trips:
        assert trip.user_id in USER_IDS
        assert trip.bike_id in BIKE_IDS
        assert trip.start_station_id in STATION_IDS


def test_complete_trip_uses_existing_end_station():
    trip = _generate_trip(USER_IDS, BIKE_IDS, STATION_IDS, active_trip=False)
    assert trip.end_station_id in STATION_IDS


def test_trip_start_time_uses_correct_range():
    trips = generate_trips(10, USER_IDS, BIKE_IDS, STATION_IDS)
    now = dt.datetime.now()

    for trip in trips:
        start_time = dt.datetime.strptime(trip.start_time, "%Y-%m-%d %H:%M:%S")

        assert now - relativedelta(months=6) <= start_time <= now


def test_completed_trip_end_time_is_after_start_time():
    trip = _generate_trip(USER_IDS, BIKE_IDS, STATION_IDS, active_trip=False)

    start_time = dt.datetime.strptime(trip.start_time, "%Y-%m-%d %H:%M:%S")
    end_time = dt.datetime.strptime(trip.end_time, "%Y-%m-%d %H:%M:%S")

    assert start_time < end_time


def test_completed_trip_duration_uses_correct_range():
    trips = [
        _generate_trip(USER_IDS, BIKE_IDS, STATION_IDS, active_trip=False)
        for _ in range(5)
    ]
    for trip in trips:
        start_time = dt.datetime.strptime(trip.start_time, "%Y-%m-%d %H:%M:%S")
        end_time = dt.datetime.strptime(trip.end_time, "%Y-%m-%d %H:%M:%S")

        assert 5 <= ((end_time - start_time).total_seconds()) // 60 <= 180


def test_active_trip_end_time_and_end_station_is_none():
    trip = _generate_trip(
        USER_IDS,
        BIKE_IDS,
        STATION_IDS,
        active_trip=True,
    )

    assert trip.end_time is None
    assert trip.end_station_id is None
