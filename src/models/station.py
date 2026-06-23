from dataclasses import dataclass


@dataclass
class Station:
    """Represents a station stored in the database"""

    station_id: int
    station_name: str
    latitude: float
    longitude: float
    max_capacity: int
    available_capacity: int
