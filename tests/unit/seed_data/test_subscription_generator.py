import pytest
import datetime as dt
from dateutil.relativedelta import relativedelta

from models.subscription_type import SubscriptionType
from seed_data.generators.subscription_generator import generate_subscriptions

USER_IDS = [1, 2, 3]
SUB_TYPES = [
    SubscriptionType(
        subscription_type_id=4, description="Type1", duration_in_days=1, price=10
    ),
    SubscriptionType(
        subscription_type_id=5, description="Type2", duration_in_days=2, price=20
    ),
    SubscriptionType(
        subscription_type_id=6, description="Type3", duration_in_days=3, price=30
    ),
    SubscriptionType(
        subscription_type_id=7, description="Type4", duration_in_days=4, price=40
    ),
]


def test_generate_subs_returns_correct_amount():
    subs = generate_subscriptions(5, USER_IDS, SUB_TYPES)
    assert len(subs) == 5


def test_generate_zero_subs_returns_empty_list():
    subs = generate_subscriptions(0, USER_IDS, SUB_TYPES)
    assert subs == []


def test_generate_negative_subs_raises_value_error():
    with pytest.raises(ValueError):
        generate_subscriptions(-1, USER_IDS, SUB_TYPES)


def test_generated_subs_use_existing_types():
    subs = generate_subscriptions(10, USER_IDS, SUB_TYPES)

    for sub in subs:
        assert sub.user_id in USER_IDS
        assert sub.sub_type in SUB_TYPES


def test_generated_subs_use_correct_start_date_range():
    subs = generate_subscriptions(10, USER_IDS, SUB_TYPES)
    now = dt.date.today()

    for sub in subs:
        assert (
            (now - relativedelta(years=8))
            <= dt.date.fromisoformat(sub.start_date)
            <= now
        )


def test_generated_subs_use_correct_duration():
    subs = generate_subscriptions(10, USER_IDS, SUB_TYPES)

    for sub in subs:
        assert dt.date.fromisoformat(sub.end_date) == dt.date.fromisoformat(
            sub.start_date
        ) + dt.timedelta(days=sub.sub_type.duration_in_days)
