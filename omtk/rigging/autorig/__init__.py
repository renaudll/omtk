import functools
import pymel.core as pymel
import logging; log = logging.getLogger(__name__); log.setLevel(logging.DEBUG)

import classNameMap
import classRigNode
import classRigCtrl
import classRigElement
import classRigPart
import classRigRoot
import classPoint

import rigFK
import rigIK
import rigSplineIK
import rigArm
import rigLeg

from rigFK import FK
from rigIK import IK
from rigSplineIK import SplineIK
from rigArm import Arm
from rigLeg import Leg
from rigTwistbone import Twistbone

from omtk.libs import libSerialization, libPymel

def create(*args, **kwargs):
    return classRigRoot.RigRoot(*args, **kwargs)

def find():
    networks = libSerialization.getNetworksByClass('RigRoot')
    return [libSerialization.import_network(network) for network in networks]

def find_one(*args, **kwargs):
    return next(iter(find(*args, **kwargs)), None)

def build_all():
    networks = libSerialization.getNetworksByClass('RigRoot')
    for network in networks:
        rigroot = libSerialization.import_network(network)
        if rigroot.build():
            pymel.delete(network)
            libSerialization.export_network(rigroot)

def unbuild_all():
    networks = libSerialization.getNetworksByClass('RigRoot')
    for network in networks:
        rigroot = libSerialization.import_network(network)
        rigroot.unbuild()
        pymel.delete(network)
        # Write changes to scene
        network = libSerialization.export_network(rigroot)
        pymel.select(network)

def detect(*args, **kwargs):
    """
    Fully automatic routine that create rig elements by analysing the joints structure.
    This is only meant as a quick way to get started and is in no way production ready.
    It is recommended that the 't-pose' or 45 angle 't-pose' is respected on the character before running this routine.
    """
    jnts = pymel.ls(type='joint')

    # Validate the joints hyerarchy since it is mandatory to autorig.
    roots = []
    for jnt in jnts:
        root = jnt.root()
        if root and root not in roots:
            roots.append(root)

    if len(roots) > 1:
        log.error("There are more than one joint root in the scene. Please clean up.")
        return None

    root = next(iter(roots), None)
    if not root:
        log.error("Found no joint root.")
        return None

    # Get the rig heights and radius
    height = 0
    radius = 0
    for jnt in jnts:
        pos = jnt.getTranslation(space='world')

        pos_x = pos.x
        h = pos.y
        pos_z = pos.z

        r = pow(pow(pos_x, 2) + pow(pos_z, 2), 0.5)

        if h > height:
            height = h

        if r > radius:
            radius = r

    MINIMUM_HEIGHT=0.01
    if height < MINIMUM_HEIGHT:
        log.error("Skeletton height is too small. Expected more than {0}".format(MINIMUM_HEIGHT))
        return None

    MINIMUM_RADIUS = 0.01
    if radius < MINIMUM_RADIUS:
        log.error("Skeletton radius is too small. Expected more than {0}".format(MINIMUM_RADIUS))
        return None

    #
    # Configure Rig
    #
    rig = classRigRoot.RigRoot()

    def get_arms(jnts):
        chains = []
        for jnt in jnts:
            arm_jnts = get_arm(jnt)
            if arm_jnts:
                chains.append(arm_jnts)
        return chains

    # Detect hands?
    def get_arm(jnt):
        children = jnt.getChildren()
        # Hand have a minimum of three fingers
        if len(children) < 2:
            return False

        # At least two parents (upperarm and forearm)
        parent = jnt.getParent()
        pparent = parent.getParent() if isinstance(parent, pymel.PyNode) else None
        if not pparent or not parent:
            return False

        arm_jnts = [pparent, parent, jnt]
        log.debug("Found Arm using {0}".format(arm_jnts))
        return arm_jnts

    def get_legs(jnts):
        chains = []
        for jnt in jnts:
            leg_jnts = get_leg(jnt)
            if leg_jnts:
                chains.append(leg_jnts)
        return chains

    def get_leg(jnt):
        # A leg have 5 joints from with the first two point to the ground
        parents = []
        parent = jnt
        while parent:
            parent = parent.getParent()
            parents.append(parent)

        if len(parents) < 5:
            return False

        thigh = parents[3]
        calf = parents[2]
        foot = parents[1]
        toe = parents[0]

        # Validate thigh direction
        thigh_pos = thigh.getTranslation(space='world')
        calf_pos = calf.getTranslation(space='world')
        thigh_dir = (calf_pos - thigh_pos); thigh_dir.normalize()
        DIR_MINIMUM = -0.5
        if thigh_dir.y >= DIR_MINIMUM:
            return False

        # Validate calf direction
        foot_pos = foot.getTranslation(space='world')
        calf_dir = foot_pos - calf_pos; calf_dir.normalize()
        if calf_dir.y >= DIR_MINIMUM:
            return False

        #print jnt, parents[3], parents[2],
        leg_jnts = [thigh, calf, foot, toe, jnt]
        log.debug("Found Leg using {0}".format(leg_jnts))
        return leg_jnts

    '''
    def get_spines(jnts):
        chains = []
        for jnt in jnts:
            spine_jnts = get_spine(jnt)
            if spine_jnts:
                chains.append(spine_jnts)
        return chains
    '''

    log.debug("Detected rig layout:")
    log.debug("\tHeight: {0}".format(height))
    log.debug("\tRadius: {0}".format(radius))

    # Detect legs
    from rigLeg import Leg
    legs_jnts = get_legs(jnts)
    for leg_jnts in legs_jnts:
        for leg_jnt in leg_jnts:
            jnts.remove(leg_jnt)
        rig.append(Leg(leg_jnts))

    print len(jnts)

    # Detect arms
    from rigArm import Arm
    arms_jnts = get_arms(jnts)
    for arm_jnts in arms_jnts:
        for arm_jnt in arm_jnts:
            print arm_jnt
            jnts.remove(arm_jnt)
        rig.append(Arm(arm_jnts))

    print len(jnts)

    rig.build()

    libSerialization.export_network(rig)





