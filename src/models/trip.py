from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trip:
    """Represents a trip stored in the database"""

    trip_id: int
    user: str
    bike: str
    start_station: str
    end_station: str | None
    start_time: datetime
    end_time: datetime | None
