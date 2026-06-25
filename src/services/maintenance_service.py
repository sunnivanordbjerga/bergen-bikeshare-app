"""Provides maintenance workflows and operational bike handling"""

from exceptions import MissingBikeError, MissingStationError, BusinessRuleError
from models.bike import Bike
from repositories.bike_repository import (
    get_bike,
    update_bike_status,
    update_bike_station,
)
from repositories.complaint_repository import has_open_complaints
from repositories.lookup_repository import (
    get_activity_status_id,
)
from repositories.station_repository import station_exists

PARKED_STATUS = "Parked"
MISSING_STATUS = "Missing"
SERVICE_STATUS = "Service"


def send_bike_to_service(bike_id: int) -> None:
    """
    Sends a bike to be serviced.

    Args:
        bike_id: The ID of the bike to service

    Raises:
        MissingBikeError: If the bike does not exist
        BusinessRuleError: If the bike is not parked
    """
    bike = _require_bike(bike_id)

    if bike.activity_status != PARKED_STATUS:
        raise BusinessRuleError("Only parked bikes can be picked up for service")

    service_id = get_activity_status_id(SERVICE_STATUS)

    update_bike_status(bike_id, service_id)


def report_missing_bike(bike_id: int) -> None:
    """
    Report a bike as missing.

    Args:
        bike_id: The ID of the missing bike

    Raises:
        MissingBikeError: If the bike does not exist
        BusinessRuleError: If the bike is already missing or currently in service
    """
    bike = _require_bike(bike_id)

    if bike.activity_status == MISSING_STATUS:
        raise BusinessRuleError(f"Bike {bike.bike_name} already reported missing")

    if bike.activity_status == SERVICE_STATUS:
        raise BusinessRuleError("Bikes in service cannot be reported missing")

    missing_id = get_activity_status_id(MISSING_STATUS)

    update_bike_status(bike_id, missing_id)


def return_serviced_bike(bike_id: int, return_station_id: int) -> None:
    """
    Returns a repaired bike to the given station.

    Args:
        bike_id: The bike to return
        return_station_id: The station to return the bike to

    Raises:
        MissingBikeError: If the bike does not exist
        MissingStationError: If the station does not exist
        BusinessRuleError: If the bike has open complaints
    """
    bike = _require_bike(bike_id)

    if not station_exists(return_station_id):
        raise MissingStationError(
            f"Station with id {return_station_id} does not exist."
        )

    if bike.activity_status != SERVICE_STATUS:
        raise BusinessRuleError("Only bikes currently in service can be returned.")

    if has_open_complaints(bike_id):
        raise BusinessRuleError(f"Bike {bike_id} has open complaints")

    parked_id = get_activity_status_id(PARKED_STATUS)

    update_bike_station(bike_id, return_station_id)
    update_bike_status(bike_id, parked_id)


def recover_missing_bike(bike_id: int, return_station_id: int) -> None:
    """
    Returns a missing bike to the given station.

    Args:
        bike_id: The bike to return
        return_station_id: The station to return the bike to

    Raises:
        MissingBikeError: If the bike does not exist
        MissingStationError: If the station does not exist
        BusinessRuleError: If the bike is not missing
    """
    bike = _require_bike(bike_id)

    if not station_exists(return_station_id):
        raise MissingStationError(
            f"Station with id {return_station_id} does not exist."
        )

    if bike.activity_status != MISSING_STATUS:
        raise BusinessRuleError("Bike is not missing.")

    parked_id = get_activity_status_id(PARKED_STATUS)

    update_bike_station(bike_id, return_station_id)
    update_bike_status(bike_id, parked_id)


def _require_bike(bike_id: int) -> Bike:
    bike = get_bike(bike_id)

    if bike is None:
        raise MissingBikeError(f"Bike with bike id {bike_id} does not exist.")

    return bike
