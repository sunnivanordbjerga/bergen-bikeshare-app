"""Generates fake complaints."""

from random import choice
from dataclasses import dataclass
from faker import Faker

fake = Faker("no_NO")


@dataclass
class GeneratedComplaint:
    bike_id: int
    user_id: int
    complaint_type_id: int
    report_date: str


def generate_complaints(
    num_complaints: int,
    user_ids: list[int],
    bike_ids: list[int],
    complaint_type_ids: list[int],
) -> list[GeneratedComplaint]:
    """
    Generates a list with the specified number of fake complaints.

    Args:
        num_complaints: Number of complaints to generate.
        bike_ids: List of existing bike ids.
        user_ids: List of existing user ids.
        complaint_type_ids: List of existing complaint type ids.

    Returns:
        A list of generated complaints.
    """

    return [
        GeneratedComplaint(
            bike_id=choice(bike_ids),
            user_id=choice(user_ids),
            complaint_type_id=choice(complaint_type_ids),
            report_date=str(fake.date_time_between(start_date="-6M", end_date="now")),
        )
        for _ in range(num_complaints)
    ]
