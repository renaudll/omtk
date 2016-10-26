import math

import pymel.core as pymel

from omtk.libs import libRigging
from omtk.libs import libPython
from omtk.libs import libAttr
from omtk.libs import libFormula
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.core.classNode import Node

class CtrlLipsUpp(rigFaceAvarGrps.CtrlFaceUpp):
    pass


class CtrlLipsLow(rigFaceAvarGrps.CtrlFaceLow):
    pass


class SplitterNode(Node):
    """
    A splitter is a node network that take take the parameterV that is normally sent through the follicles and
    split it between two destination: the follicles and the jaw ref constraint.
    The more the jaw is opened, the more we'll transfer to the jaw ref before sending to the follicle.
    This is mainly used to ensure that any lip movement created by the jaw is canceled when the
    animator try to correct the lips and the jaw is open. Otherwise since the jaw space and the surface space

    To compute the displacement caused by the was, we'll usethe circumference around the jaw pivot.
    This create an 'approximation' that might be wrong if some translation also occur in the jaw.
    todo: test with corrective jaw translation
    """
    def __init__(self):
        super(SplitterNode, self).__init__()  # useless
        self.attr_inn_jaw_pt = None
        self.attr_inn_jaw_radius = None
        self.attr_inn_surface_v = None
        self.attr_inn_surface_range_v = None
        self.attr_inn_jaw_default_ratio = None
        self.attr_out_surface_v = None
        self.attr_out_jaw_ratio = None

    def build(self, nomenclature_rig, **kwargs):
        super(SplitterNode, self).build(**kwargs)

        #
        # Create inn and out attributes.
        #
        grp_splitter_inn = pymel.createNode(
            'network',
            name=nomenclature_rig.resolve('udSplitterInn')
        )

        # The jaw opening amount in degree.
        self.attr_inn_jaw_pt = libAttr.addAttr(grp_splitter_inn, 'innJawOpen')

        # The relative uv coordinates normally sent to the follicles.
        # Note that this value is expected to change at the output of the SplitterNode (see outSurfaceU and outSurfaceV)
        self.attr_inn_surface_u = libAttr.addAttr(grp_splitter_inn, 'innSurfaceU')
        self.attr_inn_surface_v = libAttr.addAttr(grp_splitter_inn, 'innSurfaceV')

        # Use this switch to disable completely the splitter.
        self.attr_inn_bypass = libAttr.addAttr(grp_splitter_inn, 'innBypassAmount')

        # The arc length in world space of the surface controlling the follicles.
        self.attr_inn_surface_range_v = libAttr.addAttr(grp_splitter_inn, 'innSurfaceRangeV')  # How many degree does take the jaw to create 1 unit of surface deformation? (ex: 20)

        # How much inn percent is the lips following the jaw by default.
        # Note that this value is expected to change at the output of the SplitterNode (see attr_out_jaw_ratio)
        self.attr_inn_jaw_default_ratio = libAttr.addAttr(grp_splitter_inn, 'jawDefaultRatio')

        # The radius of the influence circle normally resolved by using the distance between the jaw and the avar as radius.
        self.attr_inn_jaw_radius = libAttr.addAttr(grp_splitter_inn, 'jawRadius')

        grp_splitter_out = pymel.createNode(
            'network',
            name=nomenclature_rig.resolve('udSplitterOut')
        )

        self.attr_out_surface_u = libAttr.addAttr(grp_splitter_out, 'outSurfaceU')
        self.attr_out_surface_v = libAttr.addAttr(grp_splitter_out, 'outSurfaceV')
        self.attr_out_jaw_ratio = libAttr.addAttr(grp_splitter_out, 'outJawRatio')  # How much percent this influence follow the jaw after cancellation.

        #
        # Connect inn and out network nodes so they can easily be found from the SplitterNode.
        #
        attr_inn = libAttr.addAttr(grp_splitter_inn, longName='inn', attributeType='message')
        attr_out = libAttr.addAttr(grp_splitter_out, longName='out', attributeType='message')
        pymel.connectAttr(self.node.message, attr_inn)
        pymel.connectAttr(self.node.message, attr_out)

        #
        # Create node networks
        # Step 1: Get the jaw displacement in uv space (parameterV only).
        #

        attr_jaw_circumference = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getJawCircumference'),
            input1X=self.attr_inn_jaw_radius,
            input2X=(math.pi * 2.0)
        ).outputX

        attr_jaw_open_circle_ratio = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getJawOpenCircleRatio'),
            operation=2,  # divide
            input1X=self.attr_inn_jaw_pt,
            input2X=360.0
        ).outputX

        attr_jaw_active_circumference = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getJawActiveCircumference'),
            input1X=attr_jaw_circumference,
            input2X=attr_jaw_open_circle_ratio
        ).outputX

        # We need this adjustment since we cheat the influence of the avar with the plane uvs.
        # see AvarFollicle._get_follicle_relative_uv_attr for more information.
        # attr_jaw_radius_demi = libRigging.create_utility_node(
        #     'multiplyDivide',
        #     name=nomenclature_rig.resolve('getJawRangeVRange'),
        #     input1X=self.attr_inn_surface_range_v,
        #     input2X=2.0
        # ).outputX

        attr_jaw_v_range = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getActiveJawRangeInSurfaceSpace'),
            operation=2,  # divide
            input1X=attr_jaw_active_circumference,
            input2X=self.attr_inn_surface_range_v
        ).outputX

        #
        # Step 2: Resolve attr_out_jaw_ratio
        #

        # Convert attr_jaw_default_ratio in uv space.
        attr_jaw_default_ratio_v = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getJawDefaultRatioUvSpace'),
            input1X=self.attr_inn_jaw_default_ratio,
            input2X=attr_jaw_v_range
        ).outputX

        attr_jaw_uv_pos = libRigging.create_utility_node(
            'plusMinusAverage',
            name=nomenclature_rig.resolve('getCurrentJawUvPos'),
            operation=2,  # substraction
            input1D=(attr_jaw_default_ratio_v, self.attr_inn_surface_v)
        ).output1D

        attr_jaw_ratio_out = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getJawRatioOut'),
            operation=2,  # division
            input1X=attr_jaw_uv_pos,
            input2X=attr_jaw_v_range
        ).outputX

        attr_jaw_ratio_out_limited = libRigging.create_utility_node(
            'clamp',
            name=nomenclature_rig.resolve('getLimitedJawRatioOut'),
            inputR=attr_jaw_ratio_out,
            minR=0.0,
            maxR=1.0
        ).outputR

        # Prevent division by zero
        attr_jaw_ratio_out_limited_safe = libRigging.create_utility_node(
            'condition',
            name=nomenclature_rig.resolve('getSafeJawRatioOut'),
            operation=1,  # not equal
            firstTerm=self.attr_inn_jaw_pt,
            secondTerm=0,
            colorIfTrueR=attr_jaw_ratio_out_limited,
            colorIfFalseR=self.attr_inn_jaw_default_ratio
        ).outColorR

        #
        # Step 3: Resolve attr_out_surface_u & attr_out_surface_v
        #

        attr_inn_jaw_default_ratio_inv = libRigging.create_utility_node(
            'reverse',
            name=nomenclature_rig.resolve('getJawDefaultRatioInv'),
            inputX=self.attr_inn_jaw_default_ratio
        ).outputX

        util_jaw_uv_default_ratio = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getJawDefaultRatioUvSpace'),
            input1X=self.attr_inn_jaw_default_ratio,
            input1Y=attr_inn_jaw_default_ratio_inv,
            input2X=attr_jaw_v_range,
            input2Y=attr_jaw_v_range
        )
        attr_jaw_uv_default_ratio = util_jaw_uv_default_ratio.outputX
        attr_jaw_uv_default_ratio_inv = util_jaw_uv_default_ratio.outputY

        attr_jaw_uv_limit_max = libRigging.create_utility_node(
            'plusMinusAverage',
            name=nomenclature_rig.resolve('getJawSurfaceLimitMax'),
            operation=2,  # substract
            input1D=(attr_jaw_v_range, attr_jaw_uv_default_ratio_inv)
        ).output1D

        attr_jaw_uv_limit_min = libRigging.create_utility_node(
            'plusMinusAverage',
            name=nomenclature_rig.resolve('getJawSurfaceLimitMin'),
            operation=2,  # substract
            input1D=(attr_jaw_uv_default_ratio, attr_jaw_v_range)
        ).output1D

        attr_jaw_cancel_range = libRigging.create_utility_node(
            'clamp',
            name=nomenclature_rig.resolve('getJawCancelRange'),
            inputR=self.attr_inn_surface_v,
            minR=attr_jaw_uv_limit_min,
            maxR=attr_jaw_uv_limit_max
        ).outputR

        attr_out_surface_v_cancelled = libRigging.create_utility_node(
            'plusMinusAverage',
            name=nomenclature_rig.resolve('getCanceledUv'),
            operation=2,  # substraction
            input1D=(self.attr_inn_surface_v, attr_jaw_cancel_range)
        ).output1D

        #
        # Connect output attributes
        #
        attr_inn_bypass_inv = libRigging.create_utility_node(
            'reverse',
            name=nomenclature_rig.resolve('getBypassInv'),
            inputX=self.attr_inn_bypass
        ).outputX

        # Connect output jaw_ratio
        attr_output_jaw_ratio = libRigging.create_utility_node(
            'blendWeighted',
            input=(attr_jaw_ratio_out_limited_safe, self.attr_inn_jaw_default_ratio),
            weight=(attr_inn_bypass_inv, self.attr_inn_bypass)
        ).output
        pymel.connectAttr(attr_output_jaw_ratio, self.attr_out_jaw_ratio)

        # Connect output surface u
        pymel.connectAttr(self.attr_inn_surface_u, self.attr_out_surface_u)

        # Connect output surface_v
        attr_output_surface_v = libRigging.create_utility_node(
            'blendWeighted',
            input=(attr_out_surface_v_cancelled, self.attr_inn_surface_v),
            weight=(attr_inn_bypass_inv, self.attr_inn_bypass)
        ).output
        pymel.connectAttr(attr_output_surface_v, self.attr_out_surface_v)


