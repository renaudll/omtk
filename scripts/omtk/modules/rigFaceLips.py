"""
Logic for the "FaceLips" module
"""
import pymel.core as pymel
from omtk.core.exceptions import ValidationError
from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.models import model_avar_surface_lips


class CtrlLipsUpp(rigFaceAvarGrps.CtrlFaceUpp):
    pass


class CtrlLipsLow(rigFaceAvarGrps.CtrlFaceLow):
    pass


class FaceLipsAvar(rigFaceAvar.AvarFollicle):
    """
    The Lips avar are special as they implement a Splitter mechanism that
    ensure the avars move in jaw space before moving in surface space.
    For this reason, we implement a new avar, 'avar_ud_bypass'
    to skip the splitter mechanism if necessary. (ex: avar_all)
    """

    AVAR_NAME_UD_BYPASS = "_attr_inn_ud_bypass"
    _CLS_MODEL_INFL = model_avar_surface_lips.AvarSurfaceLipModel

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

        # Define additional avars
        self.attr_ud_bypass = None

        # Contain the final applied jaw out ratio.
        # Used by the splitter network.
        self.attr_jaw_out_ratio = None

        # Jaw influence is applied as a pre-transform on the avar.
        # It is exposed here to be re-used by any controller model that need it.
        self._jaw_arc_tm = None

        # Initialize in an AvarGrp init_avar method.
        # Reference to the module containing the avar.
        # todo: replace by a generic implementation for all modules? (ex: IK in Arm)
        self._parent_module = None

        self._attr_jaw_bind_tm = None
        self._attr_jaw_pitch = None

    def add_avars(self, attr_holder):
        """
        Create the network that contain all our avars.
        For ease of use, the avars are exposed on the grp_rig,
        however to protect the connection from Maya when unbuilding
        they are really existing in an external network node.
        """
        super(FaceLipsAvar, self).add_avars(attr_holder)
        self.attr_ud_bypass = self.add_avar(attr_holder, self.AVAR_NAME_UD_BYPASS)

    def create_stacks(self):
        super(FaceLipsAvar, self).create_stacks()

        nomenclature_rig = self.get_nomenclature_rig()

        # Create additional attributes to control the jaw layer

        libAttr.addAttr_separator(self.grp_rig, "jawLayer")
        self._attr_inn_jaw_ratio_default = libAttr.addAttr(
            self.grp_rig,
            "jawRatioDefault",
            defaultValue=0.5,
            hasMinValue=True,
            hasMaxValue=True,
            minValue=0,
            maxValue=1,
            k=True,
        )
        self._attr_bypass_splitter = libAttr.addAttr(
            self.grp_rig,
            "jawSplitterBypass",
            defaultValue=0.0,
            hasMinValue=True,
            hasMaxValue=True,
            minValue=0,
            maxValue=1,
            k=True,
        )

        # Variable shared with the AvarInflModel
        self._attr_jaw_bind_tm = self._parent_module._ref_jaw_predeform.matrix
        self._attr_jaw_pitch = self._parent_module._attr_jaw_pt

    def unbuild(self):
        super(FaceLipsAvar, self).unbuild()

        # Cleanup invalid references
        self.attr_jaw_out_ratio = None


