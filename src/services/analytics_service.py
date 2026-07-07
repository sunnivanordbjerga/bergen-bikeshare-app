"""Provides KPIs and aggregated analytics data."""

import sqlite3
from dataclasses import dataclass

from repositories.bike_repository import BikeRepository
from repositories.subscription_repository import SubscriptionRepository
from repositories.trip_repository import TripRepository


@dataclass
class DashboardKPIs:
    """Key performance indicators displayed on the dashboard"""

    fleet_availability: float
    active_rides: int
    total_revenue: float
    subscriptions_sold: int


@dataclass
class DashboardData:
    """Aggregated data displayed on the dashboard"""

    kpis: DashboardKPIs
    revenue_by_month: dict[str, int]
    trips_by_month: dict[str, int]


class AnalyticsService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.bike_repository = BikeRepository(conn)
        self.subscription_repository = SubscriptionRepository(conn)
        self.trip_repository = TripRepository(conn)

    def _get_dashboard_kpis(self) -> DashboardKPIs:
        """Return the current dashboard KPIs."""
        return DashboardKPIs(
            fleet_availability=self.bike_repository.get_fleet_availability(),
            active_rides=self.trip_repository.get_num_active_trips(),
            total_revenue=self.subscription_repository.get_total_revenue(),
            subscriptions_sold=self.subscription_repository.get_total_subscription_count(),
        )

    def get_dashboard_data(self) -> DashboardData:
        """Return the current dashboard data."""
        return DashboardData(
            kpis=self._get_dashboard_kpis(),
            revenue_by_month=self.subscription_repository.get_revenue_by_month(),
            trips_by_month=self.trip_repository.get_trip_count_by_month(),
        )
