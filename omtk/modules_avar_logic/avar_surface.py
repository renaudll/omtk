import pymel.core as pymel
from omtk.modules_avar_logic import avar_linear
from omtk.libs import libRigging
from omtk.libs import libAttr
from omtk.libs import libPymel


def create_surface(nomenclature, jnts, epsilon=0.001, default_scale=1.0):
    """
    Create a simple rig to deform a nurbsSurface, allowing the rigger to easily provide
    a surface for the influence to slide on.
    :param name: The suffix of the surface name to create.
    :return: A pymel.nodetypes.Transform instance of the created surface.
    """
    root = pymel.createNode('transform')
    pymel.addAttr(root, longName='bendUpp', k=True)
    pymel.addAttr(root, longName='bendLow', k=True)
    pymel.addAttr(root, longName='bendSide', k=True)

    # Create Guide
    plane_transform, plane_make = pymel.nurbsPlane(patchesU=4, patchesV=4)

    # Create Bends
    bend_side_deformer, bend_side_handle = pymel.nonLinear(plane_transform, type='bend')
    bend_upp_deformer, bend_upp_handle = pymel.nonLinear(plane_transform, type='bend')
    bend_low_deformer, bend_low_handle = pymel.nonLinear(plane_transform, type='bend')

    plane_transform.r.set(0, -90, 0)
    bend_side_handle.r.set(90, 90, 0)
    bend_upp_handle.r.set(180, 90, 0)
    bend_low_handle.r.set(180, 90, 0)
    bend_upp_deformer.highBound.set(0)  # create pymel warning
    bend_low_deformer.lowBound.set(0)  # create pymel warning

    plane_transform.setParent(root)
    bend_side_handle.setParent(root)
    bend_upp_handle.setParent(root)
    bend_low_handle.setParent(root)

    pymel.connectAttr(root.bendSide, bend_side_deformer.curvature)
    pymel.connectAttr(root.bendUpp, bend_upp_deformer.curvature)
    pymel.connectAttr(root.bendLow, bend_low_deformer.curvature)

    # Rename all the things!
    root.rename(nomenclature.resolve('SurfaceGrp'))
    plane_transform.rename(nomenclature.resolve('Surface'))
    bend_upp_deformer.rename(nomenclature.resolve('UppBend'))
    bend_low_deformer.rename(nomenclature.resolve('LowBend'))
    bend_side_deformer.rename(nomenclature.resolve('SideBend'))
    bend_upp_handle.rename(nomenclature.resolve('UppBendHandle'))
    bend_low_handle.rename(nomenclature.resolve('LowBendHandle'))
    bend_side_handle.rename(nomenclature.resolve('SideBendHandle'))

    # Try to guess the desired position
    min_x = None
    max_x = None
    pos = pymel.datatypes.Vector()
    for jnt in jnts:
        pos += jnt.getTranslation(space='world')
        if min_x is None or pos.x < min_x:
            min_x = pos.x
        if max_x is None or pos.x > max_x:
            max_x = pos.x
    pos /= len(jnts)
    root.setTranslation(pos)

    # Try to guess the scale
    length_x = max_x - min_x
    if len(jnts) <= 1 or length_x < epsilon:
        log.debug(
            "Cannot automatically resolve scale for surface. Using default value {0}".format(default_scale))
        length_x = default_scale

    root.scaleX.set(length_x)
    root.scaleY.set(length_x * 0.5)
    root.scaleZ.set(length_x)

    pymel.select(root)

    # self.input.append(plane_transform)

    return root, plane_transform


