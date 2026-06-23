class RepositoryError(Exception):
    """Base class for repository errors."""

    pass


class DuplicateBikeError(RepositoryError):
    """Raised when a bike name already exists"""

    pass
