"""
Populates the Bergen BikeShare database.
TODO: Consider moving queries to repository layer once implemented
"""

from database.connection import get_connection, PROJECT_ROOT
from seed_data.legacy_csv_importer import import_legacy_csv_dataset
from seed_data.generators.bike_generator import GeneratedBike, generate_bikes
from seed_data.generators.subscription_generator import (
    GeneratedSubscription,
    generate_subscriptions,
)
from seed_data.generators.trip_generator import GeneratedTrip, generate_trips
from seed_data.generators.user_generator import generate_users, GeneratedUser
from seed_data.generators.complaint_generator import (
    generate_complaints,
    GeneratedComplaint,
)

CSV_PATH = PROJECT_ROOT / "data" / "bysykkel.csv"

ADDITIONAL_STATIONS = [
    ("Solheimsviken", 60.377240, 5.33543, 32),
    ("Damsgårdsveien", 60.381548, 5.319435, 27),
    ("Akvariet", 60.400724, 5.305309, 45),
    ("Bryggen", 60.393147, 5.314364, 34),
    ("Bergen Storsenter", 60.389454, 5.331953, 67),
    ("Grieghallen", 60.388990, 5.327864, 36),
    ("Fantoft", 60.346256, 5.353832, 65),
    ("Allegaten", 60.386476, 5.325827, 36),
    ("Verftet", 60.395458, 5.309613, 42),
    ("Lagunen", 60.297962, 5.327995, 62),
]

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


def _load_reference_ids() -> tuple[list[int], list[int], list[int], list[int]]:
    """Loads existing station, activity status and complaint type IDs."""
    with get_connection() as conn:
        station_ids = [
            row[0] for row in conn.execute("SELECT StationID FROM Station").fetchall()
        ]
        activity_status_ids = [
            row[0]
            for row in conn.execute(
                "SELECT ActivityStatusID FROM ActivityStatus"
            ).fetchall()
        ]
        complaint_type_ids = [
            row[0]
            for row in conn.execute(
                "SELECT ComplaintTypeID FROM ComplaintType"
            ).fetchall()
        ]
        sub_type_ids = [
            row[0]
            for row in conn.execute(
                "SELECT SubscriptionTypeID FROM SubscriptionType"
            ).fetchall()
        ]

        return station_ids, activity_status_ids, complaint_type_ids, sub_type_ids


def _load_dynamic_ids() -> tuple[list[int], list[int]]:
    """Loads existing bike and user IDs."""
    with get_connection() as conn:
        bike_ids = [
            row[0] for row in conn.execute("SELECT BikeID FROM Bike").fetchall()
        ]
        user_ids = [
            row[0] for row in conn.execute("SELECT UserID FROM User").fetchall()
        ]

        return bike_ids, user_ids


def _seed_lookup_data() -> None:
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


def _seed_additional_stations():
    with get_connection() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO Station(StationName, Latitude, Longitude, MaxCapacity) VALUES (?,?,?,?);",
            ADDITIONAL_STATIONS,
        )


def _seed_user_data(users: list[GeneratedUser]) -> None:
    """Populates the user table."""
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO User(FirstName, LastName, PhoneNr, Latitude, Longitude) 
                VALUES (?, ?, ?, ?, ?);
            """,
            [
                (
                    user.first_name,
                    user.last_name,
                    user.phone_number,
                    user.latitude,
                    user.longitude,
                )
                for user in users
            ],
        )


def _seed_bike_data(bikes: list[GeneratedBike]) -> None:
    """Populates the bike table."""
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO Bike (BikeName, LastStationID, ActivityStatusID)
                VALUES (?, ?, ?);
            """,
            [
                (
                    bike.bike_name,
                    bike.last_station_id,
                    bike.activity_status_id,
                )
                for bike in bikes
            ],
        )


def _seed_trip_data(trips: list[GeneratedTrip]) -> None:
    """Populates the trips table."""
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO Trip (UserID, BikeID, StartStationID, EndStationID, StartTime, EndTime)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            [
                (
                    trip.user_id,
                    trip.bike_id,
                    trip.start_station_id,
                    trip.end_station_id,
                    trip.start_time,
                    trip.end_time,
                )
                for trip in trips
            ],
        )


def _seed_complaint_data(complaints: list[GeneratedComplaint]) -> None:
    """Populates the complaint table."""
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO Complaint (BikeID, UserID, ComplaintTypeID, ReportDate)
            VALUES (?, ?, ?, ?);
            """,
            [
                (
                    complaint.bike_id,
                    complaint.user_id,
                    complaint.complaint_type_id,
                    complaint.report_date,
                )
                for complaint in complaints
            ],
        )


def _seed_subscription_data(subscriptions: list[GeneratedSubscription]) -> None:
    """Populates the subscription table."""
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO Subscription (UserID, StartDate, SubscriptionTypeID)
                VALUES (?, ?, ?);
            """,
            [
                (
                    subscription.user_id,
                    subscription.start_date,
                    subscription.sub_type_id,
                )
                for subscription in subscriptions
            ],
        )


def seed_database() -> None:
    """Populates the database with legacy, reference and generated data."""
    _seed_lookup_data()

    import_legacy_csv_dataset(CSV_PATH)

    _seed_additional_stations()

    station_ids, activity_status_ids, complaint_type_ids, sub_type_ids = (
        _load_reference_ids()
    )

    users = generate_users(200)
    _seed_user_data(users)

    bikes = generate_bikes(80, station_ids, activity_status_ids)
    _seed_bike_data(bikes)

    bike_ids, user_ids = _load_dynamic_ids()

    trips = generate_trips(4000, user_ids, bike_ids, station_ids)
    _seed_trip_data(trips)

    complaints = generate_complaints(100, user_ids, bike_ids, complaint_type_ids)
    _seed_complaint_data(complaints)

    subscriptions = generate_subscriptions(300, user_ids, sub_type_ids)
    _seed_subscription_data(subscriptions)


if __name__ == "__main__":
    seed_database()
