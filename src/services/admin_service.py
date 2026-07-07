"""Provides administrative operations for managing the bike fleet."""

import sqlite3

from exceptions import BusinessRuleError, DuplicateBikeError, MissingStationError
from repositories.bike_repository import BikeRepository
from repositories.station_repository import StationRepository


class AdminService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.bike_repository = BikeRepository(conn)
        self.station_repository = StationRepository(conn)

    def register_bike(self, name: str, station_id: int) -> None:
        """
        Registers a bike to the database.

        Args:
            name: the name of the new bike
            station_id: the ID of the bike's initial station

        Raises:
            BusinessRuleError: if the bike name is blank or contains non-alpha characters
            DuplicateBikeError: if a bike with the given name already exists
            MissingStationError: if the station does not exist
        """

        name = name.strip().capitalize()

        if not name:
            raise BusinessRuleError("Bike name cannot be empty")

        if not all(part.isalpha() for part in name.split()):
            raise BusinessRuleError("Bike name may only contain letters")

        if not self.station_repository.station_exists(station_id):
            raise MissingStationError(f"Station with ID {station_id} not found")

        parked_id = self.bike_repository.get_activity_status_id("Parked")

        try:
            self.bike_repository.insert_bike(name, station_id, parked_id)
        except sqlite3.IntegrityError:
            raise DuplicateBikeError(f"Bike with name '{name}' already exists")
