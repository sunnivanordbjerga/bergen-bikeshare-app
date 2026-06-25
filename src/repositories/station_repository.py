"""Database access methods for stations"""

from database.connection import get_connection
from models.station import Station


def get_station(station_id: int) -> Station | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT S.StationID,
                   S.StationName,
                   S.Latitude,
                   S.Longitude,
                   S.MaxCapacity,
                   (S.MaxCapacity - COUNT(B.BikeID)) AS AvailableCapacity
            FROM Station AS S
                     LEFT JOIN Bike AS B
                               ON S.StationID = B.LastStationID
            WHERE S.StationID = ?
            GROUP BY S.StationID, S.StationName, S.Latitude, S.Longitude, S.MaxCapacity;
            """,
            (station_id,),
        ).fetchone()

        if row is None:
            return None

        return Station(
            station_id=row[0],
            station_name=row[1],
            latitude=row[2],
            longitude=row[3],
            max_capacity=row[4],
            available_capacity=row[5],
        )


def get_stations() -> list[Station]:
    """Returns all stations."""
    with get_connection() as conn:
        stations = conn.execute("""
            SELECT S.StationID,
                   S.StationName,
                   S.Latitude,
                   S.Longitude,
                   S.MaxCapacity,
                   (S.MaxCapacity - COUNT(B.BikeID)) AS AvailableCapacity
            FROM Station AS S
                     LEFT JOIN Bike AS B
                               ON S.StationID = B.LastStationID
            GROUP BY S.StationID,
                     S.StationName,
                     S.Latitude,
                     S.Longitude,
                     S.MaxCapacity;
            """).fetchall()

    return [
        Station(
            station_id=row[0],
            station_name=row[1],
            latitude=row[2],
            longitude=row[3],
            max_capacity=row[4],
            available_capacity=row[5],
        )
        for row in stations
    ]


def station_exists(station_id: int) -> bool:
    """Returns whether a station with the given ID already exists"""
    with get_connection() as conn:
        result = conn.execute(
            "SELECT StationID FROM Station WHERE StationID = ?", (station_id,)
        ).fetchone()

    return bool(result)
