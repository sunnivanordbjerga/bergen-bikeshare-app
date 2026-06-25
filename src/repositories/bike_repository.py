"""Database access methods for bikes"""

from sqlite3 import IntegrityError

from exceptions import DuplicateBikeError
from models.bike import Bike
from database.connection import get_connection


def get_bike(bike_id: int) -> Bike | None:
    with get_connection() as conn:
        row = conn.execute(
            """
                           SELECT B.BikeID, B.BikeName, S.StationName, AST.Description 
                           FROM Bike AS B 
                           LEFT JOIN STATION AS S 
                               ON S.StationID = B.LastStationID
                            JOIN ActivityStatus AS AST
                               ON B.ActivityStatusID = AST.ActivityStatusID \
                            WHERE B.BikeID = ?;
                           """,
            (bike_id,),
        ).fetchone()

    if row is None:
        return None

    return Bike(
        bike_id=row[0], bike_name=row[1], station=row[2], activity_status=row[3]
    )


def get_bikes(
    station_id: int | None = None,
    status_id: int | None = None,
) -> list[Bike]:
    """
    Returns all bikes, optionally filtered by station and/or activity status.

    Args:
        station_id: (optional) station ID to filter by.
        status_id: (optional) activity status ID to filter by.
    """
    query = """
            SELECT B.BikeID, B.BikeName, S.StationName, AST.Description
            FROM Bike AS B
                     LEFT JOIN STATION AS S
                               ON S.StationID = B.LastStationID
                     JOIN ActivityStatus AS AST
                          ON B.ActivityStatusID = AST.ActivityStatusID \
            """
    conditions = []
    params = []

    if station_id is not None:
        conditions.append("B.LastStationID = ?")
        params.append(station_id)

    if status_id is not None:
        conditions.append("B.ActivityStatusID = ?")
        params.append(status_id)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with get_connection() as conn:
        bikes = conn.execute(query + " ORDER BY B.BikeID;", params).fetchall()

    return [
        Bike(bike_id=row[0], bike_name=row[1], station=row[2], activity_status=row[3])
        for row in bikes
    ]


def bike_exists(name: str) -> bool:
    """Returns whether a bike with the given name already exists"""
    with get_connection() as conn:
        result = conn.execute(
            "SELECT BikeName FROM Bike WHERE BikeName = ?;", name
        ).fetchone()

        return result is not None


def insert_bike(name: str, station_id: int, status_id: int) -> None:
    """Adds a new bike to the database.

    Args:
        name (str): Name of the new bike; must be unique
        station_id (int): Initial station id; must be an existing station
        status_id (int): Initial activity status id; must be an existing status

    Raises:
        DuplicateBikeError: if a bike with the same name already exists
    """
    with get_connection() as conn:
        try:
            conn.execute(
                """
                         INSERT INTO Bike (BikeName, LastStationID, ActivityStatusID)
                         VALUES (?, ?, ?);
                         """,
                (name, station_id, status_id),
            )
        except IntegrityError as e:
            if "Bike.BikeName" in str(e):
                raise DuplicateBikeError() from e
            raise


def update_bike_status(bike_id: int, status_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            """
                     UPDATE Bike
                     SET ActivityStatusID = ?
                     WHERE BikeID = ?;
                     """,
            (status_id, bike_id),
        )


def update_bike_station(bike_id: int, station_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            """
                     UPDATE Bike
                     SET LastStationID = ?
                     WHERE BikeID = ?;
                     """,
            (station_id, bike_id),
        )
