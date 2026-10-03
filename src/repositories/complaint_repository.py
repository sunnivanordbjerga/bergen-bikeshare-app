"""Database access methods for complaints."""

import sqlite3
from datetime import datetime as dt

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
        return row["ComplaintTypeID"]

    def get_complaint(self, complaint_id: int) -> Complaint | None:
        """Returns the complaint with the given ID."""

        row = self.conn.execute(
            """
                           SELECT C.ComplaintID, CT.Description, C.ReportDate, C.Resolved, C.ResolvedDate
                           FROM Complaint AS C
                                    JOIN ComplaintType AS CT ON C.ComplaintTypeID = CT.ComplaintTypeID
                           WHERE ComplaintID = ?;""",
            (complaint_id,),
        ).fetchone()
        if row is None:
            return None

        resolved_date_val = row["ResolvedDate"]

        return Complaint(
            complaint_id=row["ComplaintID"],
            complaint_type=row["Description"],
            report_date=dt.fromisoformat(row["ReportDate"]),
            resolved=bool(row["Resolved"]),
            resolved_date=dt.fromisoformat(row["ResolvedDate"])
            if resolved_date_val
            else None,
        )

    def resolve_complaint(self, complaint_id: int) -> None:
        """Marks a complaint as resolved."""

        self.conn.execute(
            "UPDATE Complaint SET Resolved = 1, ResolvedDate = DATETIME('now') WHERE ComplaintID = ?;",
            (complaint_id,),
        )

    def get_open_complaints_for_bike(self, bike_id: int) -> list[Complaint]:
        """Returns a list of open complaints for a given bike."""

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
            Complaint(
                complaint_id=row["ComplaintID"],
                complaint_type=row["Description"],
                report_date=dt.fromisoformat(row["ReportDate"]),
                resolved=False,
                resolved_date=None,
            )
            for row in complaints
        ]

    def has_open_complaints(self, bike_id: int) -> bool:
        """Checks if a given bike has open complaints."""
        row = self.conn.execute(
            """
        SELECT EXISTS (SELECT 1 FROM Complaint AS C WHERE BikeID = ? AND Resolved = 0);""",
            (bike_id,),
        ).fetchone()
        return bool(row[0])
