from pydantic import ValidationError

from exceptions import DuplicateBikeError, MissingStationError
from repositories.bike_repository import bike_exists, insert_bike
from repositories.lookup_repository import get_activity_status_id
from repositories.station_repository import station_exists


def register_bike(name: str, station_id: int) -> None:
    """
    Registers a bike to the database.

    Args:
        name: the name of the new bike
        station_id: the ID of the bike's initial station

    Raises:
        ValidationError: if the bike name is blank
        DuplicateBikeError: if a bike with the given name already exists
        MissingStationError: if the station does not exist
    """

    name = name.strip().capitalize()

    if not name:
        raise ValidationError("Bike name cannot be empty")

    if bike_exists(name):
        raise DuplicateBikeError(f"Bike '{name}' already exists")

    if not station_exists(station_id):
        raise MissingStationError(f"Station with ID {station_id} not found")

    service_id = get_activity_status_id("Parked")

    insert_bike(name, station_id, service_id)
