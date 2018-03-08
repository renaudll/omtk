"""
Simple backport of the Component logic from OMTK2.
"""
import pymel.core as pymel
from omtk.libs import libRigging


# taken from xlib
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def camel_case_join(*tokens):
    result = ''
    for i, token in enumerate(tokens):
        if i == 0:
            result += token[0].lower() + token[1:]
        else:
            result += token[0].upper() + token[1:]
    return result


def to_pascal_case(snake_str):
    components = snake_str.split('_')
    return "".join(x.title() for x in components)


# taken from sstk.maya.rigging.macros
def create_offset_grp(obj, suffix='offset'):
    offset = pymel.createNode('transform', name=(obj.name() + '_' + suffix))
    offset.setMatrix(obj.getMatrix(worldSpace=True), worldSpace=True)
    offset.setParent(obj.getParent())
    obj.setParent(offset)
    return offset


def duplicate_transform_with_shapes(ctrl):
    new_transform = pymel.duplicate(ctrl)[0]
    child_transforms = [c for c in new_transform.getChildren() if isinstance(c, pymel.nodetypes.Transform)]
    if child_transforms:
        pymel.delete(child_transforms)
    return new_transform


def _duplicate_ctrl(ctrl):
    new_ctrl = duplicate_transform_with_shapes(ctrl)
    new_ctrl.setParent(world=True)
    new_ctrl.rename(ctrl.nodeName())  # try to use the same naming, this can succeed if ctrl have a parent
    return new_ctrl


def _get_attr_name_from_obj(obj, prefix='', suffix=''):
    basename_snakecase = obj.nodeName()
    if prefix:
        basename = to_pascal_case(basename_snakecase)
    else:
        basename = to_camel_case(basename_snakecase)
    return prefix + basename + suffix


def _add_or_get_attr(holder, long_name, **kwargs):
    if not holder.hasAttr(long_name):
        pymel.addAttr(holder, longName=long_name, **kwargs)
    attr = holder.attr(long_name)
    return attr


def _connect_matrix_to_trs(attr_inn, obj_out):
    # Connect internal_obj
    util_decompose_tm = libRigging.create_utility_node(
        'decomposeMatrix',
        inputMatrix=attr_inn
    )
    pymel.connectAttr(util_decompose_tm.outputTranslate, obj_out.translate)
    pymel.connectAttr(util_decompose_tm.outputRotate, obj_out.rotate)
    pymel.connectAttr(util_decompose_tm.outputScale, obj_out.scale)


def _export_input_world_tm(attr_holder, obj_external, prefix='', suffix='WorldMatrix'):
    # Create network out attribute
    attr_name = _get_attr_name_from_obj(obj_external, prefix=prefix, suffix=suffix)
    attr = _add_or_get_attr(attr_holder, attr_name, dataType='matrix')
    pymel.connectAttr(obj_external.worldMatrix, attr)


class ComponentWizard(object):
    def __init__(self):
        self.grp_inn = None
        self.grp_out = None
        self.grp_anms = None
        self.grp_infs = None
        self.grp_dag = None

        self.parts_ctrl = []
        self.parts_guides = []
        self.parts_influences = []

    def initialize(self):
        self.grp_inn = pymel.createNode('transform', name='inn')
        self.grp_out = pymel.createNode('transform', name='out')
        self.grp_anms = pymel.createNode('transform', name='ctrls')
        self.grp_infs = pymel.createNode('transform', name='infls')
        self.grp_dag = pymel.createNode('transform', name='dag')


# todo: handle ctrl with non-zero transform???

