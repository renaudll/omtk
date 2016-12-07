import logging
import pymel.core as pymel
from omtk.core.classModule import Module
from omtk.libs import libPython
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.modules import rigFK
from omtk.modules import rigFKAdditive


'''
class Finger(Module):
    """
    Finger rig are similare to the AdditiveFK setup but can have an additional joint for the metacarpal.
    """

    @libPython.cached_property()
    def phalanges(self):
        if len(self.input) == 5:
            return self.input[1:-1]
        else:
            return self.input[:-1]

    @libPython.cached_property()
    def metacarpal(self):
        if len(self.input) == 5:
            return self.input[0]

    def build(self, *args, **kwargs):
        # Ensure we got a valid number of inputs.
        num_inputs = len(self.input)
        if num_inputs > 5:
            raise Exception("Unsupported chain length. Expected 4 or less, got {1}".format(num_inputs))

        super(Finger, self).build(create_grp_rig=False, *args, **kwargs)

        # Rig phalanges
        self.sysPhalanges = rigFK.AdditiveFK(self.phalanges)
        self.sysPhalanges.build(parent=False)
        self.sysPhalanges.grp_anm.setParent(self.grp_anm)

        # Rig metacarpal if necessary
        if self.metacarpal:
            pymel.aimConstraint(self.sysPhalanges.additive_ctrls[0], self.metacarpal, worldUpType=2, worldUpObject=self.parent)

        pymel.parentConstraint(self.parent, self.grp_anm, maintainOffset=True)
'''

