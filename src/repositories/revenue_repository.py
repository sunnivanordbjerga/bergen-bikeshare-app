"""Database access methods for revenue."""

import sqlite3


class RevenueRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_total_revenue(self) -> int:
        """Returns the total revenue over the last year."""
        return self.conn.execute("""
                                 SELECT COALESCE(SUM(ST.Price), 0) AS Revenue
                                 FROM Subscription AS S
                                          JOIN SubscriptionType AS ST ON
                                     S.SubscriptionTypeID = ST.SubscriptionTypeID
                                 WHERE S.StartDate >= date('now', '-1 year');
                                 """).fetchone()["Revenue"]

    def get_revenue_by_month(self) -> dict[str, int]:
        """Return an overview of revenue per month over the last year."""
        return {
            month: revenue
            for month, revenue in self.conn.execute("""
                                                    SELECT strftime('%Y-%m', S.StartDate) as YearAndMonth,
                                                           SUM(ST.Price)                  AS Revenue
                                                    FROM Subscription AS S
                                                             JOIN SubscriptionType AS ST ON S.SubscriptionTypeID = ST.SubscriptionTypeID
                                                    WHERE S.StartDate >= date('now', '-1 year')
                                                    GROUP BY YearAndMonth
                                                    ORDER BY YearAndMonth;
                                                    """).fetchall()
        }

    def get_revenue_by_subscription_type(self) -> dict[str, int]:
        """Return an overview of revenue per subscription type over the last year."""
        return {
            sub_type: revenue
            for sub_type, revenue in self.conn.execute("""
                                                       SELECT ST.Description,
                                                              SUM(ST.Price) AS Revenue
                                                       FROM Subscription AS S
                                                                JOIN SubscriptionType AS ST ON S.SubscriptionTypeID = ST.SubscriptionTypeID
                                                       WHERE S.StartDate >= date('now', '-1 year')
                                                       GROUP BY ST.SubscriptionTypeID, ST.Description, ST.DurationInDays
                                                       ORDER BY ST.DurationInDays;
                                                       """).fetchall()
        }
