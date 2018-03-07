import math
import pymel.core as pymel
from omtk.libs import libRigging
from omtk.core.classNode import Node
from omtk.libs import libAttr
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from . import model_avar_surface


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


class AvarSurfaceLipModel(model_avar_surface.AvarSurfaceModel):
    """
    Custom avar model for the complex situation that is the lips.
    This ensure that we are moving according to the jaw before sliding on the surface.
    """

    def __init__(self, *args, **kwargs):
        super(AvarSurfaceLipModel, self).__init__(*args, **kwargs)

        self._attr_inn_jaw_bindpose = None
        self._attr_inn_jaw_pitch = None
        self._attr_inn_jaw_ratio_default = None
        self._attr_inn_bypass_splitter = None
        
        self._attr_out_jaw_ratio = None

    def _create_interface(self):
        super(AvarSurfaceLipModel, self)._create_interface()

        self._attr_inn_jaw_bindpose = libAttr.addAttr(self.grp_rig, 'innJawBindPose', dataType='matrix')
        self._attr_inn_jaw_pitch = libAttr.addAttr(self.grp_rig, 'innJawPitch', defaultValue=0)
        self._attr_inn_jaw_ratio_default = libAttr.addAttr(self.grp_rig, 'innJawRatioDefault', defaultValue=0)
        self._attr_inn_bypass_splitter = libAttr.addAttr(self.grp_rig, 'innBypassSplitter')
        self._attr_inn_ud_bypass = libAttr.addAttr(self.grp_rig, 'innBypassUD')
        # self._attr_inn_surface_length_u = libAttr.addAttr(self.grp_rig, 'innSurfaceLengthU', defaultValue=0)
        # self._attr_inn_surface_length_v = libAttr.addAttr(self.grp_rig, 'innSurfaceLengthV', defaultValue=0)
        
        self._attr_out_jaw_ratio = libAttr.addAttr(self.grp_rig, 'outJawRatio')

    def connect_avar(self, avar):
        super(AvarSurfaceLipModel, self).connect_avar(avar)

        # Note: We expect a FaceLipAvar
        pymel.connectAttr(avar._attr_jaw_bind_tm, self._attr_inn_jaw_bindpose)
        pymel.connectAttr(avar._attr_jaw_pitch, self._attr_inn_jaw_pitch)
        pymel.connectAttr(avar._attr_inn_jaw_ratio_default, self._attr_inn_jaw_ratio_default)
        pymel.connectAttr(avar._attr_bypass_splitter, self._attr_inn_bypass_splitter)
        pymel.connectAttr(avar.attr_ud_bypass, self._attr_inn_ud_bypass)
        

    def _get_follicle_relative_uv_attr(self, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

        attr_u, attr_v = super(AvarSurfaceLipModel, self)._get_follicle_relative_uv_attr(**kwargs)

        util_decompose_jaw_bind_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=self._attr_inn_jaw_bindpose,
        )

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
            point1=self.grp_offset.translate,
            point2=util_decompose_jaw_bind_tm.outputTranslate
        ).distance

        # Resolve the jaw pitch. Used by the splitter.
        attr_jaw_pitch = self._attr_inn_jaw_pitch

        # Connect the splitter inputs
        pymel.connectAttr(attr_u, splitter.attr_inn_surface_u)
        pymel.connectAttr(attr_v, splitter.attr_inn_surface_v)
        pymel.connectAttr(self._attr_inn_jaw_ratio_default, splitter.attr_inn_jaw_default_ratio)
        pymel.connectAttr(self._attr_length_v, splitter.attr_inn_surface_range_v)
        pymel.connectAttr(attr_jaw_radius, splitter.attr_inn_jaw_radius)
        pymel.connectAttr(attr_jaw_pitch, splitter.attr_inn_jaw_pt)
        pymel.connectAttr(self._attr_inn_bypass_splitter, splitter.attr_inn_bypass)

        attr_u = splitter.attr_out_surface_u
        attr_v = splitter.attr_out_surface_v

        # Create constraint to controller the jaw reference
        pymel.connectAttr(splitter.attr_out_jaw_ratio, self._attr_out_jaw_ratio)

        #
        # Implement the 'bypass' avars.
        # Thoses avars bypass the splitter, used in corner cases only.
        #
        attr_attr_ud_bypass_adjusted = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getAdjustedUdBypass'),
            input1X=self._attr_inn_ud_bypass,
            input2X=self.multiplier_ud
        ).outputX
        attr_v = libRigging.create_utility_node(
            'addDoubleLinear',
            name=nomenclature_rig.resolve('addBypassAvar'),
            input1=attr_v,
            input2=attr_attr_ud_bypass_adjusted
        ).output

        return attr_u, attr_v
