"""Database access methods for subscriptions"""

import sqlite3
from datetime import datetime as dt

from models.subscription import Subscription
from models.subscription_type import SubscriptionType


class SubscriptionRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_subscriptions(self) -> list[Subscription]:
        """Returns all subscriptions"""
        subscriptions = self.conn.execute("""
                                     SELECT S.SubscriptionId,
                                            (U.FirstName || ' ' || U.LastName) AS User,
                                            ST.SubscriptionTypeID,
                                            ST.Description,
                                            ST.DurationInDays,
                                            ST.Price,
                                            S.StartDate,
                                            S.EndDate
                                     FROM Subscription AS S
                                              LEFT JOIN USER AS U ON S.UserID = U.UserID
                                              JOIN SubscriptionType AS ST ON ST.SubscriptionTypeID = S.SubscriptionTypeID;
                                     """).fetchall()
        return [
            Subscription(
                subscription_id=row["SubscriptionID"],
                user_name=row["User"],
                subscription_type=SubscriptionType(
                    subscription_type_id=row["SubscriptionTypeID"],
                    description=row["Description"],
                    duration_in_days=row["DurationInDays"],
                    price=row["Price"],
                ),
                start_date=dt.fromisoformat(row["StartDate"]),
                end_date=dt.fromisoformat(row["EndDate"]),
            )
            for row in subscriptions
        ]

    def get_subscription_types(self) -> list[SubscriptionType]:
        """Returns a list of subscription types"""
        types = self.conn.execute("""
        SELECT SubscriptionTypeId, Description, DurationInDays, Price
        FROM SubscriptionType;
        """).fetchall()

        return [
            SubscriptionType(
                subscription_type_id=row["SubscriptionTypeID"],
                description=row["Description"],
                duration_in_days=row["DurationInDays"],
                price=row["Price"],
            )
            for row in types
        ]

    def get_subscription_count_by_month(self) -> dict[str, int]:
        """Return an overview of subscriptions sold per month over the last year."""
        return {
            month: sub_count
            for month, sub_count in self.conn.execute("""
                                                 SELECT strftime('%Y-%m', StartDate) as YearAndMonth,
                                                        COUNT(SubscriptionID)        AS SubscriptionCount
                                                 FROM Subscription
                                                 WHERE StartDate >= date('now', '-1 year')
                                                 GROUP BY YearAndMonth
                                                 ORDER BY YearAndMonth;
                                                 """).fetchall()
        }

    def get_subscription_count_by_type(self) -> dict[str, int]:
        """Return an overview of subscriptions sold per subscription type over the last year."""
        return {
            sub_type: sub_count
            for sub_type, sub_count in self.conn.execute("""
                                                    SELECT ST.Description,
                                                           COUNT(S.SubscriptionTypeID) AS SubscriptionCount
                                                    FROM Subscription AS S
                                                             JOIN SubscriptionType AS ST ON S.SubscriptionTypeID = ST.SubscriptionTypeID
                                                    WHERE S.StartDate >= date('now', '-1 year')
                                                    GROUP BY ST.SubscriptionTypeID, ST.Description, ST.DurationInDays
                                                    ORDER BY ST.DurationInDays;
                                                    """).fetchall()
        }

    def get_total_subscription_count(self) -> int:
        """Returns the total number of subscriptions sold over the last year."""
        return self.conn.execute("""
                            SELECT COALESCE(COUNT(SubscriptionID), 0) AS Total
                            FROM Subscription
                            WHERE StartDate >= date('now', '-1 year')
                            """).fetchone()["Total"]
