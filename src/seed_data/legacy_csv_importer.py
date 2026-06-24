"""
Parses and imports CSV data from bysykkel.csv into the SQLite database.
"""

import csv
import sqlite3
from datetime import timedelta, datetime
from pathlib import Path
from dataclasses import dataclass

from database.connection import get_connection
from models.subscription_type import SubscriptionType
from repositories.subscription_repository import get_subscription_types


@dataclass
class ParsedData:
    """Normalized records extracted from the legacy CSV dataset."""

    stations: list[tuple]
    users: list[tuple]
    bikes: list[tuple]
    subscriptions: list[tuple]
    trips: list[tuple]


def _load_activity_statuses(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        """
        SELECT ActivityStatusID, Description
        FROM ActivityStatus;
        """
    ).fetchall()

    return {description: activity_id for activity_id, description in rows}


def _load_subscription_types(conn: sqlite3.Connection) -> dict[str, SubscriptionType]:
    return {sub_type.description: sub_type for sub_type in get_subscription_types()}


def _parse_station(row: dict, prefix: str) -> tuple | None:
    station_id = row.get(f"{prefix}_id")
    station_name = row.get(f"{prefix}_name", "").strip()
    latitude = row.get(f"{prefix}_latitude")
    longitude = row.get(f"{prefix}_longitude")
    max_capacity = row.get(f"{prefix}_max_spots")

    if not all([station_id, station_name, latitude, longitude, max_capacity]):
        return None

    return (
        station_id,
        station_name,
        latitude,
        longitude,
        max_capacity,
    )


def _parse_user(row: dict) -> tuple | None:
    user_id = row.get("user_id")
    user_name = row.get("user_name", "").strip()
    phone_number = row.get("user_phone_number", "").strip()

    if not all([user_id, user_name, phone_number]):
        return None

    name = user_name.split(" ", maxsplit=1)
    fname = name[0]
    lname = name[1] if len(name) > 1 else ""

    return user_id, fname, lname, phone_number, None, None


def _parse_bike(row: dict, activity_statuses: dict[str, int]) -> tuple | None:
    bike_id = row.get("bike_id")
    bike_name = row.get("bike_name", "").strip()
    activity_status = row.get("bike_status", "").strip()

    if not activity_status:
        return None

    activity_status_id = activity_statuses.get(activity_status)

    if not bike_id or not bike_name or activity_status_id is None:
        return None

    return bike_id, bike_name, row["bike_station_id"] or None, activity_status_id


def _parse_subscription(
    row: dict, sub_types: dict[str, SubscriptionType]
) -> tuple | None:
    sub_id = row.get("subscription_id")
    user_id = row.get("user_id")
    start_date_str = row.get("subscription_start_time")
    sub_type_description = row.get("subscription_type", "").strip()

    if not sub_type_description:
        return None

    sub_type = sub_types.get(sub_type_description)

    if sub_type is None or not all([sub_id, user_id, start_date_str]):
        return None

    start_date = datetime.fromisoformat(start_date_str).date()
    end_date = start_date + timedelta(days=sub_type.duration_in_days)

    return (
        sub_id,
        user_id,
        str(start_date),
        str(end_date),
        sub_type.subscription_type_id,
    )


def _parse_trip(row: dict) -> tuple | None:
    trip_id = row.get("trip_id")
    user_id = row.get("user_id")
    bike_id = row.get("bike_id")
    start_station = row.get("start_station_id")
    start_time = row.get("trip_start_time")

    if not all([trip_id, user_id, bike_id, start_station, start_time]):
        return None

    return (
        trip_id,
        user_id,
        bike_id,
        start_station,
        row["end_station_id"] or None,
        start_time,
        row["trip_end_time"] or None,
    )


def _extract_data(csv_path: Path) -> ParsedData:
    """Extracts normalized records from a legacy CSV dataset."""
    with get_connection() as conn:
        activity_statuses = _load_activity_statuses(conn)
        subscription_types = _load_subscription_types(conn)

    station_data: list[tuple] = []
    seen_stations: set[str] = set()
    bike_data: list[tuple] = []
    seen_bikes: set[str] = set()
    user_data: list[tuple] = []
    seen_users: set[str] = set()
    sub_data: list[tuple] = []
    trip_data: list[tuple] = []

    with csv_path.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for prefix in ["start_station", "end_station"]:
                station = _parse_station(row, prefix)

                if station and station[0] not in seen_stations:
                    seen_stations.add(station[0])
                    station_data.append(station)

            user = _parse_user(row)
            if user and user[0] not in seen_users:
                seen_users.add(user[0])
                user_data.append(user)

            bike = _parse_bike(row, activity_statuses)
            if bike and bike[0] not in seen_bikes:
                seen_bikes.add(bike[0])
                bike_data.append(bike)

            subscription = _parse_subscription(row, subscription_types)
            if subscription:
                sub_data.append(subscription)

            trip = _parse_trip(row)
            if trip:
                trip_data.append(trip)

    return ParsedData(
        stations=station_data,
        users=user_data,
        bikes=bike_data,
        subscriptions=sub_data,
        trips=trip_data,
    )


def _insert_data(data: ParsedData) -> None:
    """Insert extracted data from the legacy CSV file into the database."""
    with get_connection() as conn:
        cur = conn.cursor()

        cur.executemany(
            """
            INSERT OR IGNORE INTO Station
                (StationID, StationName, Latitude, Longitude, MaxCapacity)
            VALUES (?, ?, ?, ?, ?);
            """,
            data.stations,
        )

        cur.executemany(
            """
            INSERT OR IGNORE INTO User
                (UserID, FirstName, LastName, PhoneNr, Latitude, Longitude)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            data.users,
        )

        cur.executemany(
            """
            INSERT OR IGNORE INTO Bike
                (BikeID, BikeName, LastStationID, ActivityStatusID)
            VALUES (?, ?, ?, ?);
            """,
            data.bikes,
        )

        cur.executemany(
            """
            INSERT OR IGNORE INTO Subscription
                (SubscriptionID, UserID, StartDate, EndDate, SubscriptionTypeID)
            VALUES (?, ?, ?, ?, ?);
            """,
            data.subscriptions,
        )

        cur.executemany(
            """
            INSERT OR IGNORE INTO Trip
                (TripID, UserID, BikeID, StartStationID, EndStationID, StartTime, EndTime)
            VALUES (?,?,?,?,?,?,?); 
            """,
            data.trips,
        )


def import_legacy_csv_dataset(csv_path: Path) -> None:
    """
    Import a legacy CSV dataset into the database.

    Args:
        csv_path: Path to the CSV file to import.
    """
    data = _extract_data(csv_path)
    _insert_data(data)
