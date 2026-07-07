"""Provides maintenance workflows and operational bike handling"""

import enum
import sqlite3
from functools import cache

from exceptions import (
    BusinessRuleError,
    MissingBikeError,
    MissingComplaintError,
    MissingStationError,
)
from models.bike import Bike
from repositories.bike_repository import BikeRepository
from repositories.complaint_repository import ComplaintRepository
from repositories.station_repository import StationRepository


@enum.unique
class ActivityStatus(enum.StrEnum):
    PARKED = "Parked"
    ACTIVE = "Active"
    MISSING = "Missing"
    SERVICE = "Service"


class MaintenanceService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.bike_repository = BikeRepository(conn)
        self.complaint_repository = ComplaintRepository(conn)
        self.station_repository = StationRepository(conn)

    @cache
    def get_status_ids(self) -> dict[str, int]:
        return self.bike_repository.get_activity_status_map()

    def send_bike_to_service(self, bike_id: int) -> None:
        """
        Sends a bike to be serviced.

        Args:
            bike_id: The ID of the bike to service

        Raises:
            MissingBikeError: If the bike does not exist
            BusinessRuleError: If the bike is not parked
        """
        bike = self._require_bike(bike_id)

        if bike.activity_status != ActivityStatus.PARKED:
            raise BusinessRuleError("Only parked bikes can be picked up for service")

        service_id = self.get_status_ids()[ActivityStatus.SERVICE]

        self.bike_repository.update_bike_status(bike_id, service_id)

    def report_missing_bike(self, bike_id: int) -> None:
        """
        Report a bike as missing.

        Args:
            bike_id: The ID of the missing bike

        Raises:
            MissingBikeError: If the bike does not exist
            BusinessRuleError: If the bike is already missing or currently in service
        """
        bike = self._require_bike(bike_id)

        if bike.activity_status == ActivityStatus.MISSING:
            raise BusinessRuleError(f"Bike {bike.bike_name} already reported missing")

        if bike.activity_status == ActivityStatus.SERVICE:
            raise BusinessRuleError("Bikes in service cannot be reported missing")

        missing_id = self.get_status_ids()[ActivityStatus.MISSING]

        self.bike_repository.update_bike_status(bike_id, missing_id)

    def resolve_complaint(self, complaint_id: int) -> None:
        """Resolves a selected complaint"""
        complaint = self.complaint_repository.get_complaint(complaint_id)

        if complaint is None:
            raise MissingComplaintError(
                f"Complaint with ID {complaint_id} does not exist."
            )

        if complaint.resolved:
            raise BusinessRuleError("Complaint is already resolved")

        self.complaint_repository.resolve_complaint(complaint_id)

    def return_serviced_bike(self, bike_id: int, return_station_id: int) -> None:
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
        bike = self._require_bike(bike_id)

        if not self.station_repository.station_exists(return_station_id):
            raise MissingStationError(
                f"Station with id {return_station_id} does not exist."
            )

        if bike.activity_status != ActivityStatus.SERVICE:
            raise BusinessRuleError("Only bikes currently in service can be returned.")

        if self.complaint_repository.has_open_complaints(bike_id):
            raise BusinessRuleError(f"Bike {bike_id} has open complaints")

        parked_id = self.get_status_ids()[ActivityStatus.PARKED]

        self.bike_repository.update_bike_station(bike_id, return_station_id)
        self.bike_repository.update_bike_status(bike_id, parked_id)

    def recover_missing_bike(self, bike_id: int, return_station_id: int) -> None:
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
        bike = self._require_bike(bike_id)

        if not self.station_repository.station_exists(return_station_id):
            raise MissingStationError(
                f"Station with id {return_station_id} does not exist."
            )

        if bike.activity_status != ActivityStatus.MISSING:
            raise BusinessRuleError("Bike is not missing.")

        parked_id = self.get_status_ids()[ActivityStatus.PARKED]

        self.bike_repository.update_bike_station(bike_id, return_station_id)
        self.bike_repository.update_bike_status(bike_id, parked_id)

    def _require_bike(self, bike_id: int) -> Bike:
        bike = self.bike_repository.get_bike(bike_id)

        if bike is None:
            raise MissingBikeError(f"Bike with bike id {bike_id} does not exist.")

        return bike
