import itertools
import os
import re

import pymel.core as pymel
from maya import cmds
from omtk.core.classComponentDefinition import ComponentDefinition
# from omtk.core.classComponent import isolate_network_io_ports
# from omtk.core.classModule2 import Module2
# from omtk.vendor import libSerialization

_HUB_INN_NAME = 'hub_inn'
_HUB_OUT_NAME = 'hub_out'

_blacklisted_attr_names = {
    'caching',
    'isHistoricallyInteresting',
    'nodeState',
    'frozen',
    'isCollapsed',
    'blackBox',
    'publishedNodeInfo',
    'templateName',
    'templatePath',
    'templateVersion',
    'viewName',
    'iconName',
    'viewMode',
    'uiTreatment',
    'customTreatment',
    'creator',
    'creationDate',
    'containerType',
    'intermediateObject',
    'hyperLayout',
    'borderConnections',
    'publishedNode',
    'publishedNodeInfo.publishedNode',
    'renderLayerInfo',
    'renderLayerInfo.renderLayerId',
    'instObjGroups',
    'instObjGroups.objectGroups',
    'instObjGroups.objectGroups.objectGroupId',
    'instObjGroups.objectGroups.objectGrpColor',
    'template',
    'ghosting',
    'objectColorR',
    'objectColorG',
    'objectColorB',
    'objectColorRGB',
    'wireColorRGB',
    'wireColorR',
    'wireColorG',
    'wireColorB',
    'useObjectColor',
    'objectColor',
    'drawOverride',
    'overrideDisplayType',
    'overrideLevelOfDetail',
    'overrideShading',
    'overrideTexturing',
    'overridePlayback',
    'overrideEnabled',
    'overrideVisibility',
    'hideOnPlayback',
    'overrideRGBColors',
    'overrideColor',
    'overrideColorRGB',
    'overrideColorR',
    'overrideColorG',
    'overrideColorB',
    'lodVisibility',
    'selectionChildHighlighting',
    'renderInfo',
    'identification',
    'layerRenderable',
    'layerOverrideColor',
    'renderLayerInfo.renderLayerRenderable',
    'renderLayerInfo.renderLayerColor',
    'ghostingControl',
    'ghostCustomSteps',
    'ghostPreSteps',
    'ghostPostSteps',
    'ghostStepSize',
    'ghostFrames',
    'ghostColorPreA',
    'ghostColorPre',
    'ghostColorPreR',
    'ghostColorPreG',
    'ghostColorPreB',
    'ghostColorPostA',
    'ghostColorPost',
    'ghostColorPostR',
    'ghostColorPostG',
    'ghostColorPostB',
    'ghostRangeStart',
    'ghostRangeEnd',
    'ghostDriver',
    'Skipping ctrl.ghostDriver',
    'hiddenInOutliner',
    'useOutlinerColor',
    'outlinerColor',
    'outlinerColorR',
    'outlinerColorG',
    'outlinerColorB',
    'geometry',
    'selectHandle',
    'selectHandleX',
    'selectHandleY',
    'selectHandleZ',
    'displayHandle',
    'displayScalePivot',
    'displayRotatePivot',
    'displayLocalAxis',
    'dynamics',
    'showManipDefault',
    'specifiedManipLocation',
    'message',
    'boundingBox',
    'boundingBoxMin',
    'boundingBoxMax',
    'boundingBoxSize',
    'boundingBoxMinX',
    'boundingBoxMaxX',
    'boundingBoxMinY',
    'boundingBoxMaxY',
    'boundingBoxMinZ',
    'boundingBoxMaxZ',
    'boundingBoxSizeX',
    'boundingBoxSizeY',
    'boundingBoxSizeZ',
    'boundingBoxCenter',
    'boundingBoxCenterX',
    'boundingBoxCenterY',
    'boundingBoxCenterZ',
}


def _iter_leaf_attributes(obj):
    """
    Iter all the leaf nodes (including compounds and array attributes) recursively using pymel awesome
    iterDescendants method. Note that since the leavesOnly flag is not provided by the listAttr method
    we need to go through the top level Attributes first.
    :param obj:
    :return:
    """
    # for attr_top in obj.listAttr(topLevel=True):
    #     for attr in attr_top.iterDescendants(leavesOnly=False):
    #         yield attr
    for attr in obj.listAttr(descendants=True):
        yield attr


def _iter_interesting_attributes(obj):
    """
    Extend pymel.listAttr by implementing recursivity
    :param obj: A pymel.nodetypes.DagNode that contain attribute to explore.
    :param read: If True, output attributes will be yielded.
    :param write: If True, input attributes will be yielded.
    :yield: pymel.Attribute instances.
    """
    for attr in _iter_leaf_attributes(obj):
        attr_name = attr.longName()

        # Ignore some known attributes by name
        if attr_name in _blacklisted_attr_names:
            continue

        yield attr


