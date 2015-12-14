from maya import cmds
import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigNode import RigNode
from classRigElement import RigElement
from omtk.libs import libPymel
import time

class CtrlRoot(RigCtrl):
    def __init__(self, *args, **kwargs):
        super(CtrlRoot, self).__init__(create_offset=False, *args, **kwargs)

    def __createNode__(self, *args, **kwargs):
        node = pymel.circle(*args, **kwargs)[0]
        make = node.getShape().create.inputs()[0]
        make.radius.set(10)
        make.normal.set((0,1,0))

        # Add a globalScale attribute to replace the sx, sy and sz.
        pymel.addAttr(node, longName='globalScale', k=True, defaultValue=1.0)
        pymel.connectAttr(node.globalScale, node.sx)
        pymel.connectAttr(node.globalScale, node.sy)
        pymel.connectAttr(node.globalScale, node.sz)
        node.s.set(lock=True, channelBox=False)

        return node

class RigRoot(RigElement):
    NAME_ROOT_JNT = 'jnts'
    NAME_ROOT_ANM = 'anm_root'

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

    def add_part(self, _part):
        #if not isinstance(_part, RigPart):
        #    logging.error("[RigRoot:AddPart] Invalid RigPart '{0}' provided".format(_part))
        self.children.append(_part)

    def prebuild(self):
        # Ensure we got a root joint
        # If needed, parent orphan joints to this one
        all_root_jnts = libPymel.ls_root_jnts()

        if not libPymel.is_valid_PyNode(self.grp_jnts):
            if cmds.objExists(self.NAME_ROOT_JNT):
                self.grp_jnts = pymel.PyNode(self.NAME_ROOT_JNT)
            else:
                self.grp_jnts = pymel.createNode('joint', name=self.NAME_ROOT_JNT)

        all_root_jnts.setParent(self.grp_jnts)

    def build(self, **kwargs):
        if self.is_built():
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
        # Create anm root
        all_anms = libPymel.ls_root_anms()
        if not isinstance(self.grp_anms, CtrlRoot):
            self.grp_anms = CtrlRoot()
        if not self.grp_anms.is_built():
            self.grp_anms.build()
        self.grp_anms.rename(self.NAME_ROOT_ANM)
        all_anms.setParent(self.grp_anms)

        # Create rig root
        all_rigs = libPymel.ls_root_rigs()
        if not isinstance(self.grp_rigs, RigNode):
            self.grp_rigs = RigNode()
        if not self.grp_rigs.is_built():
            self.grp_rigs.build()
        self.grp_rigs.rename('rigs')
        all_rigs.setParent(self.grp_rigs)

        # Ensure self.grp_jnts is constraint to self.grp_anms
        # We use parentConstraint instead of connections to let the animator change grp_anms parent.
        pymel.delete([child for child in self.grp_jnts.getChildren() if isinstance(child, pymel.nodetypes.Constraint)])
        pymel.parentConstraint(self.grp_anms, self.grp_jnts)

        # Create geo root
        all_geos = libPymel.ls_root_geos()
        if not isinstance(self.grp_geos, RigNode):
            self.grp_geos = RigNode()
        if not self.grp_geos.is_built():
            self.grp_geos.build()
        self.grp_geos.rename('geos')
        all_geos.setParent(self.grp_geos)

        # Setup displayLayers
        self.layer_anm = pymel.createDisplayLayer(name='layer_anm', number=1, empty=True)
        pymel.editDisplayLayerMembers(self.layer_anm, self.grp_anms, noRecurse=True)
        self.layer_anm.color.set(17)  # Yellow

        self.layer_rig = pymel.createDisplayLayer(name='layer_rig', number=1, empty=True)
        pymel.editDisplayLayerMembers(self.layer_rig, self.grp_rigs, noRecurse=True)
        pymel.editDisplayLayerMembers(self.layer_rig, self.grp_jnts, noRecurse=True)
        self.layer_rig.color.set(13)  # Red
        self.layer_rig.visibility.set(0)  # Hidden
        self.layer_rig.displayType.set(2)  # Frozen

        self.layer_geo = pymel.createDisplayLayer(name='layer_geo', number=1, empty=True)
        pymel.editDisplayLayerMembers(self.layer_geo, self.grp_geos, noRecurse=True)
        self.layer_geo.color.set(12)  # Green?
        self.layer_geo.displayType.set(2)  # Frozen

    def unbuild(self, **kwargs):
        # Unbuild all childrens
        for child in self.children:
            child.unbuild(**kwargs)

        # Delete anm_grp
        self.grp_anms.unbuild()

        # Delete the rig group if it isnt used anymore
        if libPymel.is_valid_PyNode(self.grp_rigs) and len(self.grp_rigs.getChildren()) == 0:
            pymel.delete(self.grp_rigs)
            self.grp_rigs = None

        # Delete the displayLayers
        if libPymel.is_valid_PyNode(self.layer_anm):
            pymel.delete(self.layer_anm)
            self.layer_anm = None
        if libPymel.is_valid_PyNode(self.layer_geo):
            pymel.delete(self.layer_geo)
            self.layer_geo = None
        if libPymel.is_valid_PyNode(self.layer_rig):
            pymel.delete(self.layer_rig)
            self.layer_rig = None

        super(RigRoot, self).unbuild(**kwargs)