class FaceLips(rigFaceAvarGrps.AvarGrpOnSurface):
    """
    AvarGrp setup customized for lips rigging.
    Lips have the same behavior than an AvarGrpUppLow.
    However the lip curl is also connected between the macro avars and the micro avars.
    """

    _CLS_AVAR = FaceLipsAvar
    _CLS_AVAR_MACRO = FaceLipsAvar  # necessary to feed the jawArc to the ctrl model
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True
    _CLS_CTRL_UPP = CtrlLipsUpp
    _CLS_CTRL_LOW = CtrlLipsLow
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = True
    CREATE_MACRO_AVAR_ALL = True

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(FaceLips, self).validate()

        if not self.preDeform:
            if not self.get_jaw_jnt(strict=False):
                raise ValidationError("Can't resolve jaw. Please create a Jaw module.")

            # Ensure we are able to access the jaw module.
            jaw_module = self.get_jaw_module()
            if not jaw_module:
                raise ValidationError("Can't resolve jaw module.")

    def get_avars_corners(self, macro=True):
        # todo: move upper?
        fnFilter = lambda avar: "corner" in avar.name.lower()
        result = filter(fnFilter, self.avars)

        if macro and self.create_macro_horizontal:
            if self.avar_l:
                result.append(self.avar_l)
            if self.avar_r:
                result.append(self.avar_r)

        return result

    def get_default_name(self):
        return "lip"

    def connect_macro_avar(self, avar_macro, avar_micros):
        pass

    def _connect_avar_macro_horizontal(
        self,
        avar_parent,
        avar_children,
        connect_ud=True,
        connect_lr=True,
        connect_fb=True,
    ):
        """
        Connect micro avars to horizontal macro avar. (avar_l and avar_r)

        This configure the avar_lr connection differently
        depending on the position of each micro avars.
        The result is that the micro avars react like
        an 'accordion' when their macro avar_lr change.

        :param avar_parent: The macro avar, source of the connections.
        :param avar_children: The micro avars, destination of the connections.
        :param connect_ud: True if we want to connect the avar_ud.
        :param connect_lr: True if we want to connect the avar_lr.
        :param connect_fb: True if we want to connect the avar_fb.
        """
        if connect_lr:
            avar_middle = self.get_avar_mid()
            pos_s = avar_middle.jnt.getTranslation(space="world")
            pos_e = avar_parent.jnt.getTranslation(space="world")

            for avar_child in avar_children:
                # We don't want to connect the middle Avar.
                if avar_child == avar_middle:
                    continue

                pos = avar_child.jnt.getTranslation(space="world")

                # Compute the ratio between the middle and the corner.
                # ex: In the lips, we want the lips to stretch
                # when the corner are taken appart.
                try:
                    ratio = (pos.x - pos_s.x) / (pos_e.x - pos_s.x)
                except ZeroDivisionError:
                    continue
                ratio = max(0, ratio)
                ratio = min(ratio, 1)

                libRigging.connectAttr_withLinearDrivenKeys(
                    avar_parent.attr_lr, avar_child.attr_lr, kv=(-ratio, 0.0, ratio)
                )

    # def _build_avar_macro_l(self):
    #     # Create left avar if necessary
    #     ref = self.get_jnt_l_mid()
    #     if self.create_macro_horizontal and ref:
    #         self._build_avar_macro_horizontal(
    #             self.avar_l,
    #             connect_lr=True,
    #             connect_ud=False,
    #             connect_fb=False,
    #         )

    def _connect_avar_macro_l(self, avar, child_avars):
        super(FaceLips, self)._connect_avar_macro_l(avar, child_avars)

        # Connect the corner other avars
        avar_l_corner = self.get_avar_l_corner()
        if avar_l_corner and avar_l_corner in child_avars:
            libRigging.connectAttr_withLinearDrivenKeys(
                avar.attr_ud, avar_l_corner.attr_ud
            )
            libRigging.connectAttr_withLinearDrivenKeys(
                avar.attr_lr, avar_l_corner.attr_lr
            )

    # def _build_avar_macro_r(self):  # Create right avar if necessary
    #     ref = self.get_jnt_r_mid()
    #     if self.create_macro_horizontal and ref:
    #         self._build_avar_macro_horizontal(
    #             self.avar_r,
    #             self.get_avar_mid(),
    #             self.get_avars_micro_r(),
    #             connect_lr=True,
    #             connect_ud=False,
    #             connect_fb=False,
    #         )

    def _connect_avar_macro_r(self, avar, child_avars):
        super(FaceLips, self)._connect_avar_macro_r(avar, child_avars)

        # Connect the corner other avars
        avar_r_corner = self.get_avar_r_corner()
        if avar_r_corner and avar_r_corner in child_avars:
            libRigging.connectAttr_withLinearDrivenKeys(
                avar.attr_ud, avar_r_corner.attr_ud
            )
            libRigging.connectAttr_withLinearDrivenKeys(
                avar.attr_lr, avar_r_corner.attr_lr
            )

    def _get_mouth_width(self):
        min_x = max_x = 0
        for avar in self.get_avars_corners():
            x = avar.grp_offset.tx.get()
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        return min_x, max_x

    def get_dependencies_modules(self):
        return {self.get_jaw_module()}

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
                self.log.error("Failed parenting avars, no head influence found!")
                return

            jnt_jaw = self.get_jaw_jnt()
            if not jnt_jaw:
                self.log.error("Failed parenting avars, no jaw influence found!")
                return

            min_x, max_x = self._get_mouth_width()
            mouth_width = max_x - min_x

            def connect_avar(avar, ratio):
                avar._attr_inn_jaw_ratio_default.set(ratio)

            for avar in self.get_avars_corners(macro=False):
                connect_avar(avar, 0.5)

            for avar in self.get_avars_upp(macro=False):
                if use_football_interpolation:
                    avar_pos_x = avar.grp_offset.tx.get()
                    ratio = abs(avar_pos_x - min_x / mouth_width)
                    ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
                    ratio = libRigging.interp_football(ratio)  # apply football shape
                else:
                    ratio = 0.0

                connect_avar(avar, ratio)

            for avar in self.get_avars_low(macro=False):
                if use_football_interpolation:
                    avar_pos_x = avar.grp_offset.tx.get()
                    ratio = abs(avar_pos_x - min_x / mouth_width)
                    ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
                    ratio = 1.0 - libRigging.interp_football(
                        ratio
                    )  # apply football shape
                else:
                    ratio = 1.0

                connect_avar(avar, ratio)

        # Hardcode the jawRatio for the macro ctrls
        self.avar_upp._attr_inn_jaw_ratio_default.set(0.0)
        self.avar_l._attr_inn_jaw_ratio_default.set(0.5)
        self.avar_r._attr_inn_jaw_ratio_default.set(0.5)
        self.avar_low._attr_inn_jaw_ratio_default.set(1.0)

        #
        # Add custom default connections
        #

        # Squeeze animator requested that the lips work like the animation mentor rig.
        # When the corner macros ud is 1.0, they won't follow the jaw anymore.
        # When the corner macros ud is -1.0, they won't follow the head anymore.
        avar_micro_corner_l = self.get_avar_l_corner()
        avar_micro_corner_r = self.get_avar_r_corner()

        libRigging.connectAttr_withLinearDrivenKeys(
            self.avar_l.attr_ud,
            avar_micro_corner_l._attr_inn_jaw_ratio_default,
            kt=(1.0, 0.0, -1.0),
            kv=(0.0, 0.5, 1.0),
            kit=(2, 2, 2),
            kot=(2, 2, 2),
            pre="linear",
            pst="linear",
        )

        libRigging.connectAttr_withLinearDrivenKeys(
            self.avar_r.attr_ud,
            avar_micro_corner_r._attr_inn_jaw_ratio_default,
            kt=(1.0, 0.0, -1.0),
            kv=(0.0, 0.5, 1.0),
            kit=(2, 2, 2),
            kot=(2, 2, 2),
            pre="linear",
            pst="linear",
        )

        # Ensure that the all macro avar bypass the jaw splitter as we expect it to be 100% linear.
        # todo: use another class for the 'all' macro avar.
        if self.create_macro_all:
            self.avar_all._attr_bypass_splitter.set(1.0)

        # Calibration is done manually since we need to setup the jaw influence.
        if calibrate:
            self.calibrate()

    def _build_avars(self, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()
        jnt_head = self.get_head_jnt()
        jnt_jaw = self.get_jaw_jnt()
        pos_jaw = jnt_jaw.getTranslation(space="world")

        #
        # Build a network that evaluate the jaw transform in relation with it's bind pose.
        # This will be used by avars to computer the 'jawArcT' and 'jawArcR' layer.
        #
        self._ref_jaw_predeform = pymel.createNode(
            "transform",
            name=nomenclature_rig.resolve("refJawPreDeform"),
            parent=self.grp_rig,
        )
        self._ref_jaw_predeform.setTranslation(pos_jaw)

        # Create jaw bind-pose reference
        ref_head = pymel.createNode(
            "transform",
            name=nomenclature_rig.resolve("refJawBefore"),
            parent=self.grp_rig,
        )
        ref_head.setTranslation(pos_jaw)
        pymel.parentConstraint(jnt_head, ref_head, maintainOffset=True)

        # Create jaw actual pose reference
        ref_jaw = pymel.createNode(
            "transform",
            name=nomenclature_rig.resolve("refJawAfter"),
            parent=self.grp_rig,
        )
        ref_jaw.setTranslation(pos_jaw)
        pymel.parentConstraint(jnt_jaw, ref_jaw, maintainOffset=True)

        # Extract the rotation
        # By using matrix we make sure that there's no flipping introduced.
        # This happen in maya when using constraint with multiple targets since
        # Maya use individual values in it's computations.
        attr_get_relative_tm = libRigging.create_utility_node(
            "multMatrix", matrixIn=(ref_jaw.worldMatrix, ref_head.worldInverseMatrix,)
        ).matrixSum

        util_get_rotation_euler = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_get_relative_tm
        )

        self._attr_jaw_pt = util_get_rotation_euler.outputRotateX
        self._attr_jaw_yw = util_get_rotation_euler.outputRotateY
        self._attr_jaw_rl = util_get_rotation_euler.outputRotateZ

        super(FaceLips, self)._build_avars(**kwargs)

    def _patch_avars(self):
        super(FaceLips, self)._patch_avars()
        for avar in self.iter_avars():
            # We don't want the 'all' avar to be influenced by the jaw.
            if avar != self.avar_all:
                self._add_jaw_contribution(avar)

    def _add_jaw_contribution(self, avar):
        """
        Give the occasion for the AvarGrp to add a contribution before the avar.
        :param avar: The avar that the matrix will be sent to. 
        :param inn_tm: The matrix before sent to the avar, relative to the bind matrix.
        :return: A modified matrix, still relative to the bind matrix.
        """
        # todo: use a patching function?
        new_layer = avar._stack_post.append_layer(name="jawContribution")
        nomenclature_rig = self.get_nomenclature_rig()
        jaw_module = self.get_jaw_module()

        # todo: why is this still here? it should be in the AvarModel no?
        attr_jaw_out_ratio = avar.model_infl._attr_out_jaw_ratio
        attr_inn_jaw_ratio_default = avar._attr_inn_jaw_ratio_default
        parent_jaw_yw = avar._parent_module._attr_jaw_yw
        parent_jaw_pt = avar._parent_module._attr_jaw_pt
        parent_jaw_rl = avar._parent_module._attr_jaw_rl

        # Compute the rotation introduced by the jaw.
        # Note that the splitter only affect the jaw pitch (rotateX).
        attr_rotation_adjusted = libRigging.create_utility_node(
            "multiplyDivide",
            name=nomenclature_rig.resolve("getJawRotate"),
            input1X=parent_jaw_pt,
            input1Y=parent_jaw_yw,
            input1Z=parent_jaw_rl,
            input2X=attr_jaw_out_ratio,
            input2Y=attr_inn_jaw_ratio_default,
            input2Z=attr_inn_jaw_ratio_default,
        ).output

        attr_rotation_tm = libRigging.create_utility_node(
            "composeMatrix",
            name=nomenclature_rig.resolve("getJawRotateTm"),
            inputRotate=attr_rotation_adjusted,
        ).outputMatrix

        # Connect jaw translation avars to the "jawT" layer.
        attr_get_jaw_t = libRigging.create_utility_node(
            "multiplyDivide",
            name=nomenclature_rig.resolve("getJawTranslate"),
            input1X=jaw_module.avar_all.attr_lr,
            input1Y=jaw_module.avar_all.attr_ud,
            input1Z=jaw_module.avar_all.attr_fb,
            input2X=attr_inn_jaw_ratio_default,
            input2Y=attr_inn_jaw_ratio_default,
            input2Z=attr_inn_jaw_ratio_default,
        ).output

        attr_get_jaw_t_tm = libRigging.create_utility_node(
            "composeMatrix",
            name=nomenclature_rig.resolve("getJawTranslateTm"),
            inputTranslate=attr_get_jaw_t,
        ).outputMatrix

        # We want to include the jaw contribution in the parent for BOTH the AvarModel and the CtrlModel.
        jaw_avar = jaw_module.avar_all
        jaw_avar_offset_tm = jaw_avar.grp_offset.worldMatrix
        jaw_avar_offset_tm_inv = jaw_avar.grp_offset.worldInverseMatrix
        result_tm = libRigging.create_utility_node(
            "multMatrix",
            name=nomenclature_rig.resolve("getPostAvarTm"),
            matrixIn=(
                avar.grp_offset.matrix,
                jaw_avar_offset_tm_inv,  # go into jaw space
                attr_get_jaw_t_tm,  # apply jaw translation
                attr_rotation_tm,  # apply jaw rotation
                jaw_avar_offset_tm,  # exit jaw space
                avar.grp_offset.inverseMatrix,
            ),
        ).matrixSum

        util_decompose_result_tm = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=result_tm,
        )
        pymel.connectAttr(util_decompose_result_tm.outputTranslate, new_layer.translate)
        pymel.connectAttr(util_decompose_result_tm.outputRotate, new_layer.rotate)
        pymel.connectAttr(util_decompose_result_tm.outputScale, new_layer.scale)


def register_plugin():
    return FaceLips
