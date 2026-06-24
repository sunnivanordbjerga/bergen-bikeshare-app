from dataclasses import dataclass


@dataclass
class StationTraffic:
    """Represents traffic to and from a station"""

    station_name: str
    departures: int
    arrivals: int
