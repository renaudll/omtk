"""
omtk_compound manager
"""
import os
from omtk.vendor.omtk_compound import Manager, Preferences

# Note that the compounds directory is in the python package
# This all the package to be contained when used as a whell.
_COMPOUNDS_LOCATION = os.path.abspath(os.path.join(
    os.path.dirname(__file__),  # /scripts/omtk/core
    "..",  # /scripts/omtk
    "compounds"  # /scripts/omtk/compounds
))
_PREFERENCES = Preferences(compound_location=_COMPOUNDS_LOCATION)
MANAGER = Manager(preferences=_PREFERENCES)
