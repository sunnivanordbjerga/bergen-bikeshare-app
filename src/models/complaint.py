from dataclasses import dataclass
from datetime import datetime


@dataclass
class Complaint:
    """Represents a complaint stored in the database"""

    complaint_id: int
    complaint_type: str
    report_date: datetime
    resolved: bool
    resolved_date: datetime | None
