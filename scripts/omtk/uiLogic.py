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
    for i in reversed(range(num_child)):
        qt_sub_item = qt_item.child(i)
        yield qt_sub_item
        for x in get_all_QTreeWidgetItem(widget, qt_sub_item):
            yield x

class AutoRig(QtGui.QMainWindow, ui.Ui_MainWindow):
    #http://forums.cgsociety.org/archive/index.php?t-1096914.html
    #Use the intern maya resssources icon
    _STYLE_SHEET = \
    """
           QTreeView::item
           {
              background-color: rgb(45,45,45);
           }

          QTreeView::item::selected
          {
             background-color: highlight;
             color: rgb(40,40,40);
          }

          QTreeView::branch
          {
               selection-background-color: highlight;
               background-color: rgb(45,45,45);
           }

            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings
            {
                    border-image: none;
                    image: url(:/openObject.png);
            }

            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings
            {
                    border-image: none;
                    image: url(:/closeObject.png);
            }

            QTreeView::indicator:checked
            {
                image: url(:/checkboxOn.png);
            }

            QTreeView::indicator:unchecked
            {
                image: url(:/checkboxOff.png);
            }
       """

    def __init__(self, parent=None):
        if parent is None: parent = getMayaWindow()
        super(AutoRig, self).__init__(parent)
        self.setupUi(self)

        self.checkBox_hideAssigned.setCheckState(QtCore.Qt.Checked)
        self.actionAdd.setEnabled(False)

        self.actionBuild.triggered.connect(self.on_build)
        self.actionUnbuild.triggered.connect(self.on_unbuild)
        self.actionRebuild.triggered.connect(self.on_rebuild)
        self.actionImport.triggered.connect(self.on_import)
        self.actionExport.triggered.connect(self.on_export)
        self.actionUpdate.triggered.connect(self.on_update)
        self.actionAdd.triggered.connect(self.on_btn_add_pressed)
        self.actionMirrorJntsLToR.triggered.connect(self.on_mirror_jnts_LtoR)
        self.actionMirrorJntsRToL.triggered.connect(self.on_mirror_jnts_RtoL)


        self.treeWidget.itemSelectionChanged.connect(self.on_module_selection_changed)
        self.treeWidget.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.treeWidget.itemChanged.connect(self.on_module_changed)

        self.treeWidget_jnts.setStyleSheet(self._STYLE_SHEET)
        self.treeWidget.setStyleSheet(self._STYLE_SHEET)

        self.treeWidget_jnts.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidget_jnts.itemSelectionChanged.connect(self.on_influence_selection_changed)
        self.lineEdit_search_jnt.textChanged.connect(self.on_query_changed)
        self.checkBox_hideAssigned.stateChanged.connect(self.on_query_changed)

        #Right click menu
        self.treeWidget_jnts.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.treeWidget_jnts, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.on_btn_add_pressed)

        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.treeWidget, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.on_context_menu_request)

        self.refresh()

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

        # self.callbacks_nodes = OpenMaya.MDGMessage.addNodeRemovedCallback(
        #     self.callback_network_deleted, 'network'  # TODO: Restrict to network nodes
        # )


    def remove_callbacks(self):
        for callback_id in self.callbacks_events:
            OpenMaya.MEventMessage.removeCallback(callback_id)
        self.callbacks_events = []

        for callback_id in self.callbacks_scene:
            OpenMaya.MSceneMessage.removeCallback(callback_id)
        self.callbacks_scene = []

        # temporary disabled for performance issues
        # if self.callbacks_nodes is not None:
        #     OpenMaya.MMessage.removeCallback(self.callbacks_nodes)
        #     self.callbacks_nodes = None

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
    #@property
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
            qItem.setIcon(0, QtGui.QIcon(":/out_character.png"))
            for child in module:
                qSubItem = self._rigRootToQTreeWidget(child)
                qSubItem.setIcon(0, QtGui.QIcon(":/out_objectSet.png"))
                for input in child.input:
                    qInputItem = QtGui.QTreeWidgetItem(0)
                    qInputItem.setText(0, input.name())
                    qInputItem.setIcon(0, QtGui.QIcon(":/pickJointObj.png"))
                    qSubItem.addChild(qInputItem)
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

        textBrush = QtGui.QBrush(QtCore.Qt.white)

        if self._is_influence(obj):
            qItem = QtGui.QTreeWidgetItem(0)
            qItem.obj = obj
            qItem.networks = networks
            qItem.setText(0, obj_name)
            qItem.setForeground(0, textBrush)
            qItem.setIcon(0, QtGui.QIcon(":/pickJointObj.png"))
            qItem.setCheckState(0, QtCore.Qt.Checked if networks else QtCore.Qt.Unchecked)
            flags = qItem.flags()
            if flags & QtCore.Qt.ItemIsUserCheckable:
                flags ^= QtCore.Qt.ItemIsUserCheckable #Toggle checkable flag
            qItem.setFlags(flags)
            qt_parent.addChild(qItem)
            qt_parent = qItem

        for sub_jnt in obj.getChildren():
            if isinstance(sub_jnt, pymel.nodetypes.Transform):
                qSubItem = self._fill_widget_influences_recursive(qt_parent, sub_jnt)

    def refresh(self):
        self.update_modules_data()
        self.update_ui_modules()
        self.update_ui_jnts_visibility()

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
        #print obj_name

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

        unselectableBrush = QtGui.QBrush(QtCore.Qt.darkGray)
        selectableBrush = QtGui.QBrush(QtCore.Qt.white)
        for qt_item in get_all_QTreeWidgetItem(self.treeWidget_jnts):
            can_show = self.can_show_QTreeWidgetItem(qt_item, query_regex)
            qt_item.setHidden(not can_show)
            if can_show:
                qt_item.setForeground(0, selectableBrush)
                flags = qt_item.flags()
                if not flags & QtCore.Qt.ItemIsSelectable: #Make selectable
                    flags ^= QtCore.Qt.ItemIsSelectable
                    qt_item.setFlags(flags)
                self._show_parent_recursive(qt_item.parent())
            else:
                qt_item.setForeground(0, unselectableBrush)
                flags = qt_item.flags()
                if flags & QtCore.Qt.ItemIsSelectable: #Make unselectable
                    flags ^= QtCore.Qt.ItemIsSelectable
                    qt_item.setFlags(flags)

    def _show_parent_recursive(self, qt_parent_item):
        if qt_parent_item is not None:
            if qt_parent_item.isHidden:
                qt_parent_item.setHidden(False)
            self._show_parent_recursive(qt_parent_item.parent())

    def on_query_changed(self, *args, **kwargs):
        self.update_ui_jnts_visibility()


    #
    # Events
    #

    def on_build(self):
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

    def on_unbuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.is_built():
                rig.unbuild()
            else:
                pymel.warning("Can't unbuild {0}, already unbuilt.".format(rig))
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.export_network(rig)
        self.update_ui_modules()

    def on_rebuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.is_built():
                rig.unbuild()
            rig.build()
            #pymel.delete(rig._network) # TODO: AUTOMATIC UPDATE
            libSerialization.export_network(rig)

    def on_import(self):
        path, _ = QtGui.QFileDialog.getOpenFileName(caption="File Save (.json)", filter="JSON (*.json)")
        if not path:
            return

        new_rigs = libSerialization.import_json_file(path)
        if not new_rigs:
            return

        # Remove previous rigs
        all_rigs = core.find()
        for rig in all_rigs:
            if rig._network.exists():
                pymel.delete(rig._network)

        for rig in filter(None, new_rigs):
            libSerialization.export_network(rig)

        self.on_update()

    def on_export(self):
        all_rigs = core.find()

        path, _ = QtGui.QFileDialog.getSaveFileName(caption="File Save (.json)", filter="JSON (*.json)")
        if path:
            libSerialization.export_json_file(all_rigs, path)

    def on_update(self):
        self.refresh();

    def on_module_selection_changed(self):
        pymel.select([item.net for item in self.treeWidget.selectedItems() if hasattr(item, 'net')])

    def on_influence_selection_changed(self):
        pymel.select([item.obj for item in self.treeWidget_jnts.selectedItems() if item.obj.exists()])
        if self.treeWidget_jnts.selectedItems():
            self.actionAdd.setEnabled(True)
        else:
            self.actionAdd.setEnabled(False)

    def on_module_changed(self, item):
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

    def on_remove(self):
        for item in self.treeWidget.selectedItems():
            module = item.rig
            net = item.net if hasattr(item, "net") else None
            if module.is_built():
                module.unbuild()
            if net:
                pymel.delete(net)
        #Clear root cached property to make sure it's still valid
        if hasattr(self, "_cache"):
            del self._cache
        self.refresh()

    def on_context_menu_request(self):
        if self.treeWidget.selectedItems():
            menu = QtGui.QMenu()
            actionBuild = menu.addAction("Build")
            actionBuild.triggered.connect(functools.partial(self.on_build))
            actionUnbuild = menu.addAction("Unbuild")
            actionUnbuild.triggered.connect(functools.partial(self.on_unbuild))
            actionRebuild = menu.addAction("Rebuild")
            actionRebuild.triggered.connect(functools.partial(self.on_rebuild))
            menu.addSeparator()
            actionRemove = menu.addAction("Remove")
            actionRemove.triggered.connect(functools.partial(self.on_remove))

            menu.exec_(QtGui.QCursor.pos())

    def on_btn_add_pressed(self):
        if self.treeWidget_jnts.selectedItems():
            menu = QtGui.QMenu()
            for cls in libPython.get_sub_classes(classModule.Module):
                cls_name = cls.__name__
                action = menu.addAction(cls_name)
                action.triggered.connect(functools.partial(self.action_add_part, cls_name))

            menu.exec_(QtGui.QCursor.pos())

    def action_add_part(self, cls_name):
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
        self.refresh()

    def on_mirror_jnts_LtoR(self):
        libSkeleton.mirror_jnts_l_to_r()

    def on_mirror_jnts_RtoL(self):
        libSkeleton.mirror_jnts_r_to_l()

gui = None
def show():
    global gui

    gui = AutoRig()

    # Create a frame geo to easilly move it from the center
    pFrame = gui.frameGeometry()
    pScreen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
    ptCenter = QtGui.QApplication.desktop().screenGeometry(pScreen).center()
    pFrame.moveCenter(ptCenter)
    gui.move(pFrame.topLeft())

    gui.show()
