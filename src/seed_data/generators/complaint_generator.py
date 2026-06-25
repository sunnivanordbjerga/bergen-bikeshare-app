"""Generates fake complaints."""

from datetime import timedelta
from random import choice, random
from dataclasses import dataclass

from dateutil.relativedelta import relativedelta
from faker import Faker

fake = Faker("no_NO")
RESOLVED_PROBABILITY = 0.8


@dataclass
class GeneratedComplaint:
    bike_id: int
    user_id: int
    complaint_type_id: int
    report_date: str
    resolved: bool
    resolved_date: str | None


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
        bike_ids: List of existing bike IDs.
        user_ids: List of existing user IDs.
        complaint_type_ids: List of existing complaint type IDs.

    Returns:
        A list of generated complaints.
    """
    if num_complaints < 0:
        raise ValueError("num_complaints cannot be negative.")

    complaints = []

    for _ in range(num_complaints):
        resolved = random() < RESOLVED_PROBABILITY

        reported = (
            fake.date_time_between(start_date="-3y", end_date="now")
            if resolved
            else fake.date_time_between(start_date="-6m", end_date="now")
        )
        resolved_date = (
            fake.date_time_between(
                start_date=reported + timedelta(hours=1),
                end_date=reported + relativedelta(months=3),
            )
            if resolved
            else None
        )

        complaints.append(
            GeneratedComplaint(
                bike_id=choice(bike_ids),
                user_id=choice(user_ids),
                complaint_type_id=choice(complaint_type_ids),
                report_date=str(reported),
                resolved=resolved,
                resolved_date=str(resolved_date) if resolved else None,
            )
        )

    return complaints
