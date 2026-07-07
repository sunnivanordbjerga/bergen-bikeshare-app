"""Database access methods for stations"""

import sqlite3

from models.station import Station


class StationRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_station(self, station_id: int) -> Station | None:

        row = self.conn.execute(
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

    def get_stations(self) -> list[Station]:
        """Returns all stations."""

        stations = self.conn.execute("""
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

    def station_exists(self, station_id: int) -> bool:
        """Returns whether a station with the given ID already exists"""

        result = self.conn.execute(
            "SELECT StationID FROM Station WHERE StationID = ?", (station_id,)
        ).fetchone()

        return bool(result)
