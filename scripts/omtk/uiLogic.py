import os
import functools
import re
import pymel.core as pymel
from maya import OpenMaya
import libSerialization
import core
import inspect
from omtk.core import classModule
from omtk.core import classRig
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libSkeleton
from omtk.libs.libQt import QtCore, QtGui, getMayaWindow

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
    #Use the intern maya ressources icon
    _STYLE_SHEET = \
    """

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

        self._is_modifying = False
        self.checkBox_hideAssigned.setCheckState(QtCore.Qt.Checked)
        self.actionCreateModule.setEnabled(False)

        self.import_networks()
        self.update_ui()

        self.actionBuild.triggered.connect(self.on_build)
        self.actionUnbuild.triggered.connect(self.on_unbuild)
        self.actionRebuild.triggered.connect(self.on_rebuild)
        self.actionImport.triggered.connect(self.on_import)
        self.actionExport.triggered.connect(self.on_export)
        self.actionUpdate.triggered.connect(self.on_update)
        self.actionCreateModule.triggered.connect(self.on_btn_add_pressed)
        self.actionMirrorJntsLToR.triggered.connect(self.on_mirror_jnts_LtoR)
        self.actionMirrorJntsRToL.triggered.connect(self.on_mirror_jnts_RtoL)
        self.actionAddNodeToModule.triggered.connect(self.on_addToModule)
        self.actionRemoveNodeFromModule.triggered.connect(self.on_removeFromModule)


        self.treeWidget.itemSelectionChanged.connect(self.on_module_selection_changed)
        self.treeWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidget.itemChanged.connect(self.on_module_changed)
        self.treeWidget.itemDoubleClicked.connect(self.on_module_double_clicked)
        self.treeWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.treeWidget.focusInEvent = self.focus_in_module
        self.treeWidget.setAutoFillBackground(True)
        self.treeWidget.setStyleSheet(self._STYLE_SHEET)

        self.treeWidget_jnts.setStyleSheet(self._STYLE_SHEET)
        self.treeWidget_jnts.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeWidget_jnts.itemSelectionChanged.connect(self.on_influence_selection_changed)

        self.lineEdit_search_jnt.textChanged.connect(self.on_query_changed)
        self.lineEdit_search_modules.textChanged.connect(self.on_module_query_changed)
        self.checkBox_hideAssigned.stateChanged.connect(self.on_query_changed)

        #Right click menu
        self.treeWidget_jnts.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.treeWidget_jnts, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.on_btn_add_pressed)

        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.treeWidget, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.on_context_menu_request)

        self.callbacks_events = []
        self.callbacks_scene = []
        self.callbacks_nodes = None

        self.create_callbacks()

    def create_callbacks(self):
        self.remove_callbacks()
        #Disable to prevent performance drop when CTRL-Z and the tool is open
        #TODO - Reactivate back when the tool will be stable ?
        self.callbacks_events = \
        [
            # OpenMaya.MEventMessage.addEventCallback("Undo", self.update_ui),
            # OpenMaya.MEventMessage.addEventCallback("Redo", self.update_ui)
        ]
        self.callbacks_scene = \
        [
            OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterOpen, self.on_update),
            OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterNew, self.on_update)
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

    #
    # Privates
    #
    def _rig_to_tree_widget(self, module):
        # HACK: bypass the stylecheet
        # see: http://forum.qt.io/topic/22219/item-view-stylesheet-bgcolor/12
        color_invalid= QtGui.QBrush(QtGui.QColor(255,45,45))
        color_valid = QtGui.QBrush(QtGui.QColor(45, 45, 45))

        style_sheet_invalid = """
        QTreeView::item
        {
           background-color: rgb(45,45,45);
        }"""

        qItem = QtGui.QTreeWidgetItem(0)
        if hasattr(module, '_network'):
            qItem.net = module._network
        else:
            pymel.warning("{0} have no _network attributes".format(module))
        qItem.rig = module
        qItem.setText(0,str(module))

        # Set QTreeWidgetItem red if the module fail validation
        try:
            module.validate()
            color = color_valid
        except Exception, e:
            pymel.warning("Module {0} failed validation: {1}".format(module, str(e)))
            color = color_invalid
        qItem.setBackground(0, color)

        qItem._name = qItem.text(0)
        qItem._checked = module.is_built()
        qItem.setFlags(qItem.flags() | QtCore.Qt.ItemIsEditable)
        qItem.setCheckState(0, QtCore.Qt.Checked if module.is_built() else QtCore.Qt.Unchecked)
        if isinstance(module, classRig.Rig):
            qItem.setIcon(0, QtGui.QIcon(":/out_character.png"))
            sorted_modules = sorted(module, key=lambda mod: mod.name)
            for child in sorted_modules:
                qSubItem = self._rig_to_tree_widget(child)
                qSubItem.setIcon(0, QtGui.QIcon(":/out_objectSet.png"))
                for input in child.input:
                    qInputItem = QtGui.QTreeWidgetItem(0)
                    qInputItem.setText(0, input.name())
                    self._set_icon_from_type(input, qInputItem)
                    qInputItem.setFlags(qItem.flags() & QtCore.Qt.ItemIsSelectable)
                    qSubItem.addChild(qInputItem)
                qItem.addChild(qSubItem)
        return qItem

    def _is_influence(self, obj):
        """
        Supported influences are joints and nurbsSurface.
        :return:
        """
        return libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint) or libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)

    def _set_icon_from_type(self, obj, qItem):
        if isinstance(obj, pymel.nodetypes.Joint):
            qItem.setIcon(0, QtGui.QIcon(":/pickJointObj.png"))
        else:
            if getattr(obj, "getShape"):
                if isinstance(obj.getShape(), pymel.nodetypes.NurbsSurface):
                    qItem.setIcon(0, QtGui.QIcon(":/nurbsSurface.svg"))
                elif isinstance(obj.getShape(), pymel.nodetypes.NurbsCurve):
                    qItem.setIcon(0, QtGui.QIcon(":/nurbsCurve.svg"))
                else:
                    qItem.setIcon(0, QtGui.QIcon(":/question.png"))

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
            self._set_icon_from_type(obj, qItem)
            qItem.setCheckState(0, QtCore.Qt.Checked if networks else QtCore.Qt.Unchecked)
            if qItem.flags() & QtCore.Qt.ItemIsUserCheckable:
                qItem.setFlags(qItem.flags() ^ QtCore.Qt.ItemIsUserCheckable)
            qt_parent.addChild(qItem)
            qt_parent = qItem

        for sub_jnt in obj.getChildren():
            if isinstance(sub_jnt, pymel.nodetypes.Transform):
                qSubItem = self._fill_widget_influences_recursive(qt_parent, sub_jnt)

    def _fill_widget_influences_recursive2(self, qt_parent, data):
        obj, children_data = data
        if obj:
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
                self._set_icon_from_type(obj, qItem)
                qItem.setCheckState(0, QtCore.Qt.Checked if networks else QtCore.Qt.Unchecked)
                if qItem.flags() & QtCore.Qt.ItemIsUserCheckable:
                    qItem.setFlags(qItem.flags() ^ QtCore.Qt.ItemIsUserCheckable)
                qt_parent.addChild(qItem)
                qt_parent = qItem

        for child_data in children_data:
            child = child_data[0]
            if isinstance(child, pymel.nodetypes.Transform):
                qSubItem = self._fill_widget_influences_recursive2(qt_parent, child_data)

    def _show_parent_recursive(self, qt_parent_item):
        if qt_parent_item is not None:
            if qt_parent_item.isHidden:
                qt_parent_item.setHidden(False)
            self._show_parent_recursive(qt_parent_item.parent())

    def _can_show_QTreeWidgetItem(self, qItem, query_regex):
        obj = qItem.obj  # Retrieve monkey-patched data
        obj_name = obj.stripNamespace()
        #print obj_name

        if not re.match(query_regex, obj_name, re.IGNORECASE):
            return False

        if self.checkBox_hideAssigned.isChecked():
            if qItem.networks:
                return False

        return True

    def _update_network(self, module, item=None):
        if hasattr(module, "_network"):
            pymel.delete(module._network)
        new_network = libSerialization.export_network(module) #TODO : Automatic update
        #If needed, update the network item net property to match the new exported network
        if item:
            item.net = new_network

    #Block signals need to be called in a function because if called in a signal, it will block it
    def _set_text_block(self, item, str):
        self.treeWidget.blockSignals(True)
        if hasattr(item, "rig"):
            item.setText(0, str)
        self.treeWidget.blockSignals(False)

    def _add_part(self, cls_name):
        #part = _cls(pymel.selected())
        self.root.add_module(cls_name, pymel.selected())
        net = self.export_networks()
        pymel.select(net)
        #Add manually the Rig to the root list instead of importing back all network
        #if not self.root in self.roots:
        #    self.roots.append(self.root)
        #self.updateData()
        self.update_ui()

    @libPython.log_execution_time('import_networks')
    def import_networks(self, *args, **kwargs):
        path = '/home/rlessard/Desktop/test.json'

        self.roots = core.find()
        self.root = next(iter(self.roots), None)


        # self.roots = None
        # if os.path.exists(path):
        #     self.roots = libSerialization.import_json_file_maya(path)
        # self.root = next(iter(self.roots), None) if self.roots else None
        #
        # if self.root is None:
        #     self.root = core.create()
        #     self.roots = [self.root]

    @libPython.log_execution_time('export_networks')
    def export_networks(self):
        path = '/home/rlessard/Desktop/test.json'

        try:
            pymel.delete(self.root._network)
        except AttributeError:
            pass

        net = libSerialization.export_network(self.root) # Export part and only part
        return net

        # libSerialization.export_json_file_maya(path)


    #
    # Publics
    #

    #Will only refresh tree view information without removing any items
    def refresh_ui(self):
        self.refresh_ui_module()
        self.refresh_ui_jnts()

    #Recreate tree views items
    def update_ui(self, *args, **kwargs):
        self.update_ui_modules()
        self.update_ui_jnts()

    def refresh_ui_module(self):
        #Block the signal to make sure that the itemChanged event is not called when adjusting the check state
        self.treeWidget.blockSignals(True)
        for qt_item in get_all_QTreeWidgetItem(self.treeWidget):
            if hasattr(qt_item, "rig"):
                qt_item.setCheckState(0, QtCore.Qt.Checked if qt_item.rig.is_built() else QtCore.Qt.Unchecked)
        self.treeWidget.blockSignals(False)

    def update_ui_modules(self, *args, **kwargs):
        self.treeWidget.clear()
        for root in self.roots:
            qItem = self._rig_to_tree_widget(root)
            self.treeWidget.addTopLevelItem(qItem)
            self.treeWidget.expandItem(qItem)



    def update_ui_jnts(self, *args, **kwargs):
        # Resolve text query
        query_raw = self.lineEdit_search_jnt.text()
        query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        self.treeWidget_jnts.clear()
        #all_jnt_roots = libPymel.ls_root(type='joint') + list(set([shape.getParent() for shape in pymel.ls(type='nurbsSurface')]))
        all_potential_influences = self.root.get_potential_influences()

        if all_potential_influences :
            data = libPymel.get_tree_from_objs(all_potential_influences, sort=True)

            self._fill_widget_influences_recursive2(self.treeWidget_jnts.invisibleRootItem(), data)



        '''
        if all_jnt_roots:
            for jnt in all_jnt_roots:
                self._fill_widget_influences_recursive(self.treeWidget_jnts.invisibleRootItem(), jnt)
        '''

        self.refresh_ui_jnts()

    def refresh_ui_jnts(self, query_regex=None):
        if query_regex is None:
            query_raw = self.lineEdit_search_jnt.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        unselectableBrush = QtGui.QBrush(QtCore.Qt.darkGray)
        selectableBrush = QtGui.QBrush(QtCore.Qt.white)
        for qt_item in get_all_QTreeWidgetItem(self.treeWidget_jnts):
            can_show = self._can_show_QTreeWidgetItem(qt_item, query_regex)
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
                if flags & QtCore.Qt.ItemIsSelectable: #Make selectable
                    flags ^= QtCore.Qt.ItemIsSelectable
                    qt_item.setFlags(flags)

        self.treeWidget_jnts.expandAll()

    def refresh_ui_modules(self, query_regex=None):
        if query_regex is None:
            query_raw = self.lineEdit_search_modules.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        def fn_can_show(qItem, query_regex):
            # Always shows non-module
            if not hasattr(qItem, 'rig'):
                return True
            if not isinstance(qItem.rig, classModule.Module):
                return True

            module = qItem.rig  # Retrieve monkey-patched data
            module_name = str(module)

            return not query_regex or re.match(query_regex, module_name, re.IGNORECASE)

        #unselectableBrush = QtGui.QBrush(QtCore.Qt.darkGray)
        #selectableBrush = QtGui.QBrush(QtCore.Qt.white)
        for qt_item in get_all_QTreeWidgetItem(self.treeWidget):
            can_show = fn_can_show(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    #
    # Events
    #

    def on_build(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if not rig.is_built():
                if isinstance(rig, classModule.Module):
                    self.root.pre_build()
                    rig.build(self.root)
                    self.root.post_buid_module(rig)
                else:
                    rig.build()
            else:
                pymel.warning("Can't build {0}, already built.".format(rig))
        self._update_network(self.root)
        self.update_ui()

    def on_unbuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.is_built():
                rig.unbuild()
            else:
                pymel.warning("Can't unbuild {0}, already unbuilt.".format(rig))
        self._update_network(self.root)
        self.update_ui()

    def on_rebuild(self):
        for qItem in self.treeWidget.selectedItems():
            rig = qItem.rig
            if rig.is_built():
                rig.unbuild()
            rig.build()
        self._update_network(self.root)

    def on_import(self):
        path, _ = QtGui.QFileDialog.getOpenFileName(caption="File Save (.json)", filter="JSON (*.json)")
        if not path:
            return

        new_rigs = libSerialization.import_json_file_maya(path)
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
            libSerialization.export_json_file_maya(all_rigs, path)

    def on_update(self, *args, **kwargs):
        #TODO - Fix the reload problem which cause isinstance function check to fail with an existing network
        import omtk; reload(omtk); omtk._reload()
        self.import_networks()
        self.update_ui()

    def on_module_selection_changed(self):
        pymel.select([item.net for item in self.treeWidget.selectedItems() if hasattr(item, 'net')])

    def on_influence_selection_changed(self):
        pymel.select([item.obj for item in self.treeWidget_jnts.selectedItems() if item.obj.exists()])
        if self.treeWidget_jnts.selectedItems():
            self.actionCreateModule.setEnabled(True)
        else:
            self.actionCreateModule.setEnabled(False)

    def on_module_changed(self, item):
        # todo: handle exception
        #Check first if the checkbox have changed
        need_update = False
        new_state = item.checkState(0) == QtCore.Qt.Checked
        new_text = item.text(0)
        module = item.rig
        if item._checked != new_state:
            item._checked = new_state
            #Handle checkbox change
            module_is_built = module.is_built()
            if new_state:
                if module_is_built:
                    module.unbuild()
                if isinstance(module, classModule.Module):
                    self.root.pre_build()
                    module.build(self.root)
                    self.root.post_buid_module(module)
                else:
                    module.build()
            else:
                if module_is_built:
                    module.unbuild()
            need_update = True
            self._update_network(self.root, item=item)

        #Check if the name have changed
        if (item._name != new_text):
            item._name = new_text
            module.name = new_text

            #Update directly the network value instead of re-exporting it
            if hasattr(item, "net"):
                name_attr = item.net.attr("name")
                name_attr.set(new_text)

        #Ensure to only refresh the UI and not recreate all
        if need_update:
            self.refresh_ui()

    def on_query_changed(self, *args, **kwargs):
        self.refresh_ui_jnts()

    def on_module_query_changed(self, *args, **kwargs):
        self.refresh_ui_modules()

    def on_module_double_clicked(self, item):
        if hasattr(item, "rig"):
            self._set_text_block(item, item.rig.name)
            self._is_modifying = True #Flag to know that we are currently modifying the name
            self.treeWidget.editItem(item, 0)

    def on_remove(self):
        for item in self.treeWidget.selectedItems():
            module = item.rig
            #net = item.net if hasattr(item, "net") else None
            if module.is_built():
                module.unbuild()
            self.root.modules.remove(module)
        self.export_networks()
        self.update_ui()

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
            sel = self.treeWidget.selectedItems()
            if len(sel) == 1:
                actionRemove = menu.addAction("Rename")
                #actionRemove.triggered.connect(functools.partial(self.treeWidget.editItem, sel[0], 0))
                actionRemove.triggered.connect(functools.partial(self.treeWidget.itemDoubleClicked.emit, sel[0], 0))
            actionRemove = menu.addAction("Remove")
            actionRemove.triggered.connect(functools.partial(self.on_remove))

            # Expose decorated functions
            module = sel[0].rig

            def is_exposed(val):
                if not hasattr(val, '__can_show__'):
                    return False
                fn = getattr(val, '__can_show__')
                if fn is None:
                    return False
                #if not inspect.ismethod(fn):
                #    return False
                return val.__can_show__()

            functions = inspect.getmembers(module, is_exposed)
            if functions:
                menu.addSeparator()
                for fn_name, fn in functions:
                    action = menu.addAction(fn_name)
                    action.triggered.connect(fn)

            menu.exec_(QtGui.QCursor.pos())

    def on_btn_add_pressed(self):
        if self.treeWidget_jnts.selectedItems():
            menu = QtGui.QMenu()
            cls_name = [cls.__name__ for cls in libPython.get_sub_classes(classModule.Module) if cls.SHOW_IN_UI]
            for name in sorted(cls_name):
                cls_name = name
                action = menu.addAction(cls_name)
                action.triggered.connect(functools.partial(self._add_part, cls_name))

            menu.exec_(QtGui.QCursor.pos())

    def on_addToModule(self):
        need_update = False
        for item in self.treeWidget.selectedItems():
            module = item.rig
            if module:
                for obj in pymel.selected():
                    if obj in module.input:
                        continue
                    module.input.append(obj)
                    need_update = True

        # TODO: Faster by manually connecting to the inputs?
        if need_update:
            self.export_networks()
            self.update_ui()

    def on_removeFromModule(self):
        need_update = False
        for item in self.treeWidget.selectedItems():
            module = item.rig
            if module:
                for obj in pymel.selected():
                    if obj not in module.input:
                        continue
                    module.input.remove(obj)
                    need_update = True

        # TODO: Faster by manually connecting to the inputs?
        if need_update:
            self.export_networks()
            self.update_ui()

    def on_mirror_jnts_LtoR(self):
        libSkeleton.mirror_jnts_l_to_r()

    def on_mirror_jnts_RtoL(self):
        libSkeleton.mirror_jnts_r_to_l()

    def focus_in_module(self, event):
        #Set back the text with the information about the module in it
        if self._is_modifying:
            sel = self.treeWidget.selectedItems()
            if sel:
                self._set_text_block(sel[0], str(sel[0].rig))
                #sel[0].setText(0, str(sel[0].rig))
            self._is_modifying = False
        self.focusInEvent(event)

    def closeEvent(self, *args, **kwargs):
        self.remove_callbacks()
        super(AutoRig, self).closeEvent(*args, **kwargs)

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
