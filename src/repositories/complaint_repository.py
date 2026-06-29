"""Database access methods for complaints."""

from database.connection import get_connection
from models.complaint import Complaint


def get_complaint_type_id(description: str) -> int:
    """
    Returns the complaint type ID for the given description.

    Args:
        description: complaint type description

    Raises:
         LookupError: if no matching complaint type ID exists.
    """
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT ComplaintTypeID
            FROM ComplaintType
            WHERE Description = ?;
            """,
            (description,),
        ).fetchone()

    if row is None:
        raise LookupError(f"Unknown complaint type: {description}")
    return row[0]


def get_complaint(complaint_id: int) -> Complaint | None:
    with get_connection() as conn:
        row = conn.execute("""
                           SELECT C.ComplaintID, CT.Description, C.ReportDate, C.Resolved, C.ResolvedDate
                           FROM Complaint AS C
                                    JOIN ComplaintType AS CT ON C.ComplaintTypeID = CT.ComplaintTypeID
                           WHERE ComplaintID = ?;""").fetchone()
        if row is None:
            return None

        return Complaint(
            complaint_id=row[0],
            complaint_type=row[1],
            report_date=row[2],
            resolved=row[3],
            resolved_date=row[4],
        )


def resolve_complaint(complaint_id: int) -> None:
    """Marks a complaint as resolved."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE Complaint SET Resolved = 1, ResolvedDate = DATETIME('now') WHERE ComplaintID = ?;",
            (complaint_id,),
        )


def get_open_complaints_for_bike(bike_id: int) -> list[Complaint]:
    with get_connection() as conn:
        complaints = conn.execute(
            """
            SELECT C.ComplaintID, CT.Description, C.ReportDate
            FROM Complaint AS C
                     JOIN ComplaintType AS CT
                          ON C.ComplaintTypeID = CT.ComplaintTypeID
            WHERE C.BikeID = ? AND C.Resolved = 0;
            """,
            (bike_id,),
        ).fetchall()

    return [
        Complaint(complaint_id=row[0], complaint_type=row[1], report_date=row[2])
        for row in complaints
    ]


def has_open_complaints(bike_id: int) -> bool:
    """Checks if a given bike has open complaints."""
    result = get_open_complaints_for_bike(bike_id)
    return bool(result)
