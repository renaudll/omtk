import logging
import pymel.core as pymel
from omtk.classModule import Module
from omtk.modules import rigFK
from omtk.libs import libPython
from omtk.libs import libPymel


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
    def __init__(self, *args, **kwargs):
        super(Hand, self).__init__(*args, **kwargs)
        self.sysFingers = []
        self.ctrls_metacarpals = []

    @libPython.cached_property()
    def chains(self):
        """
        Sort the finger chains by their relative position to the hand. This give consistent order.
        :return: The chains sorted by their position relative to the hand.
        """
        # TODO: Implement 'super' behavior in property
        parent_tm_inv = self.parent.getMatrix(worldSpace=True) if self.parent else pymel.datatypes.Matrix()
        chains = libPymel.get_chains_from_objs(self.input)

        def sort_chain(chain):
            local_tm = chain.end.getMatrix(worldSpace=True) * parent_tm_inv
            return local_tm.translate.z

        return sorted(chains, key=sort_chain)

    def build(self, rig, *args, **kwargs):
        super(Hand, self).build(rig, parent=False, *args, **kwargs)


        # Resolve fingers and metacarpals
        jnts_metacarpals = []

        for i, chain in enumerate(self.chains):
            chain_length = len(chain)

            # Skip unsupported chain length
            if chain_length > 5:
                logging.warning("Unsupported chain length for {0}. Expected 4 or less, got {1}".format(
                        chain, chain_length
                ))
                continue

            # Resolve phalanges and metacarpal from chain
                if chain_length == 5:
                jnt_metacarpal = chain[0]
                jnts_phalanges = chain[1:-1]
                jnts_metacarpals.append(jnt_metacarpal)
            else:
                jnt_metacarpal = None
                jnts_phalanges = chain[:-1]

            # Rig fingers
            sysFinger = rigFK.AdditiveFK(jnts_phalanges)
            self.sysFingers.append(sysFinger)
            sysFinger.build(rig, parent=False)
            sysFinger.grp_anm.setParent(self.grp_anm)

            # Rig metacarpals if necessary
            if jnt_metacarpal:
                pymel.aimConstraint(sysFinger.additive_ctrls[0], jnt_metacarpal, worldUpType=2,
                                    worldUpObject=self.parent)
            # pymel.parentConstraint(jnt_metacarp, metacarpal, maintainOffset=True)

        '''
        # Rig the 'cup' setup
        if jnts_metacarpals:
            pos_inn = jnts_metacarpals[0].getTranslation(space='world')
            pos_out = jnts_metacarpals[-1].getTranslation(space='world')
            pos_mid = (pos_out - pos_inn) / 2.0 + pos_inn

            # Resolve the metacarpal plane orientation
            parent_tm = self.parent.getMatrix(worldSpace=True)
            x = pos_out - pos_inn
            x.normalize()
            y = pymel.datatypes.Vector(parent_tm.a10, parent_tm.a11, parent_tm.a12)
            z = x.cross(y)
            ref_tm = pymel.datatypes.Matrix(
                    z.x, z.y, z.z, 0.0,
                    y.x, y.y, y.z, 0.0,
                    x.x, x.y, x.z, 0.0,
                    pos_mid.x, pos_mid.y, pos_mid.z, 1.0
            )
            rig_metacarpal_center = pymel.spaceLocator(name=self.name_rig.resolve('metacarpCenter'))
            rig_metacarpal_center.setMatrix(ref_tm)
            rig_metacarpal_center.setParent(self.grp_rig)
            pymel.parentConstraint(self.parent, rig_metacarpal_center, maintainOffset=True)

            # Create the 'cup' attribute
            attr_holder = self.grp_anm
            pymel.addAttr(attr_holder, longName='cup', keyable=True)
            attr_cup = attr_holder.attr('cup')


            for jnt_metacarpal in jnts_metacarpals:
                width = pos_inn.distanceTo(pos_out)
                pos = jnt_metacarpal.getTranslation(space='world')
                ratio = (pos - pos_inn).length() / width

                grp_pivot_name = self.name_anm.resolve('pivot')
                grp_pivot = pymel.createNode('transform', name=grp_pivot_name)
                grp_pivot.setMatrix(ref_tm)
                grp_pivot.setParent(rig_metacarpal_center)

                multiplier = (ratio * 2.0) - 1.0
                attr_rotate_x = libRigging.create_utility_node('multiplyDivide',
                                                               input1X=attr_cup,
                                                               input2X=multiplier,
                                                               ).outputX
                pymel.connectAttr(attr_rotate_x, grp_pivot.rotateX)

                jnt_phalange_inn = next(iter(jnt_metacarpal.getChildren()))
                grp_pos = pymel.createNode('transform')
                grp_pos.setMatrix(jnt_phalange_inn.getMatrix(worldSpace=True))
                grp_pos.setParent(grp_pivot)

                #pymel.parentConstraint(grp_pivot, jnt_metacarpal, maintainOffset=True, skipRotate=['x', 'y', 'z'])

                # HACK: Override the phalanges rig parent
                # pymel.disconnectAttr(sysFinger.grp_anm.translateX)
                # pymel.disconnectAttr(sysFinger.grp_anm.translateY)
                # pymel.disconnectAttr(sysFinger.grp_anm.translateZ)
                # #pymel.parentConstraint(grp_pivot, sysFinger.grp_anm, maintainOffset=True, skipRotate=['x', 'y', 'z'])
                # pymel.pointConstraint(grp_pos, sysFinger.grp_anm, maintainOffset=True)
            '''

        pymel.parentConstraint(self.parent, self.grp_anm, maintainOffset=True)

    def unbuild(self):
        for sysFinger in self.sysFingers:
            sysFinger.unbuild()

        super(Hand, self).unbuild()
