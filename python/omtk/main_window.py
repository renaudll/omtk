import functools
import inspect
import logging

import core

import pymel.core as pymel
from maya import OpenMaya
from omtk.core import api
from omtk.core import classModule
from omtk.libs import libPython
from omtk.libs import libSkeleton
from omtk.ui import main_window

from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

log = logging.getLogger('omtk')


class EnumSections:
    """Define the section available in the ui."""
    Welcome = 0
    Edit = 1


class AutoRig(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AutoRig, self).__init__()

        # Internal data
        self.root = None
        self.roots = []

        self.ui = main_window.Ui_OpenRiggingToolkit()
        self.ui.setupUi(self)

        version = api.get_version()
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

        # Connect widget signals
        self.ui.widget_modules.needImportNetwork.connect(self.import_networks)
        self.ui.widget_modules.needExportNetwork.connect(self.export_networks)
        self.ui.widget_modules.deletedRig.connect(self.on_rig_deleted)
        self.ui.widget_jnts.onRightClick.connect(self.on_btn_add_pressed)

        self.callbacks_events = []
        self.callbacks_scene = []
        self.callbacks_nodes = None

        self.create_callbacks()

        # Configure welcome screen
        if not self.root:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        self.ui.widget_welcome.onCreate.connect(self.on_welcome_rig_created)

        # Configure logger and status-bar
        self.ui.dockWidget.hide()
        self.ui.widget_logger.onRecordAdded.connect(self.update_status_bar)

        # Hack: Skip subclassing QDockWidget to modify closeEvent
        def _logger_close_event(e):
            self.update_status_bar(force_show=True)
            e.accept()

        self.ui.dockWidget.closeEvent = _logger_close_event

        # Hack: Skip subclassing QStatusBar to modify mousePressEvent
        def _status_bar_mouse_press_event(e):
            self.ui.dockWidget.show()
            self.update_status_bar()

        self.ui.statusbar.mousePressEvent = _status_bar_mouse_press_event

        self.update_status_bar()

    def on_welcome_rig_created(self):
        self.import_networks()
        self.update_internal_data()
        # self.update_ui()
        self.set_current_widget(EnumSections.Edit)

    def update_status_bar(self, force_show=False):
        # No need for the status bar if the logger is visible
        if self.ui.widget_logger.isVisible() and not force_show:
            self.ui.statusbar.setStyleSheet('')
            self.ui.statusbar.showMessage('')
            return

        # If the logger is now visible, the status bar will resume the logs.
        num_errors = 0
        num_warnings = 0
        model = self.ui.widget_logger.model()
        for entry in model.items:
            if entry.levelno >= logging.ERROR:
                num_errors += 1
            elif entry.levelno >= logging.WARNING:
                num_warnings += 1

        # Define style
        stylesheet = ''
        if num_errors:
            stylesheet = "background-color: rgb(200, 128, 128); color: rgb(0, 0, 0);"
        elif num_warnings:
            stylesheet = "background-color: rgb(200, 200, 128); color: rgb(0, 0, 0);"
        self.ui.statusbar.setStyleSheet(stylesheet)

        # Define message
        messages = []
        if num_errors:
            messages.append('{0} errors'.format(num_errors))
        elif num_warnings:
            messages.append('{0} warnings'.format(num_warnings))
        else:
            self.ui.statusbar.setStyleSheet("")
        self.ui.statusbar.showMessage(', '.join(messages))

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
        self.root.add_module(inst)
        net = self.export_networks()
        pymel.select(net)

        self.update_ui()

    @libPython.log_execution_time('import_networks')
    def import_networks(self, *args, **kwargs):
        self.roots = core.find()
        self.root = next(iter(self.roots), None)

        # # Create a rig instance if the scene is empty.
        # if self.root is None:
        #     self.root = core.create()
        #     self.roots = [self.root]
        #     self.export_networks()  # Create network tree in the scene

        self.update_internal_data()

    def update_internal_data(self):
        self.ui.widget_modules.set_rigs(self.roots)
        self.ui.widget_jnts.set_rig(self.root)
        self.ui.widget_meshes.set_rig(self.root)

    @libPython.log_execution_time('export_networks')
    def export_networks(self, update=True):
        try:
            network = self.root._network
            if network and network.exists():
                pymel.delete(network)
        except AttributeError:
            pass

        net = libSerialization.export_network(self.root)  # Export part and only part

        if update:
            self.update_ui()

        return net

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
        all_rigs = core.find()
        for rig in all_rigs:
            if rig._network.exists():
                pymel.delete(rig._network)

        for rig in filter(None, new_rigs):
            libSerialization.export_network(rig)

        self.on_update()

    def on_export(self):
        all_rigs = core.find()

        path, _ = QtWidgets.QFileDialog.getSaveFileName(caption="File Save (.json)", filter="JSON (*.json)")
        if path:
            libSerialization.export_json_file_maya(all_rigs, path)

    def on_update(self, *args, **kwargs):
        self.import_networks()
        self.update_ui()

    def on_rig_deleted(self, rig):
        """
        Called from an internal widget to delete a rig.
        We take in consideration that the rig is already unbuilt and we only need to cleanup.
        """
        need_update = False
        if rig in self.roots:
            self.roots.remove(rig)
            need_update = True
        if rig is self.root:
            self.root = next(iter(self.roots), None)
        if need_update:
            self.update_internal_data()

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
        objs = self.root.get_potential_influences()
        # Filter joints
        fn_filter = lambda x: isinstance(x, pymel.nodetypes.Joint)
        objs = filter(fn_filter, objs)
        # Filter l side only
        fn_filter = functools.partial(self._is_l_influence, self.root)
        return filter(fn_filter, objs)

    def _get_r_influences(self):
        objs = self.root.get_potential_influences()
        # Filter joints
        fn_filter = lambda x: isinstance(x, pymel.nodetypes.Joint)
        objs = filter(fn_filter, objs)
        # Filter r side only
        fn_filter = functools.partial(self._is_r_influence, self.root)
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
        from omtk import pluginmanager_window
        pluginmanager_window.show()

    def on_show_preferences(self):
        from omtk import preferences_window
        preferences_window.show()

    #
    # QMainWindow show/close events
    #

    def showEvent(self, *args, **kwargs):
        super(AutoRig, self).showEvent(*args, **kwargs)

    def closeEvent(self, *args, **kwargs):
        log.info('Closed OMTK GUI')
        try:
            self.ui.widget_logger.remove_logger_handler()
        except Exception, e:
            log.warning("Error removing logging handler: {0}:".format(e))
        try:
            self.remove_callbacks()
        except Exception, e:
            log.warning("Error removing callbacks: {0}".format(e))
        QtWidgets.QMainWindow.closeEvent(self, *args)

        #
        # Logger handling
        #


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