class Hand(Module):
    """
    Multiple FK setup customized for hand rigging. Include metacarpal controls.
    """
    def __init__(self, *args, **kwargs):
        super(Hand, self).__init__(*args, **kwargs)
        self.sysFingers = []
        self.metacarpals = []
        self.fk_sys_metacarpals = []

    @libPython.cached_property()
    def chains(self):
        """
        Sort the finger chains by their relative position to the hand. This give consistent order.
        :return: The chains sorted by their position relative to the hand.
        """
        # TODO: Implement 'super' behavior in property
        chains = libPymel.get_chains_from_objs(self.input)

        #TODO : Do we want to check the distance in the world or related to the parent ?
        def sort_chain(chain):
            local_tm = chain.end.getMatrix(worldSpace=True)
            return local_tm.translate.z

        #Sorted by distance, but doesn't detect positive/negative value
        sorted_chain = sorted(chains, key=sort_chain)

        return sorted_chain

    def validate(self):
        super(Hand, self).validate()

        # Skip unsupported chain length
        for chain in self.chains:
            chain_length = len(chain)
            if chain_length > 5:
                raise Exception("Unsupported chain length for {0}. Expected 4 or less, got {1}".format(
                    chain, chain_length
                ))

    def build(self, *args, **kwargs):
        super(Hand, self).build(parent=False, *args, **kwargs)

        # Resolve fingers and metacarpals
        #jnts_metacarpals = []
        #metacarpals_sys = []

        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        # Resolve how many fingers we want.
        # Note that a finger don't necessarily have a metacarpal.
        # To properly preserve the mapping between the finger and the metacarpal, we
        # ensure that self.fk_sys_metacarpals have the same numbers of elements than self.sysFingers.
        num_fingers = len(self.chains)
        libPython.resize_list(self.sysFingers, num_fingers)
        libPython.resize_list(self.fk_sys_metacarpals, num_fingers)

        # Resolve the influences for each fingers.
        # This compute a two-sized tuple that contain the influences for the metacarpal and the phalanges influences.
        finger_entries = []
        for chain in self.chains:
            chain_length = len(chain)

            # Resolve phalanges and metacarpal from chain
            if chain_length == 5:
                jnts_metacarpal = [chain[0]]
                jnts_phalanges = chain[1:-1]
            else:
                jnts_metacarpal = None
                jnts_phalanges = chain[:-1]

            finger_entries.append((jnts_metacarpal, jnts_phalanges))

        # Initialize modules
        for i, finger_entry in enumerate(finger_entries):
            jnts_metacarpal, jnts_phalanges = finger_entry

            # Init metacarpal module
            if jnts_metacarpal is None:
                self.fk_sys_metacarpals[i] = None
            else:
                sys_metacarpal = self.fk_sys_metacarpals[i]
                sys_metacarpal = self.init_module(rigFK.FK, sys_metacarpal, inputs=jnts_metacarpal)
                sys_metacarpal._NAME_CTRL_MERGE = False  # Ensure we'll always use the input name.
                self.fk_sys_metacarpals[i] = sys_metacarpal

            # Init finger module
            self.sysFingers[i] = self.init_module(
                rigFKAdditive.AdditiveFK,
                self.sysFingers[i],
                inputs=jnts_phalanges
            )

        # Build modules
        for sys_metacarpal, sys_finger in zip(self.fk_sys_metacarpals, self.sysFingers):
            if sys_metacarpal:
                sys_metacarpal.create_spaceswitch = False
                sys_metacarpal.build()
                sys_metacarpal.grp_anm.setParent(self.grp_anm)

            sys_finger.create_spaceswitch = False
            sys_finger.build()
            if sys_metacarpal:
                sys_finger.grp_anm.setParent(sys_metacarpal.ctrls[0])
            else:
                sys_finger.grp_anm.setParent(self.grp_anm)

        # Rig the 'cup' setup
        sys_metacarpals = filter(None, self.fk_sys_metacarpals)
        if len(sys_metacarpals) >= 2:
            pos_inn = sys_metacarpals[0].ctrls[0].getTranslation(space='world')
            pos_out = sys_metacarpals[-1].ctrls[0].getTranslation(space='world')
            pos_mid = ((pos_out - pos_inn) / 2.0) + pos_inn

            # Resolve the metacarpal plane orientation
            parent_tm = self.parent.getMatrix(worldSpace=True)
            x = pos_out - pos_inn
            x.normalize()
            y = pymel.datatypes.Vector(parent_tm.a10, parent_tm.a11, parent_tm.a12)
            z = x.cross(y) #Get the front vector
            z.normalize()
            y = x.cross(z) #Ensure the up vector is orthogonal
            y.normalize()
            ref_tm = pymel.datatypes.Matrix(
                    z.x, z.y, z.z, 0.0,
                    y.x, y.y, y.z, 0.0,
                    x.x, x.y, x.z, 0.0,
                    pos_mid.x, pos_mid.y, pos_mid.z, 1.0
            )
            rig_metacarpal_center = pymel.spaceLocator(name=nomenclature_rig.resolve('metacarpCenter'))
            rig_metacarpal_center.setMatrix(ref_tm)
            rig_metacarpal_center.setParent(self.grp_rig)
            pymel.parentConstraint(self.parent, rig_metacarpal_center, maintainOffset=True)

            # Create the 'cup' attribute
            attr_holder = self.grp_anm
            pymel.addAttr(attr_holder, longName='cup', keyable=True)
            attr_cup = attr_holder.attr('cup')


            for i, ctrl_metacarpal in enumerate(sys_metacarpals):
                width = pos_inn.distanceTo(pos_out)
                pos = ctrl_metacarpal.ctrls[0].getTranslation(space='world')
                ratio = (pos - pos_inn).length() / width

                grp_pivot_name = nomenclature_rig.resolve(ctrl_metacarpal.input[0].name() + '_pivot')
                grp_pivot = pymel.createNode('transform', name=grp_pivot_name)
                grp_pivot.setMatrix(ref_tm)
                grp_pivot.setParent(rig_metacarpal_center)

                multiplier = (ratio * 2.0) - 1.0
                attr_rotate_x = libRigging.create_utility_node('multiplyDivide',
                                                               input1X=attr_cup,
                                                               input2X=multiplier,
                                                               ).outputX
                pymel.connectAttr(attr_rotate_x, grp_pivot.rotateY)

                # jnt_phalange_inn = next(iter(jnt_metacarpal.getChildren()))
                # grp_pos = pymel.createNode('transform')
                # grp_pos.rename(nomenclature_rig.resolve(jnt_phalange_inn.name() + "_parentPos"))
                # grp_pos.setMatrix(jnt_phalange_inn.getMatrix(worldSpace=True))
                # grp_pos.setParent(grp_pivot)

                # Note that the cup system worked with a partial parentConstraint.
                # I've remove it since it was breaking things.
                # TODO: Make it work again.
                pymel.parentConstraint(grp_pivot, ctrl_metacarpal.ctrls[0].offset, maintainOffset=True)

                # HACK: Override the phalanges rig parent
                # sysFinger = metacarpals_sys[i]
                # pymel.disconnectAttr(sysFinger.grp_anm.translateX)
                # pymel.disconnectAttr(sysFinger.grp_anm.translateY)
                # pymel.disconnectAttr(sysFinger.grp_anm.translateZ)
                # pymel.parentConstraint(grp_pivot, sysFinger.grp_anm, maintainOffset=True, skipRotate=['x', 'y', 'z'])
                # pymel.pointConstraint(grp_pos, sysFinger.grp_anm, maintainOffset=True)

            #Connect Global scale
            pymel.connectAttr(self.grp_rig.globalScale, self.grp_rig.scaleX)
            pymel.connectAttr(self.grp_rig.globalScale, self.grp_rig.scaleY)
            pymel.connectAttr(self.grp_rig.globalScale, self.grp_rig.scaleZ)

        pymel.parentConstraint(self.parent, self.grp_anm, maintainOffset=True)

    def unbuild(self):
        for sysFinger in self.sysFingers:
            sysFinger.unbuild()

        for ctrl_meta in self.fk_sys_metacarpals:
            if ctrl_meta:  # might not exist!
                ctrl_meta.unbuild()

        super(Hand, self).unbuild()

    def iter_ctrls(self):
        for ctrl in super(Hand, self).iter_ctrls():
            yield ctrl
        if self.sysFingers:
            for sys in self.sysFingers:
                for ctrl in sys.iter_ctrls():
                    yield ctrl
        if self.fk_sys_metacarpals:
            for sys in self.fk_sys_metacarpals:
                if sys is not None:
                    for ctrl in sys.iter_ctrls():
                        yield ctrl

def register_plugin():
    return Hand
