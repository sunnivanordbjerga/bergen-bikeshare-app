class RepositoryError(Exception):
    """Base class for repository errors."""


class DuplicateBikeError(RepositoryError):
    """Raised when a bike name already exists"""


class MissingBikeError(RepositoryError):
    """Raised when attempting to use a bike id not in the database"""


class MissingStationError(RepositoryError):
    """Raised when attempting to use a station id not in the database"""


class MissingComplaintError(RepositoryError):
    """Raised when attempting to use a complaint id not in the database"""


class BusinessRuleError(Exception):
    """Raised when a business rule fails"""
