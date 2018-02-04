import functools
import logging

import omtk.constants
import omtk.core
import pymel.core as pymel
from maya import OpenMaya
from omtk import api
from omtk import constants
from omtk.core import preferences, session
from omtk.libs import libPython
from omtk.libs import libSkeleton
from omtk.qt_widgets.ui import main_window
from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
from omtk.qt_widgets import main_window_extended

log = logging.getLogger('omtk')


class EnumSections:
    """Define the section available in the ui."""
    Welcome = 0
    Edit = 1


class AutoRig(main_window_extended.MainWindowExtended):
    # Called when the user launched Component actions, generally via a customContextMenu.
    actionRequested = QtCore.Signal(list)

    # Called when something change internally and a refresh is needed.
    exportRequested = QtCore.Signal()

    def __init__(self, parent=None):
        self.callbacks_events = []
        self.callbacks_scene = []
        self.callbacks_nodes = None

        super(AutoRig, self).__init__()

        self.ui = main_window.Ui_OpenRiggingToolkit()
        self.ui.setupUi(self)

        # Makes Maya perform magic which makes the window stay
        # on top in OS X and Linux. As an added bonus, it'll
        # make Maya remember the window position
        # credit: https://github.com/fredrikaverpil/pyVFX-boilerplate
        self.setProperty("saveWindowPref", True)

        # Extract version number from rez package.py file and display it
        version = omtk.constants.get_version()
        self.setWindowTitle('Open Rigging Toolkit {}'.format(version))

        #
        # First update
        #

        self.import_networks()

        # Connect events
        self.ui.actionBuildAll.triggered.connect(self.on_build_all)
        self.ui.actionRebuildAll.triggered.connect(self.on_rebuild_all)
        self.ui.actionUnbuildAll.triggered.connect(self.on_unbuild_all)
        self.ui.actionImport.triggered.connect(self.on_import)
        self.ui.actionExport.triggered.connect(self.on_export)
        self.ui.actionUpdate.triggered.connect(self.on_update)
        self.ui.actionCreateModule.triggered.connect(self.on_btn_add_pressed)
        self.ui.actionMirrorJntsLToR.triggered.connect(self.on_mirror_influences_l_to_r)
        self.ui.actionMirrorJntsRToL.triggered.connect(self.on_mirror_influences_r_to_l)
        self.ui.actionMirrorSelection.triggered.connect(self.on_mirror_selection)
        self.ui.actionAddNodeToModule.triggered.connect(self.on_addToModule)
        self.ui.actionRemoveNodeFromModule.triggered.connect(self.on_removeFromModule)
        self.ui.actionShowPluginManager.triggered.connect(self.on_show_pluginmanager)
        self.ui.actionShowPreferences.triggered.connect(self.on_show_preferences)
        self.ui.actionCreateComponent.triggered.connect(self.on_create_component)

        # Configure drag and drop
        # self.ui.widget_modules.ui.treeWidget.set_mime_type('omtk_modules')  # todo: create const
        self.ui.widget_modules.ui.treeWidget.setDragDropOverwriteMode(False)
        self.ui.widget_modules.ui.treeWidget.setDragEnabled(True)

        # self.ui.widget_jnts.ui.treeWidget.set_mime_type('omtk_influences')  # todo: create const
        self.ui.widget_jnts.ui.treeWidget.setDragDropOverwriteMode(False)
        self.ui.widget_jnts.ui.treeWidget.setDragEnabled(True)

        # self.ui.widget_meshes.ui.treeWidget.set_mime_type('omtk_meshe')  # todo: create const
        self.ui.widget_meshes.ui.treeWidget.setDragDropOverwriteMode(False)
        self.ui.widget_meshes.ui.treeWidget.setDragEnabled(True)

        self.create_callbacks()

        # Configure welcome screen
        if not preferences.get_preferences().hide_welcome_screen and not self.manager.get_rigs():
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)
            self.ui.widget_welcome.onCreate.connect(self.on_welcome_rig_created)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

        # Connect events
        self.actionRequested.connect(self.on_action_requested)
        self.ui.widget_jnts.onRightClick.connect(self.on_btn_add_pressed)

        # Note that currently we update the modules view when the drag enter it.
        # However it would be more useful for the user to update it as soon as drag start.
        # Sadly I didn't find a way to call on_influence_drag_drop if the drag end out-of-bound.
        self.ui.widget_modules.ui.treeWidget.dragEnter.connect(self.on_influence_drag_enter)
        self.ui.widget_modules.ui.treeWidget.dragLeave.connect(self.on_influence_drag_drop)
        self.ui.widget_modules.ui.treeWidget.dragDrop.connect(self.on_influence_drag_drop)

        #
        # Configure Node Editor
        #
        # self.ui.widget_node_editor.ui.widget_view.actionRequested.connect(self.actionRequested.emit)

        # Pre-configure QDockWidget
        self.tabifyDockWidget(self.ui.dockWidget_influences, self.ui.dockWidget_meshes)
        self.tabifyDockWidget(self.ui.dockWidget_meshes, self.ui.dockWidget_modules)
        # self.tabifyDockWidget(self.ui.dockWidget_modules, self.ui.dockWidget_modules)


        # Add existing rigs in the NodeGraph on startup
        # for rig in self.manager._roots:
        #     ctrl = self.ui.widget_node_editor.get_controller()
        #     model, widget = ctrl.add_node(rig)
        #     ctrl.expand_node_connections(model)

        self.manager.onSceneChanged.connect(self.on_scene_changed)
        self.manager.onRigCreated.connect(self.on_manager_created_rig)
        self.ui.widget_modules.actionRequested.connect(self.on_action_requested)

        self.set_logger(log)

    @property
    def manager(self):
        return session.get_session()

    def on_manager_created_rig(self, rig):
        node_editor_ctrl = self.ui.widget_node_editor.get_controller()
        model = node_editor_ctrl.get_node_model_from_value(rig)
        node_editor_ctrl.add_node(model)

    def on_action_requested(self, actions):
        need_export_network = False
        # entities = self.get_selected_components()
        # action_map = self._get_actions(entities)
        for action in actions:
            action.execute()
            if constants.ComponentActionFlags.trigger_network_export in action.iter_flags():
                need_export_network = True

        if need_export_network:
            self.export_networks()
            self.ui.widget_modules.update()
            self.ui.widget_node_editor.ui.widget.update()
            # todo: update node editor?

    def on_scene_changed(self):
        """Called when something change somewhere but we don't known exactly what."""
        self.ui.widget_modules.update()
        self.ui.widget_node_editor.get_view().update()

    def on_request_export(self):
        self.export_networks()
        self.ui.widget_modules.update()

    # --- Drag ---

    def dragLeaveEvent(self, event):
        self.on_influence_drag_drop()

    def on_influence_drag_enter(self, event):
        print "Influence drag enter!"
        data = event.mimeData().data('omtk-influence')
        self.ui.widget_modules._refresh_ui_enabled(data)

    def on_influence_drag_drop(self):
        print "Influence grag drop!"
        self.ui.widget_modules._reset_ui_enabled()

    def on_welcome_rig_created(self):
        # self.import_networks()
        self.update_internal_data()
        # self.update_ui()
        self.set_current_widget(EnumSections.Edit)

    def set_current_widget(self, index):
        old_index = self.ui.stackedWidget.currentIndex()
        # self.ui.stackedWidget.setCurrentIndex(index)
        transition_duration = 500
        width = self.ui.stackedWidget.width()
        height = self.ui.stackedWidget.height()
        widgets_pages = [self.ui.page_1, self.ui.page_2]
        num_widgets = len(widgets_pages)
        for page in widgets_pages:
            page.show()

        old_positions = [QtCore.QRect(width * (i - old_index), 0, width, height) for i in range(num_widgets)]
        new_positions = [QtCore.QRect(width * (i - index), 0, width, height) for i in range(num_widgets)]

        self._qt_animation = QtCore.QParallelAnimationGroup()  # member variable necessary to bypass garbage collection
        for widget, old_pos, new_pos in zip(widgets_pages, old_positions, new_positions):
            animation = QtCore.QPropertyAnimation(widget, "geometry")
            animation.setDuration(transition_duration)
            animation.setStartValue(old_pos)
            animation.setEndValue(new_pos)
            animation.setEasingCurve(QtCore.QEasingCurve.InOutSine)
            animation.start()
            self._qt_animation.addAnimation(animation)
            self._qt_animation.finished.connect(
                functools.partial(self.ui.stackedWidget.setCurrentWidget, widgets_pages[index]))

        self._qt_animation.start()

    def create_callbacks(self):
        self.remove_callbacks()
        # Disable to prevent performance drop when CTRL-Z and the tool is open
        # TODO - Reactivate back when the tool will be stable ?
        # self.callbacks_events = \
        #     [
        #         OpenMaya.MEventMessage.addEventCallback("Undo", self.update_ui),
        #         OpenMaya.MEventMessage.addEventCallback("Redo", self.update_ui)
        #     ]
        self.callbacks_scene = \
            [
                OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterOpen, self.on_update),
                OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterNew, self.on_update)
            ]

        # self.callbacks_nodes = OpenMaya.MDGMessage.addNodeRemovedCallback(
        #     self.callback_network_deleted, 'network'  # TODO: Restrict to network nodes
        # )

    def remove_callbacks(self):
        # for callback_id in self.callbacks_events:
        #     OpenMaya.MEventMessage.removeCallback(callback_id)
        # self.callbacks_events = []

        for callback_id in self.callbacks_scene:
            OpenMaya.MSceneMessage.removeCallback(callback_id)
        self.callbacks_scene = []

        # temporary disabled for performance issues
        # if self.callbacks_nodes is not None:
        #     OpenMaya.MMessage.removeCallback(self.callbacks_nodes)
        #     self.callbacks_nodes = None

    def on_build_all(self):
        raise NotImplementedError

    def on_rebuild_all(self):
        raise NotImplementedError

    def on_unbuild_all(self):
        raise NotImplementedError

    def _add_part(self, cls):
        # part = _cls(pymel.selected())
        inst = cls(pymel.selected())
        self.manager._root.add_module(inst)
        net = self.export_networks()
        pymel.select(net)

        self.update_ui()

    @libPython.log_execution_time('import_networks')
    def import_networks(self, *args, **kwargs):
        self.manager.import_networks()

        # # Create a rig instance if the scene is empty.
        # if self.root is None:
        #     self.root = core.create()
        #     self.roots = [self.root]
        #     self.export_networks()  # Create network tree in the scene

        self.update_internal_data()

    def update_internal_data(self):
        # self.ui.widget_modules.set_rigs(self.manager._roots) disabled for now
        self.ui.widget_jnts.set_rig(self.manager._root)
        self.ui.widget_meshes.set_rig(self.manager._root)

    @libPython.log_execution_time('export_networks')
    def export_networks(self, update=True):
        self.manager.export_networks()

        if update:
            self.update_ui()

    # Will only refresh tree view information without removing any items
    def refresh_ui(self):
        self.ui.widget_modules.update_checked()
        self.ui.widget_modules.update_visibility()
        self.ui.widget_jnts.update_visibility()

    # Recreate tree views items
    def update_ui(self, *args, **kwargs):
        self.ui.widget_modules.update()
        self.ui.widget_jnts.update()
        self.ui.widget_meshes.update()

    def on_import(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(caption="File Save (.json)", filter="JSON (*.json)")
        if not path:
            return

        new_rigs = libSerialization.import_json_file_maya(path)
        if not new_rigs:
            return

        # Remove previous rigs
        all_rigs = omtk.core.find()
        for rig in all_rigs:
            if rig._network.exists():
                pymel.delete(rig._network)

        for rig in filter(None, new_rigs):
            libSerialization.export_network(rig)

        self.on_update()

    def on_export(self):
        all_rigs = omtk.core.find()

        path, _ = QtWidgets.QFileDialog.getSaveFileName(caption="File Save (.json)", filter="JSON (*.json)")
        if path:
            libSerialization.export_json_file_maya(all_rigs, path)

    def on_update(self, *args, **kwargs):
        self.import_networks()
        self.update_ui()

    def on_btn_add_pressed(self):
        selected_items = self.ui.widget_jnts.get_selection()
        if not selected_items:
            return

        menu = QtWidgets.QMenu()

        from omtk.core.plugin_manager import plugin_manager
        for plugin in sorted(plugin_manager.get_loaded_plugins_by_type('modules')):
            if getattr(plugin.cls, 'SHOW_IN_UI', False):
                action = menu.addAction(plugin.name)
                action.triggered.connect(functools.partial(self._add_part, plugin.cls))

        menu.exec_(QtGui.QCursor.pos())

    def on_addToModule(self):
        need_update = False
        selected_module_items = self.ui.widget_modules.ui.treeWidget.selectedItems()
        selected_influences = self.ui.widget_jnts.get_selection()

        for item in selected_module_items:
            module = item.rig
            if module:
                for obj in selected_influences:
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
        selected_module_items = self.ui.widget_modules.ui.treeWidget.selectedItems()
        selected_influences = self.ui.widget_jnts.get_selection()

        for item in selected_module_items:
            module = item.rig
            if module:
                for obj in selected_influences:
                    if obj not in module.input:
                        continue
                    module.input.remove(obj)
                    need_update = True

        # TODO: Faster by manually connecting to the inputs?
        if need_update:
            self.export_networks()
            self.update_ui()

    def _is_l_influence(self, root, inf):
        inf_name = inf.stripNamespace().nodeName()
        nomenclature = root.nomenclature()
        nomenclature.build_from_string(inf_name)
        return nomenclature.side == nomenclature.SIDE_L

    def _is_r_influence(self, root, inf):
        inf_name = inf.stripNamespace().nodeName()
        nomenclature = root.nomenclature()
        nomenclature.build_from_string(inf_name)
        return nomenclature.side == nomenclature.SIDE_R

    def _get_l_influences(self):
        objs = self.manager._root.get_potential_influences()
        # Filter joints
        fn_filter = lambda x: isinstance(x, pymel.nodetypes.Joint)
        objs = filter(fn_filter, objs)
        # Filter l side only
        fn_filter = functools.partial(self._is_l_influence, self.manager._root)
        return filter(fn_filter, objs)

    def _get_r_influences(self):
        objs = self.manager._root.get_potential_influences()
        # Filter joints
        fn_filter = lambda x: isinstance(x, pymel.nodetypes.Joint)
        objs = filter(fn_filter, objs)
        # Filter r side only
        fn_filter = functools.partial(self._is_r_influence, self.manager._root)
        return filter(fn_filter, objs)

    def on_mirror_influences_l_to_r(self):
        objs = self._get_l_influences()
        if not objs:
            pymel.warning('No joints found!')
            return
        libSkeleton.mirror_jnts(objs)

        self.ui.widget_jnts.update()

    def on_mirror_influences_r_to_l(self):
        objs = self._get_r_influences()
        if not objs:
            pymel.warning('No joints found!')
            return
        libSkeleton.mirror_jnts(objs)

        self.ui.widget_jnts.update()

    def on_mirror_selection(self):
        objs = pymel.selected(type='joint')
        if not objs:
            pymel.warning('No joints found!')
            return
        libSkeleton.mirror_jnts(objs)

        self.ui.widget_jnts.update()

    def on_show_pluginmanager(self):
        from omtk.qt_widgets import window_pluginmanager
        window_pluginmanager.show()

    def on_show_preferences(self):
        from omtk.qt_widgets import window_preferences
        window_preferences.show()

    def on_create_component(self):
        from omtk.qt_widgets import form_create_component
        form_create_component.show()
        # from omtk.qt_widgets import widget_component_wizard
        # widget_component_wizard.show()

    #
    # QMainWindow show/close events
    #

    def showEvent(self, *args, **kwargs):
        super(AutoRig, self).showEvent(*args, **kwargs)

    def closeEvent(self, *args, **kwargs):
        # Properly remove events
        # todo: fix
        # self.manager.onSceneChanged.disconnect(self.on_scene_changed)
        # self.manager.onRigCreated.disconnect(self.on_manager_created_rig)
        # self.ui.widget_modules.actionRequested.disconnect(self.manager.onSceneChanged.emit)

        try:
            self.remove_callbacks()
        except Exception, e:
            log.warning("Error removing callbacks: {0}".format(e))
        QtWidgets.QMainWindow.closeEvent(self, *args)


gui = None


def show():
    # Try to kill latest Autorig ui window
    try:
        pymel.deleteUI('OpenRiggingToolkit')
    except:
        pass

    global gui

    gui = AutoRig()

    # Create a frame geo to easilly move it from the center
    pFrame = gui.frameGeometry()
    pScreen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    ptCenter = QtWidgets.QApplication.desktop().screenGeometry(pScreen).center()
    pFrame.moveCenter(ptCenter)
    gui.move(pFrame.topLeft())

    gui.show()
