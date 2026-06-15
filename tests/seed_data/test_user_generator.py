from seed_data.generators.user_generator import generate_users

USER_IDS = [1, 2, 3]
BIKE_IDS = [4, 5, 6]
STATION_IDS = [7, 8, 9, 10]


def test_generate_users_returns_correct_amount():
    users = generate_users(5)
    assert len(users) == 5