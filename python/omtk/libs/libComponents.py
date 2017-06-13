import pymel.core as pymel

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


def _iter_interesting_attributes(obj, read=True, write=False):
    """
    Extend pymel.listAttr by implementing recursivity
    :param obj: A pymel.nodetypes.DagNode that contain attribute to explore.
    :param read: If True, output attributes will be yielded.
    :param write: If True, input attributes will be yielded.
    :yield: pymel.Attribute instances.
    """
    attr_names = pymel.listAttr(obj, connectable=True, read=read, write=write)
    for attr_name in attr_names:
        # Ignore some known attributes by name
        if attr_name in _blacklisted_attr_names:
            continue

        try:
            attr = obj.attr(attr_name)
        except AttributeError, e:
            # print('Error obtaining attribute {0}.{1}: {2}'.format(obj, attr_name, e))
            continue

        if attr.type() in (
                'message',
        ):
            continue

        yield attr


def identify_network_io_ports(objs):
    """
    :param objs: Objects that are part of the network and that will define the bounds.
    :return: Two list of pymel.Attribute delimiting the inputs and outputs of the network.
    """
    all_objs = set(objs)

    # Search for input attributes
    def is_input(attr, known_nodes, known_attributes, future=True):
        attr_node = attr.node()

        plugs = attr.outputs(plugs=True) if future else attr.inputs(plugs=True)
        for plug in plugs:
            # Re-use information from previous scans
            if plug in known_attributes:
                return known_attributes[plug]

            # Ignore self-referencing
            plug_node = plug.node()
            if plug_node == attr_node:
                continue

            if plug_node in all_objs:
                return True

            found = False
            for sub_attr in _iter_interesting_attributes(plug_node, read=future, write=not future):
                found = is_input(sub_attr, known_nodes, known_attributes, future=future)
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
        for attr in _iter_interesting_attributes(obj, read=True, write=False):
            if is_input(attr, known_nodes, known_attributes, future=False):
                result_out.add(attr)
    for obj in objs:
        known_nodes = {obj: False}
        known_attributes = {}
        for attr in _iter_interesting_attributes(obj, read=False, write=True):
            if is_input(attr, known_nodes, known_attributes, future=True):
                result_inn.add(attr)

    return result_out, result_inn


def optimize_network_io_ports(attrs_inn, attrs_out):
    """
    Try to diminish the number of input and outputs ports by creating auxiliary nodes.
    :param attrs_inn: A list of pymel.Attribute representing the network input attributes.
    :param attrs_out: A list of pymel.Attribute representing the network output attributes.
    :return: Two list of pymel.Attribute representing the network optimized input and output attributes.
    """
    raise NotImplementedError
