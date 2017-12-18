"""
Simple backport of the Component logic from OMTK2.
"""
import pymel.core as pymel
from omtk.libs import libRigging


# taken from xlib
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


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


class ComponentWizard(object):
    def __init__(self):
        self.grp_inn = pymel.createNode('transform', name='inn')
        self.grp_out = pymel.createNode('transform', name='out')
        self.grp_parent = pymel.createNode('transform', name='parent')
        self.grp_anms = pymel.createNode('transform', name='ctrls')
        self.grp_infs = pymel.createNode('transform', name='infls')

        pymel.addAttr(self.grp_inn, longName='parentWorldMatrix', dataType='matrix')
        pymel.connectAttr(self.grp_parent.worldMatrix, self.grp_inn.attr('parentWorldMatrix'))

    def _get_attr_name_from_obj(self, obj, prefix='', suffix=''):
        basename_snakecase = obj.nodeName()
        if prefix:
            basename = to_pascal_case(basename_snakecase)
        else:
            basename = to_camel_case(basename_snakecase)
        return prefix + basename + suffix

    def _export_input_local_tm(self, obj_internal, obj_external, prefix='', suffix='LocalMatrix'):
        attr_name = self._get_attr_name_from_obj(obj_internal, prefix=prefix, suffix=suffix)
        pymel.addAttr(self.grp_inn, longName=attr_name, dataType='matrix')
        attr = self.grp_inn.attr(attr_name)

        # Connect external obj
        pymel.connectAttr(obj_external.matrix, attr)

        # Connect internal_obj
        decomposeTM = libRigging.create_utility_node(
            'decomposeMatrix',
            name='decompose{0}'.format(attr_name),
            inputMatrix=attr
        )
        pymel.connectAttr(decomposeTM.outputTranslate, obj_internal.translate)
        pymel.connectAttr(decomposeTM.outputRotate, obj_internal.rotate)
        pymel.connectAttr(decomposeTM.outputScale, obj_internal.scale)

    def _expose_output_tm(self, obj_internal, obj_external, prefix='', suffix='WorldMatrix'):
        # Create network out attribute
        attr_name = self._get_attr_name_from_obj(obj_internal, prefix=prefix, suffix=suffix)
        pymel.addAttr(self.grp_out, longName=attr_name, dataType='matrix')
        attr_out = self.grp_out.attr(attr_name)
        pymel.connectAttr(obj_internal.worldMatrix, attr_out)

        multTM = libRigging.create_utility_node(
            'multMatrix',
            name='getLocal{0}'.format(attr_name),
            matrixIn=(attr_out, obj_external.parentInverseMatrix)
        )

        decomposeTM = libRigging.create_utility_node(
            'decomposeMatrix',
            name='decompose{0}'.format(attr_name),
            inputMatrix=multTM.matrixSum
        )
        pymel.connectAttr(decomposeTM.outputTranslate, obj_external.translate)
        pymel.connectAttr(decomposeTM.outputRotate, obj_external.rotate)
        pymel.connectAttr(decomposeTM.outputScale, obj_external.scale)

    def expose_ctrl(self, ctrl_internal):
        ctrl_offset_internal = ctrl_internal.getParent()

        # Create a duplicate of the ctrl
        ctrl_external = _duplicate_ctrl(ctrl_internal)

        # Create the offset
        ctrl_offset_external = macros.create_offset_grp(ctrl_external)
        ctrl_offset_external.setParent(self.grp_anms)

        self._export_input_local_tm(ctrl_internal, ctrl_external, prefix='ctrl')
        self._expose_output_tm(ctrl_offset_internal, ctrl_offset_external, prefix='ctrl')

    def expose_infl(self, internal_infl):
        infl = pymel.createNode('joint')
        infl.rename(internal_infl.nodeName())
        infl.setParent(self.grp_infs)

        self._expose_output_tm(internal_infl, infl, prefix='infl')


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


