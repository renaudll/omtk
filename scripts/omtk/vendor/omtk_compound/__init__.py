"""
Public entry points. All members are part of the public API.
"""
from omtk_compound.core import (
    Compound,
    CompoundDefinition,
    CompoundValidationError,
    Manager,
    Preferences,
    Registry,
)

__all__ = (
    "Compound",
    "CompoundDefinition",
    "CompoundValidationError",
    "Manager",
    "Preferences",
    "Registry",
    "manager",
)

# Default manager
manager = Manager()  # pylint: disable=invalid-name
