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


def get_stations(status_id: int | None = None) -> list[Station]:
    """
        Returns all stations, optionally filtered by activity status for bikes.

    Args:
        status_id (optional): Activity status ID to filter by
    """
    query = """
            SELECT S.StationID,
                   S.StationName,
                   S.Latitude,
                   S.Longitude,
                   S.MaxCapacity,
                   (S.MaxCapacity - COUNT(B.BikeID)) AS AvailableCapacity
            FROM Station AS S
                LEFT JOIN Bike AS B
            ON S.StationID = B.LastStationID 
            """

    params = []

    if status_id is not None:
        query += " AND B.ActivityStatusID = ?"
        params.append(status_id)

    with get_connection() as conn:
        stations = conn.execute(
            query
            + """
            GROUP BY
            S.StationID,
            S.StationName,
            S.Latitude,
            S.Longitude,
            S.MaxCapacity;
            """,
            params,
        ).fetchall()

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
