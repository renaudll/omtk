import pymel.core as pymel

from omtk.core import classNode
from omtk.libs import libRigging
from omtk.libs import libAttr
from omtk.models import model_avar_base


class AvarSurfaceModel(model_avar_base.AvarInflBaseModel):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """

    SHOW_IN_UI = False

    _ATTR_NAME_U_BASE = "baseU"
    _ATTR_NAME_V_BASE = "baseV"
    _ATTR_NAME_U = "surfaceU"
    _ATTR_NAME_V = "surfaceV"
    _ATTR_NAME_MULT_LR = "multiplierLr"
    _ATTR_NAME_MULT_UD = "multiplierUd"
    _ATTR_NAME_MULT_FB = "multiplierFb"

    # Define how many unit is moved in uv space in relation with the avars.
    # Taking in consideration that the avar is centered in uv space,
    # we want at minimum 0.5 of multiplier so moving the avar to 1.0 will
    # move the follicle at the top of uv space (0.5 units).
    # However in production, we found that limiting
    # the range of avars  from -1.0 to 1.0 is not very flexible.
    # ex: We want the lips to follow the chin but we don't necessarily
    # want the lips reach the chin when the UD avar is -1.
    # For this reason, we found that using a multiplier of 0.25 work best.
    # This also help rigger visually since the surface plane have
    # a visual edge at at each 25% of it's length.
    # todo: Move this to AvarFollicle.
    default_multiplier_lr = 0.25
    default_multiplier_ud = 0.25
    default_multiplier_fb = 0.10

    def __init__(self, *args, **kwargs):
        super(AvarSurfaceModel, self).__init__(*args, **kwargs)

        self._stack = None
        self._attr_u_base = None
        self._attr_v_base = None

        self._attr_inn_surface = None
        self._attr_inn_surface_tm = None
        self._attr_inn_surface_min_value_u = None
        self._attr_inn_surface_min_value_v = None
        self._attr_inn_surface_max_value_u = None
        self._attr_inn_surface_max_value_v = None

        self._attr_length_v = None
        self._attr_length_u = None

        # Reference to the object containing the bind pose of the avar.
        self._obj_offset = None

    def _get_follicle_relative_uv_attr(self, mult_u=1.0, mult_v=1.0):
        """
        Resolve the relative U and V attributes that will be sent to the follicles.

        :return: he relative parameterU and relative parameterV attributes.
        :rtype: tuple[pymel.Attribute, pymel.Attribute]
        """
        # Apply custom multiplier
        attr_u = libRigging.create_utility_node(
            "multiplyDivide", input1X=self._attr_inn_lr, input2X=self.multiplier_lr
        ).outputX

        attr_v = libRigging.create_utility_node(
            "multiplyDivide", input1X=self._attr_inn_ud, input2X=self.multiplier_ud
        ).outputX

        return attr_u, attr_v

    def _get_follicle_absolute_uv_attr(self, mult_u=1.0, mult_v=1.0):
        """
        Resolve the absolute parameterU and parameterV that will be sent to the follicles.
        :param mult_u: Custom multiplier
        :param mult_v:
        :return: A tuple containing two pymel.Attribute: the absolute parameterU and relative parameterV.
        """
        # TODO: Move attribute definition outside this function.
        attr_u_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U)
        attr_v_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V)

        attr_u_relative, attr_v_relative = self._get_follicle_relative_uv_attr(
            mult_u=mult_u, mult_v=mult_v
        )

        # Add base parameterU & parameterV
        attr_u_cur = libRigging.create_utility_node(
            "addDoubleLinear", input1=self._attr_u_base, input2=attr_u_relative
        ).output

        attr_v_cur = libRigging.create_utility_node(
            "addDoubleLinear", input1=self._attr_v_base, input2=attr_v_relative
        ).output

        # TODO: Move attribute connection outside of this function.
        pymel.connectAttr(attr_u_cur, attr_u_inn)
        pymel.connectAttr(attr_v_cur, attr_v_inn)

        return attr_u_inn, attr_v_inn

    def _create_interface(self):
        super(AvarSurfaceModel, self)._create_interface()

        self._attr_inn_surface = libAttr.addAttr(
            self.grp_rig, "innSurface", dt="nurbsSurface"
        )
        self._attr_inn_surface_tm = libAttr.addAttr(
            self.grp_rig, "innSurfaceTm", dataType="matrix"
        )
        self._attr_inn_surface_min_value_u = libAttr.addAttr(
            self.grp_rig, "innSurfaceMinValueU", defaultValue=0
        )
        self._attr_inn_surface_min_value_v = libAttr.addAttr(
            self.grp_rig, "innSurfaceMinValueV", defaultValue=0
        )
        self._attr_inn_surface_max_value_u = libAttr.addAttr(
            self.grp_rig, "innSurfaceMaxValueU", defaultValue=1
        )
        self._attr_inn_surface_max_value_v = libAttr.addAttr(
            self.grp_rig, "innSurfaceMaxValueV", defaultValue=1
        )

    def _build(self):
        """
        The dag stack is a chain of transform nodes daisy chained together that computer the final transformation of the influence.
        The decision of using transforms instead of multMatrix nodes is for clarity.
        Note also that because of it's parent (the offset node) the stack relative to the influence original translation.
        """
        nomenclature_rig = self.get_nomenclature_rig()

        # Currently our utilities expect a complete surface shape.
        # It is also more friendly for the rigger to see
        # the surface directly in the model.
        surface_shape = pymel.createNode(
            "nurbsSurface", name=nomenclature_rig.resolve("surface"),
        )
        self._surface = surface_shape.getParent()
        self._surface.visibility.set(False)
        self._surface.setParent(self.grp_rig)
        self._surface.rename(nomenclature_rig.resolve("surface"))
        pymel.connectAttr(self._attr_inn_surface, surface_shape.create)
        libRigging.connect_matrix_to_node(
            self._attr_inn_surface_tm, self._surface, name="decomposeSurfaceTm"
        )

        self._stack = classNode.Node()
        self._stack.build(name=nomenclature_rig.resolve("avar"))
        self._stack.setParent(self.grp_rig)
        # self.build_stack(self._stack)

        self.grp_offset = pymel.createNode(
            "transform", name=nomenclature_rig.resolve("offset"), parent=self.grp_rig,
        )
        libRigging.connect_matrix_to_node(
            self._attr_inn_offset_tm,
            self.grp_offset,
            name=nomenclature_rig.resolve("decomposeOffset"),
        )

        #
        # Extract the base U and V of the base influence using the stack parent. (the 'offset' node)
        #

        util_get_base_uv_absolute = libRigging.create_utility_node(
            "closestPointOnSurface",
            inPosition=self.grp_offset.t,
            inputSurface=self._attr_inn_surface,
        )

        util_get_base_uv_normalized = libRigging.create_utility_node(
            "setRange",
            oldMinX=self._attr_inn_surface_min_value_u,
            oldMaxX=self._attr_inn_surface_max_value_u,
            oldMinY=self._attr_inn_surface_min_value_v,
            oldMaxY=self._attr_inn_surface_max_value_v,
            minX=0,
            maxX=1,
            minY=0,
            maxY=1,
            valueX=util_get_base_uv_absolute.parameterU,
            valueY=util_get_base_uv_absolute.parameterV,
        )
        attr_base_u_normalized = util_get_base_uv_normalized.outValueX
        attr_base_v_normalized = util_get_base_uv_normalized.outValueY

        self._attr_u_base = libAttr.addAttr(
            self.grp_rig,
            longName=self._ATTR_NAME_U_BASE,
            defaultValue=attr_base_u_normalized.get(),
        )
        self._attr_v_base = libAttr.addAttr(
            self.grp_rig,
            longName=self._ATTR_NAME_V_BASE,
            defaultValue=attr_base_v_normalized.get(),
        )

        pymel.connectAttr(
            attr_base_u_normalized, self.grp_rig.attr(self._ATTR_NAME_U_BASE)
        )
        pymel.connectAttr(
            attr_base_v_normalized, self.grp_rig.attr(self._ATTR_NAME_V_BASE)
        )

        #
        # Create follicle setup
        # The setup is composed of two follicles.
        # One for the "bind pose" and one "driven" by the avars..
        # The delta between the "bind pose" and the "driven" follicles is then applied to the influence.
        #

        # Determine the follicle U and V on the reference nurbsSurface.
        base_u_val = self._attr_u_base.get()
        base_v_val = self._attr_v_base.get()

        # Resolve the length of each axis of the surface
        (
            self._attr_length_u,
            self._attr_length_v,
            arcdimension_shape,
        ) = libRigging.create_arclengthdimension_for_nurbsplane(self._surface)
        arcdimension_transform = arcdimension_shape.getParent()
        arcdimension_transform.rename(nomenclature_rig.resolve("arcdimension"))
        arcdimension_transform.setParent(self.grp_rig)

        #
        # Resolve the parameterU and parameterV
        #

        attr_u_inn, attr_v_inn = self._get_follicle_absolute_uv_attr()

        #
        # Create two follicle.
        # - bindPoseFollicle: A follicle that stay in place and keep track of the original position.
        # We'll then compute the delta of the position of the two follicles.
        # This allow us to move or resize the plane without affecting the built rig. (if the rig is in neutral pose)
        #
        offset_name = nomenclature_rig.resolve("bindPoseRef")
        self._obj_offset = pymel.createNode("transform", name=offset_name)
        self._obj_offset.setParent(self.grp_offset)

        fol_offset_name = nomenclature_rig.resolve("bindPoseFollicle")
        fol_offset_shape = libRigging.create_follicle2(
            self._surface, u=base_u_val, v=base_v_val
        )
        fol_offset = fol_offset_shape.getParent()
        fol_offset.rename(fol_offset_name)
        pymel.parentConstraint(fol_offset, self._obj_offset, maintainOffset=False)
        fol_offset.setParent(self.grp_rig)

        from omtk.core.compounds import create_compound

        # Create an "InfinityFollicle"
        # This follicle setup can continue out of the bound of it's surface.
        infinity_follicle = create_compound(
            "omtk.InfinityFollicle",
            nomenclature_rig.resolve("infinityFollicle"),
            inputs={
                "surface": self._surface.worldSpace,
                "surfaceU": attr_u_inn,
                "surfaceV": attr_v_inn,
            },
        )
        infinity_follicle_tm = pymel.Attribute("%s.outputTM" % infinity_follicle.output)

        #
        # Extract the delta of the influence follicle and it's initial pose follicle
        #
        attr_localTM = libRigging.create_utility_node(
            "multMatrix",
            matrixIn=[infinity_follicle_tm, self._obj_offset.worldInverseMatrix],
        ).matrixSum

        # Since we are extracting the delta between the influence
        # and the bindpose matrix, the rotation of the surface is not
        # taken in consideration wich make things less intuitive for the rigger.
        # So we'll add an adjustement matrix so the rotation
        # of the surface is taken in consideration.
        util_decompose_tm_bindPose = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=self._obj_offset.worldMatrix
        )
        attr_translate_tm = libRigging.create_utility_node(
            "composeMatrix", inputTranslate=util_decompose_tm_bindPose.outputTranslate
        ).outputMatrix
        attr_translate_tm_inv = libRigging.create_utility_node(
            "inverseMatrix", inputMatrix=attr_translate_tm,
        ).outputMatrix
        attr_rotate_tm = libRigging.create_utility_node(
            "multMatrix", matrixIn=[self._obj_offset.worldMatrix, attr_translate_tm_inv]
        ).matrixSum
        attr_rotate_tm_inv = libRigging.create_utility_node(
            "inverseMatrix", inputMatrix=attr_rotate_tm
        ).outputMatrix
        attr_final_tm = libRigging.create_utility_node(
            "multMatrix", matrixIn=[attr_rotate_tm_inv, attr_localTM, attr_rotate_tm]
        ).matrixSum
        util_decompose_tm = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_final_tm
        )

        #
        # Create the 1st (follicleLayer) that will contain the extracted position from the ud and lr Avar.
        #
        layer_follicle = self._stack.append_layer("follicleLayer")
        pymel.connectAttr(util_decompose_tm.outputTranslate, layer_follicle.translate)

        pymel.connectAttr(self._attr_u_base, fol_offset.parameterU)
        pymel.connectAttr(self._attr_v_base, fol_offset.parameterV)

        # Create the third layer that apply the translation provided by the fb Avar.
        layer_fb = self._stack.append_layer("fbLayer")
        attr_get_fb = libRigging.create_utility_node(
            "multiplyDivide", input1X=self._attr_inn_fb, input2X=self._attr_length_u
        ).outputX
        attr_get_fb_adjusted = libRigging.create_utility_node(
            "multiplyDivide", input1X=attr_get_fb, input2X=self.multiplier_fb
        ).outputX
        pymel.connectAttr(attr_get_fb_adjusted, layer_fb.translateZ)

        # Create the 4th layer (folRot) that apply the rotation provided by
        # the follicle controlled by the ud and lr Avar.
        # This is necessary since we don't want to rotation
        # to affect the oobLayer and fbLayer.
        layer_follicle_rot = self._stack.append_layer("folRot")
        pymel.connectAttr(util_decompose_tm.outputRotate, layer_follicle_rot.rotate)

        # Create a 5th layer that apply the avar rotation and scale.
        layer_rot = self._stack.append_layer("rotLayer")
        pymel.connectAttr(self._attr_inn_yw, layer_rot.rotateY)
        pymel.connectAttr(self._attr_inn_pt, layer_rot.rotateX)
        pymel.connectAttr(self._attr_inn_rl, layer_rot.rotateZ)
        pymel.connectAttr(self._attr_inn_sx, layer_rot.scaleX)
        pymel.connectAttr(self._attr_inn_sy, layer_rot.scaleY)
        pymel.connectAttr(self._attr_inn_sz, layer_rot.scaleZ)

        return self._stack.worldMatrix

    def connect_surface(self, surface):
        pymel.connectAttr(surface.worldSpace, self._attr_inn_surface)
        pymel.connectAttr(surface.worldMatrix, self._attr_inn_surface_tm)
        pymel.connectAttr(surface.minValueU, self._attr_inn_surface_min_value_u)
        pymel.connectAttr(surface.maxValueU, self._attr_inn_surface_max_value_u)
        pymel.connectAttr(surface.minValueV, self._attr_inn_surface_min_value_v)
        pymel.connectAttr(surface.maxValueV, self._attr_inn_surface_max_value_v)

    def connect_avar(self, avar):
        super(AvarSurfaceModel, self).connect_avar(avar)

        self.connect_surface(avar.surface)
