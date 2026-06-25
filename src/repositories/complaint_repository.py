"""Database access methods for complaints."""

from database.connection import get_connection
from models.complaint import Complaint


def get_complaints_for_bike(bike_id: int) -> list[Complaint]:
    with get_connection() as conn:
        complaints = conn.execute(
            """
            SELECT C.ComplaintID, CT.Description, C.ReportDate
            FROM Complaint AS C
                     JOIN ComplaintType AS CT
                          ON C.ComplaintTypeID = CT.ComplaintTypeID
            WHERE C.BikeID = ?;
            """,
            (bike_id,),
        ).fetchall()

    return [
        Complaint(complaint_id=row[0], complaint_type=row[1], report_date=row[2])
        for row in complaints
    ]


def remove_complaint(complaint_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM Complaint WHERE ComplaintID = ?;",
            (complaint_id,),
        )


def has_open_complaints(bike_id: int) -> bool:
    """Checks if a given bike has open complaints."""
    result = get_complaints_for_bike(bike_id)
    return bool(result)
