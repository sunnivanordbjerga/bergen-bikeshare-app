from dataclasses import dataclass


@dataclass
class SubscriptionType:
    """Represents a subscription stored in the database"""

    subscription_type_id: int
    description: str
    duration_in_days: int
    price: float
