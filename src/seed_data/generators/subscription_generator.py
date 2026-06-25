"""Generates fake subscriptions."""

from datetime import timedelta
from random import choice, choices
from dataclasses import dataclass
from faker import Faker

from models.subscription_type import SubscriptionType

SUB_TYPE_WEIGHTS = [40, 20, 30, 10]

fake = Faker("no_NO")


@dataclass
class GeneratedSubscription:
    user_id: int
    start_date: str
    end_date: str
    sub_type: SubscriptionType


def generate_subscriptions(
    num_subs: int,
    user_ids: list[int],
    sub_types: list[SubscriptionType],
) -> list[GeneratedSubscription]:
    """
    Generates a list with the specified number of fake subscriptions.

    Args:
        num_subs: Number of subscriptions to generate.
        user_ids: List of existing user IDs.
        sub_types: List of existing subscription types.

    Returns:
        A list of generated subscriptions.
    """
    if num_subs < 0:
        raise ValueError("num_subs cannot be negative.")

    subscriptions = []
    for _ in range(num_subs):
        sub_type = choices(sub_types, SUB_TYPE_WEIGHTS, k=1)[0]
        start = fake.date_between(start_date="-2y", end_date="now")
        end = start + timedelta(days=sub_type.duration_in_days)
        subscriptions.append(
            GeneratedSubscription(
                user_id=choice(user_ids),
                start_date=str(start),
                end_date=str(end),
                sub_type=sub_type,
            )
        )

    return subscriptions
