from dataclasses import dataclass


@dataclass
class Bike:
    """Represents a bike stored in the database"""

    bike_id: int
    bike_name: str
    station: str | None
    activity_status: str
