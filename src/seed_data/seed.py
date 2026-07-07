"""
Populates the Bergen BikeShare database.
"""

import sqlite3

from database.connection import PROJECT_ROOT
from models.subscription_type import SubscriptionType
from seed_data.generators.bike_generator import GeneratedBike, generate_bikes
from seed_data.generators.complaint_generator import (
    GeneratedComplaint,
    generate_complaints,
)
from seed_data.generators.subscription_generator import (
    GeneratedSubscription,
    generate_subscriptions,
)
from seed_data.generators.trip_generator import GeneratedTrip, generate_trips
from seed_data.generators.user_generator import GeneratedUser, generate_users
from seed_data.legacy_csv_importer import import_legacy_csv_dataset

CSV_PATH = PROJECT_ROOT / "data" / "bysykkel.csv"

ADDITIONAL_STATIONS = [
    ("Solheimsviken", 60.377240, 5.33543, 32),
    ("Damsgårdsveien", 60.381548, 5.319435, 27),
    ("Akvariet", 60.400724, 5.305309, 45),
    ("Bryggen", 60.393147, 5.314364, 46),
    ("Bergen Storsenter", 60.389454, 5.331953, 58),
    ("Grieghallen", 60.388990, 5.327864, 36),
    ("Fantoft", 60.346256, 5.353832, 60),
    ("Allegaten", 60.386476, 5.325827, 24),
    ("Verftet", 60.395458, 5.309613, 23),
    ("Lagunen", 60.297962, 5.327995, 47),
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


def _load_reference_data(
    conn: sqlite3.Connection,
) -> tuple[list[int], list[int], list[int], list[SubscriptionType]]:
    """Loads existing subscription types, station-, activity status- and complaint type IDs."""

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
        for row in conn.execute("SELECT ComplaintTypeID FROM ComplaintType").fetchall()
    ]
    sub_types = [
        SubscriptionType(
            subscription_type_id=row[0],
            description=row[1],
            duration_in_days=row[2],
            price=row[3],
        )
        for row in conn.execute(
            "SELECT SubscriptionTypeID, Description, DurationInDays, Price FROM SubscriptionType"
        ).fetchall()
    ]

    return station_ids, activity_status_ids, complaint_type_ids, sub_types


def _load_dynamic_ids(conn: sqlite3.Connection) -> tuple[list[int], list[int]]:
    """Loads existing bike and user IDs."""
    bike_ids = [row[0] for row in conn.execute("SELECT BikeID FROM Bike").fetchall()]
    user_ids = [row[0] for row in conn.execute("SELECT UserID FROM User").fetchall()]

    return bike_ids, user_ids


def _seed_lookup_data(conn: sqlite3.Connection) -> None:
    """Populates the look-up tables."""

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


def _seed_additional_stations(conn: sqlite3.Connection):
    conn.executemany(
        "INSERT OR IGNORE INTO Station(StationName, Latitude, Longitude, MaxCapacity) VALUES (?,?,?,?);",
        ADDITIONAL_STATIONS,
    )


def _seed_user_data(users: list[GeneratedUser], conn: sqlite3.Connection) -> None:
    """Populates the user table."""

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


def _seed_bike_data(bikes: list[GeneratedBike], conn: sqlite3.Connection) -> None:
    """Populates the bike table."""

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


def _seed_trip_data(trips: list[GeneratedTrip], conn: sqlite3.Connection) -> None:
    """Populates the trips table."""
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


def _seed_complaint_data(
    complaints: list[GeneratedComplaint], conn: sqlite3.Connection
) -> None:
    """Populates the complaint table."""

    conn.executemany(
        """
        INSERT OR IGNORE INTO Complaint (BikeID, UserID, ComplaintTypeID, ReportDate, Resolved, ResolvedDate)
        VALUES (?, ?, ?, ?, ?, ?);
        """,
        [
            (
                complaint.bike_id,
                complaint.user_id,
                complaint.complaint_type_id,
                complaint.report_date,
                complaint.resolved,
                complaint.resolved_date,
            )
            for complaint in complaints
        ],
    )


def _seed_subscription_data(
    subscriptions: list[GeneratedSubscription], conn: sqlite3.Connection
) -> None:
    """Populates the subscription table."""

    conn.executemany(
        """
        INSERT OR IGNORE INTO Subscription (UserID, StartDate, EndDate, SubscriptionTypeID)
            VALUES (?, ?, ?, ?);
        """,
        [
            (
                subscription.user_id,
                subscription.start_date,
                subscription.end_date,
                subscription.sub_type.subscription_type_id,
            )
            for subscription in subscriptions
        ],
    )


def seed_database(conn: sqlite3.Connection) -> None:
    """Populates the database with legacy, reference and generated data."""
    _seed_lookup_data(conn)

    conn.commit()

    import_legacy_csv_dataset(CSV_PATH, conn)

    _seed_additional_stations(conn)

    station_ids, activity_status_ids, complaint_type_ids, sub_types = (
        _load_reference_data(conn)
    )

    users = generate_users(200)
    _seed_user_data(users, conn)

    bikes = generate_bikes(150, station_ids, activity_status_ids)
    _seed_bike_data(bikes, conn)

    bike_ids, user_ids = _load_dynamic_ids(conn)

    trips = generate_trips(6000, user_ids, bike_ids, station_ids)
    _seed_trip_data(trips, conn)

    complaints = generate_complaints(800, user_ids, bike_ids, complaint_type_ids)
    _seed_complaint_data(complaints, conn)

    subscriptions = generate_subscriptions(500, user_ids, sub_types)
    _seed_subscription_data(subscriptions, conn)
