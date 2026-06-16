import pytest

from seed_data.generators.user_generator import (
    generate_users,
    BERGEN_MIN_LAT,
    BERGEN_MAX_LAT,
    BERGEN_MIN_LON,
    BERGEN_MAX_LON,
)


def test_generate_users_returns_correct_amount():
    users = generate_users(5)
    assert len(users) == 5


def test_generate_zero_users_returns_empty_list():
    users = generate_users(0)
    assert users == []


def test_generate_negative_users_raises_value_error():
    with pytest.raises(ValueError):
        generate_users(-1)


def test_generated_users_have_valid_phone_numbers():
    users = generate_users(5)
    for user in users:
        phone_number = user.phone_number.replace(" ", "").replace("-", "").strip()

        assert 8 <= len(phone_number) <= 11


def test_generated_users_use_correct_location_range():
    users = generate_users(5)
    for user in users:
        assert BERGEN_MIN_LAT <= user.latitude <= BERGEN_MAX_LAT
        assert BERGEN_MIN_LON <= user.longitude <= BERGEN_MAX_LON
