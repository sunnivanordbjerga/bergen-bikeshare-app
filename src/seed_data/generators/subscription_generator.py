"""Generates fake subscriptions."""

from random import choice, choices
from dataclasses import dataclass
from faker import Faker

SUB_TYPE_WEIGHTS = [40, 20, 30, 10]

fake = Faker("no_NO")


@dataclass
class GeneratedSubscription:
    user_id: int
    start_date: str
    sub_type_id: int


def generate_subscriptions(
    num_subs: int,
    user_ids: list[int],
    sub_type_ids: list[int],
) -> list[GeneratedSubscription]:
    """
    Generates a list with the specified number of fake subscriptions.

    Args:
        num_subs: Number of subscriptions to generate.
        user_ids: List of existing user IDs.
        sub_type_ids: List of existing subscription type IDs.

    Returns:
        A list of generated subscriptions.
    """
    if num_subs < 0:
        raise ValueError("num_subs cannot be negative.")

    return [
        GeneratedSubscription(
            user_id=choice(user_ids),
            start_date=str(fake.date_time_between(start_date="-8y", end_date="now")),
            sub_type_id=choices(sub_type_ids, SUB_TYPE_WEIGHTS, k=1)[0],
        )
        for _ in range(num_subs)
    ]
