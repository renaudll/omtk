import logging

import pymel.core as pymel
from omtk import constants
from omtk.core.classComponent import ComponentScripted
from omtk.core.classDagBuilder import DagBuilder

log = logging.getLogger('omtk')


class ComponentTwistExtractor(ComponentScripted):
    need_grp_dag = True
    component_name = 'TwistExtractor'
    component_id = constants.BuiltInComponentIds.TwistExtractor

    ATTR_NAME_INN_PARENT_TM = 'hook'
    ATTR_NAME_INN_PREV_TM = 'inn1'
    ATTR_NAME_INN_PREV_TM_BIND = 'bind1'
    ATTR_NAME_INN_MID_TM = 'inn2'
    ATTR_NAME_INN_MID_TM_BIND = 'bind2'
    ATTR_NAME_INN_NEXT_TM = 'inn3'
    ATTR_NAME_INN_NEXT_TM_BIND = 'bind3'
    ATTR_NAME_OUT_TWIST = 'out'

    def __init__(self, **kwargs):
        super(ComponentTwistExtractor, self).__init__(**kwargs)

    def _create_io(self):
        self._attr_inn_chain_1 = self.add_input_attr(self.ATTR_NAME_INN_PREV_TM, dt='matrix')
        self._attr_inn_chain_2 = self.add_input_attr(self.ATTR_NAME_INN_MID_TM, dt='matrix')
        self._attr_inn_chain_3 = self.add_input_attr(self.ATTR_NAME_INN_NEXT_TM, dt='matrix')
        self._attr_inn_chain_1_bind = self.add_input_attr(self.ATTR_NAME_INN_PREV_TM_BIND, dt='matrix')
        self._attr_inn_chain_2_bind = self.add_input_attr(self.ATTR_NAME_INN_MID_TM_BIND, dt='matrix')
        self._attr_inn_chain_3_bind = self.add_input_attr(self.ATTR_NAME_INN_NEXT_TM_BIND, dt='matrix')
        self._attr_out_twist = self.add_output_attr(self.ATTR_NAME_OUT_TWIST)

    def build(self):
        super(ComponentTwistExtractor, self).build()
        self._create_io()

        builder = DagBuilder()

        # Create a 2-joint IK setup with zero pole vector
        # This is a hack to have quaternion behavior in Maya.
        # This 
        pymel.select(clear=True)
        start = pymel.joint()
        end = pymel.joint()
        end.setTranslation([1, 0, 0])
        pymel.makeIdentity((start, end), apply=True, r=True)

        ikHandle, ikEffector = pymel.ikHandle(
            solver='ikRPsolver',
            startJoint=start,
            endEffector=end
        )
        ikHandle.poleVectorX.set(0)
        ikHandle.poleVectorY.set(0)
        ikHandle.poleVectorZ.set(0)

        # Create the extract node for the twist information
        self.twist_extractor = pymel.createNode('transform')
        self.twist_extractor.setMatrix(start.getMatrix(worldSpace=True), worldSpace=True)
        self.twist_extractor.setParent(start)
        aimConstraint = pymel.aimConstraint(end, self.twist_extractor, worldUpType=2)
        print aimConstraint
        # , worldUpObject=self._attr_inn_chain_2

        # Rename
        start.rename('jntStart')
        end.rename('jntEnd')
        ikHandle.rename('ikHandle')
        ikEffector.rename('ikEffector')
        self.twist_extractor.rename('twistExtractor')

        # Set Hierarchy
        start.setParent(self.grp_dag)
        ikHandle.setParent(self.grp_dag)

        # Extract the twist
        pymel.connectAttr(self.twist_extractor.rotateX, self._attr_out_twist)


def register_plugin():
    return ComponentTwistExtractor
