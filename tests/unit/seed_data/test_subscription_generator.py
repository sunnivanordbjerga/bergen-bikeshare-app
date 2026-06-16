import pytest
import datetime as dt
from dateutil.relativedelta import relativedelta
from seed_data.generators.subscription_generator import generate_subscriptions

USER_IDS = [1, 2, 3]
SUB_TYPE_IDS = [4, 5, 6, 7]


def test_generate_subs_returns_correct_amount():
    subs = generate_subscriptions(5, USER_IDS, SUB_TYPE_IDS)
    assert len(subs) == 5


def test_generate_zero_subs_returns_empty_list():
    subs = generate_subscriptions(0, USER_IDS, SUB_TYPE_IDS)
    assert subs == []


def test_generate_negative_subs_raises_value_error():
    with pytest.raises(ValueError):
        generate_subscriptions(-1, USER_IDS, SUB_TYPE_IDS)


def test_generated_subs_use_existing_ids():
    subs = generate_subscriptions(10, USER_IDS, SUB_TYPE_IDS)

    for sub in subs:
        assert sub.user_id in USER_IDS
        assert sub.sub_type_id in SUB_TYPE_IDS


def test_generated_subs_use_correct_date_range():
    subs = generate_subscriptions(10, USER_IDS, SUB_TYPE_IDS)
    now = dt.datetime.now()

    for sub in subs:
        assert (
            (now - relativedelta(years=8))
            <= dt.datetime.strptime(sub.start_date, "%Y-%m-%d %H:%M:%S")
            <= now
        )
