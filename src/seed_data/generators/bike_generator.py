"""Generates fake bikes."""

from random import choice
from dataclasses import dataclass
from faker import Faker

fake = Faker("no_NO")


@dataclass
class GeneratedBike:
    bike_name: str
    last_station_id: int
    activity_status_id: int


def generate_bikes(
    num_bikes: int, station_ids: list[int], activity_status_ids: list[int]
) -> list[GeneratedBike]:
    """
    Generates a list with the specified number of fake bikes.

    Args:
        num_bikes: Number of bikes to generate.
        station_ids: List of existing station IDs.
        activity_status_ids: List of existing activity status IDs.

    Returns:
        A list of generated bikes.
    """

    return [
        GeneratedBike(
            bike_name=fake.first_name(),
            last_station_id=choice(station_ids),
            activity_status_id=choice(activity_status_ids),
        )
        for _ in range(num_bikes)
    ]
