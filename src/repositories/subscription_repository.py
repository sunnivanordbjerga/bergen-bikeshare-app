"""Database access methods for subscriptions"""

from database.connection import get_connection
from models.subscription import Subscription
from models.subscription_type import SubscriptionType


def get_subscriptions():
    with get_connection() as conn:
        subscriptions = conn.execute("""
                                     SELECT S.SubscriptionId,
                                            (U.FirstName || ' ' || U.LastName) AS User,
                                            ST.Description,
                                            S.StartDate,
                                            S.EndDate
                                     FROM Subscription AS S
                                              LEFT JOIN USER AS U ON S.UserID = U.UserID
                                              JOIN SubscriptionType AS ST ON ST.SubscriptionTypeID = S.SubscriptionTypeID;
                                     """).fetchall()
    return [
        Subscription(
            subscription_id=row[0],
            user_name=row[1],
            subscription_type=row[2],
            start_date=row[3],
            end_date=row[4],
        )
        for row in subscriptions
    ]


def get_subscription_types():
    with get_connection() as conn:
        types = conn.execute("""
        SELECT SubscriptionTypeId, Description, DurationInDays, Price
        FROM SubscriptionType;
        """).fetchall()

    return [
        SubscriptionType(
            subscription_type_id=row[0],
            description=row[1],
            duration_in_days=row[2],
            price=row[3],
        )
        for row in types
    ]
