class RepositoryError(Exception):
    """Base class for repository errors."""

    pass


class DuplicateBikeError(RepositoryError):
    """Raised when a bike name already exists"""

    pass


class MissingBikeError(RepositoryError):
    """Raised when attempting to use a bike id not in the database"""

    pass


class MissingStationError(RepositoryError):
    """Raised when attempting to use a station id not in the database"""

    pass


class MissingComplaintError(RepositoryError):
    """Raised when attempting to use a complaint id not in the database"""

    pass


class BusinessRuleError(Exception):
    """Raised when a business rule fails"""

    pass
