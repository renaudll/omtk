"""
Helpers for compound management and creation.
"""
import os

import pymel.core as pymel

from omtk.vendor.omtk_compound import Manager, Preferences
from omtk.libs import libRigging

# Note that the compounds directory is in the python package
# This all the package to be contained when used as a whell.
_COMPOUNDS_LOCATION = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),  # /scripts/omtk/core
        "..",  # /scripts/omtk
        "compounds",  # /scripts/omtk/compounds
    )
)
_PREFERENCES = Preferences(compound_location=_COMPOUNDS_LOCATION)
_MANAGER = Manager(preferences=_PREFERENCES)


def create_compound(name, namespace, inputs=None, outputs=None):
    """
    Create a compound

    :param str name: The compound registered name
    :param str namespace: The namespace to use
    :param dict inputs: An optional map of inputs
    :param dict outputs: An optional map of outputs
    :return: A compound
    :rtype: omtk.vendor.omtk_compound.Compound
    """
    compound = _MANAGER.create_compound(name=name, namespace=namespace)
    inputs = inputs or {}
    outputs = outputs or {}
    for attr_name, value in inputs.items():
        if value is None:
            continue
        attr = pymel.Attribute("%s.%s" % (compound.input, attr_name))
        libRigging.connect_or_set_attr(attr, value)

    for attr_name, value in outputs.items():
        if value is None:
            continue
        attr = pymel.Attribute("%s.%s" % (compound.output, attr_name))
        pymel.connectAttr(attr, value, force=True)

    return compound