class AvarLogicSurface(avar_linear.AvarLogicLinear):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """
    name = 'Surface'
    SHOW_IN_UI = False

    _ATTR_NAME_U_BASE = 'baseU'
    _ATTR_NAME_V_BASE = 'baseV'
    _ATTR_NAME_U = 'surfaceU'
    _ATTR_NAME_V = 'surfaceV'
    _ATTR_NAME_MULT_LR = 'multiplierLr'
    _ATTR_NAME_MULT_UD = 'multiplierUd'
    _ATTR_NAME_MULT_FB = 'multiplierFb'

    def __init__(self, *args, **kwargs):
        super(AvarLogicSurface, self).__init__(*args, **kwargs)
        self.surface = None

        self._attr_u_base = None
        self._attr_v_base = None
        self.attr_multiplier_lr = None
        self.attr_multiplier_ud = None
        self.attr_multiplier_fb = None

        self._attr_length_v = None
        self._attr_length_u = None

        # Define how many unit is moved in uv space in relation with the avars.
        # Taking in consideration that the avar is centered in uv space, we at minimum want 0.5 of multiplier
        # so moving the avar of 1.0 will move the follicle at the top of uv space (0.5 units).
        # However in production, we found that defining the range of avar using the whole is not flexible.
        # ex: We want the lips to follow the chin but we don't want to have the lips reach the chin when the UD avar is -1.
        # For this reason, we found that using a multiplier of 0.25 work best.
        # This also help rigger visually since the surface plane have an edge at 0.25 location.
        # todo: Move this to AvarFollicle.
        self.multiplier_lr = 0.25
        self.multiplier_ud = 0.25
        self.multiplier_fb = 0.10

    def _hold_uv_multiplier(self):
        """
        Save the current uv multipliers.
        It is very rare that the rigger will tweak this advanced setting manually,
        however for legacy reasons, it might be useful when upgrading an old rig.
        """
        if self.attr_multiplier_lr and self.attr_multiplier_lr.exists():
            self.multiplier_lr = self.attr_multiplier_lr.get()
        if self.attr_multiplier_ud and self.attr_multiplier_ud.exists():
            self.multiplier_ud = self.attr_multiplier_ud.get()
        if self.attr_multiplier_fb and self.attr_multiplier_fb.exists():
            self.multiplier_fb = self.attr_multiplier_fb.get()

    def unbuild(self):
        self._hold_uv_multiplier()
        super(AvarLogicSurface, self).unbuild()

    def _get_follicle_relative_uv_attr(self, mult_u=1.0, mult_v=1.0):
        """
        Resolve the relative parameterU and parameterV that will be sent to the follicles.
        :return: A tuple containing two pymel.Attribute: the relative parameterU and relative parameterV.
        """
        # Apply custom multiplier
        attr_u = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=self.avar.attr_lr,
            input2X=self.attr_multiplier_lr
        ).outputX

        attr_v = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=self.avar.attr_ud,
            input2X=self.attr_multiplier_ud
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

        attr_u_relative, attr_v_relative = self._get_follicle_relative_uv_attr(mult_u=mult_u, mult_v=mult_v)

        # Add base parameterU & parameterV
        attr_u_cur = libRigging.create_utility_node(
            'addDoubleLinear',
            input1=self._attr_u_base,
            input2=attr_u_relative
        ).output

        attr_v_cur = libRigging.create_utility_node(
            'addDoubleLinear',
            input1=self._attr_v_base,
            input2=attr_v_relative
        ).output

        # TODO: Move attribute connection outside of this function.
        pymel.connectAttr(attr_u_cur, attr_u_inn)
        pymel.connectAttr(attr_v_cur, attr_v_inn)

        return attr_u_inn, attr_v_inn

    def handle_surface(self):
        """
        Create the surface that the follicle will slide on if necessary.
        :return:
        """
        # Hack: Provide backward compatibility for when surface was provided as an input.
        if not libPymel.isinstance_of_shape(self.surface, pymel.nodetypes.NurbsSurface):
            fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
            surface = next(iter(filter(fn_is_nurbsSurface, self.input)), None)
            if surface:
                self.input.remove(surface)
                self.surface = surface
                return True

            # Create surface if it doesn't exist.
            self.warning("Can't find surface for {0}, creating one...".format(self))
            self.surface = self.create_surface()

    def create_surface(self, name='Surface', epsilon=0.001, default_scale=1.0):
        """
        Create a simple rig to deform a nurbsSurface, allowing the rigger to easily provide
        a surface for the influence to slide on.
        :param name: The suffix of the surface name to create.
        :return: A pymel.nodetypes.Transform instance of the created surface.
        """
        nomenclature = self.get_nomenclature_rig().copy()
        nomenclature.add_tokens(name)

        root, plane_transform = create_surface(nomenclature, self.jnts, epsilon=epsilon, default_scale=default_scale)
        root.setParent(self.grp_rig)

        return plane_transform

    def build_stack(self, stack, mult_u=1.0, mult_v=1.0, parent_module=None):
        """
        The dag stack is a chain of transform nodes daisy chained together that computer the final transformation of the influence.
        The decision of using transforms instead of multMatrix nodes is for clarity.
        Note also that because of it's parent (the offset node) the stack relative to the influence original translation.
        """
        # TODO: Maybe use sub-classing to differenciate when we need to use a surface or not.
        nomenclature_rig = self.get_nomenclature_rig()

        #
        # Extract the base U and V of the base influence using the stack parent. (the 'offset' node)
        #
        self.handle_surface()
        surface_shape = self.surface.getShape()

        util_get_base_uv_absolute = libRigging.create_utility_node(
            'closestPointOnSurface',
            inPosition=self._grp_offset.t,
            inputSurface=surface_shape.worldSpace
        )

        util_get_base_uv_normalized = libRigging.create_utility_node(
            'setRange',
            oldMinX=surface_shape.minValueU,
            oldMaxX=surface_shape.maxValueU,
            oldMinY=surface_shape.minValueV,
            oldMaxY=surface_shape.maxValueV,
            minX=0,
            maxX=1,
            minY=0,
            maxY=1,
            valueX=util_get_base_uv_absolute.parameterU,
            valueY=util_get_base_uv_absolute.parameterV
        )
        attr_base_u_normalized = util_get_base_uv_normalized.outValueX
        attr_base_v_normalized = util_get_base_uv_normalized.outValueY

        self._attr_u_base = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U_BASE,
                                            defaultValue=attr_base_u_normalized.get())
        self._attr_v_base = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V_BASE,
                                            defaultValue=attr_base_v_normalized.get())

        pymel.connectAttr(attr_base_u_normalized, self.grp_rig.attr(self._ATTR_NAME_U_BASE))
        pymel.connectAttr(attr_base_v_normalized, self.grp_rig.attr(self._ATTR_NAME_V_BASE))

        #
        # Create follicle setup
        # The setup is composed of two follicles.
        # One for the "bind pose" and one "driven" by the avars..
        # The delta between the "bind pose" and the "driven" follicles is then applied to the influence.
        #

        # Determine the follicle U and V on the reference nurbsSurface.
        # jnt_pos = self.jnt.getTranslation(space='world')
        # fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_surface(self.surface, jnt_pos)
        base_u_val = self._attr_u_base.get()
        base_v_val = self._attr_v_base.get()

        # Resolve the length of each axis of the surface
        self._attr_length_u, self._attr_length_v, arcdimension_shape = libRigging.create_arclengthdimension_for_nurbsplane(
            self.surface)
        arcdimension_transform = arcdimension_shape.getParent()
        arcdimension_transform.rename(nomenclature_rig.resolve('arcdimension'))
        arcdimension_transform.setParent(self.grp_rig)

        #
        # Create two follicle.
        # - influenceFollicle: Affected by the ud and lr Avar
        # - bindPoseFollicle: A follicle that stay in place and keep track of the original position.
        # We'll then compute the delta of the position of the two follicles.
        # This allow us to move or resize the plane without affecting the built rig. (if the rig is in neutral pose)
        #
        offset_name = nomenclature_rig.resolve('bindPoseRef')
        obj_offset = pymel.createNode('transform', name=offset_name)
        obj_offset.setParent(self._grp_offset)

        fol_offset_name = nomenclature_rig.resolve('bindPoseFollicle')
        # fol_offset = libRigging.create_follicle(obj_offset, self.surface, name=fol_offset_name)
        fol_offset_shape = libRigging.create_follicle2(self.surface, u=base_u_val, v=base_v_val)
        fol_offset = fol_offset_shape.getParent()
        fol_offset.rename(fol_offset_name)
        pymel.parentConstraint(fol_offset, obj_offset, maintainOffset=False)
        fol_offset.setParent(self.grp_rig)

        # Create the influence follicle
        influence_name = nomenclature_rig.resolve('influenceRef')
        influence = pymel.createNode('transform', name=influence_name)
        influence.setParent(self._grp_offset)

        fol_influence_name = nomenclature_rig.resolve('influenceFollicle')
        fol_influence_shape = libRigging.create_follicle2(self.surface, u=base_u_val, v=base_v_val)
        fol_influence = fol_influence_shape.getParent()
        fol_influence.rename(fol_influence_name)
        pymel.parentConstraint(fol_influence, influence, maintainOffset=False)
        fol_influence.setParent(self.grp_rig)

        #
        # Extract the delta of the influence follicle and it's initial pose follicle
        #
        attr_localTM = libRigging.create_utility_node('multMatrix', matrixIn=[
            influence.worldMatrix,
            obj_offset.worldInverseMatrix
        ]).matrixSum

        # Since we are extracting the delta between the influence and the bindpose matrix, the rotation of the surface
        # is not taken in consideration wich make things less intuitive for the rigger.
        # So we'll add an adjustement matrix so the rotation of the surface is taken in consideration.
        util_decomposeTM_bindPose = libRigging.create_utility_node('decomposeMatrix',
                                                                   inputMatrix=obj_offset.worldMatrix
                                                                   )
        attr_translateTM = libRigging.create_utility_node('composeMatrix',
                                                          inputTranslate=util_decomposeTM_bindPose.outputTranslate
                                                          ).outputMatrix
        attr_translateTM_inv = libRigging.create_utility_node('inverseMatrix',
                                                              inputMatrix=attr_translateTM,
                                                              ).outputMatrix
        attr_rotateTM = libRigging.create_utility_node('multMatrix',
                                                       matrixIn=[obj_offset.worldMatrix, attr_translateTM_inv]
                                                       ).matrixSum
        attr_rotateTM_inv = libRigging.create_utility_node('inverseMatrix',
                                                           inputMatrix=attr_rotateTM
                                                           ).outputMatrix
        attr_finalTM = libRigging.create_utility_node('multMatrix',
                                                      matrixIn=[attr_rotateTM_inv,
                                                                attr_localTM,
                                                                attr_rotateTM]
                                                      ).matrixSum

        util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                          inputMatrix=attr_finalTM
                                                          )

        #
        # Resolve the parameterU and parameterV
        #
        self.attr_multiplier_lr = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_LR,
                                                  defaultValue=self.multiplier_lr)
        self.attr_multiplier_ud = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_UD,
                                                  defaultValue=self.multiplier_ud)
        self.attr_multiplier_fb = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_FB,
                                                  defaultValue=self.multiplier_fb)

        attr_u_inn, attr_v_inn = self._get_follicle_absolute_uv_attr()

        #
        # Create the 1st (follicleLayer) that will contain the extracted position from the ud and lr Avar.
        #
        layer_follicle = stack.append_layer('follicleLayer')
        pymel.connectAttr(util_decomposeTM.outputTranslate, layer_follicle.translate)

        pymel.connectAttr(attr_u_inn, fol_influence.parameterU)
        pymel.connectAttr(attr_v_inn, fol_influence.parameterV)
        pymel.connectAttr(self._attr_u_base, fol_offset.parameterU)
        pymel.connectAttr(self._attr_v_base, fol_offset.parameterV)

        #
        # The second layer (oobLayer for out-of-bound) that allow the follicle to go outside it's original plane.
        # If the UD value is out the nurbsPlane UV range (0-1), ie 1.1, we'll want to still offset the follicle.
        # For that we'll compute a delta between a small increment (0.99 and 1.0) and multiply it.
        #
        nomenclature_rig = self.get_nomenclature_rig()
        oob_step_size = 0.001  # TODO: Expose a Maya attribute?

        fol_clamped_v_name = nomenclature_rig.resolve('influenceClampedV')
        fol_clamped_v_shape = libRigging.create_follicle2(self.surface, u=base_u_val, v=base_v_val)
        fol_clamped_v = fol_clamped_v_shape.getParent()
        fol_clamped_v.rename(fol_clamped_v_name)
        fol_clamped_v.setParent(self.grp_rig)

        fol_clamped_u_name = nomenclature_rig.resolve('influenceClampedU')
        fol_clamped_u_shape = libRigging.create_follicle2(self.surface, u=base_u_val, v=base_v_val)
        fol_clamped_u = fol_clamped_u_shape.getParent()
        fol_clamped_u.rename(fol_clamped_u_name)
        fol_clamped_u.setParent(self.grp_rig)

        # Clamp the values so they never fully reach 0 or 1 for U and V.
        util_clamp_uv = libRigging.create_utility_node('clamp',
                                                       inputR=attr_u_inn,
                                                       inputG=attr_v_inn,
                                                       minR=oob_step_size,
                                                       minG=oob_step_size,
                                                       maxR=1.0 - oob_step_size,
                                                       maxG=1.0 - oob_step_size)
        clamped_u = util_clamp_uv.outputR
        clamped_v = util_clamp_uv.outputG

        pymel.connectAttr(clamped_v, fol_clamped_v.parameterV)
        pymel.connectAttr(attr_u_inn, fol_clamped_v.parameterU)

        pymel.connectAttr(attr_v_inn, fol_clamped_u.parameterV)
        pymel.connectAttr(clamped_u, fol_clamped_u.parameterU)

        # Compute the direction to add for U and V if we are out-of-bound.
        dir_oob_u = libRigging.create_utility_node('plusMinusAverage',
                                                   operation=2,
                                                   input3D=[
                                                       fol_influence.translate,
                                                       fol_clamped_u.translate
                                                   ]).output3D
        dir_oob_v = libRigging.create_utility_node('plusMinusAverage',
                                                   operation=2,
                                                   input3D=[
                                                       fol_influence.translate,
                                                       fol_clamped_v.translate
                                                   ]).output3D

        # Compute the offset to add for U and V

        condition_oob_u_neg = libRigging.create_utility_node('condition',
                                                             operation=4,  # less than
                                                             firstTerm=attr_u_inn,
                                                             secondTerm=0.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_u_pos = libRigging.create_utility_node('condition',  # greater than
                                                             operation=2,
                                                             firstTerm=attr_u_inn,
                                                             secondTerm=1.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_v_neg = libRigging.create_utility_node('condition',
                                                             operation=4,  # less than
                                                             firstTerm=attr_v_inn,
                                                             secondTerm=0.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_v_pos = libRigging.create_utility_node('condition',  # greater than
                                                             operation=2,
                                                             firstTerm=attr_v_inn,
                                                             secondTerm=1.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR

        # Compute the amount of oob
        oob_val_u_pos = libRigging.create_utility_node('plusMinusAverage', operation=2,
                                                       input1D=[attr_u_inn, 1.0]).output1D
        oob_val_u_neg = libRigging.create_utility_node('multiplyDivide', input1X=attr_u_inn, input2X=-1.0).outputX
        oob_val_v_pos = libRigging.create_utility_node('plusMinusAverage', operation=2,
                                                       input1D=[attr_v_inn, 1.0]).output1D
        oob_val_v_neg = libRigging.create_utility_node('multiplyDivide', input1X=attr_v_inn, input2X=-1.0).outputX
        oob_val_u = libRigging.create_utility_node('condition', operation=0, firstTerm=condition_oob_u_pos,
                                                   secondTerm=1.0, colorIfTrueR=oob_val_u_pos,
                                                   colorIfFalseR=oob_val_u_neg).outColorR
        oob_val_v = libRigging.create_utility_node('condition', operation=0, firstTerm=condition_oob_v_pos,
                                                   secondTerm=1.0, colorIfTrueR=oob_val_v_pos,
                                                   colorIfFalseR=oob_val_v_neg).outColorR

        oob_amount_u = libRigging.create_utility_node('multiplyDivide', operation=2, input1X=oob_val_u,
                                                      input2X=oob_step_size).outputX
        oob_amount_v = libRigging.create_utility_node('multiplyDivide', operation=2, input1X=oob_val_v,
                                                      input2X=oob_step_size).outputX

        oob_offset_u = libRigging.create_utility_node('multiplyDivide', input1X=oob_amount_u, input1Y=oob_amount_u,
                                                      input1Z=oob_amount_u, input2=dir_oob_u).output
        oob_offset_v = libRigging.create_utility_node('multiplyDivide', input1X=oob_amount_v, input1Y=oob_amount_v,
                                                      input1Z=oob_amount_v, input2=dir_oob_v).output

        # Add the U out-of-bound-offset only if the U is between 0.0 and 1.0
        oob_u_condition_1 = condition_oob_u_neg
        oob_u_condition_2 = condition_oob_u_pos
        oob_u_condition_added = libRigging.create_utility_node('addDoubleLinear',
                                                               input1=oob_u_condition_1,
                                                               input2=oob_u_condition_2
                                                               ).output
        oob_u_condition_out = libRigging.create_utility_node('condition',
                                                             operation=0,  # equal
                                                             firstTerm=oob_u_condition_added,
                                                             secondTerm=1.0,
                                                             colorIfTrue=oob_offset_u,
                                                             colorIfFalse=[0, 0, 0]
                                                             ).outColor

        # Add the V out-of-bound-offset only if the V is between 0.0 and 1.0
        oob_v_condition_1 = condition_oob_v_neg
        oob_v_condition_2 = condition_oob_v_pos
        oob_v_condition_added = libRigging.create_utility_node('addDoubleLinear',
                                                               input1=oob_v_condition_1,
                                                               input2=oob_v_condition_2
                                                               ).output
        oob_v_condition_out = libRigging.create_utility_node('condition',
                                                             operation=0,  # equal
                                                             firstTerm=oob_v_condition_added,
                                                             secondTerm=1.0,
                                                             colorIfTrue=oob_offset_v,
                                                             colorIfFalse=[0, 0, 0]
                                                             ).outColor

        oob_offset = libRigging.create_utility_node('plusMinusAverage',
                                                    input3D=[oob_u_condition_out, oob_v_condition_out]).output3D

        layer_oob = stack.append_layer('oobLayer')
        pymel.connectAttr(oob_offset, layer_oob.t)

        #
        # Create the third layer that apply the translation provided by the fb Avar.
        #

        layer_fb = stack.append_layer('fbLayer')
        attr_get_fb = libRigging.create_utility_node('multiplyDivide',
                                                     input1X=self.avar.attr_fb,
                                                     input2X=self._attr_length_u).outputX
        attr_get_fb_adjusted = libRigging.create_utility_node('multiplyDivide',
                                                              input1X=attr_get_fb,
                                                              input2X=self.attr_multiplier_fb).outputX
        pymel.connectAttr(attr_get_fb_adjusted, layer_fb.translateZ)

        #
        # Create the 4th layer (folRot) that apply the rotation provided by the follicle controlled by the ud and lr Avar.
        # This is necessary since we don't want to rotation to affect the oobLayer and fbLayer.
        #
        layer_follicle_rot = stack.append_layer('folRot')
        pymel.connectAttr(util_decomposeTM.outputRotate, layer_follicle_rot.rotate)

        #
        # Create a 5th layer that apply the avar rotation and scale..
        #
        layer_rot = stack.append_layer('rotLayer')
        pymel.connectAttr(self.avar.attr_yw, layer_rot.rotateY)
        pymel.connectAttr(self.avar.attr_pt, layer_rot.rotateX)
        pymel.connectAttr(self.avar.attr_rl, layer_rot.rotateZ)
        pymel.connectAttr(self.avar.attr_sx, layer_rot.scaleX)
        pymel.connectAttr(self.avar.attr_sy, layer_rot.scaleY)
        pymel.connectAttr(self.avar.attr_sz, layer_rot.scaleZ)

        return stack


def register_plugin():
    return AvarLogicSurface
