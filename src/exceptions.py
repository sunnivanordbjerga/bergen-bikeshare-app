class RepositoryError(Exception):
    """Base class for repository errors."""

    pass


class DuplicateBikeError(RepositoryError):
    """Raised when a bike name already exists"""

    pass


class MissingStationError(RepositoryError):
    """Raised when attempting to use a station id not in the database"""

    pass
