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
                trip_id=row["TripID"],
                user=row["User"],
                bike=row["BikeName"],
                start_station=row["StartStation"],
                end_station=row["EndStation"] if row["EndStation"] else None,
                start_time=datetime.fromisoformat(row["StartTime"]),
                end_time=datetime.fromisoformat(row["EndTime"])
                if row["EndTime"]
                else None,
            )
            for row in trips
        ]

    def get_active_trips_count(self) -> int:
        return self.conn.execute("""
            SELECT COUNT(*) AS ActiveTripsCount
            FROM Trip
                WHERE EndTime IS NULL AND EndStationID IS NULL;
            """).fetchone()["ActiveTripsCount"]

    def get_trip_count_by_station(self) -> list[dict]:
        """Returns an overview of departures and arrivals per station."""
        return [
            dict(row)
            for row in self.conn.execute("""
                                 SELECT S.StationID,
                                        S.StationName,
                                        COALESCE(Dep.DepCount, 0)                               AS Departures,
                                        COALESCE(Arr.ArrCount, 0)                               AS Arrivals,
                                        (COALESCE(Arr.ArrCount, 0) - COALESCE(Dep.DepCount, 0)) AS NetFlow
                                 FROM Station AS S
                                          LEFT JOIN (SELECT StartStationID, COUNT(*) AS DepCount
                                                     FROM Trip
                                                     GROUP BY StartStationID) AS Dep
                                                    ON S.StationID = Dep.StartStationID
                                          LEFT JOIN (SELECT EndStationID, COUNT(*) AS ArrCount
                                                     FROM Trip
                                                     WHERE EndStationID IS NOT NULL
                                                     GROUP BY EndStationID) AS Arr ON S.StationID = Arr.EndStationID
                                 ORDER BY Departures DESC;
                                 """).fetchall()
        ]

    def get_trip_count_by_month(
        self, station_id: int | None = None
    ) -> list[dict[str, int]]:
        """Returns an overview of total trips per month for the last year, optionally filtered by station."""
        query = """
                SELECT strftime('%Y-%m', StartTime) AS YearAndMonth,
                       COUNT(TripID)                AS TripCount
                FROM Trip
                WHERE StartTime >= date('now', '-1 year')
                """
        params = []

        if station_id is not None:
            query += " AND StartStationID = ? "
            params.append(station_id)

        query += " GROUP BY YearAndMonth ORDER BY YearAndMonth;"

        return [dict(row) for row in self.conn.execute(query, params).fetchall()]
