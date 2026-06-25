"""Database access methods for subscriptions"""

from database.connection import get_connection
from models.subscription import Subscription
from models.subscription_type import SubscriptionType


def get_subscriptions() -> list[Subscription]:
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


def get_subscription_types() -> list[SubscriptionType]:
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


def get_subscription_count_by_month() -> dict[str, int]:
    """Return an overview of subscriptions sold per month over the last year."""
    with get_connection() as conn:
        return {
            month: sub_count
            for month, sub_count in conn.execute("""
                                                 SELECT strftime('%Y-%m', StartDate) as YearAndMonth,
                                                        COUNT(SubscriptionID)        AS SubscriptionCount
                                                 FROM Subscription
                                                 WHERE StartDate >= date('now', '-1 year')
                                                 GROUP BY YearAndMonth
                                                 ORDER BY YearAndMonth;
                                                 """).fetchall()
        }


def get_subscription_count_by_type() -> dict[str, int]:
    """Return an overview of subscriptions sold per subscription type over the last year."""
    with get_connection() as conn:
        return {
            sub_type: sub_count
            for sub_type, sub_count in conn.execute("""
                                                    SELECT ST.Description,
                                                           COUNT(S.SubscriptionTypeID) AS SubscriptionCount
                                                    FROM Subscription AS S
                                                             JOIN SubscriptionType AS ST ON S.SubscriptionTypeID = ST.SubscriptionTypeID
                                                    WHERE S.StartDate >= date('now', '-1 year')
                                                    GROUP BY ST.SubscriptionTypeID, ST.Description, ST.DurationInDays
                                                    ORDER BY ST.DurationInDays;
                                                    """).fetchall()
        }


def get_total_subscription_count() -> int:
    """Returns the total number of subscriptions sold over the last year."""
    with get_connection() as conn:
        return conn.execute("""
                            SELECT COALESCE(COUNT(SubscriptionID), 0) AS Total
                            FROM Subscription
                            WHERE StartDate >= date('now', '-1 year')
                            """).fetchone()[0]


def get_total_revenue() -> int:
    """Returns the total revenue over the last year."""
    with get_connection() as conn:
        return conn.execute("""
                            SELECT COALESCE(SUM(ST.Price), 0)
                            FROM Subscription AS S
                                     JOIN SubscriptionType AS ST ON
                                S.SubscriptionTypeID = ST.SubscriptionTypeID
                            WHERE S.StartDate >= date('now', '-1 year');
                            """).fetchone()[0]


def get_revenue_by_month() -> dict[str, int]:
    """Return an overview of revenue per month over the last year."""
    with get_connection() as conn:
        return {
            month: revenue
            for month, revenue in conn.execute("""
                                               SELECT strftime('%Y-%m', S.StartDate) as YearAndMonth,
                                                      SUM(ST.Price)                  AS Revenue
                                               FROM Subscription AS S
                                                        JOIN SubscriptionType AS ST ON S.SubscriptionTypeID = ST.SubscriptionTypeID
                                               WHERE S.StartDate >= date('now', '-1 year')
                                               GROUP BY YearAndMonth
                                               ORDER BY YearAndMonth;
                                               """).fetchall()
        }


def get_revenue_by_subscription_type() -> dict[str, int]:
    """Return an overview of revenue per subscription type over the last year."""
    with get_connection() as conn:
        return {
            sub_type: revenue
            for sub_type, revenue in conn.execute("""
                                                  SELECT ST.Description,
                                                         SUM(ST.Price) AS Revenue
                                                  FROM Subscription AS S
                                                           JOIN SubscriptionType AS ST ON S.SubscriptionTypeID = ST.SubscriptionTypeID
                                                  WHERE S.StartDate >= date('now', '-1 year')
                                                  GROUP BY ST.SubscriptionTypeID, ST.Description, ST.DurationInDays
                                                  ORDER BY ST.DurationInDays;
                                                  """).fetchall()
        }
