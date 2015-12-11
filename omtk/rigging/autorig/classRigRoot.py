import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigNode import RigNode
from classRigElement import RigElement
from omtk.libs import libRigging, libPymel
import logging
import time
import traceback

class CtrlRoot(RigCtrl):
    def __init__(self, *args, **kwargs):
        super(CtrlRoot, self).__init__(create_offset=False, *args, **kwargs)

    def build(self, *args, **kwargs):
        self.node = pymel.circle(*args, **kwargs)[0]
        oMake = self.node.getShape().create.inputs()[0]
        oMake.radius.set(10)
        oMake.normal.set((0,1,0))

        # Add a globalScale attribute to replace the sx, sy and sz.
        pymel.addAttr(self.node, longName='globalScale', k=True, defaultValue=1.0)
        pymel.connectAttr(self.node.globalScale, self.node.sx)
        pymel.connectAttr(self.node.globalScale, self.node.sy)
        pymel.connectAttr(self.node.globalScale, self.node.sz)
        self.node.s.set(lock=True, channelBox=False)

        return self.node

class RigRoot(RigElement):
    def __init__(self):
        self.children = []
        self.grp_anms = None
        self.grp_geos = None
        self.grp_jnts = None
        self.grp_rigs = None
        self.layer_anm = None
        self.layer_geo = None
        self.layer_rig = None

    def __str__(self):
        return '<rig {0}/>'.format('???')

    def AddPart(self, _part):
        #if not isinstance(_part, RigPart):
        #    logging.error("[RigRoot:AddPart] Invalid RigPart '{0}' provided".format(_part))
        self.children.append(_part)

    def prebuild(self):
        # Ensure we got a root joint
        # If needed, parent orphan joints to this one
        all_root_jnts = libPymel.ls_root_jnts()
        if not libPymel.is_valid_PyNode(self.grp_jnts):
            self.grp_jnts = pymel.createNode('joint', name='jnts')
        all_root_jnts.set_parent(self.grp_jnts)

    def build(self, **kwargs):
        if self.isBuilt():
            pymel.warning("Can't build {0} because it's already built!".format(self))
            return False

        sTime = time.time()

        self.prebuild()

        #try:
        for child in self.children:
            #try:
            child.build(**kwargs)
            #except Exception, e:
            #    logging.error("\n\nAUTORIG BUILD FAIL! (see log)\n")
            #    traceback.print_stack()
            #    logging.error(str(e))
            #    raise e
        self.postbuild()


        print ("[classRigRoot.Build] took {0} ms".format(time.time() - sTime))

        return True

    def postbuild(self):
        # Group everything
        all_anms = libPymel.ls_root_anms()
        if not isinstance(self.grp_anms, CtrlRoot):
            self.grp_anms = CtrlRoot()
        self.grp_anms.build()
        self.grp_anms.rename('anm_root')
        all_anms.set_parent(self.grp_anms)

        all_rigs = libPymel.ls_root_rigs()
        self.grp_rigs = RigNode(name='rigs', _create=True)
        all_rigs.set_parent(self.grp_rigs)

        # note: self.grp_jnts is now handled in prebuild
        #all_jnts = libPymel.ls_root_jnts()
        #self.grp_jnts = pymel.createNode('joint', name='jnts')
        #all_jnts.setParent(self.grp_jnts)

        # Ensure self.grp_jnts is constraint to self.grp_anms
        # We use parentConstraint instead of connections in the the animator change self.grp_anms parent
        pymel.delete([child for child in self.grp_jnts.getChildren() if isinstance(child, pymel.nodetypes.Constraint)])
        pymel.parentConstraint(self.grp_anms, self.grp_jnts)

        all_geos = libPymel.ls_root_geos()
        self.grp_geos = RigNode(name='geos', _create=True)
        all_geos.set_parent(self.grp_geos)

        # Setup displayLayers
        self.layer_anm = pymel.createDisplayLayer(name='layer_anm', number=1, empty=True)
        pymel.editDisplayLayerMembers(self.layer_anm, self.grp_anms, noRecurse=True)
        self.layer_anm.color.set(17) # Yellow

        self.layer_rig = pymel.createDisplayLayer(name='layer_rig', number=1, empty=True)
        pymel.editDisplayLayerMembers(self.layer_rig, self.grp_rigs, noRecurse=True)
        pymel.editDisplayLayerMembers(self.layer_rig, self.grp_jnts, noRecurse=True)
        self.layer_rig.color.set(13) # Red
        #oLayerRig.visibility.set(0) # Hidden
        self.layer_rig.displayType.set(2) # Frozen

        self.layer_geo = pymel.createDisplayLayer(name='layer_geo', number=1, empty=True)
        pymel.editDisplayLayerMembers(self.layer_geo, self.grp_geos, noRecurse=True)
        self.layer_geo.color.set(12) # Green?
        self.layer_geo.displayType.set(2) # Frozen

    def unbuild(self, **kwargs):
        for child in self.children:
            child.unbuild(**kwargs)

        # Delete the rig group if it isnt used anymore
        if libPymel.is_valid_PyNode(self.grp_rigs) and len(self.grp_rigs.getChildren()) == 0:
            pymel.delete(self.grp_rigs)
            self.grp_rigs = None

        super(RigRoot, self).unbuild(**kwargs)