def identify_network_io_ports(objs):
    """
    :param objs: Objects that are part of the network and that will define the bounds.
    :return: Two list of pymel.Attribute delimiting the inputs and outputs of the network.
    """
    all_objs = set(objs)

    # Search for input attributes
    def fn_search(attr, known_nodes, known_attributes, future=True):
        attr_node = attr.node()

        # If we encounter a multi attribute, we'll simply ignore it since it's elements attributes are next.
        # The main reason is that there can not be any connections directly on the multi attribute, calling
        # inputs/outputs on it will return the connections from all it's elements which is not precise.
        if attr.isMulti():
            return False

        plugs = attr.outputs(plugs=True) if future else attr.inputs(plugs=True)
        for plug in plugs:
            # Re-use information from previous scans
            # if plug in known_attributes:
            #     return known_attributes[plug]

            # Ignore self-referencing
            plug_node = plug.node()
            if plug_node == attr_node:
                continue

            if plug_node in all_objs:
                return True

            found = False
            for sub_attr in _iter_interesting_attributes(plug_node):
                found = fn_search(sub_attr, known_nodes, known_attributes, future=future)
                known_attributes[sub_attr] = found
                if found:
                    break
            known_nodes[plug_node] = found
            if found:
                return True

        return False

    result_out = set()
    result_inn = set()
    for obj in objs:
        known_nodes = {obj: False}
        known_attributes = {}
        for attr in _iter_interesting_attributes(obj):
            if fn_search(attr, known_nodes, known_attributes, future=True):
                result_inn.add(attr)
    for obj in objs:
        known_nodes = {obj: False}
        known_attributes = {}
        for attr in _iter_interesting_attributes(obj):
            if fn_search(attr, known_nodes, known_attributes, future=False):
                result_out.add(attr)

    return result_inn, result_out


def optimize_network_io_ports(attrs_inn, attrs_out):
    """
    Try to diminish the number of input and outputs ports by creating auxiliary nodes.
    :param attrs_inn: A list of pymel.Attribute representing the network input attributes.
    :param attrs_out: A list of pymel.Attribute representing the network output attributes.
    :return: Two list of pymel.Attribute representing the network optimized input and output attributes.
    """
    raise NotImplementedError


def _escape_attr_name(attr_name):
    return attr_name.replace('[', '_').replace(']', '_')


def _get_unique_attr_name(obj, attr_name):
    if not obj.hasAttr(attr_name):
        return attr_name
    for i in itertools.count():
        new_attr_name = attr_name + str(i)
        if not obj.hasAttr(new_attr_name):
            return new_attr_name


def _get_all_namespaces():
    cmds.namespace(setNamespace="::")
    return cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)


def _get_unique_namespace(namespace):
    all_namespaces = _get_all_namespaces()
    if namespace not in all_namespaces:
        return namespace
    for i in itertools.count():
        new_namespace = namespace + str(i)
        if new_namespace not in all_namespaces:
            return new_namespace


def import_component_from_file(path, namespace='untitled'):
    namespace = _get_unique_namespace(namespace)
    cmds.file(path, i=True, namespace=namespace)
    hub_inn = pymel.PyNode('|{0}:{1}'.format(namespace, _HUB_INN_NAME))
    hub_out = pymel.PyNode('|{0}:{1}'.format(namespace, _HUB_OUT_NAME))
    return hub_inn, hub_out


# def create_component(objs):
#     attrs_inn, attrs_out = identify_network_io_ports(objs)
#     if not attrs_inn:
#         raise Exception("Found no inputs")
#     if not attrs_out:
#         raise Exception("Found no outputs")
#
#     hub_inn, hub_out = isolate_network_io_ports(attrs_inn, attrs_out, isolate=True)
#
#     module = Module2()
#     module.grp_inn = hub_inn
#     module.grp_out = hub_out
#
#     network = libSerialization.export_network(module)
#     pymel.select(network)
#
#     return module


class MultipleComponentDefinitionError(Exception):
    """Raised when two component with the same uid and version are found."""


def walk_available_component_definitions():
    # todo: clearly define where are the components in omtk
    path_component_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'components')
    if not os.path.exists(path_component_dir):
        raise Exception()
    paths = [path_component_dir]

    known = set()

    for dirname in paths:
        if os.path.exists(dirname):
            for filename in os.listdir(dirname):
                basename, ext = os.path.splitext(filename)
                if ext != '.ma':
                    continue
                path = os.path.join(dirname, filename)

                component_def = ComponentDefinition.from_file(path)
                if not component_def:
                    continue

                key = hash((component_def.uid, component_def.version))
                if key in known:
                    raise MultipleComponentDefinitionError(
                        "Found more than two component with the same uid and version: {0}".format(
                            component_def
                        )
                    )
                known.add(key)

                yield component_def
