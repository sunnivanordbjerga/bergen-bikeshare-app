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
            fleet_availability=self.get_fleet_availability(),
            active_rides=self.trip_repository.get_active_trips_count(),
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

    def get_fleet_availability(self) -> float:
        """Returns the current percentage of available bikes"""
        total = self.bike_repository.get_total_bikes_count()
        parked = self.bike_repository.get_parked_bikes_count()

        if total == 0:
            return 0.0

        return round((float(total) / float(parked) * 100), 1)

    def get_trip_count_by_station(self):
        """Returns an overview of departures and arrivals per station."""



    def get_trip_count_by_month(self, station_id: int | None = None) -> dict[str, int]:
        """Returns an overview of total trips per month, optionally filtered by station."""
