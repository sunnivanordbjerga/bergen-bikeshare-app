"""Provides administrative operations for managing the bike fleet."""

from sqlite3 import IntegrityError

from exceptions import BusinessRuleError, DuplicateBikeError, MissingStationError
from repositories.bike_repository import insert_bike
from repositories.lookup_repository import get_activity_status_id
from repositories.station_repository import station_exists


def register_bike(name: str, station_id: int) -> None:
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

    if not station_exists(station_id):
        raise MissingStationError(f"Station with ID {station_id} not found")

    parked_id = get_activity_status_id("Parked")

    try:
        insert_bike(name, station_id, parked_id)
    except IntegrityError:
        raise DuplicateBikeError(f"Bike with name '{name}' already exists")
