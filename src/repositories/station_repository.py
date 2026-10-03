"""Database access methods for stations"""

import sqlite3

from models.station import Station


class StationRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_stations(self, station_id: int | None = None) -> list[Station]:
        """
        Returns a list of stations, optionally filtered by a given Station ID.
        Args:
            station_id(int): Station ID to filter by. If None, all stations are returned.
        """
        query = """
                SELECT S.StationID,
                       S.StationName,
                       S.Latitude,
                       S.Longitude,
                       S.MaxCapacity,
                       (S.MaxCapacity - COUNT(CASE WHEN AST.Description = 'Parked' THEN 1 END)) AS AvailableCapacity
                FROM Station AS S
                         LEFT JOIN Bike AS B
                                   ON S.StationID = B.LastStationID
                         LEFT JOIN ActivityStatus AS AST
                                   ON AST.ActivityStatusID = B.ActivityStatusID \
                """
        params = []

        if station_id is not None:
            query += " WHERE S.StationID = ?"
            params.append(station_id)

        query += "GROUP BY S.StationID, S.StationName, S.Latitude, S.Longitude, S.MaxCapacity;"

        rows = self.conn.execute(query, params).fetchall()

        return [
            Station(
                station_id=row["StationID"],
                station_name=row["StationName"],
                latitude=row["Latitude"],
                longitude=row["Longitude"],
                max_capacity=row["MaxCapacity"],
                available_capacity=row["AvailableCapacity"],
            )
            for row in rows
        ]

    def station_exists(self, station_id: int) -> bool:
        """Returns whether a station with the given ID already exists"""

        result = self.conn.execute(
            "SELECT EXISTS (SELECT 1 FROM Station WHERE StationID = ?)", (station_id,)
        ).fetchone()

        return bool(result[0])
