from seed_data.generators.subscription_generator import generate_subscriptions

USER_IDS = [1, 2, 3]
SUB_TYPE_IDS = [4, 5, 6, 7]


def test_generate_subscriptions_returns_correct_amount():
    subs = generate_subscriptions(5, USER_IDS, SUB_TYPE_IDS)
    assert len(subs) == 5
