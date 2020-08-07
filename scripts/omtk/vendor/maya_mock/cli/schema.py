"""
A schema is a snapshot of a Maya session registered node.
"""
import argparse
import json
import logging
import os
import shutil
import tempfile

from maya_mock.base import _maya
from maya_mock.base.schema import (
    MockedSessionSchema,
    NodeTypeDef,
    get_namespace_leaf,
    get_namespace_parent,
    iter_namespaces,
)
from maya import cmds, standalone

_LOG = logging.getLogger(__name__)
_DEFAULT_PATH = os.path.abspath("schema.json")

_PARSER = argparse.ArgumentParser(description="Generate a schema.json file from a maya session.")
_PARSER.add_argument("path", nargs="?", default=_DEFAULT_PATH)
_PARSER.add_argument("-d", "--debug", action="store_true", help="Increate _LOG level to DEBUG")


def _generate():
    """
    Generate a Schema instance by analysing the current session.

    :return: A new Schema instance
    :rtype: MockedSessionSchema
    """
    # Determine empty scene default state
    cmds.file(new=True, force=True)
    default_state = {name: cmds.nodeType(name) for name in cmds.ls()}

    inst = MockedSessionSchema(default_state=default_state)

    # Determine known nodes and their ports
    node_types = cmds.allNodeTypes()

    namespaces = sorted(
        ".".join(_maya.get_node_type_namespace(node_type)) for node_type in node_types
    )
    for namespace in iter_namespaces(namespaces):
        _LOG.info("Registering %r", namespace)
        node_type = get_namespace_leaf(namespace)
        parent_namespace = get_namespace_parent(namespace)
        parent = inst.get_node_by_namespace(parent_namespace) if parent_namespace else None
        data = _maya.get_node_attributes_info(node_type)
        classification = _maya.get_node_classification(node_type)
        node = NodeTypeDef(namespace, data, classification, parent=parent)
        inst.register_node(node)

    return inst


def main():
    """
    Main entry point.
    """
    args = _PARSER.parse_args()
    if args.debug:
        _LOG.setLevel(logging.DEBUG)
        _LOG.debug("Detected debug flag, _LOG level changed to DEBUG")

    _, path_tmp = tempfile.mkstemp(suffix="json")
    path = os.path.abspath(args.path)
    _LOG.info("Will save schema to %r", path)

    _LOG.info("Initializing Maya...")
    standalone.initialize()
    cmds.loadPlugin("matrixNodes")

    _LOG.info("Generating schema...")
    schema = _generate()
    data = schema.to_dict()

    _LOG.debug("Saving schema...")
    with open(path_tmp, "w") as stream:
        json.dump(data, stream, indent=4, sort_keys=True)

    _LOG.debug("Applying changes...")
    shutil.copy2(path_tmp, path)
    os.remove(path_tmp)

    _LOG.info("Saved to %r", path)
    _LOG.info("Done. Closing Maya...")

    standalone.uninitialize()
