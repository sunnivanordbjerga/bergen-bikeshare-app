from seed_data.generators.trip_generator import generate_trips

USER_IDS = [1, 2, 3]
BIKE_IDS = [4, 5, 6]
STATION_IDS = [7, 8, 9, 10]


def test_generate_trips_returns_correct_amount():
    trips = generate_trips(5, USER_IDS, BIKE_IDS, STATION_IDS)
    assert len(trips) == 5
