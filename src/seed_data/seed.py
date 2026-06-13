"""
Populates the Bergen BikeShare database.
"""

from legacy_csv_importer import import_legacy_csv_dataset
from database.connection import get_connection, PROJECT_ROOT

CSV_PATH = PROJECT_ROOT / "data" / "bysykkel.csv"

ACTIVITY_STATUSES = ["Parked", "Active", "Missing", "Service"]

SUBSCRIPTION_TYPES = [
    ("Day", 39, 1),
    ("Week", 99, 7),
    ("Month", 299, 30),
    ("Year", 999, 365),
]

COMPLAINT_TYPES = [
    "Flat Tire",
    "Chain Issue",
    "Gear Issue",
    "Brake Issue",
    "Damaged Frame",
    "Damaged or Missing Pedal",
    "Damaged or Missing Saddle",
    "Damaged or Missing Handlebar",
    "Damaged or Missing Bell",
    "Damaged or Missing Lock",
    "Damaged or Missing Light",
    "Damaged or Missing Helmet",
]


def _seed_reference_data() -> None:
    """Populates the look-up tables."""

    with get_connection() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO ActivityStatus (Description) VALUES (?);",
            [(status,) for status in ACTIVITY_STATUSES],
        )

        conn.executemany(
            """
            INSERT OR IGNORE INTO SubscriptionType
                (Description, Price, DurationInDays)
            VALUES (?, ?, ?);
            """,
            SUBSCRIPTION_TYPES,
        )

        conn.executemany(
            "INSERT OR IGNORE INTO ComplaintType (Description) VALUES (?);",
            [(complaint_type,) for complaint_type in COMPLAINT_TYPES],
        )


if __name__ == "__main__":
    _seed_reference_data()
    import_legacy_csv_dataset(CSV_PATH)

    # TODO: generate faker data for more users, complaints and trips
