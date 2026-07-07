"""Database access methods for complaints."""

import sqlite3

from models.complaint import Complaint


class ComplaintRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def get_complaint_type_id(self, description: str) -> int:
        """
        Returns the complaint type ID for the given description.

        Args:
            description: complaint type description

        Raises:
             LookupError: if no matching complaint type ID exists.
        """
        row = self.conn.execute(
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

    def get_complaint(self, complaint_id: int) -> Complaint | None:

        row = self.conn.execute("""
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

    def resolve_complaint(self, complaint_id: int) -> None:
        """Marks a complaint as resolved."""

        self.conn.execute(
            "UPDATE Complaint SET Resolved = 1, ResolvedDate = DATETIME('now') WHERE ComplaintID = ?;",
            (complaint_id,),
        )

    def get_open_complaints_for_bike(self, bike_id: int) -> list[Complaint]:

        complaints = self.conn.execute(
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

    def has_open_complaints(self, bike_id: int) -> bool:
        """Checks if a given bike has open complaints."""
        result = self.get_open_complaints_for_bike(bike_id)
        return bool(result)