#################

from omtk.libs.libQt import QtGui, getMayaWindow

import ui
class AutoRig(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        if parent is None: parent = getMayaWindow()
        super(AutoRig, self).__init__(parent)
        self.setupUi(self)

        self.actionBuild.triggered.connect(self._actionBuild)
        self.actionUnbuild.triggered.connect(self._actionUnbuild)
        self.actionRebuild.triggered.connect(self._actionRebuild)
        self.actionImport.triggered.connect(self._actionImport)
        self.actionExport.triggered.connect(self._actionExport)
        self.actionUpdate.triggered.connect(self._actionUpdate)
        self.actionAdd.triggered.connect(self._actionAdd)

        self.treeWidget.itemSelectionChanged.connect(self._itemSelectionChanged)
        self.treeWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self.updateData()
        self.updateUi()

    #
    # root property
    #
    @property
    def root(self):
        return self.__dict__['_root']
    @root.getter
    def root(self):
        if not '_root' in self.__dict__:
            self.__dict__['_root'] = create()
        return self.__dict__['_root']

    def _rigRootToQTreeWidget(self, _rig):
        qItem = QtGui.QTreeWidgetItem(0)
        if hasattr(_rig, '_network'):
            qItem.net = _rig._network
        else:
            pymel.warning("{0} have no _network attributes".format(_rig))
        qItem.rig = _rig
        qItem.setText(0, str(_rig))
        if isinstance(_rig, classRigElement.RigElement):
            for child in _rig:
                qSubItem = self._rigRootToQTreeWidget(child)
                qItem.addChild(qSubItem)
        return qItem

    def updateData(self):
        networks = libSerialization.getNetworksByClass('RigRoot')
        self.roots = [libSerialization.import_network(network) for network in networks]

    def updateUi(self):
        self.treeWidget.clear()
        for root in self.roots:
            qItem = self._rigRootToQTreeWidget(root)
            self.treeWidget.addTopLevelItem(qItem)
            self.treeWidget.expandItem(qItem)

    #
    # Events
    #

    def _actionBuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if not rig.isBuilt():
                rig.build()
            else:
                pymel.warning("Can't build {0}, already built.".format(rig))
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.export_network(rig)

    def _actionUnbuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.isBuilt():
                rig.unbuild()
            else:
                pymel.warning("Can't unbuild {0}, already unbuilt.".format(rig))
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.export_network(rig)

    def _actionRebuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.isBuilt():
                rig.unbuild()
            rig.build()
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.export_network(rig)

    def _actionImport(self):
        raise NotImplementedError

    def _actionExport(self):
        raise NotImplementedError

    def _actionUpdate(self):
        self.updateData()
        self.updateUi()

    def _itemSelectionChanged(self):
        pymel.select([item.net for item in self.treeWidget.selectedItems() if hasattr(item, 'net')])

    def _actionAddPart(self, _cls):
        part = _cls(_input=pymel.selected())
        self.root.append(part)
        net = libSerialization.export_network(self.root) # Export part and only part
        pymel.select(net)
        self.updateData()
        self.updateUi()

    # TODO: Move to lib
    def _getSubClasses(self, _cls):
        for subcls in _cls.__subclasses__():
            yield subcls
            for subsubcls in self._getSubClasses(subcls):
                yield subsubcls

    def _actionAdd(self):
        menu     = QtGui.QMenu()
        for cls in self._getSubClasses(classRigPart.RigPart):
            action = menu.addAction(cls.__name__)
            action.triggered.connect(functools.partial(self._actionAddPart, cls))

        menu.exec_(QtGui.QCursor.pos())             

gui = None
def show():
    global gui
    gui = AutoRig()
    gui.show()

#
# Unit testing
#
import unittest
import os, glob
from maya import cmds
class TestAutoRig(unittest.TestCase):
    def test_RigCtrl(self):
        from classRigCtrl import RigCtrl
        from omtk.libs import libSerialization
        log.info("test_RigCtrl")
        foo = RigCtrl()
        foo.build()
        pymel.setKeyframe(foo.node)
        foo.unbuild()

        network = libSerialization.export_network(foo)
        pymel.select(network)
        foo.build()

    def test_buildAndUnbuildExamples(self):
        log.info("test_buildAndUnbuildExamples")
        import omtk
        directory = os.path.join(os.path.dirname(omtk.__file__), 'examples')
        files = glob.glob(os.path.join(directory, '*.mb')) + glob.glob(os.path.join(directory, '*.ma'))
        self.assertTrue(len(files)) # Ensure we got files to test
        for path in files:
            log.info('Testing {0}'.format(path))
            self.assertTrue(True)
            cmds.file(path, open=True, force=True)
            # Find rig
            rig = find_one()
            log.info('Building...')
            rig.build()
            log.info('Unbuilding...')
            rig.unbuild()
            # Ensure we're not loosing data
            log.info('Re-Building...')
            rig.build()
            log.info('Re-Unbuilding...')
            rig.unbuild()

    def runTest(self):
        pass

def test(**kwargs):
    case = TestAutoRig()
    case.test_RigCtrl()
    case.test_buildAndUnbuildExamples()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestAutoRig)
    #unittest.TextTestRunner(**kwargs).run(suite)


# Get the largest distance from the floor and