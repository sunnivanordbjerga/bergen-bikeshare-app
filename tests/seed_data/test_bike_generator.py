from seed_data.generators.bike_generator import generate_bikes

STATION_IDS = [1, 2, 3, 4]
ACTIVITY_STATUS_IDS = [5, 6, 7, 8]


def test_generate_bikes_returns_correct_amount():
    bikes = generate_bikes(5, STATION_IDS, ACTIVITY_STATUS_IDS)
    assert len(bikes) == 5
