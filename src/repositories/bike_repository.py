"""Database access methods for bikes"""
import sqlite3
from sqlite3 import IntegrityError

from exceptions import DuplicateBikeError
from models.bike import Bike

class BikeRepository:

        def __init__(self, conn: sqlite3.Connection) -> None:
            self.conn = conn

        def get_activity_status_id(self, description: str) -> int:
            """
            Returns the activity status ID for the given description.

            Args:
                description: activity status description

            Raises:
                 LookupError: if no matching activity status ID exists.
            """
            row = self.conn.execute(
                """
                SELECT ActivityStatusID
                FROM ActivityStatus
                WHERE Description = ?;
                """,
                (description,),
            ).fetchone()

            if row is None:
                raise LookupError(f"Unknown activity status: {description}")
            return row[0]


        def get_activity_status_map(self) -> dict[str, int]:
            """Returns a mapping from activity status description to activity status ID."""
            return {
                description: status_id
                for status_id, description in self.conn.execute("""
                             SELECT ActivityStatusID, Description
                             FROM ActivityStatus;""").fetchall()
            }


        def get_bike(self, bike_id: int) -> Bike | None:
            row = self.conn.execute(
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
                self,
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

            bikes = self.conn.execute(query + " ORDER BY B.BikeID;", params).fetchall()

            return [
                Bike(bike_id=row[0], bike_name=row[1], station=row[2], activity_status=row[3])
                for row in bikes
            ]


        def insert_bike(self, name: str, station_id: int, status_id: int) -> None:
            """Adds a new bike to the database.

            Args:
                name (str): Name of the new bike; must be unique
                station_id (int): Initial station id; must be an existing station
                status_id (int): Initial activity status id; must be an existing status

            Raises:
                DuplicateBikeError: if a bike with the same name already exists
            """
            try:
                self.conn.execute(
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


        def update_bike_status(self,bike_id: int, status_id: int) -> None:
            self.conn.execute(
                """
                         UPDATE Bike
                         SET ActivityStatusID = ?
                         WHERE BikeID = ?;
                         """,
                (status_id, bike_id),
            )


        def update_bike_station(self, bike_id: int, station_id: int) -> None:
            self.conn.execute(
                """
                         UPDATE Bike
                         SET LastStationID = ?
                         WHERE BikeID = ?;
                         """,
                (station_id, bike_id),
            )


        def get_fleet_availability(self) -> float:
            """Returns the current percentage of available bikes"""
            parked_status = self.get_activity_status_id("Parked")

            return self.conn.execute(
                """
                SELECT ROUND((SELECT COUNT(*)
                              FROM Bike
                              WHERE Bike.ActivityStatusID = ?) * 100.0 /
                             (SELECT COUNT(*) FROM Bike), 1);
                """,
                (parked_status,),
            ).fetchone()[0]
