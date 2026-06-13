"""Generates fake users."""

from random import uniform
from dataclasses import dataclass
from faker import Faker

fake = Faker("no_NO")

BERGEN_MIN_LAT = 60.1017
BERGEN_MAX_LAT = 60.6167

BERGEN_MIN_LON = 5.0833
BERGEN_MAX_LON = 5.8533


@dataclass
class GeneratedUser:
    first_name: str
    last_name: str
    phone_number: str
    latitude: float
    longitude: float


def generate_users(num_users: int) -> list[GeneratedUser]:
    """
    Generates a list with the specified number of fake users.

    Args:
        num_users: Number of users to generate.

    Returns:
        A list of generated users.
    """

    return [
        GeneratedUser(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number(),
            latitude=round(uniform(BERGEN_MIN_LAT, BERGEN_MAX_LAT), 6),
            longitude=round(uniform(BERGEN_MIN_LON, BERGEN_MAX_LON), 6),
        )
        for _ in range(num_users)
    ]
