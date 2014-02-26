import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigNode import RigNode
from classRigElement import RigElement
from omtk.libs import libRigging
import logging
import time

class CtrlRoot(RigCtrl):
    def __init__(self, *args, **kwargs):
        super(CtrlRoot, self).__init__(_bOffset=False, *args, **kwargs)

    def __createNode__(self, *args, **kwargs):
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
    def __str__(self):
        return '<rig {0}/>'.format('???')

    def AddPart(self, _part):
        #if not isinstance(_part, RigPart):
        #    logging.error("[RigRoot:AddPart] Invalid RigPart '{0}' provided".format(_part))
        self.aChildrens.append(_part)

    def PreBuild(self):
        pass

    def Build(self, **kwargs):
        sTime = time.time()

        self.PreBuild()

        aObjsBefore = pymel.ls('*')
        try:
            for children in self.aChildrens:
                children.Build(**kwargs)
            self.PostBuild()
        except Exception, e:
            logging.error("AUTORIG BUILD FAIL! (see log)")
            #import traceback
            #traceback.print_stack()
            logging.error(str(e))
            aNewObjs = [o for o in pymel.ls('*') if o not in aObjsBefore]
            logging.info("Deleting {0} nodes...".format(len(aNewObjs)))
            pymel.delete(aNewObjs)
            pymel.error()

        print ("[classRigRoot.Build] took {0} ms".format(time.time() - sTime))

    def PostBuild(self):
        # Group everything
        aAllCtrls = filter(lambda x: x.getParent() is None, iter(pymel.ls('anm*')))
        oGrpAnms = CtrlRoot(name='anm_root', _create=True)
        for oCtrl in aAllCtrls: 
            oCtrl.setParent(oGrpAnms)

        aAllRigs = filter(lambda x: x.getParent() is None, iter(pymel.ls('rig*')))
        oGrpRigs = RigNode(name='rigs', _create=True)
        for oRig in aAllRigs:
            oRig.setParent(oGrpRigs)

        aAllJnts = filter(lambda x: x.getParent() is None, iter(pymel.ls('jnt*')))
        oGrpJnts = RigNode(name='jnts', _create=True)
        oGrpJnts.setParent(oGrpRigs)
        for oJnt in aAllJnts:
            oJnt.setParent(oGrpJnts)

        aAllGeos = filter(lambda x: x.getParent() is None, iter(pymel.ls('geo*')))
        oGrpGeos = RigNode(name='geos', _create=True)
        for oGeo in aAllGeos:
            oGeo.setParent(oGrpGeos)

        # Setup displayLayers
        oLayerAnm = pymel.createDisplayLayer(name='layer_anm', number=1, empty=True)
        pymel.editDisplayLayerMembers(oLayerAnm, oGrpAnms, noRecurse=True)
        oLayerAnm.color.set(17) # Yellow

        oLayerRig = pymel.createDisplayLayer(name='layer_rig', number=1, empty=True)
        pymel.editDisplayLayerMembers(oLayerRig, oGrpRigs, noRecurse=True)
        oLayerRig.color.set(13) # Red
        oLayerRig.visibility.set(0) # Hidden
        oLayerRig.displayType.set(2) # Frozen

        oLayerGeo = pymel.createDisplayLayer(name='layer_geo', number=1, empty=True)
        pymel.editDisplayLayerMembers(oLayerGeo, oGrpGeos, noRecurse=True)
        oLayerGeo.color.set(12) # Green?
        oLayerGeo.displayType.set(2) # Frozen

        # TODO: This need to be called individually on each rigpart, not just when unbuilding the whole rig.
        libRigging.RestoreCtrlShapes()

    def Unbuild(self, **kwargs):
        # TODO: This need to be called individually on each rigpart, not just when unbuilding the whole rig.
        libRigging.BackupCtrlShapes()

        for child in self.aChildrens:
            child.Unbuild(**kwargs)