class ComponentWizard(object):
    def __init__(self):
        self.grp_inn = pymel.createNode('transform', name='inn')
        self.grp_out = pymel.createNode('transform', name='out')
        self.grp_parent = pymel.createNode('transform', name='parent')
        self.grp_anms = pymel.createNode('transform', name='ctrls')
        self.grp_infs = pymel.createNode('transform', name='infls')

        self.parts_ctrl = []
        self.parts_guides = []
        self.parts_influences = []

    def _export_input_local_tm(self, obj_internal, obj_external, prefix='', suffix='LocalMatrix'):
        attr_name = _get_attr_name_from_obj(obj_internal, prefix=prefix, suffix=suffix)
        attr = _add_or_get_attr(self.grp_inn, attr_name, dataType='matrix')

        # Connect external obj
        pymel.connectAttr(obj_external.matrix, attr)

        # Connect internal_obj
        decomposeTM = libRigging.create_utility_node(
            'decomposeMatrix',
            name='decompose{0}'.format(attr_name),
            inputMatrix=attr
        )
        pymel.connectAttr(decomposeTM.outputTranslate, obj_internal.translate)
        pymel.connectAttr(decomposeTM.outputRotate, obj_internal.rotate)
        pymel.connectAttr(decomposeTM.outputScale, obj_internal.scale)

    def _expose_output_tm(self, obj_internal, obj_external, prefix='', suffix='WorldMatrix'):
        # Create network out attribute
        attr_name = _get_attr_name_from_obj(obj_internal, prefix=prefix, suffix=suffix)
        attr_out = _add_or_get_attr(self.grp_out, attr_name, dataType='matrix')
        pymel.connectAttr(obj_internal.worldMatrix, attr_out)

        multTM = libRigging.create_utility_node(
            'multMatrix',
            name='getLocal{0}'.format(attr_name),
            matrixIn=(attr_out, obj_external.parentInverseMatrix)
        )

        decomposeTM = libRigging.create_utility_node(
            'decomposeMatrix',
            name='decompose{0}'.format(attr_name),
            inputMatrix=multTM.matrixSum
        )
        pymel.connectAttr(decomposeTM.outputTranslate, obj_external.translate)
        pymel.connectAttr(decomposeTM.outputRotate, obj_external.rotate)
        pymel.connectAttr(decomposeTM.outputScale, obj_external.scale)

    def expose_ctrl(self, ctrl_internal):
        ctrl_offset_internal = ctrl_internal.getParent()

        # Create a duplicate of the ctrl
        ctrl_external = _duplicate_ctrl(ctrl_internal)

        # Create the offset
        ctrl_offset_external = create_offset_grp(ctrl_external)
        ctrl_offset_external.setParent(self.grp_anms)

        self._export_input_local_tm(ctrl_internal, ctrl_external, prefix='ctrl')
        self._expose_output_tm(ctrl_offset_internal, ctrl_offset_external, prefix='ctrl')

    def expose_infl(self, internal_infl):
        infl = pymel.createNode('joint')
        infl.rename(internal_infl.nodeName())
        infl.setParent(self.grp_infs)

        self._expose_output_tm(internal_infl, infl, prefix='infl')


# todo: handle ctrl with non-zero transform???

class ComponentPart(object):
    def __init__(self, parent=None, obj=None):  # hack: parent and obj are keywoard argument for libSerialization compatibility
        # type: (ComponentWizard) -> None
        self.parent = parent
        self.obj = obj

    def __repr__(self):
        return self.obj.nodeName()

    def initialize(self):
        pass

    def is_connected(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError


class ComponentPartCtrl(ComponentPart):
    def __init__(self, parent=None, obj=None):  # hack: parent and obj are keywoard argument for libSerialization compatibility
        super(ComponentPartCtrl, self).__init__(parent, obj)
        # assert(isinstance(parent, ComponentWizard))
        # self._obj = obj
        self.obj_offset = None
        self.external_ctrl = None
        self.external_ctrl_offset = None

        self._attr_inn_ctrl_tm = None
        self._attr_out_ctrl_offset_tm = None

    def initialize(self):
        self.obj_offset = self.obj.getParent()

        # Create a duplicate of the ctrl
        self.external_ctrl = _duplicate_ctrl(self.obj)

        # Create the offset
        self.external_ctrl_offset = create_offset_grp(self.external_ctrl)
        self.external_ctrl_offset.setParent(self.parent.grp_anms)

        # Create CtrlLocalMatrix network input attribute
        attr_inn_ctrl_tm_name = _get_attr_name_from_obj(self.obj, prefix='ctrl', suffix='LocalMatrix')
        self._attr_inn_ctrl_tm = _add_or_get_attr(self.parent.grp_inn, attr_inn_ctrl_tm_name, dataType='matrix')

        # Create CtrlOffsetWorldMatrix network output attribute
        attr_out_ctrl_offset_tm = _get_attr_name_from_obj(self.obj, prefix='ctrl', suffix='WorldMatrix')
        self._attr_out_ctrl_offset_tm = _add_or_get_attr(self.parent.grp_out, attr_out_ctrl_offset_tm,
                                                         dataType='matrix')

    def is_connected(self):
        return self.obj.translate.isDestination()

    def connect(self):
        self.parent._export_input_local_tm(self.obj, self.external_ctrl, prefix='ctrl')
        self.parent._expose_output_tm(self.obj_offset, self.external_ctrl_offset, prefix='ctrl')

    def disconnect(self):
        # Remove the decomposeMatrix between the network input hub and the ctrl itself.
        util_decompose_tm = self.obj.translate.inputs()[0]
        pymel.delete(util_decompose_tm)


class ComponentPartInfluence(ComponentPart):
    def __init__(self, parent=None, obj=None):  # hack: parent and obj are keywoard argument for libSerialization compatibility
        super(ComponentPartInfluence, self).__init__(parent, obj)
        self._obj_external = None

    def initialize(self):
        self._obj_external = pymel.createNode("joint")  # todo: rename?

    def connect(self):
        self.parent._expose_output_tm(self.obj, self._obj_external, prefix='infl')


class ComponentPartGuide(ComponentPart):
    def __init__(self, parent=None, obj=None):  # hack: parent and obj are keywoard argument for libSerialization compatibility
        super(ComponentPartGuide, self).__init__(parent, obj)
        self._obj_external = None

    def initialize(self):
        self._obj_external = pymel.createNode("joint")  # todo: rename?

    def connect(self):
        self.parent._export_input_world_tm(self._obj_external, self.obj, prefix='ctrl')