class FaceLipsAvar(rigFaceAvar.AvarFollicle):
    def __init__(self, *args, **kwargs):
        super(FaceLipsAvar, self).__init__(*args, **kwargs)

        # Define how many percent is the avar following the jaw. (ex: 0.5)
        self._attr_inn_jaw_ratio_default = None

        # Define how many degree create the same deformation as the full surface V.

        # Define the length
        
        # Define the length of worldspace length of the surface v arc.
        self._attr_surface_length_v = None

        self._attr_inn_jaw_pt = None

        # Allow the rigger to completely bypass the splitter node influence.
        self._attr_bypass_splitter = None

        self._jaw_ref = None

    def build_stack(self, stack, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()
        jnt_head = self.rig.get_head_jnt()
        jnt_jaw = self.rig.get_jaw_jnt()

        #
        # Create additional attributes to control the jaw layer
        #

        libAttr.addAttr_separator(self.grp_rig, 'jawLayer')
        self._attr_inn_jaw_ratio_default = libAttr.addAttr(
            self.grp_rig,
            'jawRatioDefault',
            defaultValue=0.5,
            hasMinValue=True,
            hasMaxValue=True,
            minValue=0,
            maxValue=1,
            k=True
        )
        self._attr_bypass_splitter = libAttr.addAttr(
            self.grp_rig,
            'jawSplitterBypass',
            defaultValue=0.0,
            hasMinValue=True,
            hasMaxValue=True,
            minValue=0,
            maxValue=1,
            k=True
        )

        #
        # Create reference objects used for calculations.
        #

        # Create a reference node that follow the head
        self._target_head = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('innHead'),
            parent=self.grp_rig
        )
        self._target_head.setTranslation(jnt_head.getTranslation(space='world'))
        pymel.parentConstraint(jnt_head, self._target_head, maintainOffset=True)
        pymel.scaleConstraint(jnt_head, self._target_head, maintainOffset=True)

        # Create a reference node that follow the jaw initial position
        jaw_pos = jnt_jaw.getTranslation(space='world')
        self._target_jaw_bindpose = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('innJawBindPose'),
            parent=self.grp_rig
        )
        self._target_jaw_bindpose.setTranslation(jaw_pos)

        # Create a reference node that follow the jaw
        self._target_jaw = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('innJaw'),
            parent=self._target_jaw_bindpose
        )
        self._target_jaw.t.set(0,0,0)
        pymel.parentConstraint(jnt_jaw, self._target_jaw, maintainOffset=True)
        pymel.scaleConstraint(jnt_jaw, self._target_jaw, maintainOffset=True)

        # Create a node that contain the out jaw influence.
        # Note that the out jaw influence can be modified by the splitter node.
        grp_parent_pos = self._grp_parent.getTranslation(space='world')  # grp_offset is always in world coordinates
        self._jaw_ref = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('outJawInfluence'),
            parent=self.grp_rig
        )
        self._jaw_ref.t.set(grp_parent_pos)
        pymel.parentConstraint(self._target_jaw, self._jaw_ref, maintainOffset=True)

        # Extract jaw influence
        attr_delta_tm = libRigging.create_utility_node('multMatrix', matrixIn=[
            self._jaw_ref.worldMatrix,
            self._grp_parent.worldInverseMatrix
        ]).matrixSum

        util_extract_jaw = libRigging.create_utility_node(
            'decomposeMatrix',
            name=nomenclature_rig.resolve('getJawRotation'),
            inputMatrix=attr_delta_tm
        )

        super(FaceLipsAvar, self).build_stack(stack, **kwargs)

        #
        # Create jaw influence layer
        # Create a reference object to extract the jaw displacement.
        #

        # Add the jaw influence as a new stack layer.
        layer_jaw_r = stack.prepend_layer(name='jawRotate')
        layer_jaw_t = stack.prepend_layer(name='jawTranslate')

        pymel.connectAttr(util_extract_jaw.outputTranslate, layer_jaw_t.t)
        pymel.connectAttr(util_extract_jaw.outputRotate, layer_jaw_r.r)

    def _get_follicle_relative_uv_attr(self, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

        attr_u, attr_v = super(FaceLipsAvar, self)._get_follicle_relative_uv_attr(**kwargs)

        #
        # Create and connect Splitter Node
        #
        splitter = SplitterNode()
        splitter.build(
            nomenclature_rig,
            name=nomenclature_rig.resolve('splitter')
        )
        splitter.setParent(self.grp_rig)

        # Resolve the radius of the jaw influence. Used by the splitter.
        attr_jaw_radius = libRigging.create_utility_node(
            'distanceBetween',
            name=nomenclature_rig.resolve('getJawRadius'),
            point1=self._grp_offset.translate,
            point2=self._target_jaw_bindpose.translate
        ).distance

        # Resolve the jaw pitch. Used by the splitter.
        attr_jaw_pitch = libRigging.create_utility_node(
            'decomposeMatrix',
            name=nomenclature_rig.resolve('getJawPitch'),
            inputMatrix=libRigging.create_utility_node(
                'multMatrix',
                name=nomenclature_rig.resolve('extractJawPitch'),
                matrixIn=(
                    self._target_jaw.worldMatrix,
                    self._grp_parent.worldInverseMatrix
                )
            ).matrixSum
        ).outputRotateX

        # Connect the splitter inputs
        pymel.connectAttr(attr_u, splitter.attr_inn_surface_u)
        pymel.connectAttr(attr_v, splitter.attr_inn_surface_v)
        pymel.connectAttr(self._attr_inn_jaw_ratio_default, splitter.attr_inn_jaw_default_ratio)
        pymel.connectAttr(self._attr_length_v, splitter.attr_inn_surface_range_v)
        pymel.connectAttr(attr_jaw_radius, splitter.attr_inn_jaw_radius)
        pymel.connectAttr(attr_jaw_pitch, splitter.attr_inn_jaw_pt)
        pymel.connectAttr(self._attr_bypass_splitter, splitter.attr_inn_bypass)

        attr_u = splitter.attr_out_surface_u
        attr_v = splitter.attr_out_surface_v

        # Create constraint to controller the jaw reference
        attr_jaw_ratio = splitter.attr_out_jaw_ratio
        attr_jaw_ratio_inv = libRigging.create_utility_node('reverse', inputX=attr_jaw_ratio).outputX

        constraint_pr = pymel.parentConstraint(self._target_head, self._target_jaw, self._jaw_ref, maintainOffset=True)
        constraint_s = pymel.scaleConstraint(self._target_head, self._target_jaw, self._jaw_ref)
        weight_pr_head, weight_pr_jaw = constraint_pr.getWeightAliasList()
        weight_s_head, weight_s_jaw = constraint_s.getWeightAliasList()

        # Connect splitter outputs
        pymel.connectAttr(attr_jaw_ratio_inv, weight_pr_jaw)
        pymel.connectAttr(attr_jaw_ratio_inv, weight_s_jaw)
        pymel.connectAttr(attr_jaw_ratio, weight_pr_head)
        pymel.connectAttr(attr_jaw_ratio, weight_s_head)

        return attr_u, attr_v


class FaceLips(rigFaceAvarGrps.AvarGrpAreaOnSurface):
    """
    AvarGrp setup customized for lips rigging.
    Lips have the same behavior than an AvarGrpUppLow.
    However the lip curl is also connected between the macro avars and the micro avars.
    """
    _CLS_AVAR = FaceLipsAvar
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True
    _CLS_CTRL_UPP = CtrlLipsUpp
    _CLS_CTRL_LOW = CtrlLipsLow

    def validate(self):
        """
        If we are using the preDeform flag, we will need to validate that we can find the Jaw influence!
        """
        super(FaceLips, self).validate()

        if not self.preDeform:
            if self.rig.get_jaw_jnt(strict=False) is None:
                raise Exception("Can't resolve jaw. Please create a Jaw module.")

    def get_avars_corners(self):
        # todo: move upper?
        fnFilter = lambda avar: 'corner' in avar.name.lower()
        result = filter(fnFilter, self.avars)

        if self.avar_l:
            result.append(self.avar_l)
        if self.avar_r:
            result.append(self.avar_r)

        return result

    def get_module_name(self):
        return 'Lip'

    def connect_macro_avar(self, avar_macro, avar_micros):
        for avar_micro in avar_micros:
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_ud, avar_micro.attr_ud)
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_lr, avar_micro.attr_lr)
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_fb, avar_micro.attr_fb)
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_pt)

            # Add default FB avars to 'fake' a better lip curl pivot.
            # see: Art of Moving Points page 146
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_ud, kv=[0.01, 0.0, -0.01])
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_fb, kv=[0.01, 0.0, -0.01])

    def _build_avar_macro_horizontal(self, avar_parent, avar_middle, avar_children, cls_ctrl, connect_ud=False, connect_lr=True, connect_fb=False):
        self._build_avar_macro(cls_ctrl, avar_parent)

        pos_s = avar_middle.jnt.getTranslation(space='world')
        pos_e = avar_parent.jnt.getTranslation(space='world')

        for avar_child in avar_children:
            # We don't want to connect the middle Avar.
            if avar_child == avar_middle:
                continue

            pos = avar_child.jnt.getTranslation(space='world')

            # Compute the ratio between the middle and the corner.
            # ex: In the lips, we want the lips to stretch when the corner are taken appart.
            ratio = (pos.x - pos_s.x) / (pos_e.x - pos_s.x)
            ratio = max(0, ratio)
            ratio = min(ratio, 1)

            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_ud, avar_child.attr_ud)
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_lr, avar_child.attr_lr,  kv=(-ratio,0.0,ratio))
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_fb, avar_child.attr_fb)

    def _build_avar_macro_l(self):
        # Create left avar if necessary
        ref = self.get_jnt_l_mid()
        if self.create_macro_horizontal and ref:
            if not self.avar_l:
                self.avar_l = self.create_avar_macro_left(self._CLS_CTRL_LFT, ref)
            self._build_avar_macro_horizontal(self.avar_l, self.get_avar_mid(), self.get_avars_l(), self._CLS_CTRL_LFT, connect_lr=True, connect_ud=False, connect_fb=False)

            # Connect the corner other avars
            avar_l_corner = self.get_avar_l_corner()
            if avar_l_corner:
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_ud, avar_l_corner.attr_ud)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_fb, avar_l_corner.attr_fb)

    def _build_avar_macro_r(self):# Create right avar if necessary
        ref = self.get_jnt_r_mid()
        if self.create_macro_horizontal and ref:
            # Create l ctrl
            if not self.avar_r:
                self.avar_r = self.create_avar_macro_right(self._CLS_CTRL_RGT, ref)
            self._build_avar_macro_horizontal(self.avar_r, self.get_avar_mid(), self.get_avars_r(), self._CLS_CTRL_RGT, connect_lr=True, connect_ud=False, connect_fb=False)

            avar_r_corner = self.get_avar_r_corner()
            if avar_r_corner:
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_ud, avar_r_corner.attr_ud)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_fb, avar_r_corner.attr_fb)

    @libPython.memoized
    def _get_mouth_width(self):
        min_x = max_x = 0
        for avar in self.get_avars_corners():
            x = avar._grp_offset.tx.get()
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        return min_x, max_x

    def build(self, calibrate=True, use_football_interpolation=False, **kwargs):
        """
        :param calibrate:
        :param use_football_interpolation: If True, the resolved influence of the jaw on
        each lips avar will give a 'football' shape. It is False by default since we take
        in consideration that the weightmaps follow the 'Art of Moving Points' theory and
        already result in a football shape if they are uniformly translated.
        :param kwargs:
        :return:
        """
        super(FaceLips, self).build(calibrate=False, **kwargs)

        if not self.preDeform:
            # Resolve the head influence
            jnt_head = self.rig.get_head_jnt()
            if not jnt_head:
                self.error("Failed parenting avars, no head influence found!")
                return

            jnt_jaw = self.rig.get_jaw_jnt()
            if not jnt_jaw:
                self.error("Failed parenting avars, no jaw influence found!")
                return

            nomenclature_rig = self.get_nomenclature_rig()

            # Note #2: A common target for the head
            target_head_name = nomenclature_rig.resolve('targetHead')
            target_head = pymel.createNode('transform', name=target_head_name)
            target_head.setTranslation(jnt_head.getTranslation(space='world'))
            target_head.setParent(self.grp_rig)
            pymel.parentConstraint(jnt_head, target_head, maintainOffset=True)
            pymel.scaleConstraint(jnt_head, target_head, maintainOffset=True)

            # Note #3: A common target for the jaw
            target_jaw_name = nomenclature_rig.resolve('targetJaw')
            target_jaw = pymel.createNode('transform', name=target_jaw_name)
            target_jaw.setTranslation(jnt_jaw.getTranslation(space='world'))
            target_jaw.setParent(self.grp_rig)
            pymel.parentConstraint(jnt_jaw, target_jaw, maintainOffset=True)
            pymel.scaleConstraint(jnt_jaw, target_jaw, maintainOffset=True)

            attr_bypass = libAttr.addAttr(self.grp_rig, 'bypassSplitter')


            # For each avars, create an extractor node and extract the delta from the bind pose.
            # We'll then feed this into the stack layers.
            # This will apply jaw deformation to the rig.

            # Moving the lips when they are influenced by the jaw is a hard task.
            # This is because the jaw introduce movement in 'jaw' space while the
            # standard avars introduce movement in 'surface' space.
            # This mean that if we try to affect a deformation occuring in 'jaw' space
            # with the 'surface' space (ex: moving the lips corners up when the jaw is open)
            # this will not result in perfect results.

            # To prevent this situation, taking in consideration that there's a one on one correlation
            # between the lips and jaw deformation (ex: the football shape created by the jaw at 1.0
            # is the same as if upp and low lips are set at 0.5 each), we'll always use the jaw space
            # before using the lips space.


            min_x, max_x = self._get_mouth_width()
            mouth_width = max_x - min_x

            def connect_avar(avar, ratio):
                avar._attr_inn_jaw_ratio_default.set(ratio)
                #pymel.connectAttr(self._attr_inn_jaw_range, avar._attr_inn_jaw_range)
                #pymel.connectAttr(self._attr_length_v, avar._attr_inn_jaw_range)

            for avar in self.get_avars_corners():
                connect_avar(avar, 0.5)

            for avar in self.get_avars_upp():
                if use_football_interpolation:
                    avar_pos_x = avar._grp_offset.tx.get()
                    ratio = abs(avar_pos_x - min_x / mouth_width)
                    ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
                    ratio = libRigging.interp_football(ratio)  # apply football shape
                else:
                    ratio = 0.0

                connect_avar(avar, ratio)

            for avar in self.get_avars_low():
                if use_football_interpolation:
                    avar_pos_x = avar._grp_offset.tx.get()
                    ratio = abs(avar_pos_x - min_x / mouth_width)
                    ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
                    ratio = 1.0 - libRigging.interp_football(ratio)  # apply football shape
                else:
                    ratio = 1.0

                connect_avar(avar, ratio)

        # Calibration is done manually since we need to setup the jaw influence.
        if calibrate:
            self.calibrate()


def register_plugin():
    return FaceLips