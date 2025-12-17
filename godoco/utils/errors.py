"""Custom exceptions for Godoco."""


class GodocoError(Exception):
    """Base exception for all Godoco errors."""

    pass


class GodotNotFoundError(GodocoError):
    """Raised when Godot executable cannot be found."""

    pass


class ProjectNotFoundError(GodocoError):
    """Raised when a specific project cannot be found."""

    pass


class InvalidConfigError(GodocoError):
    """Raised when configuration is invalid or corrupt."""

    pass


class ExportError(GodocoError):
    """Raised when project export fails."""

    pass
