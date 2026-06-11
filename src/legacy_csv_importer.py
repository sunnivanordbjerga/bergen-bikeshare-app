"""
Parses and imports CSV data from bysykkel.csv into the SQLite database.
"""

import csv
import sqlite3
from pathlib import Path
from dataclasses import dataclass

from database.connection import get_connection


@dataclass
class ParsedData:
    """Normalised records extracted from the legacy CSV dataset."""

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


def _load_subscription_types(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        """
        SELECT SubscriptionTypeID, Description
        FROM SubscriptionType;
        """
    ).fetchall()

    return {description: sub_id for sub_id, description in rows}


def _parse_station(row: dict, prefix: str) -> tuple | None:
    station_id = row.get(f"{prefix}_id")

    if not station_id:
        return None

    return (
        station_id,
        row[f"{prefix}_name"],
        row[f"{prefix}_latitude"],
        row[f"{prefix}_longitude"],
        row[f"{prefix}_max_spots"],
    )


def _parse_user(row: dict) -> tuple | None:
    user_id = row.get("user_id")
    user_name = row.get("user_name")
    phone_number = row.get("user_phone_number")

    if not user_id or not user_name or not phone_number:
        return None

    name = user_name.split(" ", maxsplit=1)
    fname = name[0]
    lname = name[1] if len(name) > 1 else ""

    return user_id, fname, lname, phone_number, None, None


def _parse_bike(row: dict, activity_statuses: dict) -> tuple | None:
    # TODO: Parse bikes, lookup activityStatus
    pass


def _parse_subscription(row: dict, sub_types: dict) -> tuple | None:
    sub_id = row.get("subscription_id")
    user_id = row.get("user_id")
    start_date = row.get("subscription_start_time")
    sub_type = sub_types.get(row.get("subscription_type"))

    if not all([sub_id, user_id, start_date, sub_type]):
        return None

    return sub_id, user_id, start_date, sub_type


def _parse_trip(row: dict) -> tuple | None:  # TODO: Parse trips using FKs
    pass


def _extract_data(csv_path: Path) -> ParsedData:
    """Extracts normalized records from a legacy CSV dataset."""
    with get_connection() as conn:
        activity_statuses = _load_activity_statuses(conn)
        subscription_types = _load_subscription_types(conn)

    station_data = []
    seen_stations = set()
    bike_data = []
    seen_bikes = set()
    user_data = []
    seen_users = set()
    sub_data = []
    trip_data = []

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
                (SubscriptionID, UserID, StartDate, SubscriptionTypeID)
            VALUES (?, ?, ?, ?);
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
