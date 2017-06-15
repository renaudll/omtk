import pymel.core as pymel
from omtk.libs import libAttr

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
                # if future and not pymel.attributeQuery(sub_attr.attrName(), node=plug_node, readable=True):
                #     continue
                # elif not future and not pymel.attributeQuery(sub_attr.attrName(), node=plug_node, writable=True):
                #     continue

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


def isolate_network_io_ports(attrs_inn, attrs_out):
    hub_inn = pymel.createNode('transform', name='hub_inn')
    hub_out = pymel.createNode('transform', name='hub_out')

    for attr_inn in attrs_inn:
        attr_name = attr_inn.longName()
        # Check if the attribute exist before transfering it.
        # This can happen with build-in attribute like translateX since the hub is a transform.
        # It might be more logical to use networks for this, but we'll stick with transforms for now.
        if not hub_inn.hasAttr(attr_name):
            data = libAttr.holdAttr(attr_inn, delete=False)
            data['node'] = hub_inn
            libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
        if attr_inn.isDestination():
            attr_src = next(iter(attr_inn.inputs(plugs=True)))
            pymel.disconnectAttr(attr_src, attr_inn)
        pymel.connectAttr(hub_inn.attr(attr_name), attr_inn)

    for attr_out in attrs_out:
        attr_name = attr_out.longName()
        if not hub_out.hasAttr(attr_name):
            data = libAttr.holdAttr(attr_out, delete=False)
            data['node'] = hub_out
            attr_name = data['longName']
            libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
        if attr_out.isSource():
            for attr_dst in attr_out.outputs(plugs=True):
                pymel.disconnectAttr(attr_out, attr_dst)
        pymel.connectAttr(attr_out, hub_out.attr(attr_name))

    return hub_inn, hub_out
