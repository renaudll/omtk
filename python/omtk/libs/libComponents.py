import os
import re
import uuid
import itertools
from maya import cmds
import pymel.core as pymel
from omtk.core.classModule2 import Module2
from omtk.libs import libAttr
from omtk.vendor import libSerialization

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


def isolate_network_io_ports(attrs_inn, attrs_out, isolate=True):
    hub_inn = pymel.createNode('network', name=_HUB_INN_NAME)
    hub_out = pymel.createNode('network', name=_HUB_OUT_NAME)

    for attr_inn in attrs_inn:
        attr_name = _get_unique_attr_name(hub_inn, _escape_attr_name(attr_inn.longName()))
        # Check if the attribute exist before transfering it.
        # This can happen with build-in attribute like translateX since the hub is a transform.
        # It might be more logical to use networks for this, but we'll stick with transforms for now.
        data = libAttr.holdAttr(attr_inn, delete=False)
        data['node'] = hub_inn
        data['longName'] = attr_name
        data['shortName'] = attr_name
        data['niceName'] = attr_name
        libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
        libAttr.swapAttr(attr_inn, hub_inn.attr(attr_name), inputs=False, outputs=True)
        if not isolate:
            pymel.connectAttr(attr_inn, hub_inn.attr(attr_name))

    for attr_out in attrs_out:
        attr_name = _get_unique_attr_name(hub_out, _escape_attr_name(attr_out.longName()))
        data = libAttr.holdAttr(attr_out, delete=False)
        data['node'] = hub_out
        data['longName'] = attr_name
        data['shortName'] = attr_name
        data['niceName'] = attr_name
        libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
        libAttr.swapAttr(hub_out.attr(attr_name), attr_out, inputs=True, outputs=False)
        if not isolate:
            pymel.connectAttr(hub_out.attr(attr_name), attr_out)

    return hub_inn, hub_out


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


def create_component(objs):
    attrs_inn, attrs_out = identify_network_io_ports(objs)
    if not attrs_inn:
        raise Exception("Found no inputs")
    if not attrs_out:
        raise Exception("Found no outputs")

    hub_inn, hub_out = isolate_network_io_ports(attrs_inn, attrs_out, isolate=True)

    module = Module2()
    module.grp_inn = hub_inn
    module.grp_out = hub_out

    network = libSerialization.export_network(module)
    pymel.select(network)

    return module


def embed_component_metadata_in_file(path, component):
    """
    OMTK use the fileInfo flag to embed metadata in maya ascii files.
    However the fileInfo command only operate on the current file.
    This method will modify an existing file to include the metadata without opening it.
    Note that we expect at least one fileInfo entry in the provided .ma file.
    :param path:
    :param component:
    :return:
    """


regex_ma_header = re.compile('^\/\/Maya ASCII .* scene$')
regex_fileinfo = re.compile('^fileInfo "(.*)" "(.*");')


def iter_ma_file_metadata(path):
    with open(path, 'r') as fp:
        line = fp.readline()
        if not regex_ma_header.match(line):
            raise Exception("Invalid first line for file {0}: {1}".format(path, line))

        found = False
        while fp:
            line = fp.readline()
            regex_result = regex_fileinfo.match(line)
            if regex_result:
                found = True
                key, val = regex_result.groups()
                yield key, val
            # If we encountered fileInfo and suddenly stop encountering, we are finished with the file
            elif found:
                break


def get_component_metadata_from_file(path):
    metadata = {}
    for key, val in iter_ma_file_metadata(path):
        if key.startswith(_metadata_prefix):
            key = key[len(_metadata_prefix):]
            metadata[key] = val
    return metadata


_metadata_prefix = 'omtk.component.'


def write_metadata_to_ma_file(path, metadata):
    path_tmp = os.path.join(os.path.dirname(path), os.path.basename(path) + '_omtktmp')

    success = False
    found = False
    with open(path, 'r') as fp_read:
        with open(path_tmp, 'w') as fp_write:
            line = fp_read.readline()
            if not regex_ma_header.match(line):
                raise Exception("Invalid Maya ASCII file {0}".format(path))
            fp_write.write(line)

            for line in fp_read:
                regex_result = regex_fileinfo.match(line)
                if regex_result:
                    found = True
                    key, val = regex_result.groups()
                    # Ignore any existing omtk metadata
                    if key.startswith(_metadata_prefix):
                        continue
                # Only dump the metadata on the last fileInfo encounter
                elif found:
                    for key, val in metadata.iteritems():
                        fp_write.write(
                            'fileInfo "{0}{1}" "{2}";'.format(_metadata_prefix, key, val)
                        )
                    success = True
                    found = False

                fp_write.write(line)

    os.rename(path_tmp, path)

    return success


_component_metadata_mandatory_fields = (
    'uid', 'name', 'version'
)


class ComponentDefinition(object):
    def __init__(self, name, version=None, uid=None, author=None, path=None):
        self.uid = uid if uid else uuid.uuid4()
        self.name = name
        self.version = version if version else '0.0.0'
        self.author = author
        self.path = path

    def __eq__(self, other):
        if isinstance(other, ComponentDefinition):
            return self.get_metadata() == other.get_metadata()
        if isinstance(other, dict):
            return self.get_metadata() == other
        raise Exception("Unexpected right operand type. Expected ComponentDefinition or dict, got {0}: {1}".format(
            type(other), other
        ))

    def get_metadata(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'version': self.version,
            'author': self.author
        }

    @classmethod
    def validate_metadata(cls, metadata):
        for field in _component_metadata_mandatory_fields:
            field_with_prefix = _metadata_prefix + field
            if field not in metadata:
                raise Exception("Incomplete metadata. Missing field {0} in {1}".format(
                    field, metadata
                ))

    @classmethod
    def from_metadata(cls, metadata):
        return cls(
            uid=metadata['uid'],
            name=metadata['name'],
            version=metadata['version'],
            author=metadata.get('author')
        )

    @classmethod
    def from_file(cls, path):
        metadata = get_component_metadata_from_file(path)
        cls.validate_metadata(metadata)
        return cls.from_metadata(metadata)

    def save_to_file(self, path):
        metadata = self.get_metadata()
        return write_metadata_to_ma_file(path, metadata)


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
