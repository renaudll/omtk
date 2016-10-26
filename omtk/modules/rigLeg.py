import logging

import pymel.core as pymel
from maya import cmds
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules import rigIK
from omtk.modules import rigLimb

log = logging.getLogger('omtk')


class CtrlIkLeg(rigIK.CtrlIk):
    """
    Inherit of base CtrlIk to create a specific box shaped controller
    """
    def __createNode__(self, refs=None, geometries=None, *args, **kwargs):
        return libCtrlShapes.create_shape_box_feet(refs, geometries, *args, **kwargs)


class LegIk(rigIK.IK):
    """
    IK/FK setup customized for Leg rigging. Include a FootRoll.
    Create an IK chain with an embeded footroll.
    Two modes are supported:
    1) leg_upp, leg_low, leg_foot, leg_toes, leg_tip (classical setup)
    2) leg_upp, leg_low, leg_foot, leg_heel, leg_toes, leg_tip (advanced setup)
    Setup #2 is more usefull if the character have shoes.
    This allow us to ensure the foot stay fixed when the 'Ankle Side' attribute is used.
    """
    _CLASS_CTRL_IK = CtrlIkLeg
    SHOW_IN_UI = False

    BACK_ROTX_LONGNAME = 'rollBack'
    BACK_ROTX_NICENAME = 'Back Roll'
    BACK_ROTY_LONGNAME = 'backTwist'
    BACK_ROTY_NICENAME = 'Back Twist'

    HEEL_ROTY_LONGNAME = 'footTwist'
    HEEL_ROTY_NICENAME = 'Heel Twist'

    ANKLE_ROTX_LONGNAME = 'rollAnkle'
    ANKLE_ROTX_NICENAME = 'Ankle Roll'
    ANKLE_ROTZ_LONGNAME = 'heelSpin'
    ANKLE_ROTZ_NICENAME = 'Ankle Side'

    TOES_ROTY_LONGNAME = 'toesTwist'
    TOES_ROTY_NICENAME = 'Toes Twist'

    TOESFK_ROTX_LONGNAME = 'toeWiggle'
    TOESFK_ROTX_NICENAME = 'Toe Wiggle'

    FRONT_ROTX_LONGNAME = 'rollFront'
    FRONT_ROTX_NICENAME = 'Front Roll'
    FRONT_ROTY_LONGNAME = 'frontTwist'
    FRONT_ROTY_NICENAME = 'Front Twist'

    """
    A standard footroll that remember it's pivot when building/unbuilding.
    """

    def __init__(self, *args, **kwargs):
        super(LegIk, self).__init__(*args, **kwargs)

        self.pivot_foot_heel = None
        self.pivot_toes_heel = None
        self.pivot_toes_ankle = None
        self.pivot_foot_front = None
        self.pivot_foot_back = None
        self.pivot_foot_inn = None
        self.pivot_foot_out = None
        self.pivot_foot_ankle = None
        self.pivot_foot_toes_fk = None

        self.pivot_foot_heel_pos = None
        self.pivot_toes_heel_pos = None
        self.pivot_toes_ankle_pos = None
        self.pivot_foot_front_pos = None
        self.pivot_foot_back_pos = None
        self.pivot_foot_inn_pos = None
        self.pivot_foot_out_pos = None

    def _get_reference_plane(self):
        """
        When holding/fetching the footroll pivots, we do not want to use their worldSpace transforms.
        :return: The reference worldSpace matrix to use when holding/fetching pivot positions.
        """
        jnts = self.input[self.iCtrlIndex:]
        pos_s = jnts[0].getTranslation(space='world')
        pos_e = jnts[-1].getTranslation(space='world')

        # We take in account that the foot is always flat on the floor.
        axis_y = pymel.datatypes.Vector(0,1,0)
        axis_z = pos_e - pos_s
        axis_z.y = 0
        axis_z.normalize()
        axis_x = axis_y.cross(axis_z)
        axis_x.normalize()

        pos = pymel.datatypes.Point(self.chain_jnt[self.iCtrlIndex].getTranslation(space='world'))
        tm = pymel.datatypes.Matrix(
            axis_x.x, axis_x.y, axis_x.z, 0,
            axis_y.x, axis_y.y, axis_y.z, 0,
            axis_z.x, axis_z.y, axis_z.z, 0,
            pos.x, pos.y, pos.z, 1
        )
        return tm

    def _get_recommended_pivot_heelfloor(self, pos_foot):
        """
        :param pos_foot: The position of the foot jnt
        :return: The position of the heel pivot
        """
        result = pymel.datatypes.Point(pos_foot)
        result.y = 0
        return result

    def _get_recommended_pivot_front(self, geometries, tm_ref, tm_ref_dir, pos_toes, pos_tip):
        """
        Determine recommended position using ray-cast from the toes.
        If the ray-cast fail, use the last joint position.
        return: The recommended position as a world pymel.datatypes.Vector
        """
        dir = pymel.datatypes.Point(0, 0, 1) * tm_ref_dir
        pos = libRigging.ray_cast_farthest(pos_toes, dir, geometries)
        if not pos:
            cmds.warning("Can't automatically solve FootRoll front pivot, using last joint as reference.")
            pos = pos_tip
        else:
            # Compare our result with the last joint position and take the longuest.
            pos.z = max(pos.z, pos_tip.z)

        # Ensure we are aligned with the reference matrix.
        pos_relative = pos * tm_ref.inverse()
        pos_relative.x = 0
        pos_relative.y = 0
        pos = pos_relative * tm_ref
        pos.y = 0

        #HACK : Ensure that the point is size 3 and not 4
        return pymel.datatypes.Point(pos.x,pos.y,pos.z)

    def _get_recommended_pivot_back(self, geometries, tm_ref, tm_ref_dir, pos_toes):
        """
        Determine recommended position using ray-cast from the toes.
        If the ray-cast fail, use the toes position.
        return: The recommended position as a world pymel.datatypes.Vector
        """
        dir = pymel.datatypes.Point(0,0,-1) * tm_ref_dir
        pos = libRigging.ray_cast_farthest(pos_toes, dir, geometries)
        if not pos:
            cmds.warning("Can't automatically solve FootRoll back pivot.")
            pos = pos_toes

        # Ensure we are aligned with the reference matrix.
        pos_relative = pos * tm_ref.inverse()
        pos_relative.x = 0
        pos_relative.y = 0
        pos = pos_relative * tm_ref
        pos.y = 0

        #HACK : Ensure that the point is size 3 and not 4
        return pymel.datatypes.Point(pos.x,pos.y,pos.z)

    def _get_recommended_pivot_bank(self, geometries, tm_ref, tm_ref_dir, pos_toes, direction=1):
        """
        Determine recommended position using ray-cast from the toes.
        TODO: If the ray-case fail, use a specified default value.
        return: The recommended position as a world pymel.datatypes.Vector
        """
        # Sanity check, ensure that at least one point is in the bounds of geometries.
        # This can prevent rays from being fired from outside a geometry.
        # TODO: Make it more robust.
        filtered_geometries = []
        for geometry in geometries:
            xmin, ymin, zmin, xmax, ymax, zmax = cmds.exactWorldBoundingBox(geometry.__melobject__())
            bound = pymel.datatypes.BoundingBox((xmin, ymin, zmin), (xmax, ymax, zmax))
            if bound.contains(pos_toes):
                filtered_geometries.append(geometry)

        dir = pymel.datatypes.Point(direction, 0, 0) * tm_ref_dir
        pos = libRigging.ray_cast_nearest(pos_toes, dir, filtered_geometries)
        if not pos:
            cmds.warning("Can't automatically solve FootRoll bank inn pivot.")
            pos = pos_toes

        pos.y = 0

        return pos

    def build(self, attr_holder=None, constraint_handle=False, setup_softik=True, **kwargs):
        """
        Build the LegIk system
        :param attr_holder: The attribute holder object for all the footroll params
        :param kwargs: More kwargs pass to the superclass
        :return: Nothing
        """
        # Compute ctrl_ik orientation
        # Hack: Bypass pymel bug (see https://github.com/LumaPictures/pymel/issues/355)
        ctrl_ik_orientation = pymel.datatypes.TransformationMatrix(self._get_reference_plane()).rotate

        super(LegIk, self).build(ctrl_ik_orientation=ctrl_ik_orientation, constraint_handle=constraint_handle, setup_softik=setup_softik, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()

        jnts = self._chain_ik[self.iCtrlIndex:]
        num_jnts = len(jnts)
        if num_jnts == 4:
            jnt_foot, jnt_heel, jnt_toes, jnt_tip = jnts
        elif num_jnts == 3:
            jnt_foot, jnt_toes, jnt_tip = jnts
            jnt_heel = None
        else:
            raise Exception("Unexpected number of joints after the limb. Expected 3 or 4, got {0}".format(num_jnts))

        # Create FootRoll (chain?)
        pos_foot = pymel.datatypes.Point(jnt_foot.getTranslation(space='world'))
        pos_heel = pymel.datatypes.Point(jnt_heel.getTranslation(space='world')) if jnt_heel else None
        pos_toes = pymel.datatypes.Point(jnt_toes.getTranslation(space='world'))
        pos_tip = pymel.datatypes.Point(jnt_tip.getTranslation(space='world'))

        # Resolve pivot locations
        tm_ref = self._get_reference_plane()
        tm_ref_dir = pymel.datatypes.Matrix(  # Used to compute raycast directions
            tm_ref.a00, tm_ref.a01, tm_ref.a02, tm_ref.a03,
            tm_ref.a10, tm_ref.a11, tm_ref.a12, tm_ref.a13,
            tm_ref.a20, tm_ref.a21, tm_ref.a22, tm_ref.a23,
            0, 0, 0, 1
        )

        #
        # Resolve pivot positions
        #
        geometries = self.rig.get_meshes()

        # Resolve pivot inn
        if self.pivot_foot_inn_pos:
            pos_pivot_inn = pymel.datatypes.Point(self.pivot_foot_inn_pos) * tm_ref
        else:
            pos_pivot_inn = self._get_recommended_pivot_bank(geometries, tm_ref, tm_ref_dir, pos_toes, direction=-1)

        # Resolve pivot bank out
        if self.pivot_foot_out_pos:
            pos_pivot_out = pymel.datatypes.Point(self.pivot_foot_out_pos) * tm_ref
        else:
            pos_pivot_out = self._get_recommended_pivot_bank(geometries, tm_ref, tm_ref_dir, pos_toes, direction=1)

        # Resolve pivot Back
        if self.pivot_foot_back_pos:
            pos_pivot_back = pymel.datatypes.Point(self.pivot_foot_back_pos) * tm_ref
        else:
            pos_pivot_back = self._get_recommended_pivot_back(geometries, tm_ref, tm_ref_dir, pos_toes)

        # Set pivot Front
        if self.pivot_foot_front_pos:
            pos_pivot_front = pymel.datatypes.Point(self.pivot_foot_front_pos) * tm_ref
        else:
            pos_pivot_front = self._get_recommended_pivot_front(geometries, tm_ref, tm_ref_dir, pos_toes, pos_tip)

        # Set pivot Ankle
        if self.pivot_toes_ankle_pos:
            pos_pivot_ankle = pymel.datatypes.Point(self.pivot_toes_ankle_pos) * tm_ref
        else:
            pos_pivot_ankle = pos_toes

        # Set pivot Heel floor
        if self.pivot_toes_heel_pos:
            pos_pivot_heel = pymel.datatypes.Point(self.pivot_toes_heel_pos) * tm_ref
        else:
            if jnt_heel:
                pos_pivot_heel = pos_heel
            else:
                pos_pivot_heel = pymel.datatypes.Point(pos_foot)
                pos_pivot_heel.y = 0


        #
        # Build Setup
        #

        root_footRoll = pymel.createNode('transform', name=nomenclature_rig.resolve('footRoll'))

        # Align all pivots to the reference plane
        root_footRoll.setMatrix(tm_ref)

        # Create pivots hierarchy
        self.pivot_toes_heel = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotToesHeel'))
        self.pivot_toes_ankle = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotToesAnkle'))
        self.pivot_foot_ankle = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotFootAnkle'))
        self.pivot_foot_front = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotFootFront'))
        self.pivot_foot_back = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotFootBack'))
        self.pivot_foot_inn = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotFootBankInn'))
        self.pivot_foot_out = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotFootBankOut'))
        self.pivot_foot_heel = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotFootHeel'))
        self.pivot_foot_toes_fk = pymel.spaceLocator(name=nomenclature_rig.resolve('pivotToesFkRoll'))

        chain_footroll = [
            root_footRoll,
            self.pivot_foot_ankle,
            self.pivot_foot_inn,
            self.pivot_foot_out,
            self.pivot_foot_back,
            self.pivot_foot_heel,
            self.pivot_foot_front,
            self.pivot_toes_ankle,
            self.pivot_toes_heel
        ]
        libRigging.create_hyerarchy(chain_footroll)
        chain_footroll[0].setParent(self.grp_rig)
        self.pivot_foot_toes_fk.setParent(self.pivot_foot_heel)

        self.pivot_foot_ankle.setTranslation(pos_pivot_ankle, space='world')
        self.pivot_foot_inn.setTranslation(pos_pivot_inn, space='world')
        self.pivot_foot_out.setTranslation(pos_pivot_out, space='world')
        self.pivot_foot_back.setTranslation(pos_pivot_back, space='world')
        self.pivot_foot_heel.setTranslation(pos_pivot_heel, space='world')
        self.pivot_foot_front.setTranslation(pos_pivot_front, space='world')
        self.pivot_toes_ankle.setTranslation(pos_pivot_ankle, space='world')
        self.pivot_foot_toes_fk.setTranslation(pos_pivot_ankle, space='world')
        self.pivot_toes_heel.setTranslation(pos_pivot_heel, space='world')

        # Create attributes
        attr_holder = self.ctrl_ik
        libAttr.addAttr_separator(attr_holder, 'footRoll', niceName='Foot Roll')
        attr_inn_roll_auto = libAttr.addAttr(attr_holder, longName='rollAuto', k=True)
        attr_inn_roll_auto_threshold = libAttr.addAttr(attr_holder, longName='rollAutoThreshold', k=True, defaultValue=25)
        attr_inn_bank = libAttr.addAttr(attr_holder, longName='bank', k=True)
        attr_inn_ankle_rotz   = libAttr.addAttr(attr_holder, longName=self.ANKLE_ROTZ_LONGNAME, niceName=self.ANKLE_ROTZ_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=-90, maxValue=90)
        attr_inn_back_rotx   = libAttr.addAttr(attr_holder, longName=self.BACK_ROTX_LONGNAME, niceName=self.BACK_ROTX_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=-90, maxValue=0)
        attr_inn_ankle_rotx  = libAttr.addAttr(attr_holder, longName=self.ANKLE_ROTX_LONGNAME, niceName=self.ANKLE_ROTX_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=90)
        attr_inn_front_rotx  = libAttr.addAttr(attr_holder, longName=self.FRONT_ROTX_LONGNAME, niceName=self.FRONT_ROTX_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=90)
        attr_inn_back_roty  = libAttr.addAttr(attr_holder, longName=self.BACK_ROTY_LONGNAME, niceName=self.BACK_ROTY_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=-90, maxValue=90)
        attr_inn_heel_roty  = libAttr.addAttr(attr_holder, longName=self.HEEL_ROTY_LONGNAME, niceName=self.HEEL_ROTY_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=-90, maxValue=90)
        attr_inn_toes_roty = libAttr.addAttr(attr_holder, longName=self.TOES_ROTY_LONGNAME, niceName=self.TOES_ROTY_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=-90, maxValue=90)
        attr_inn_front_roty = libAttr.addAttr(attr_holder, longName=self.FRONT_ROTY_LONGNAME, niceName=self.FRONT_ROTY_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=-90, maxValue=90)
        attr_inn_toes_fk_rotx = libAttr.addAttr(attr_holder, longName=self.TOESFK_ROTX_LONGNAME, niceName=self.TOESFK_ROTX_NICENAME, k=True, hasMinValue=True, hasMaxValue=True, minValue=-90, maxValue=90)

        attr_roll_auto_pos = libRigging.create_utility_node('condition', operation=2, firstTerm=attr_inn_roll_auto,
                                                            secondTerm=0,
                                                            colorIfTrueR=attr_inn_roll_auto,
                                                            colorIfFalseR=0.0).outColorR  # Greater

        attr_roll_auto_f = libRigging.create_utility_node('condition', operation=2,
                                                          firstTerm=attr_inn_roll_auto,
                                                          secondTerm=attr_inn_roll_auto_threshold,
                                                          colorIfFalseR=0,
                                                          colorIfTrueR=(
                                                              libRigging.create_utility_node('plusMinusAverage',
                                                                                             operation=2,
                                                                                             input1D=[
                                                                                                 attr_inn_roll_auto,
                                                                                                 attr_inn_roll_auto_threshold]).output1D)
                                                          ).outColorR  # Substract
        attr_roll_auto_b = libRigging.create_utility_node('condition', operation=2, firstTerm=attr_inn_roll_auto,
                                                          secondTerm=0.0,
                                                          colorIfTrueR=0, colorIfFalseR=attr_inn_roll_auto
                                                          ).outColorR  # Greater

        attr_roll_m = libRigging.create_utility_node('addDoubleLinear', input1=attr_roll_auto_pos,
                                                     input2=attr_inn_ankle_rotx).output
        attr_roll_f = libRigging.create_utility_node('addDoubleLinear', input1=attr_roll_auto_f,
                                                     input2=attr_inn_front_rotx).output
        attr_roll_b = libRigging.create_utility_node('addDoubleLinear', input1=attr_roll_auto_b,
                                                     input2=attr_inn_back_rotx).output

        attr_bank_inn = libRigging.create_utility_node('condition', operation=2,
                                                       firstTerm=attr_inn_bank, secondTerm=0,
                                                       colorIfTrueR=attr_inn_bank,
                                                       colorIfFalseR=0.0
                                                       ).outColorR  # Greater

        attr_bank_out = libRigging.create_utility_node('condition', operation=4,
                                                       firstTerm=attr_inn_bank, secondTerm=0,
                                                       colorIfTrueR=attr_inn_bank,
                                                       colorIfFalseR=0.0).outColorR  # Less

        pymel.connectAttr(attr_roll_m, self.pivot_toes_ankle.rotateX)
        pymel.connectAttr(attr_roll_f, self.pivot_foot_front.rotateX)
        pymel.connectAttr(attr_roll_b, self.pivot_foot_back.rotateX)
        pymel.connectAttr(attr_bank_inn, self.pivot_foot_inn.rotateZ)
        pymel.connectAttr(attr_bank_out, self.pivot_foot_out.rotateZ)
        pymel.connectAttr(attr_inn_heel_roty, self.pivot_foot_heel.rotateY)
        pymel.connectAttr(attr_inn_front_roty, self.pivot_foot_front.rotateY)
        pymel.connectAttr(attr_inn_back_roty, self.pivot_foot_back.rotateY)
        pymel.connectAttr(attr_inn_ankle_rotz, self.pivot_toes_heel.rotateZ)
        pymel.connectAttr(attr_inn_toes_roty, self.pivot_foot_ankle.rotateY)
        pymel.connectAttr(attr_inn_toes_fk_rotx, self.pivot_foot_toes_fk.rotateX)

        # Create ikHandles and parent them
        # Note that we are directly parenting them so the 'Preserve Child Transform' of the translate tool still work.
        if jnt_heel:
            ikHandle_foot, ikEffector_foot = pymel.ikHandle(startJoint=jnt_foot, endEffector=jnt_heel, solver='ikSCsolver')
        else:
            ikHandle_foot, ikEffector_foot = pymel.ikHandle(startJoint=jnt_foot, endEffector=jnt_toes, solver='ikSCsolver')
        ikHandle_foot.rename(nomenclature_rig.resolve('ikHandle', 'foot'))
        ikHandle_foot.setParent(self.grp_rig)
        ikHandle_foot.setParent(self.pivot_toes_heel)
        if jnt_heel:
            ikHandle_heel, ikEffector_foot = pymel.ikHandle(startJoint=jnt_heel, endEffector=jnt_toes, solver='ikSCsolver')
            ikHandle_heel.rename(nomenclature_rig.resolve('ikHandle', 'heel'))
            ikHandle_heel.setParent(self.grp_rig)
            ikHandle_heel.setParent(self.pivot_foot_front)
        ikHandle_toes, ikEffector_toes = pymel.ikHandle(startJoint=jnt_toes, endEffector=jnt_tip, solver='ikSCsolver')
        ikHandle_toes.rename(nomenclature_rig.resolve('ikHandle', 'toes'))
        ikHandle_toes.setParent(self.grp_rig)
        ikHandle_toes.setParent(self.pivot_foot_toes_fk)

        # Hack: Re-constraint foot ikhandle
        # todo: cleaner!
        pymel.parentConstraint(self.ctrl_ik, root_footRoll, maintainOffset=True)

        # Connect the footroll to the main ikHandle
        # Note that we also need to hijack the softik network.
        fn_can_delete = lambda x: isinstance(x, pymel.nodetypes.Constraint) and \
                                  not isinstance(x, pymel.nodetypes.PoleVectorConstraint)
        pymel.delete(filter(fn_can_delete, self._ik_handle_target.getChildren()))

        if jnt_heel:
            pymel.parentConstraint(self.pivot_toes_heel, self._ik_handle_target, maintainOffset=True)
        else:
            pymel.parentConstraint(self.pivot_toes_ankle, self._ik_handle_target, maintainOffset=True)


        '''
        # Constraint swivel to ctrl_ik
        pymel.parentConstraint(self.ctrl_ik, self.ctrl_swivel,
                               maintainOffset=True)  # TODO: Implement SpaceSwitch
        '''

        # Handle globalScale
        pymel.connectAttr(self.grp_rig.globalScale, root_footRoll.scaleX)
        pymel.connectAttr(self.grp_rig.globalScale, root_footRoll.scaleY)
        pymel.connectAttr(self.grp_rig.globalScale, root_footRoll.scaleZ)

    def unbuild(self):
        """
        Unbuild the system
        Remember footroll locations in relation with a safe matrix
        The reference matrix is the ankle, maybe we should zero out the y axis.
        :return: Nothing
        """
        tm_ref_inv = self._get_reference_plane().inverse()

        if self.pivot_foot_heel:
            self.pivot_foot_heel_pos = (self.pivot_foot_heel.getMatrix(worldSpace=True) * tm_ref_inv).translate
        if self.pivot_toes_heel:
            self.pivot_toes_heel_pos = (self.pivot_toes_heel.getMatrix(worldSpace=True) * tm_ref_inv).translate
        if self.pivot_toes_ankle:
            self.pivot_toes_ankle_pos = (self.pivot_toes_ankle.getMatrix(worldSpace=True) * tm_ref_inv).translate
        if self.pivot_foot_front:
            self.pivot_foot_front_pos = (self.pivot_foot_front.getMatrix(worldSpace=True) * tm_ref_inv).translate
        if self.pivot_foot_back:
            self.pivot_foot_back_pos = (self.pivot_foot_back.getMatrix(worldSpace=True) * tm_ref_inv).translate
        if self.pivot_foot_inn:
            self.pivot_foot_inn_pos = (self.pivot_foot_inn.getMatrix(worldSpace=True) * tm_ref_inv).translate
        if self.pivot_foot_out:
            self.pivot_foot_out_pos = (self.pivot_foot_out.getMatrix(worldSpace=True) * tm_ref_inv).translate

        super(LegIk, self).unbuild()

        self.pivot_foot_heel = None
        self.pivot_toes_heel = None
        self.pivot_toes_ankle = None
        self.pivot_foot_front = None
        self.pivot_foot_back = None
        self.pivot_foot_inn = None
        self.pivot_foot_out = None
        self.pivot_foot_toes_fk = None


class Leg(rigLimb.Limb):
    """
    Basic leg system which use the LegIk class implementation.
    """
    _CLASS_SYS_IK = LegIk

    def validate(self):
        """
        Allow the ui to know if the module is valid to be builded or not
        :return: True or False depending if it pass the building validation
        """
        super(Leg, self).validate()

        num_inputs = len(self.input)
        if num_inputs < 5 or num_inputs > 6:
            raise Exception("Expected between 5 to 6 joints, got {0}".format(num_inputs))

        return True


def register_plugin():
    return Leg
