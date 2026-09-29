"""Database access methods for trips"""

import sqlite3
from datetime import datetime

from models.trip import Trip


class TripRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_trips(
        self,
        bike_id: int | None = None,
        start_station_id: int | None = None,
        end_station_id: int | None = None,
    ) -> list[Trip]:
        """
        Returns a list of trips optionally filtered by bike ID, start- and end station.

        Args:
            bike_id: Bike ID to filter by
            start_station_id: Start station ID to filter by
            end_station_id: End station ID to filter by
        """
        query = """
                SELECT T.TripID,
                       U.FirstName || ' ' || U.LastName AS User,
                       B.BikeName,
                       SS.StationName                   AS StartStation,
                       ES.StationName                   AS EndStation,
                       T.StartTime,
                       T.EndTime
                FROM Trip AS T
                         JOIN User AS U ON T.UserID = U.UserID
                         JOIN Bike AS B ON T.BikeID = B.BikeID
                         JOIN Station AS SS ON T.StartStationID = SS.StationID
                         LEFT JOIN Station AS ES ON T.EndStationID = ES.StationID \
                """

        conditions = []
        params = []

        if bike_id is not None:
            conditions.append("B.BikeID = ?")
            params.append(bike_id)
        if start_station_id is not None:
            conditions.append("T.StartStationID = ?")
            params.append(start_station_id)
        if end_station_id is not None:
            conditions.append("T.EndStationID = ?")
            params.append(end_station_id)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        trips = self.conn.execute(query + " ORDER BY T.TripID;", params).fetchall()

        return [
            Trip(
                trip_id=row[0],
                user=row[1],
                bike=row[2],
                start_station=row[3],
                end_station=row[4] if row[4] else None,
                start_time=datetime.fromisoformat(row[5]),
                end_time=datetime.fromisoformat(row[6]) if row[6] else None,
            )
            for row in trips
        ]

    def get_active_trips_count(self) -> int:
        return self.conn.execute("""
            SELECT COUNT(*) AS NumActiveTrips
            FROM Trip
                WHERE EndTime IS NULL AND EndStationID IS NULL;
            """).fetchone()[0]
