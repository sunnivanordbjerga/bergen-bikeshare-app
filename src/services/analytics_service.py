"""Provides KPIs and aggregated analytics data."""

from dataclasses import dataclass

from repositories.bike_repository import get_fleet_availability
from repositories.subscription_repository import get_total_revenue, get_revenue_by_month
from repositories.trip_repository import get_num_active_trips, get_trip_count_by_month


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


def _get_dashboard_kpis() -> DashboardKPIs:
    """Return the current dashboard KPIs."""
    return DashboardKPIs(
        fleet_availability=get_fleet_availability(),
        active_rides=get_num_active_trips(),
        total_revenue=get_total_revenue(),
        subscriptions_sold=get_num_active_trips(),
    )


def get_dashboard_data() -> DashboardData:
    """Return the current dashboard data."""
    return DashboardData(
        kpis=_get_dashboard_kpis(),
        revenue_by_month=get_revenue_by_month(),
        trips_by_month=get_trip_count_by_month(),
    )


result = _get_dashboard_kpis()
print(
    result.active_rides,
    result.total_revenue,
    result.fleet_availability,
    result.subscriptions_sold,
)
