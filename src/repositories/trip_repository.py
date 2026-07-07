"""Database access methods for trips"""

import sqlite3
from datetime import datetime

from models.station_traffic import StationTraffic
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

    def get_trip_count_by_station(self) -> list[StationTraffic]:
        """Returns an overview of departures and arrivals per station."""
        traffic_overview = self.conn.execute("""
                                        SELECT S.StationName,
                                               COUNT(Distinct TS.TripID) AS Departures,
                                               COUNT(DISTINCT TE.TripID) AS Arrivals
                                        FROM Station AS S
                                                 LEFT JOIN TRIP AS TS ON S.StationID = TS.StartStationID
                                                 LEFT JOIN Trip AS TE ON S.StationID = TE.EndStationID
                                        GROUP BY S.StationID, S.StationName
                                        """).fetchall()

        return [
            StationTraffic(station_name=row[0], departures=row[1], arrivals=row[2])
            for row in traffic_overview
        ]

    def get_trip_count_by_month(self, station_id: int | None = None) -> dict[str, int]:
        """Returns an overview of total trips per month, optionally filtered by station."""
        query = """
            SELECT 
                strftime('%Y-%m', StartTime) as YearAndMonth,
                COUNT(*) AS TripCount
            FROM Trip
                WHERE StartTime >= date('now','-1 year')
        """

        if station_id is not None:
            query += " AND (StartStationID = ? OR EndStationID = ?)"

        query += " GROUP BY strftime('%Y-%m', StartTime) ORDER BY strftime('%Y-%m', StartTime);"

        if station_id is not None:
            trips = self.conn.execute(query, (station_id, station_id)).fetchall()
        else:
            trips = self.conn.execute(query).fetchall()

        return {name: count for name, count in trips}

    def get_num_active_trips(self) -> int:
        return self.conn.execute("""
            SELECT COUNT(*) AS NumActiveTrips
            FROM Trip
                WHERE EndTime IS NULL AND EndStationID IS NULL;
            """).fetchone()[0]
