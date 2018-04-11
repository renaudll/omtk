import functools
import inspect
import os
import logging
from collections import defaultdict

import core

from maya import cmds
import pymel.core as pymel
from maya import OpenMaya
from omtk.core import api
from omtk.core import classModule
from omtk.libs import libPython
from omtk.libs import libSkeleton
from omtk.ui import main_window
from omtk import ui_shared

from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

log = logging.getLogger('omtk')


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
        self.ui.actionAddSelectedInfluencesToModule.triggered.connect(self.on_add_selected_influences_to_module)
        self.ui.actionAddSelectedMeshesToModule.triggered.connect(self.on_add_selected_meshes_to_module)
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

        # from omtk.core import plugin_manager
        # pm = plugin_manager.plugin_manager
        # failed_plugins = pm.get_failed_plugins()
        # if failed_plugins:
        #     log.warning("The following plugins failed to load: {0}".format(', '.join(str(p) for p in failed_plugins)))

        # Build the template menu
        available_templates = self._get_available_templates()
        if available_templates:
            menu_template = QtWidgets.QMenu(self.ui.menubar)
            menu_template.setTitle("Templates")

            for template in available_templates:
                template_name = os.path.basename(template)
                action = QtWidgets.QAction(template_name, self)
                action.triggered.connect(functools.partial(self.action_import_template, template))
                menu_template.addAction(action)

            self.ui.menubar.addAction(menu_template.menuAction())

    def action_import_template(self, path):
        for root in self.roots:
            pymel.delete(root._network)
            self.on_rig_deleted(root)
        log.info('Importing template {0}'.format(path))
        
        cmds.file(path, i=True)
        self.on_update()

    def _get_available_templates(self):
        results = set()

        for plugin_dir in os.environ.get('OMTK_PLUGINS', []).split(os.pathsep):
            if not os.path.exists(plugin_dir):
                continue

            template_dir = os.path.join(plugin_dir, 'templates')
            if not os.path.exists(template_dir):
                continue

            for filename in os.listdir(template_dir):
                if filename.endswith('.ma') or filename.endswith('.mb'):
                    path = os.path.join(template_dir, filename)
                    results.add(path)

        return results

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

    def on_context_menu_request(self):
        if self.ui.treeWidget.selectedItems():
            menu = QtWidgets.QMenu()
            actionBuild = menu.addAction("Build")
            actionBuild.triggered.connect(self.on_build_selected)
            actionUnbuild = menu.addAction("Unbuild")
            actionUnbuild.triggered.connect(self.on_unbuild_selected)
            actionRebuild = menu.addAction("Rebuild")
            actionRebuild.triggered.connect(self.on_rebuild_selected)
            menu.addSeparator()
            actionLock = menu.addAction("Lock")
            actionLock.triggered.connect(self.on_lock_selected)
            action_unlock = menu.addAction("Unlock")
            action_unlock.triggered.connect(self.on_unlock_selected)
            menu.addSeparator()
            sel = self.ui.treeWidget.selectedItems()
            if len(sel) == 1:
                actionRemove = menu.addAction("Rename")
                # actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.editItem, sel[0], 0))
                actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.itemDoubleClicked.emit, sel[0], 0))
            actionRemove = menu.addAction("Remove")
            actionRemove.triggered.connect(functools.partial(self.on_remove))

            # Expose decorated functions
            module = sel[0].metadata_data

            def is_exposed(val):
                if not hasattr(val, '__can_show__'):
                    return False
                fn = getattr(val, '__can_show__')
                if fn is None:
                    return False
                # if not inspect.ismethod(fn):
                #    return False
                return val.__can_show__()

            functions = inspect.getmembers(module, is_exposed)

            if functions:
                menu.addSeparator()
                for fn_name, fn in functions:

                    # Always pass the rig as the first argument in an exposed module function.
                    if isinstance(module, classModule.Module):
                        fn = functools.partial(fn, self._rig)

                    action = menu.addAction(fn_name)
                    action.triggered.connect(fn)

            menu.exec_(QtGui.QCursor.pos())

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

        # Create a rig instance if the scene is empty.
        if self.root is None:
            self.root = core.create()
            self.roots = [self.root]
            self.export_networks()  # Create network tree in the scene

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

    # --- Widget traversal methods ---
    # todo: put this elsewhere?

    def _get_selected_items_by_metadata_type(self, qtreeview, metadata_type):
        items = qtreeview.selectedItems()
        return [item for item in items if item.metadata_type == metadata_type]

    def _get_qtreeview_selected_metadata(self, qtreeview, metadata_type, search_up=False):
        items = self._get_selected_items_by_metadata_type(qtreeview, metadata_type)
        return [item.metadata_data for item in items]

    def get_selected_modules(self, search_up=False):
        return self._get_qtreeview_selected_metadata(
            self.ui.widget_modules.ui.treeWidget,
            ui_shared.MetadataType.Module,
            search_up=search_up
        )

    def get_selected_rigs(self, search_up=False):
        return self._get_qtreeview_selected_metadata(
            self.ui.widget_modules.ui.treeWidget,
            ui_shared.MetadataType.Rig,
            search_up=search_up
        )

    def get_selected_influences(self, search_up=False):
        return self._get_qtreeview_selected_metadata(
            self.ui.widget_jnts.ui.treeWidget,
            ui_shared.MetadataType.Influece,
            search_up=search_up
        )

    def get_selected_meshes(self, search_up=False):
        return self._get_qtreeview_selected_metadata(
            self.ui.widget_meshes.ui.treeWidget,
            ui_shared.MetadataType.Mesh,
            search_up=search_up
        )

    def _get_parent_item_by_metadata_type(self, qtreewidgetitem, metadata_type):
        while qtreewidgetitem and not qtreewidgetitem.metadata_type == metadata_type:
            qtreewidgetitem = qtreewidgetitem.parent()
        return qtreewidgetitem

    # --- Events ---

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

    def on_add_selected_influences_to_module(self):
        selected_modules = self.get_selected_modules()
        selected_meshes = self.get_selected_influences()
        need_update = False

        for module in selected_modules:
            for mesh in selected_meshes:
                if mesh in module.input:
                    continue
                module.input.append(mesh)
                need_update = True

        if need_update:
            self.export_networks()
            self.update_ui()

    def on_add_selected_meshes_to_module(self):
        selected_modules = self.get_selected_modules()
        selected_meshes = self.get_selected_meshes()
        need_update = False

        for module in selected_modules:
            for mesh in selected_meshes:
                if mesh in module.input:
                    continue
                module.input.append(mesh)
                need_update = True

        if need_update:
            self.export_networks()
            self.update_ui()

    def on_removeFromModule(self):
        need_update = False
        selected_items = self.ui.widget_modules.ui.treeWidget.selectedItems()
        items_to_remove_by_module = defaultdict(list)

        for item in selected_items:
            if item.metadata_type in (ui_shared.MetadataType.Influece, ui_shared.MetadataType.Mesh):
                module_item = self._get_parent_item_by_metadata_type(item, ui_shared.MetadataType.Module)
                module = module_item.metadata_data
                influence = item.metadata_data
                items_to_remove_by_module[module].append(influence)

        for module, influences in items_to_remove_by_module.iteritems():
            for influence in influences:
                module.input.remove(influence)
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
