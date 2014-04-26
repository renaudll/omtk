import os
import functools
from maya import OpenMayaUI
import pymel.core as pymel

import classNameMap
import classRigNode
import classRigCtrl
import classRigElement
import classRigPart
import classRigRoot
import classPoint

import rigFK
import rigIK
import rigArm
import rigLeg
import classCurveDeformer


from omtk.libs import libSerialization

def _reload():
    reload(classNameMap)
    reload(classRigNode)
    reload(classRigCtrl)
    reload(classRigElement)
    reload(classRigPart)
    reload(classRigRoot)
    reload(classPoint)
    reload(classCurveDeformer)

    reload(rigFK)
    reload(rigIK)
    reload(rigArm)
    reload(rigLeg)

    reload(libSerialization)

def Create(*args, **kwargs):
    return classRigRoot.RigRoot(*args, **kwargs)

def BuildAll():
    networks = libSerialization.getNetworksByClass('RigRoot')
    for network in networks:
        rigroot = libSerialization.importFromNetwork(network)
        rigroot.Build()
        pymel.delete(network)
        libSerialization.exportToNetwork(rigroot)

def UnbuildAll():
    networks = libSerialization.getNetworksByClass('RigRoot')
    for network in networks:
        rigroot = libSerialization.importFromNetwork(network)
        rigroot.Unbuild()
        pymel.delete(network)
        pymel.select(libSerialization.exportToNetwork(rigroot))

'''
Usage example:
from pymel import core as pymel
from omtk.rigging import AutoRig

rig = AutoRig.Create()
rig.AddPart(AutoRig.Arm(pymel.ls('jnt_arm_l_*')))
rig.AddPart(AutoRig.Arm(pymel.ls('jnt_arm_r_*')))
rig.AddPart(AutoRig.FK(pymel.ls('jnt_spine')))
rig.AddPart(AutoRig.FK(pymel.ls('jnt_chest')))
rig.AddPart(AutoRig.FK(pymel.ls('jnt_neck')))
rig.AddPart(AutoRig.FK(pymel.ls('jnt_head')))
rig.Build()
'''

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
        self.m_rigs = [libSerialization.importFromNetwork(network) for network in networks]

    def updateUi(self):
        self.treeWidget.clear()
        for rig in self.m_rigs:
            qItem = self._rigRootToQTreeWidget(rig)
            self.treeWidget.addTopLevelItem(qItem)
            self.treeWidget.expandItem(qItem)

    #
    # Events
    #

    def _actionBuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if not rig.isBuilt():
                rig.Build()
            else:
                pymel.warning("Can't build {0}, already built.".format(rig))
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.exportToNetwork(rig)

    def _actionUnbuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.isBuilt():
                rig.Unbuild()
            else:
                pymel.warning("Can't unbuild {0}, already unbuilt.".format(rig))
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.exportToNetwork(rig)

    def _actionRebuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.isBuilt():
                rig.Unbuild()
            rig.Build()
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.exportToNetwork(rig)

    def _actionImport(self):
        print 'import'
        raise NotImplementedError

    def _actionExport(self):
        print 'export'
        raise NotImplementedError

    def _actionUpdate(self):
        self.updateData()
        self.updateUi()

    def _itemSelectionChanged(self):
        pymel.select([item.net for item in self.treeWidget.selectedItems()])

    def _actionAddPart(self, _cls):
        root = next(iter(self.m_rigs), None)
        if root is None: return
        part = _cls(_aInput=pymel.selected())
        root.append(part)
        libSerialization.exportToNetwork(part) # Export part and only part
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

def show():
    p = AutoRig()
    p.show()
