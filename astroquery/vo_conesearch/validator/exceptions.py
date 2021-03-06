# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Exceptions related to Virtual Observatory (VO) validation."""

__all__ = ['BaseVOValidationError', 'ValidationMultiprocessingError']


class BaseVOValidationError(Exception):  # pragma: no cover
    """Base class for VO validation exceptions."""
    pass


class ValidationMultiprocessingError(BaseVOValidationError):  # pragma: no cover  # noqa
    """Validation using multiprocessing failed."""
    pass


class InvalidValidationAttribute(BaseVOValidationError):  # pragma: no cover
    """Invalid validation attribute."""
    pass
