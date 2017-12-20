import math

import pymel.core as pymel
from omtk.core.node import Node
from omtk.libs import libAttr
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar, rigFaceAvarGrps


class CtrlLipsUpp(rigFaceAvarGrps.CtrlFaceUpp):
    pass


class CtrlLipsLow(rigFaceAvarGrps.CtrlFaceLow):
    pass


class SplitterNode(Node):
    """
    A splitter is a node network that take the parameterV that is normally sent through the follicles and
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
        self.attr_inn_surface_range_v = libAttr.addAttr(grp_splitter_inn,
                                                        'innSurfaceRangeV')  # How many degree does take the jaw to create 1 unit of surface deformation? (ex: 20)

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
        self.attr_out_jaw_ratio = libAttr.addAttr(grp_splitter_out,
                                                  'outJawRatio')  # How much percent this influence follow the jaw after cancellation.

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

        attr_jaw_v_range = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getActiveJawRangeInSurfaceSpace'),
            operation=2,  # divide
            input1X=attr_jaw_active_circumference,
            input2X=self.attr_inn_surface_range_v
        ).outputX

        #
        # Step 2: Resolve the output jaw_ratio
        #

        # Note that this can throw a zero division warning in Maya.
        # To prevent that we'll use some black-magic-ugly-ass-trick.
        attr_jaw_ratio_cancelation = libRigging.create_safe_division(
            self.attr_inn_surface_v,
            attr_jaw_v_range,
            nomenclature_rig,
            'getJawRatioCancellation'
        )

        attr_jaw_ratio_out_raw = libRigging.create_utility_node(
            'plusMinusAverage',
            name=nomenclature_rig.resolve('getJawRatioOutUnlimited'),
            operation=2,  # substraction,
            input1D=(
                self.attr_inn_jaw_default_ratio,
                attr_jaw_ratio_cancelation
            )
        ).output1D

        attr_jaw_ratio_out_limited = libRigging.create_utility_node(
            'clamp',
            name=nomenclature_rig.resolve('getJawRatioOutLimited'),
            inputR=attr_jaw_ratio_out_raw,
            minR=0.0,
            maxR=1.0
        ).outputR

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
            input=(attr_jaw_ratio_out_limited, self.attr_inn_jaw_default_ratio),
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


class FaceLipsAvar(rigFaceAvar.Avar):
    """
    The Lips avar are special as they implement a Splitter mechanism that ensure the avars move in jaw space before moving in surface space.
    For this reason, we implement a new avar, 'avar_ud_bypass' to skip the splitter mechanism if necessary. (ex: avar_all)
    """
    AVAR_NAME_UD_BYPASS = 'attr_ud_bypass'

    def __init__(self, *args, **kwargs):
        super(FaceLipsAvar, self).__init__(*args, **kwargs)

        # Define how many percent is the avar following the jaw. (ex: 0.5)
        self._attr_inn_jaw_ratio_default = None

        # Define how many degree create the same deformation as the full surface V.

        # Define the length

        # Define the length of worldspace length of the surface v arc.
        self._attr_surface_length_v = None

        self._attr_inn_jaw_pt = None

        # self._jaw_ref = None

        # Allow the rigger to completely bypass the splitter node influence.
        self._attr_bypass_splitter = None

        # Define additional avars
        self.attr_ud_bypass = None

        # Contain the final applied jaw out ratio.
        # Used by the splitter network.
        self.attr_jaw_out_ratio = None

        # Initialize in an AvarGrp init_avar method.
        # Reference to the module containing the avar.
        # todo: replace by a generic implementation for all modules? (ex: IK in Arm)
        self._parent_module = None

    def add_avars(self, attr_holder):
        """
        Create the network that contain all our avars.
        For ease of use, the avars are exposed on the grp_rig, however to protect the connection from Maya
        when unbuilding they are really existing in an external network node.
        """
        super(FaceLipsAvar, self).add_avars(attr_holder)
        self.attr_ud_bypass = self.add_avar(attr_holder, self.AVAR_NAME_UD_BYPASS)

    def build_stack(self, stack, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()
        jnt_head = self.get_head_jnt()
        jnt_jaw = self.get_jaw_jnt()
        jaw_pos = jnt_jaw.getTranslation(space='world')
        jaw_module = self.get_jaw_module()

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

        self._target_jaw_bindpose = self._parent_module._ref_jaw_predeform
        self._attr_jaw_pitch = self._parent_module._attr_jaw_pt

        super(FaceLipsAvar, self).build_stack(stack, **kwargs)

        #
        # Create jaw influence layer
        # Create a reference object to extract the jaw displacement.
        #

        # Compute the rotation introduced by the jaw.
        # Note that the splitter only affect the jaw pitch (rotateX).
        attr_rotation_adjusted = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=self._parent_module._attr_jaw_pt,
            input1Y=self._parent_module._attr_jaw_yw,
            input1Z=self._parent_module._attr_jaw_rl,
            input2X=self.attr_jaw_out_ratio,
            input2Y=self._attr_inn_jaw_ratio_default,
            input2Z=self._attr_inn_jaw_ratio_default,
        ).output

        attr_rotation_tm = libRigging.create_utility_node(
            'composeMatrix',
            inputRotate=attr_rotation_adjusted
        ).outputMatrix

        # Compute the arc offset relative to the avar root
        attr_get_arc_tm = libRigging.create_utility_node(
            'multMatrix',
            matrixIn=(
                self._grp_offset.matrix,  # todo: remove?
                self._parent_module._ref_jaw_predeform.inverseMatrix,
                attr_rotation_tm,
                self._parent_module._ref_jaw_predeform.matrix,
                self._grp_offset.inverseMatrix,  # todo: remove?
            )
        ).matrixSum

        util_decompose_arc_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=attr_get_arc_tm
        )

        # Add the jaw influence as a new stack layer.
        layer_jaw_r = stack.prepend_layer(name='jawArcR')
        layer_jaw_t = stack.prepend_layer(name='jawArcT')

        pymel.connectAttr(util_decompose_arc_tm.outputTranslate, layer_jaw_t.t)
        pymel.connectAttr(util_decompose_arc_tm.outputRotate, layer_jaw_r.r)

        # Connect jaw translation avars to the "jawT" layer.
        layer_jaw_t_to_t = stack.prepend_layer(name='jawT')
        attr_get_jaw_t = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=jaw_module.avar_macro_all.attr_lr,
            input1Y=jaw_module.avar_macro_all.attr_ud,
            input1Z=jaw_module.avar_macro_all.attr_fb,
            input2X=self._attr_inn_jaw_ratio_default,
            input2Y=self._attr_inn_jaw_ratio_default,
            input2Z=self._attr_inn_jaw_ratio_default,
            name=nomenclature_rig.resolve('getJawT')
        ).output
        pymel.connectAttr(attr_get_jaw_t, layer_jaw_t_to_t.translate)

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
        attr_jaw_pitch = self._attr_jaw_pitch

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
        self.attr_jaw_out_ratio = splitter.attr_out_jaw_ratio

        #
        # Implement the 'bypass' avars.
        # Thoses avars bypass the splitter, used in corner cases only.
        #
        attr_attr_ud_bypass_adjusted = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getAdjustedUdBypass'),
            input1X=self.attr_ud_bypass,
            input2X=self.attr_multiplier_ud
        ).outputX
        attr_v = libRigging.create_utility_node(
            'addDoubleLinear',
            name=nomenclature_rig.resolve('addBypassAvar'),
            input1=attr_v,
            input2=attr_attr_ud_bypass_adjusted
        ).output

        return attr_u, attr_v


class FaceLips(rigFaceAvarGrps.AvarGrp):
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
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = True
    CREATE_MACRO_AVAR_ALL = True

    def validate(self):
        """
        If we are using the preDeform flag, we will need to validate that we can find the Jaw influence!
        """
        super(FaceLips, self).validate()

        if not self.preDeform:
            if self.get_jaw_jnt(strict=False) is None:
                raise Exception("Can't resolve jaw. Please create a Jaw module.")

            # Ensure we are able to access the jaw module.
            jaw_module = self.get_jaw_module()
            if not jaw_module:
                raise Exception("Can't resolve jaw module.")

            # If the jaw module is already built, ensure it respect the minimum version requirement.
            # Jaw-0.4.18 introducing support for the 'all' avar macro which we need.
            if jaw_module.is_built:
                version_major, version_minor, version_patch = jaw_module.get_version()
                if version_major == 0 and version_minor == 4 and version_patch < 18:
                    raise Exception("Associated Jaw module version is too low. Expected 0.4.18+, got {}.{}.{}".format(
                        version_major, version_minor, version_patch
                    ))

    def validate_version(self, major_version, minor_version, patch_version):
        if major_version == 0 and minor_version == 4 and patch_version < 23:
            raise Exception("See Task #67153")

    def get_avars_corners(self, macro=True):
        # todo: move upper?
        fnFilter = lambda avar: 'corner' in avar.name.lower()
        result = filter(fnFilter, self.avars)

        if macro:
            if self.avar_macro_lft:
                result.append(self.avar_macro_lft)
            if self.avar_macro_rgt:
                result.append(self.avar_macro_rgt)

        return result

    def get_default_name(self):
        return 'lip'

    def connect_macro_avar(self, avar_macro, avar_micros):
        pass
        # for avar_micro in avar_micros:
        #     libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_ud, avar_micro.attr_ud)
        #     libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_lr, avar_micro.attr_lr)
        #     libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_fb, avar_micro.attr_fb)
        #     libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_pt)
        #
        #     # Add default FB avars to 'fake' a better lip curl pivot.
        #     # see: Art of Moving Points page 146
        #     libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_ud, kv=[0.01, 0.0, -0.01])
        #     libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_fb, kv=[0.01, 0.0, -0.01])
        #
        # # Squeeze animator requested that the lips work like the animation mentor rig.
        # # When the corner macros ud is 1.0, they won't follow the jaw anymore.
        # # When the corner macros ud is -1.0, they won't follow the head anymore.
        # libRigging.connectAttr_withLinearDrivenKeys(
        #     self.avar_l.attr_ud,
        #     self.get_avar_l_corner().attr_jaw_out_ratio,
        #     kt=(1.0, 0.0, -1.0), kv=(0.0, 0.5, 1.0), kit=(2, 2, 2),
        #     kot=(2, 2, 2), pre='linear', pst='linear'
        # )
        #
        # libRigging.connectAttr_withLinearDrivenKeys(
        #     self.avar_r.attr_ud,
        #     self.get_avar_r_corner().attr_jaw_out_ratio,
        #     kt=(1.0, 0.0, -1.0), kv=(0.0, 0.5, 1.0), kit=(2, 2, 2),
        #     kot=(2, 2, 2), pre='linear', pst='linear'
        # )

    def _connect_avar_macro_horizontal(self, avar_parent, avar_children, connect_ud=True, connect_lr=True,
                                       connect_fb=True):
        """
        Connect micro avars to horizontal macro avar. (avar_macro_lft and avar_macro_rgt)
        This configure the avar_lr connection differently depending on the position of each micro avars.
        The result is that the micro avars react like an 'accordion' when their macro avar_lr change.
        :param avar_parent: The macro avar, source of the connections.
        :param avar_children: The micro avars, destination of the connections.
        :param connect_ud: True if we want to connect the avar_ud.
        :param connect_lr: True if we want to connect the avar_lr.
        :param connect_fb: True if we want to connect the avar_fb.
        """
        # super(FaceLips, self)._connect_avar_macro_horizontal(avar_parent, avar_children, connect_ud=False, connect_lr=False, connect_fb=False)

        if connect_lr:
            avar_middle = self.get_avar_micro_mid()
            pos_s = avar_middle.jnt.getTranslation(space='world')
            pos_e = avar_parent.jnt.getTranslation(space='world')

            for avar_child in avar_children:
                # We don't want to connect the middle Avar.
                if avar_child == avar_middle:
                    continue

                pos = avar_child.jnt.getTranslation(space='world')

                # Compute the ratio between the middle and the corner.
                # ex: In the lips, we want the lips to stretch when the corner are taken appart.
                try:
                    ratio = (pos.x - pos_s.x) / (pos_e.x - pos_s.x)
                except ZeroDivisionError:
                    continue
                ratio = max(0, ratio)
                ratio = min(ratio, 1)

                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_lr, avar_child.attr_lr,
                                                            kv=(-ratio, 0.0, ratio))

    def _build_avar_macro_l(self):
        # Create left avar if necessary
        ref = self.get_jnt_l_mid()
        if self.create_macro_horizontal and ref:
            self._build_avar_macro_horizontal(self.avar_macro_lft, self.get_avar_micro_mid(), self.get_avar_micros_lft(),
                                              self._CLS_CTRL_LFT, connect_lr=True, connect_ud=False, connect_fb=False)

    def _connect_avar_macro_l(self):
        super(FaceLips, self)._connect_avar_macro_l()

        # Connect the corner other avars
        avar_macro_lft_corner = self.get_avar_micro_lft_corner()
        if avar_macro_lft_corner:
            libRigging.connectAttr_withLinearDrivenKeys(self.avar_macro_lft.attr_ud, avar_macro_lft_corner.attr_ud)
            libRigging.connectAttr_withLinearDrivenKeys(self.avar_macro_lft.attr_fb, avar_macro_lft_corner.attr_fb)

    def _build_avar_macro_r(self):  # Create right avar if necessary
        ref = self.get_jnt_r_mid()
        if self.create_macro_horizontal and ref:
            self._build_avar_macro_horizontal(self.avar_macro_rgt, self.get_avar_micro_mid(), self.get_avars_micro_rgt(),
                                              self._CLS_CTRL_RGT, connect_lr=True, connect_ud=False, connect_fb=False)

    def _connect_avar_macro_r(self):
        super(FaceLips, self)._connect_avar_macro_r()

        # Connect the corner other avars
        avar_micro_rgt_corner = self.get_avar_micro_rgt_corner()
        if avar_micro_rgt_corner:
            libRigging.connectAttr_withLinearDrivenKeys(self.avar_macro_rgt.attr_ud, avar_micro_rgt_corner.attr_ud)
            libRigging.connectAttr_withLinearDrivenKeys(self.avar_macro_rgt.attr_fb, avar_micro_rgt_corner.attr_fb)

    @libPython.memoized_instancemethod
    def _get_mouth_width(self):
        min_x = max_x = 0
        for avar in self.get_avars_corners():
            x = avar._grp_offset.tx.get()
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        return min_x, max_x

    def _create_avar_macro_all_ctrls(self, parent_pos=None, parent_rot=None, **kwargs):
        """
        Since the avar_all ctrl don't follow the geometry, we'll want it to follow the avar influence.
        This however create double transformation when rotating, it's not that much visible so it will do for now.
        # todo: fix double transformation when rotating
        :param parent_pos:
        :param parent_rot:
        """
        # parent_pos = self.avar_all._grp_output
        parent_rot = self.avar_macro_all._grp_output
        super(FaceLips, self)._create_avar_macro_all_ctrls(parent_pos=parent_pos, parent_rot=parent_rot, **kwargs)

    def get_dependencies_modules(self):
        return [self.get_jaw_module()]

    def __init__(self, *args, **kwargs):
        super(FaceLips, self).__init__(*args, **kwargs)

        # Contain the jaw bind pos before any parenting.
        self._ref_jaw_predeform = None

        # Contain the jaw rotation relative to the bind pose.
        self._attr_jaw_relative_rot = None

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
            jnt_head = self.get_head_jnt()
            if not jnt_head:
                self.error("Failed parenting avars, no head influence found!")
                return

            jnt_jaw = self.get_jaw_jnt()
            if not jnt_jaw:
                self.error("Failed parenting avars, no jaw influence found!")
                return

            min_x, max_x = self._get_mouth_width()
            mouth_width = max_x - min_x

            def connect_avar(avar, ratio):
                avar._attr_inn_jaw_ratio_default.set(ratio)

            for avar in self.get_avars_corners(macro=False):
                connect_avar(avar, 0.5)

            for avar in self.get_avars_upp(macro=False):
                if use_football_interpolation:
                    avar_pos_x = avar._grp_offset.tx.get()
                    ratio = abs(avar_pos_x - min_x / mouth_width)
                    ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
                    ratio = libRigging.interp_football(ratio)  # apply football shape
                else:
                    ratio = 0.0

                connect_avar(avar, ratio)

            for avar in self.get_avars_low(macro=False):
                if use_football_interpolation:
                    avar_pos_x = avar._grp_offset.tx.get()
                    ratio = abs(avar_pos_x - min_x / mouth_width)
                    ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
                    ratio = 1.0 - libRigging.interp_football(ratio)  # apply football shape
                else:
                    ratio = 1.0

                connect_avar(avar, ratio)

        #
        # Add custom default connections
        #

        # Squeeze animator requested that the lips work like the animation mentor rig.
        # When the corner macros ud is 1.0, they won't follow the jaw anymore.
        # When the corner macros ud is -1.0, they won't follow the head anymore.
        avar_micro_corner_l = self.get_avar_micro_lft_corner()
        avar_micro_corner_r = self.get_avar_micro_rgt_corner()

        libRigging.connectAttr_withLinearDrivenKeys(
            self.avar_macro_lft.attr_ud,
            avar_micro_corner_l._attr_inn_jaw_ratio_default,
            kt=(1.0, 0.0, -1.0), kv=(0.0, 0.5, 1.0), kit=(2, 2, 2),
            kot=(2, 2, 2), pre='linear', pst='linear'
        )

        libRigging.connectAttr_withLinearDrivenKeys(
            self.avar_macro_rgt.attr_ud,
            avar_micro_corner_r._attr_inn_jaw_ratio_default,
            kt=(1.0, 0.0, -1.0), kv=(0.0, 0.5, 1.0), kit=(2, 2, 2),
            kot=(2, 2, 2), pre='linear', pst='linear'
        )

        # Calibration is done manually since we need to setup the jaw influence.
        if calibrate:
            self.calibrate()

    def _build_avars(self, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()
        jnt_head = self.get_head_jnt()
        jnt_jaw = self.get_jaw_jnt()
        pos_jaw = jnt_jaw.getTranslation(space='world')

        #
        # Build a network that evaluate the jaw transform in relation with it's bind pose.
        # This will be used by avars to computer the 'jawArcT' and 'jawArcR' layer.
        #
        self._ref_jaw_predeform = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('refJawPreDeform'),
            parent=self.grp_rig
        )
        self._ref_jaw_predeform.setTranslation(pos_jaw)

        # Create jaw bind-pose reference
        ref_head = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('refJawBefore'),
            parent=self.grp_rig
        )
        ref_head.setTranslation(pos_jaw)
        pymel.parentConstraint(jnt_head, ref_head, maintainOffset=True)

        # Create jaw actual pose reference
        ref_jaw = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('refJawAfter'),
            parent=self.grp_rig
        )
        ref_jaw.setTranslation(pos_jaw)
        pymel.parentConstraint(jnt_jaw, ref_jaw, maintainOffset=True)

        # Extract the rotation
        # By using matrix we make sure that there's no flipping introduced.
        # This happen in maya when using constraint with multiple targets since
        # Maya use individual values in it's computations.
        attr_get_relative_tm = libRigging.create_utility_node(
            'multMatrix',
            matrixIn=(
                ref_jaw.worldMatrix,
                ref_head.worldInverseMatrix,
            )
        ).matrixSum

        util_get_rotation_euler = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=attr_get_relative_tm
        )

        self._attr_jaw_pt = util_get_rotation_euler.outputRotateX
        self._attr_jaw_yw = util_get_rotation_euler.outputRotateY
        self._attr_jaw_rl = util_get_rotation_euler.outputRotateZ

        super(FaceLips, self)._build_avars(**kwargs)


def register_plugin():
    return FaceLips
