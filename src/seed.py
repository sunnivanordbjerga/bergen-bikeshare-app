"""
Populates the Bergen BikeShare database.
"""

from database.connection import get_connection

ACTIVITY_STATUSES = [
    'Parked',
    'Active',
    'Missing',
    'Service'
]

SUBSCRIPTION_TYPES = [
    ('Day', 39, 1),
    ('Week', 99, 7),
    ('Month', 299, 30),
    ('Year', 999, 365)
]

COMPLAINT_TYPES = [
    'Flat Tire',
    'Chain issues',
    'Gear issues',
    'Dysfunctional brake',
    'Damaged Frame',
    'Damaged/Missing Pedal',
    'Damaged/Missing Saddle',
    'Damaged/Missing Handlebars',
    'Damaged/Missing Bell',
    'Damaged/Missing Lock',
    'Damaged/Missing Light',
    'Damaged/Missing Helmet'
]


def seed_reference_data() -> None:
    with get_connection() as conn:

        conn.executemany(
            'INSERT OR IGNORE INTO ActivityStatus (Description) VALUES (?);',
            [(status,) for status in ACTIVITY_STATUSES]
        )

        conn.executemany(
            'INSERT OR IGNORE INTO SubscriptionType (Description, Price, DurationInDays) VALUES (?,?,?);',
            SUBSCRIPTION_TYPES
        )

        conn.executemany(
            'INSERT OR IGNORE INTO ComplaintType (Description) VALUES (?);',
            [(c_type,) for c_type in COMPLAINT_TYPES]
        )


if __name__ == "__main__":
    seed_reference_data()
    # import legacy dataset
    # generate faker data for more users, complaints and trips
