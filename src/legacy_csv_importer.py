"""
Parses and imports csv data from bysykkel.csv to the database.
"""

import csv
from pathlib import Path
from dataclasses import dataclass

from database.connection import get_connection


@dataclass
class ParsedData:
    stations: list[tuple]
    users: list[tuple]
    bikes: list[tuple]
    subscriptions: list[tuple]
    trips: list[tuple]


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
        row[f"{prefix}_available_spots"],
    )


def _parse_user(row: dict) -> tuple | None:
    user_id = row.get("user_id")
    user_name = row.get("user_name")
    phone_number = row.get("phone_number")
    
    if not user_id or not user_name or not phone_number:
        return None

    name = user_name.split(" ", maxsplit=1)
    fname = name[0]
    lname = name[1] if len(name) > 1 else ""

    return (
        user_id,
        fname,
        lname,
        phone_number,
        None,
        None
    )


def _parse_bike(row: dict) -> tuple | None:
    #TODO: Parse bikes, lookup activityStatus
    pass


def _parse_subscription(row: dict) -> tuple | None:
    pass


def _parse_trip(row: dict) -> tuple | None:
    pass


def _extract_data(csv_path: Path) -> ParsedData:
    station_data = []
    seen_stations = set()
    bike_data = []
    seen_bike = set()
    user_data = []
    seen_user = set()
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
            if user and user[0] not in seen_user:
                seen_user.add(user[0])
                user_data.append(user)

            bike = _parse_bike(row)
            if bike and bike[0] not in seen_bike:
                seen_bike.add(bike[0])
                bike_data.append(bike)

            subscription = _parse_subscription(row)

            trip = _parse_trip(row)

    return ParsedData(
        stations=station_data,
        users=user_data,
        bikes=bike_data,
        subscriptions=sub_data,
        trips=trip_data,
    )


def _insert_data(data: ParsedData) -> None:
    with get_connection() as conn:
        cur = conn.cursor()

        cur.executemany(
            """
        INSERT OR IGNORE INTO Station
            (StationID, StationName, Latitude, Longitude, MaxCapacity) 
        VALUES (?,?,?,?,?);
                        """,
            data.stations,
        )

        cur.executemany(
            """
        INSERT OR IGNORE INTO User
                        (UserID, FirstName, LastName, PhoneNr, Latitude, Longitude)
                        VALUES (?,?,?,?,?,?);
                        """,
            data.users,
        )

        cur.executemany(
            """
        INSERT OR IGNORE INTO Bike
            (BikeID, BikeName, LastStationID, ActivityStatusID) 
        VALUES (?,?,?,?);
        """,
            data.bikes,
        )

        #TODO: Subs and trips


def import_legacy_csv_dataset(csv_path: Path) -> None:
    data = _extract_data(csv_path)
    _insert_data(data)
