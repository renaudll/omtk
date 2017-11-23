import pymel.core as pymel

from omtk.core import module_logic_ctrl
from omtk.libs import libRigging
from omtk.libs import libHistory


class CtrlLogicInteractive(module_logic_ctrl.CtrlLogicFaceCalibratable):
    """
    An InteractiveCtrl ctrl is directly constrained on a mesh via a layer_fol.
    To prevent double deformation, the trick is an additional layer before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so the animator don't need to see the whole setup.

    However an InterfactiveCtrl might still have to be callibrated.
    This is necessay to keep the InteractiveCtrl values in a specific range (ex: -1 to 1) in any scale.
    The calibration apply non-uniform scaling on the ctrl parent to cheat the difference.

    For this reason an InteractiveCtrl is created using the following steps:
    1) Create the setup (using build)
    2) Connecting the doritos ctrl to something
    3) Optionally call .calibrate()
    """
    name = 'Interactive'
    _ATTR_NAME_SENSITIVITY_TX = 'sensitivityX'
    _ATTR_NAME_SENSITIVITY_TY = 'sensitivityY'
    _ATTR_NAME_SENSITIVITY_TZ = 'sensitivityZ'

    def __init__(self, *args, **kwargs):
        super(CtrlLogicInteractive, self).__init__(*args, **kwargs)
        self.follicle = None  # Used for calibration
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None
        self.mesh = None

        self._stack = None

    # def validate(self):
    #     super(CtrlLogicInteractive, self).validate()
    # 
    #     # Ensure we have an head influence to base our rotation on.
    #     jnt_head = self.get_head_jnt()
    #     if not jnt_head:
    #         raise Exception("Can't resolve head influence. Please create a Head module.")
    # 
    #     # Ensure we have a mesh to slide on.
    #     meshes = libHistory.get_affected_shapes(self.jnts)
    #     if not meshes:
    #         raise Exception("Found no mesh associated with influences {0}".format(self.jnts))

    def parent_to(self, parent):
        """
        Bypass default parent mecanism since it is computer internally.
        """
        pass

    def get_default_tm_ctrl(self):
        """
        :return: The ctrl transformation.
        """
        if self.jnt is None:
            self.warning("Cannot resolve ctrl matrix with no inputs!")
            return None

        tm = self.jnt.getMatrix(worldSpace=True)

        # We always try to position the controller on the surface of the face.
        # The face is always looking at the positive Z axis.
        pos = tm.translate
        dir = pymel.datatypes.Point(0, 0, 1)
        result = self.rig.raycast_farthest(pos, dir)
        if result:
            tm.a30 = result.x
            tm.a31 = result.y
            tm.a32 = result.z

        return tm

    def build(self, avar, cancel_r=False, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

        # # todo: use property?
        # if self.mesh is None:
        #     self.mesh = next(iter(libHistory.get_affected_shapes(self.jnts)), None)
        # 
        pos_ref = self.get_default_tm_ctrl().translate
        jnt_head = self.get_head_jnt()
        # pos_ref_local = pos_ref * jnt_head.getMatrix(worldSpace=True).inverse()
        # need_flip = pos_ref_local.x < 0

        super(CtrlLogicInteractive, self).build(avar, cancel_r=cancel_r, **kwargs)

        # Create the follicle setup
        fol_name = nomenclature_rig.resolve('follicle')
        _, u_coord, v_coord = libRigging.get_closest_point_on_shape(self.mesh, pos_ref)
        fol_shape = libRigging.create_follicle2(self.mesh, u=u_coord, v=v_coord)
        fol_transform = fol_shape.getParent()
        self.follicle = fol_transform
        fol_transform.rename(fol_name)
        fol_transform.setParent(self.grp_rig)

        layer_fol_name = nomenclature_rig.resolve('doritosFol')
        layer_fol = self._stack.append_layer()
        layer_fol.rename(layer_fol_name)
        layer_fol.setParent(self.grp_rig)

        layer_fol = self._stack.prepend_layer('follicle')

        attr_get_follicle_local_tm = libRigging.create_utility_node(
            'multMatrix',
            name=nomenclature_rig.resolve('getFollicleLocalTm'),
            matrixIn=(
                fol_transform.worldMatrix,
                self._grp_parent.worldInverseMatrix
            )
        ).matrixSum

        util_decompose_follicle_local_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            name=nomenclature_rig.resolve('decomposeFollicleLocalTm'),
            inputMatrix=attr_get_follicle_local_tm
        )
        pymel.connectAttr(util_decompose_follicle_local_tm.outputTranslate, layer_fol.translate)

        # pymel.parentConstraint(fol_transform, layer_fol)
        # pymel.parentConstraint(fol_transform, layer_fol, maintainOffset=True, skipRotate=['x', 'y', 'z'])
        # pymel.orientConstraint(jnt_head, layer_fol, maintainOffset=True)

        #
        # Constraint grp_rig
        #
        # pymel.parentConstraint(layer_fol, self._grp_output, maintainOffset=True, skipRotate=['x', 'y', 'z'])

        # Constraint rotation
        # The doritos setup can be hard to control when the rotation of the controller depend on the layer_fol since
        # any deformation can affect the normal of the faces.
        # pymel.orientConstraint(jnt_head, layer_fol, maintainOffset=True)

    def _connect_output_tr(self):
        # Position
        stack_end = self._stack.get_stack_end()

        util_decompose_stack_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=stack_end.worldMatrix
        )
        util_decompose_parent_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=self._grp_parent.worldMatrix
        )
        attr_pos_world_tm = libRigging.create_utility_node(
            'composeMatrix',
            inputTranslate=util_decompose_stack_tm.outputTranslate,
            inputRotate=util_decompose_parent_tm.outputRotate,
            inputScale=util_decompose_parent_tm.outputScale
        ).outputMatrix

        util_decompose_local_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=attr_pos_world_tm
        )

        pymel.connectAttr(util_decompose_local_tm.outputTranslate, self._grp_output.translate)
        pymel.connectAttr(util_decompose_local_tm.outputRotate, self._grp_output.rotate)

    def _get_calibration_reference(self):
        return self.follicle

    def unbuild(self):
        super(CtrlLogicInteractive, self).unbuild()
        # TODO: Maybe hold and fetch the senstivity? Will a doritos will ever be serialzied?
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

        self.follicle = None


def register_plugin():
    return CtrlLogicInteractive
