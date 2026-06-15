"""Generates fake users."""

from random import uniform, random
from dataclasses import dataclass

from faker import Faker

BERGEN_MIN_LAT = 60.1017
BERGEN_MAX_LAT = 60.6167

BERGEN_MIN_LON = 5.0833
BERGEN_MAX_LON = 5.8533

INTERNATIONAL_USER_PERCENTAGE = 0.15
INTERNATIONAL_LOCALES = ["en_US", "de_DE", "pl_PL", "uk_UA"]

fake_no = Faker("no_NO")
fake_inter = Faker(INTERNATIONAL_LOCALES)


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
    users = []

    for _ in range(num_users):
        fake = fake_no if random() > INTERNATIONAL_USER_PERCENTAGE else fake_inter

        users.append(
            GeneratedUser(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake_no.phone_number(),
                latitude=round(uniform(BERGEN_MIN_LAT, BERGEN_MAX_LAT), 6),
                longitude=round(uniform(BERGEN_MIN_LON, BERGEN_MAX_LON), 6),
            )
        )

    return users
