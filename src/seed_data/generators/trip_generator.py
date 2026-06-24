"""Generates fake trips."""

from datetime import timedelta
from random import random, choice, randint, choices
from dataclasses import dataclass
from faker import Faker

ACTIVE_TRIP_PROBABILITY: float = 0.005
SAME_STATION_PROBABILITY: float = 0.02
SHORT_TRIP_PROBABILITY: float = 0.8
STATION_WEIGHTS = {
    1: 9,  # Høyteknologisenteret
    2: 10,  # Nygårdsporten
    3: 11,  # Festplassen
    4: 10,  # Småstrandgaten
    5: 12,  # Torgallmenningen,
    6: 6,  # Solheimsviken
    7: 5,  # Damsgårdsveien
    8: 5,  # Akvariet
    9: 11,  # Bryggen
    10: 11,  # Bergen Storsenter
    11: 7,  # Grieghallen
    12: 6,  # Fantoft
    13: 9,  # Allegaten
    14: 6,  # Verftet
    15: 4,  # Lagunen
}

fake = Faker("no_NO")


@dataclass
class GeneratedTrip:
    user_id: int
    bike_id: int
    start_station_id: int
    end_station_id: int | None
    start_time: str
    end_time: str | None


def _generate_trip(
    user_ids: list[int],
    bike_ids: list[int],
    station_ids: list[int],
    active_trip: bool | None = None,
) -> GeneratedTrip:
    """Generates a single fake trip.
    Args:
        user_ids: List of existing user IDs.
        bike_ids: List of existing bike IDs.
        station_ids: List of existing station IDs.

    Returns:
        A generated trip.
    """

    if active_trip is None:
        active_trip = random() < ACTIVE_TRIP_PROBABILITY

    trip_started = fake.date_time_between(
        start_date="-24h" if active_trip else "-6M", end_date="now"
    )

    trip_duration = (
        randint(5, 30) if random() < SHORT_TRIP_PROBABILITY else randint(31, 180)
    )

    trip_ended = (
        None if active_trip else trip_started + timedelta(minutes=trip_duration)
    )

    start_station = choices(
        station_ids, [STATION_WEIGHTS[s] for s in station_ids], k=1
    )[0]

    if active_trip:
        end_station = None
    elif random() < SAME_STATION_PROBABILITY:
        end_station = start_station
    else:
        possible_destinations = [
            station for station in station_ids if station != start_station
        ]
        weights = [STATION_WEIGHTS[station] for station in possible_destinations]

        end_station = choices(possible_destinations, weights, k=1)[0]

    return GeneratedTrip(
        user_id=choice(user_ids),
        bike_id=choice(bike_ids),
        start_station_id=start_station,
        end_station_id=end_station,
        start_time=str(trip_started),
        end_time=str(trip_ended) if trip_ended else None,
    )


def generate_trips(
    num_trips: int, user_ids: list[int], bike_ids: list[int], station_ids: list[int]
) -> list[GeneratedTrip]:
    """
    Generates a list with the specified number of fake trips.

    Args:
        num_trips: Number of trips to generate.
        user_ids: List of existing user IDs.
        bike_ids: List of existing bike IDs.
        station_ids: List of existing station IDs.

    Returns:
        A list of generated trips.
    """
    if num_trips < 0:
        raise ValueError("num_trips cannot be negative.")

    return [_generate_trip(user_ids, bike_ids, station_ids) for _ in range(num_trips)]
