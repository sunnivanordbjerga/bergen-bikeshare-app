from dataclasses import dataclass
from datetime import date


@dataclass
class Complaint:
    """Represents a complaint stored in the database"""

    complaint_id: int
    complaint_type: str
    report_date: date
    resolved: bool
    resolved_date: str
