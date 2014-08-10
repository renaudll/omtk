import functools
import pymel.core as pymel
import logging; log = logging.getLogger(__name__); log.setLevel(logging.INFO)

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

from omtk.libs import libSerialization

def create(*args, **kwargs):
    return classRigRoot.RigRoot(*args, **kwargs)

def find():
    networks = libSerialization.getNetworksByClass('RigRoot')
    return [libSerialization.importFromNetwork(network) for network in networks]

def find_one(*args, **kwargs):
    return next(iter(find(*args, **kwargs)), None)

def build_all():
    networks = libSerialization.getNetworksByClass('RigRoot')
    for network in networks:
        rigroot = libSerialization.importFromNetwork(network)
        if rigroot.build():
            pymel.delete(network)
            libSerialization.exportToNetwork(rigroot)

def unbuild_all():
    networks = libSerialization.getNetworksByClass('RigRoot')
    for network in networks:
        rigroot = libSerialization.importFromNetwork(network)
        rigroot.unbuild()
        pymel.delete(network)
        # Write changes to scene
        network = libSerialization.exportToNetwork(rigroot)
        pymel.select(network)


#################

from omtk.libs.libQt import QtGui, getMayaWindow

import ui
class AutoRig(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=getMayaWindow()):
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
        self.roots = [libSerialization.importFromNetwork(network) for network in networks]

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
            libSerialization.exportToNetwork(rig)

    def _actionUnbuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.isBuilt():
                rig.unbuild()
            else:
                pymel.warning("Can't unbuild {0}, already unbuilt.".format(rig))
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.exportToNetwork(rig)

    def _actionRebuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.isBuilt():
                rig.unbuild()
            rig.build()
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.exportToNetwork(rig)

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
        net = libSerialization.exportToNetwork(self.root) # Export part and only part
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

    def runTest(self):
        pass

def test(**kwargs):
    case = TestAutoRig()
    case.test_buildAndUnbuildExamples()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestAutoRig)
    #unittest.TextTestRunner(**kwargs).run(suite)


