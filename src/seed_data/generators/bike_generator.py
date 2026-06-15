"""Generates fake bikes."""

from random import choice, choices
from dataclasses import dataclass
from faker import Faker

ACTIVITY_STATUS_WEIGHTS = [70, 20, 8, 2]

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
    if num_bikes < 0:
        raise ValueError("num_bikes cannot be negative.")

    return [
        GeneratedBike(
            bike_name=fake.unique.first_name(),
            last_station_id=choice(station_ids),
            activity_status_id=choices(
                activity_status_ids, ACTIVITY_STATUS_WEIGHTS, k=1
            )[0],
        )
        for _ in range(num_bikes)
    ]
