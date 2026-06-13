"""Generates fake users."""

from dataclasses import dataclass
from faker import Faker

fake = Faker("nb_NO")


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
            latitude=float(fake.latitude()),
            longitude=float(fake.longitude()),
        )
        for _ in range(num_users)
    ]
