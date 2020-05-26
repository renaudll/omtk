"""
Logic for the "FK" module
"""
from maya import cmds
import pymel.core as pymel

from omtk.core.ctrl import BaseCtrl
from omtk.core.module import Module, CompoundModule
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.vendor.omtk_compound.core import create_empty


class CtrlFk(BaseCtrl):
    """
    An FK controller
    """

    def create_ctrl(self, *args, **kwargs):
        node = super(CtrlFk, self).create_ctrl(multiplier=1.1, *args, **kwargs)

        make = next(iter(node.inputs()), None)
        if make:
            make.degree.set(1)
            make.sections.set(8)

        return node


class FK(CompoundModule):
    """
    A Simple FK with support for multiple hierarchy.
    """

    CREATE_GRP_RIG = False
    DEFAULT_NAME_USE_FIRST_INPUT = True
    _NAME_CTRL_ENUMERATE = False  # If set to true, the ctrl will use the module name.
    _FORCE_INPUT_NAME = (
        False  # Force using the name of the input in the name of the ctrl
    )
    # Otherwise they will use their associated input name.
    _CLS_CTRL = CtrlFk

    def __init__(self, *args, **kwargs):
        super(FK, self).__init__(*args, **kwargs)
        self.ctrls = []
        self.sw_translate = False
        self.create_spaceswitch = True

    def build(self, constraint=True, parent=True, *args, **kwargs):
        """
        :param bool constraint: Should we constraint the inputs to the controller?
        :param bool parent: Unused
        """
        naming = self.get_nomenclature()

        super(FK, self).build(parent=False, *args, **kwargs)

        # Initialize ctrls
        libPython.resize_list(self.ctrls, len(self.jnts))
        for idx, ctrl in enumerate(self.ctrls):
            self.ctrls[idx] = self._CLS_CTRL.from_instance(ctrl)

        # TODO: Do we really want to support multiple chains?
        for chain in self.chains:
            chain_ctrls = self._build_chain(chain)
            chain_ctrls[0].setParent(self.grp_anm, relative=True)
            libRigging.create_hyerarchy(chain_ctrls, relative=True)

            # Build space-switch for first chain ctrl
            if self.create_spaceswitch:
                kwargs = {"add_world": True}
                if not self.sw_translate:
                    kwargs["skipTranslate"] = ["x", "y", "z"]
                chain_ctrls[0].create_spaceswitch(self, self.parent_jnt, **kwargs)
        
        # TODO: Simplify this, move it to the Module class maybe?
        if self.parent_jnt and self.parent_jnt != self.rig.grp_jnt:  # TODO: This check should not be per-module
            parent_tm = libRigging.create_multiply_matrix([
                self.parent_jnt.worldMatrix, self.rig.grp_jnt.worldInverseMatrix
            ])
            libRigging.connect_matrix_to_node(
                parent_tm,
                self.grp_anm,
                name=naming.resolve("getParentWorldTM"),
            )

        attr_outs = self.compound_outputs.out
        for idx, ctrl in enumerate(self.ctrls):
            attr_tm = get_tm_from_ctrl(ctrl)
            pymel.connectAttr(attr_tm, attr_outs[idx])

        if constraint:
            for jnt, attr_out in zip(self.jnts, attr_outs):
                libRigging.connect_matrix_to_node(attr_out, jnt)

    def _build_compound(self):
        """
        Re-crete the IK3 compound but with a variable number of inputs.
        """
        inst = create_empty(namespace=self.name)
        cmds.addAttr(inst.output, longName="out", dataType="matrix", multi=True)
        return inst

    def _build_chain(self, chain):
        """
        Build the setup for a chain oj joints.

        :param chain: A chain of joints
        :type chain: omtk.libs.libPymel.PyNodeChain
        :return: The chain controllers
        :rtype: list of CtrlFk
        """
        ctrls = []
        for j, jnt in enumerate(chain):
            ctrl = self.ctrls[self.jnts.index(jnt)]
            ctrl_name = self._get_ctrl_name(jnt, j)
            ctrl.build(name=ctrl_name, refs=jnt, geometries=self.rig.get_meshes())
            ctrl.setMatrix(jnt.getMatrix())
            ctrls.append(ctrl)

        return ctrls

    def _get_ctrl_name(self, obj, index):
        """
        Helper method to resolve the name of a controller.

        Note that there's multiple way to name the ctrls.

        1) If there are multiple inputs, each ctrl will use the input as it's base.
            ex: (considering a module named "arm")
            jnt_upperarm_l -> ctrl_arm_upperarm_l
            jnt_forearm_l  -> ctrl_arm_forearm_l

        2) If there is only one input, the single ctrl will use the module name.
            ex: (considering a module named "arm")
            jnt_upperarm_l -> ctrl_arm_l

        3) If `_NAME_CTRL_ENUMERATE` is True, the first object of each chain
           will act as the base name
           ex (considering a module named "arm")
           jnt_upperarm_l -> ctrl_arm_01_l
           jnt_forearm_l  -> ctrl_arm_02_l

        :param int index: The influence index in the chain
        :param obj: The influence to extract base name from
        :type obj: pymel.nodetypes.Joint
        :return: The controller name
        :rtype: str
        """
        # TODO: Write unit-tests for this
        # TODO: Simplify rules
        basename = obj.stripNamespace().nodeName()
        naming_anm = self.get_nomenclature_anm()

        # Resolve ctrl name.
        naming = naming_anm + self.rig.nomenclature(basename, suffix=None, prefix=None)

        if self._FORCE_INPUT_NAME:
            return naming.resolve()

        if len(self.jnts) == 1 and len(self.chains) == 1:
            return naming_anm.resolve()

        if len(self.chains) == 1 or self._NAME_CTRL_ENUMERATE:
            return naming_anm.resolve("{0:02d}".format(index))

        return naming.resolve()


def register_plugin():
    """
    Register the plugin. This function is expected by plugin_manager.

    :return: The plugin to register
    :rtype: omtk.core.modules.Module
    """
    return FK


def _iter_ctrl_local_tm_contributors(ctrl):
    """

    :param ctrl:
    :type ctrl: omtk.core.ctrl.BaseCtrl
    :return:
    """
    node = ctrl.node
    while node:
        yield node
        if node == ctrl.offset:
            return
        node = node.getParent()


def get_tm_from_ctrl(ctrl):
    """

    :param ctrl:
    :type ctrl: omtk.core.ctrl.BaseCtrl
    :return:
    """
    return libRigging.create_multiply_matrix(
        [node.matrix for node in _iter_ctrl_local_tm_contributors(ctrl)]
    )
