"""Database access methods for lookup tables."""

from database.connection import get_connection


def get_activity_status_id(description: str) -> int:
    """
    Returns the activity status ID for the given description.

    Args:
        description: activity status description

    Raises:
         LookupError: if no matching activity status ID exists.
    """
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT ActivityStatusID
            FROM ActivityStatus
            WHERE Description = ?;
            """,
            (description,),
        ).fetchone()

    if row is None:
        raise LookupError(f"Unknown activity status: {description}")
    return row[0]


def get_activity_status_map() -> dict[str, int]:
    """Returns a mapping from activity status description to activity status ID."""
    with get_connection() as conn:
        return {
            description: status_id
            for status_id, description in conn.execute("""
                         SELECT ActivityStatusID, Description
                         FROM ActivityStatus""").fetchall()
        }


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