class ComponentPart(object):
    attr_prefix = ''

    def __init__(self, parent=None,
                 obj=None):  # hack: parent and obj are keywoard argument for libSerialization compatibility
        # type: (ComponentWizard) -> None
        self.parent = parent
        self.obj = obj
        self.attr_name = _get_attr_name_from_obj(self.obj) if self.obj else None

    def __repr__(self):
        return self.obj.nodeName()

    def iter_nodes(self):
        """Iter the nodes affected by the part."""
        yield self.obj

    def initialize(self):
        pass

    def iter_interface_infos(self):
        """
        Yield the public interface for this part.
        (attribute_holder, attribute_name, creation_kwargs)
        :return: 
        """
        return
        yield  # Hack: Force the method to be a generator.

    def create_interface(self):
        """Create the attributes on the network input and output hubs."""
        for attr_holder, attr_name, attr_kwargs in self.iter_interface_infos():
            _add_or_get_attr(attr_holder, attr_name, **attr_kwargs)

    def delete_interface(self):
        """Destroy the attributes on the network input and output hubs. Used for interface changes."""
        for attr_holder, attr_name, attr_kwargs in self.iter_interface_infos():
            if attr_holder.hasAttr(attr_name):
                pymel.deleteAttr(attr_holder, attribute=attr_name)

    def rename_attr(self, new_name):
        if self.is_connected():
            self.disconnect()
        self.delete_interface()
        self.attr_name = new_name
        self.create_interface()
        self.connect()

    def delete(self):
        pass

    def is_connected(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError


class ComponentPartCtrl(ComponentPart):
    attr_prefix = 'ctrl'

    def __init__(self, parent=None,
                 obj=None):  # hack: parent and obj are keywoard argument for libSerialization compatibility
        super(ComponentPartCtrl, self).__init__(parent, obj)
        # assert(isinstance(parent, ComponentWizard))
        # self._obj = obj
        self.obj_offset = None
        self.external_ctrl = None
        self.external_ctrl_offset = None

        self._attr_inn_ctrl_tm = None
        self._attr_out_ctrl_offset_tm = None

    def iter_nodes(self):
        for yielded in super(ComponentPartCtrl, self).iter_nodes():
            yield yielded

        yield self.obj_offset
        yield self.external_ctrl
        yield self.external_ctrl_offset

    def _get_attr_inn_ctrl_local_tm_infos(self):
        attr_inn_ctrl_tm_name = camel_case_join(self.attr_prefix, self.attr_name, 'LocalMatrix')
        return self.parent.grp_inn, attr_inn_ctrl_tm_name, {'dataType': 'matrix'}

    def _get_attr_inn_ctrl_local_tm(self):
        attr_holder, attr_name, _ = self._get_attr_inn_ctrl_local_tm_infos()
        return attr_holder.attr(attr_name)

    def _get_attr_out_ctrl_offset_world_tm_infos(self):
        attr_out_offset_tm_name = camel_case_join(self.attr_prefix, self.attr_name, 'OffsetWorldMatrix')
        return self.parent.grp_out, attr_out_offset_tm_name, {'dataType': 'matrix'}

    def _get_attr_out_ctrl_offset_world_tm(self):
        attr_holder, attr_name, _ = self._get_attr_out_ctrl_offset_world_tm_infos()
        return attr_holder.attr(attr_name)

    def iter_interface_infos(self):
        """
        Yield the public interface for this part.
        (attribute_holder, attribute_name, creation_kwargs)
        :return: 
        """
        yield self._get_attr_inn_ctrl_local_tm_infos()

        yield self._get_attr_out_ctrl_offset_world_tm_infos()

    def initialize(self):
        self.obj_offset = self.obj.getParent()

        # Create a duplicate of the ctrl
        self.external_ctrl = _duplicate_ctrl(self.obj)

        # Create the offset
        self.external_ctrl_offset = create_offset_grp(self.external_ctrl)
        self.external_ctrl_offset.setParent(self.parent.grp_anms)

        self.create_interface()

    def delete(self):
        pymel.delete([self.external_ctrl_offset, self.external_ctrl])

    def is_connected(self):
        return self.obj.translate.isDestination()

    def connect(self):
        # Connect external ctrl to network
        attr_inn = self._get_attr_inn_ctrl_local_tm()
        pymel.connectAttr(self.external_ctrl.matrix, attr_inn)

        # Connect network to internal ctrl
        _connect_matrix_to_trs(attr_inn, self.obj)

        # Connect internal offset to network
        attr_out = self._get_attr_out_ctrl_offset_world_tm()
        pymel.connectAttr(self.obj_offset.worldMatrix, attr_out)

        # Connect network to external ctrl offset
        _connect_matrix_to_trs(attr_out, self.external_ctrl_offset)

    def disconnect(self):
        # Disconnect external ctrl from network
        attr_inn = self._get_attr_inn_ctrl_local_tm()
        pymel.disconnectAttr(self.external_ctrl.matrix, attr_inn)

        # Disconnect network from internal ctrl
        util_decompose_tm = self.obj.inputs()[0]
        pymel.delete(util_decompose_tm)

        # Disconnect internal offset from network
        attr_out = self._get_attr_out_ctrl_offset_world_tm()
        pymel.disconnectAttr(self.obj_offset.worldMatrix, attr_out)

        # Diconnect output network from external ctrl offset
        util_decompose_tm = self.external_ctrl_offset.inputs()[0]
        pymel.delete(util_decompose_tm)


class ComponentPartInfluence(ComponentPart):
    attr_prefix = 'inf'

    def __init__(self, parent=None, obj=None):
        # hack: parent and obj are keywoard argument for libSerialization compatibility
        super(ComponentPartInfluence, self).__init__(parent, obj)
        self.obj_external = None

    def initialize(self):
        self.obj_external = pymel.createNode("joint")  # todo: rename?
        self.obj_external.rename(self.obj.nodeName())
        self.obj_external.setParent(self.parent.grp_infs)

        self.create_interface()

    def _get_attr_out_world_tm_infos(self):
        attr_out_offset_tm_name = camel_case_join(self.attr_prefix, self.attr_name, 'WorldMatrix')
        return self.parent.grp_out, attr_out_offset_tm_name, {'dataType': 'matrix'}

    def _get_attr_out_world_tm(self):
        attr_holder, attr_name, _ = self._get_attr_out_world_tm_infos()
        return attr_holder.attr(attr_name)

    def iter_interface_infos(self):
        """
        Yield the public interface for this part.
        (attribute_holder, attribute_name, creation_kwargs)
        :return: 
        """
        yield self._get_attr_out_world_tm_infos()

    def delete(self):
        pymel.delete([self.obj_external])

    def is_connected(self):
        return self.obj_external.translate.isDestination()

    def connect(self):
        # Connect internal influence to network
        attr_out = self._get_attr_out_world_tm()
        pymel.connectAttr(self.obj.worldMatrix, attr_out)

        # Connect network to external influence
        _connect_matrix_to_trs(attr_out, self.obj_external)

    def disconnect(self):
        # Disconnect internal influence from network
        attr_out = self._get_attr_out_world_tm()
        pymel.disconnectAttr(self.obj.worldMatrix, attr_out)

        # Disconnect external influence from network
        util_decompose_tm = self.obj_external.translate.inputs()[0]
        pymel.delete(util_decompose_tm)


class ComponentPartGuide(ComponentPart):
    attr_prefix = 'guide'

    def initialize(self):
        self.create_interface()

    def _get_attr_inn_world_tm_infos(self):
        attr_out_offset_tm_name = camel_case_join(self.attr_prefix, self.attr_name + 'WorldMatrix')
        return self.parent.grp_inn, attr_out_offset_tm_name, {'dataType': 'matrix'}

    def _get_attr_inn_world_tm(self):
        attr_holder, attr_name, _ = self._get_attr_inn_world_tm_infos()
        # print attr_holder, attr_name
        return attr_holder.attr(attr_name)

    def iter_interface_infos(self):
        """
        Yield the public interface for this part.
        (attribute_holder, attribute_name, creation_kwargs)
        :return: 
        """
        yield self._get_attr_inn_world_tm_infos()

    def is_connected(self):
        attr = self._get_attr_inn_world_tm()
        return attr.isDestination()

    def connect(self):
        # Connect external guide to network
        attr_inn = self._get_attr_inn_world_tm()
        pymel.connectAttr(self.obj.worldMatrix, attr_inn)

    def disconnect(self):
        # Disconnect external guide from network
        attr_inn = self._get_attr_inn_world_tm()
        pymel.disconnectAttr(self.obj.worldMatrix, attr_inn)
