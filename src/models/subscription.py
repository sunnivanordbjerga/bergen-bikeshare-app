from dataclasses import dataclass
from datetime import date

from models.subscription_type import SubscriptionType


@dataclass
class Subscription:
    """Represents a subscription stored in the database"""

    subscription_id: int
    user_name: str
    subscription_type: SubscriptionType
    start_date: date
    end_date: date
