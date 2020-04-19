"""
omtk_compound manager
"""
import os

from omtk_compound.core import Manager, Preferences, _factory

_COMPOUNDS_LOCATION = os.path.join(
    os.path.dirname(__file__),  # /scripts/omtk/core
    "..",  # /scripts/omtk
    "..",  # /scripts
    "..",  # /
    "compounds"  # /compounds
)

_PREFERENCES = Preferences(compound_location=_COMPOUNDS_LOCATION)
MANAGER = Manager(preferences=_PREFERENCES)

