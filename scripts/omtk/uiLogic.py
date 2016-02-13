import functools, re
import pymel.core as pymel
from libs.libQt import QtCore, QtGui, getMayaWindow
import libSerialization
import classModule
import classRig
from maya import OpenMaya
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libSkeleton
import core

import ui; reload(ui)


def get_all_QTreeWidgetItem(widget, qt_item=None):
    """
    Iterate through all items of a provided QTreeWidgetItem.
    :param widget: The QTreeWidgetItem to iterate through.
    :param qt_item: The starting point of the iteration. If nothing is provided the invisibleRootItem will be used.
    :return:
    """
    if qt_item is None:
        qt_item = widget.invisibleRootItem()

    num_child = qt_item.childCount()
    for i in range(num_child):
        qt_sub_item = qt_item.child(i)
        yield qt_sub_item
        for x in get_all_QTreeWidgetItem(widget, qt_sub_item):
            yield x

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
        self.actionMirrorJntsLToR.triggered.connect(self._actionMirrorJntsLToR)
        self.actionMirrorJntsRToL.triggered.connect(self._actionMirrorJntsRToL)


        self.treeWidget.itemSelectionChanged.connect(self._itemSelectionChanged)
        self.treeWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidget.itemChanged.connect(self._itemChanged)

        self.treeWidget_jnts.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidget_jnts.itemSelectionChanged.connect(self._jnt_iteSelectedChanged)
        self.lineEdit_search_jnt.textChanged.connect(self.on_query_changed)
        self.checkBox_hideAssigned.stateChanged.connect(self.on_query_changed)

        self.update_modules_data()
        self.update_ui_modules()

        self.callbacks_events = []
        self.callbacks_scene = []
        self.callbacks_nodes = None

        self.create_callbacks()

    def create_callbacks(self):
        self.remove_callbacks()
        self.callbacks_events = [
            OpenMaya.MEventMessage.addEventCallback("Undo", self.update_ui_modules),
            OpenMaya.MEventMessage.addEventCallback("Redo", self.update_ui_modules),
        ]
        self.callbacks_scene = [
            OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kSceneUpdate, self.update_ui_modules)
        ]

        self.callbacks_nodes = OpenMaya.MDGMessage.addNodeRemovedCallback(
            self.callback_network_deleted, 'network'  # TODO: Restrict to network nodes
        )


    def remove_callbacks(self):
        for callback_id in self.callbacks_events:
            OpenMaya.MEventMessage.removeCallback(callback_id)
        self.callbacks_events = []

        for callback_id in self.callbacks_scene:
            OpenMaya.MSceneMessage.removeCallback(callback_id)
        self.callbacks_scene = []

        # temporary disabled for performance issues
        if self.callbacks_nodes is not None:
            OpenMaya.MMessage.removeCallback(self.callbacks_nodes)
            self.callbacks_nodes = None

    def closeEvent(self, *args, **kwargs):
        self.remove_callbacks()
        super(AutoRig, self).closeEvent(*args, **kwargs)

    def callback_network_deleted(self, *args, **kwargs):
        print 'callback_network_deleted', args, kwargs
        self.update_modules_data()
        self.update_ui_modules()

    #
    # root property
    #
    #@property
    #def root(self):
    #    return self.__dict__['_root']
    @libPython.cached_property()
    def root(self):
        root = core.find_one()
        if root:
            return root
        return classRig.Rig()

    def _rigRootToQTreeWidget(self, module):
        qItem = QtGui.QTreeWidgetItem(0)
        if hasattr(module, '_network'):
            qItem.net = module._network
        else:
            pymel.warning("{0} have no _network attributes".format(module))
        qItem.rig = module
        qItem.setText(0, str(module))
        qItem.setCheckState(0, QtCore.Qt.Checked if module.is_built() else QtCore.Qt.Unchecked)
        if isinstance(module, classRig.Rig):
            for child in module:
                qSubItem = self._rigRootToQTreeWidget(child)
                qItem.addChild(qSubItem)
        return qItem

    def _is_influence(self, obj):
        """
        Supported influences are joints and nurbsSurface.
        :return:
        """
        return libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint) or libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)


    def _fill_widget_influences_recursive(self, qt_parent, obj):
        obj_name = obj.stripNamespace()

        fnFilter = lambda x: libSerialization.isNetworkInstanceOfClass(x, 'Module')
        networks = libSerialization.getConnectedNetworks(obj, key=fnFilter)

        if self._is_influence(obj):
            qItem = QtGui.QTreeWidgetItem(0)
            qItem.obj = obj
            qItem.networks = networks
            qItem.setText(0, obj_name)
            qItem.setCheckState(0, QtCore.Qt.Checked if networks else QtCore.Qt.Unchecked)
            qt_parent.addChild(qItem)
            qt_parent = qItem

        for sub_jnt in obj.getChildren():
            if isinstance(sub_jnt, pymel.nodetypes.Transform):
                qSubItem = self._fill_widget_influences_recursive(qt_parent, sub_jnt)

    def update_modules_data(self):
        self.roots = core.find()

    def update_ui_modules(self, *args, **kwargs):
        self.treeWidget.clear()
        for root in self.roots:
            qItem = self._rigRootToQTreeWidget(root)
            self.treeWidget.addTopLevelItem(qItem)
            self.treeWidget.expandItem(qItem)
        self.update_ui_jnts()  # TODO: Better update implementation!

    def update_ui_jnts(self, *args, **kwargs):
        # Resolve text query
        query_raw = self.lineEdit_search_jnt.text()
        query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        self.treeWidget_jnts.clear()
        all_jnt_roots = libPymel.ls_root(type='joint') + list(set([shape.getParent() for shape in pymel.ls(type='nurbsSurface')]))
        for jnt in all_jnt_roots:
            self._fill_widget_influences_recursive(self.treeWidget_jnts.invisibleRootItem(), jnt)

        self.treeWidget_jnts.expandAll()

    def can_show_QTreeWidgetItem(self, qItem, query_regex):
        obj = qItem.obj  # Retrieve monkey-patched data
        obj_name = obj.stripNamespace()
        print obj_name

        if not re.match(query_regex, obj_name, re.IGNORECASE):
            return False

        if self.checkBox_hideAssigned.isChecked():
            if qItem.networks:
                return False

        return True

    def update_ui_jnts_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.lineEdit_search_jnt.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        for qt_item in get_all_QTreeWidgetItem(self.treeWidget_jnts):
            can_show = self.can_show_QTreeWidgetItem(qt_item, query_regex)
            qt_item.setHidden(not can_show)


    def on_query_changed(self, *args, **kwargs):
        self.update_ui_jnts_visibility()


    #
    # Events
    #

    def _actionBuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if not rig.is_built():
                if isinstance(rig, classModule.Module):
                    rig.build(self.root)
                else:
                    rig.build()
            else:
                pymel.warning("Can't build {0}, already built.".format(rig))
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.export_network(rig)
        self.update_ui_modules()

    def _actionUnbuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.is_built():
                rig.unbuild()
            else:
                pymel.warning("Can't unbuild {0}, already unbuilt.".format(rig))
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.export_network(rig)
        self.update_ui_modules()

    def _actionRebuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.is_built():
                rig.unbuild()
            rig.build()
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.export_network(rig)

    def _actionImport(self):
        raise NotImplementedError

    def _actionExport(self):
        raise NotImplementedError

    def _actionUpdate(self):
        self.update_modules_data()
        self.update_ui_modules()

    def _itemSelectionChanged(self):
        pymel.select([item.net for item in self.treeWidget.selectedItems() if hasattr(item, 'net')])

    def _jnt_iteSelectedChanged(self):
        pymel.select([item.obj for item in self.treeWidget_jnts.selectedItems() if item.obj.exists()])

    def _itemChanged(self, item):
        # todo: handle exception
        module = item.rig
        module_is_built = module.is_built()
        new_state = item.checkState(0) == QtCore.Qt.Checked
        if new_state:
            if module_is_built:
                module.unbuild()
            if isinstance(module, classModule.Module):
                module.build(self.root)
            else:
                module.build()
        else:
            if module_is_built:
                module.unbuild()

        # If we just built a rig, we might want to update all checkboxes.
        if isinstance(module, classRig.Rig):
            self.update_ui_modules()

    def _actionAddPart(self, cls_name):
        #part = _cls(pymel.selected())
        self.root.add_module(cls_name, pymel.selected())
        try:
            pymel.delete(self.root._network)
        except AttributeError:
            pass
        net = libSerialization.export_network(self.root) # Export part and only part
        pymel.select(net)
        #Add manually the Rig to the root list instead of importing back all network
        #if not self.root in self.roots:
        #    self.roots.append(self.root)
        #self.updateData()
        self.update_modules_data()
        self.update_ui_modules()

    # TODO: Move to lib
    def _getSubClasses(self, _cls):
        # TODO: Move to libPython?
        for subcls in _cls.__subclasses__():
            yield subcls
            for subsubcls in self._getSubClasses(subcls):
                yield subsubcls

    def _actionAdd(self):
        menu = QtGui.QMenu()
        for cls in self._getSubClasses(classModule.Module):
            cls_name = cls.__name__
            action = menu.addAction(cls_name)
            action.triggered.connect(functools.partial(self._actionAddPart, cls_name))

        menu.exec_(QtGui.QCursor.pos())

    def _actionMirrorJntsLToR(self):
        libSkeleton.mirror_jnts_l_to_r()

    def _actionMirrorJntsRToL(self):
        libSkeleton.mirror_jnts_r_to_l()

gui = None
def show():
    global gui
    gui = AutoRig()
    gui.show()
