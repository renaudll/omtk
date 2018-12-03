"""
Utility method to run in Maya to extract all know node types and their attributes.
"""
import json
import logging

from maya import cmds
from maya import standalone

standalone.initialize()

log = logging.getLogger(__name__)


def _get_node_schema(node_type):
    data = {}

    attributes = cmds.attributeInfo(allAttributes=True, type=node_type)
    for attribute in attributes:
        attr_type = cmds.attributeQuery(attribute, type=node_type, attributeType=True)

        # Some attributes will return 'typed' as the type.
        # I don't know of any way of knowing in advance the type.
        # However for what we need, guessing might be enough.
        if attr_type == 'typed':
            if 'matrix' in attribute.lower():  # HACK
                attr_type = 'matrix'

        attr_name_short = cmds.attributeQuery(attribute, type=node_type, shortName=True)
        attr_name_nice = cmds.attributeQuery(attribute, type=node_type, niceName=True)

        attr_data = {
            'port_type': attr_type,
            'short_name': attr_name_short,
            'nice_name': attr_name_nice,
        }

        data[attribute] = attr_data

    return data


def _generate():
    data = {}
    node_types = cmds.allNodeTypes(includeAbstract=False)
    for node_type in node_types:
        sub_data = _get_node_schema(node_type)
        if sub_data:
            data[node_type] = sub_data
    return data


cmds.loadPlugin('matrixNodes')

data = _generate()

path = '/home/rll/dev/python/omtk/python/omtk/vendor/mock_maya/schema.json'

with open(path, 'w') as fp:
    json.dump(data, fp, indent=4, sort_keys=True)
