import datetime
import functools
import inspect
import logging
import re
import traceback

import core
import libSerialization
import pymel.core as pymel
from maya import OpenMaya
from omtk.core import classModule
from omtk.core import classRig
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libSkeleton
from omtk.libs.libQt import QtCore, QtGui, getMayaWindow
from omtk.ui import main_window

reload(main_window)

log = logging.getLogger('omtk')


class MetadataType:
    """
    Used to quickly determine what metadata have been monkey-patched to a QWidget.
    """
    Rig = 0
    Module = 1
    Influece = 2
    Mesh = 3


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

def log_level_to_str(level):
    if level >= logging.CRITICAL:
        return 'Critical'
    if level >= logging.ERROR:
        return 'Error'
    if level >= logging.WARNING:
        return 'Warning'
    return 'Info'

class UiLoggerModel(QtCore.QAbstractTableModel):
    HEADER = ('Date', 'Type', 'Message')

    ROW_LEVEL = 1
    ROW_MESSAGE = 2
    ROW_DATE = 0

    COLOR_FOREGROUND_ERROR = QtGui.QColor(0, 0, 0)
    COLOR_FOREGROUND_WARNING = QtGui.QColor(255, 255, 0)
    COLOR_FOREGROUND_INFO = None
    COLOR_FOREGROUND_DEBUG = QtGui.QColor(128, 128, 128)

    COLOR_BACKGROUND_ERROR = QtGui.QColor(255, 0, 0)
    COLOR_BACKGROUND_WARNING = None
    COLOR_BACKGROUND_INFO = None
    COLOR_BACKGROUND_DEBUG = None

    def __init__(self, parent, data, *args):
        super(UiLoggerModel, self).__init__(parent, *args)
        self.items = data
        self.header = self.HEADER

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.ForegroundRole:
            record = self.items[index.row()]
            level = record.levelno
            if level >= logging.ERROR:
                return self.COLOR_FOREGROUND_ERROR
            if level >= logging.WARNING:
                return self.COLOR_FOREGROUND_WARNING
            if level <= logging.DEBUG:
                return self.COLOR_FOREGROUND_DEBUG
            return self.COLOR_FOREGROUND_INFO

        if role == QtCore.Qt.BackgroundColorRole:
            record = self.items[index.row()]
            level = record.levelno
            if level >= logging.ERROR:
                return self.COLOR_BACKGROUND_ERROR
            if level >= logging.WARNING:
                return self.COLOR_BACKGROUND_WARNING
            if level <= logging.DEBUG:
                return self.COLOR_BACKGROUND_DEBUG
            return self.COLOR_BACKGROUND_INFO

        if role != QtCore.Qt.DisplayRole:
            return None

        record = self.items[index.row()]
        col_index = index.column()
        if col_index == self.ROW_LEVEL:
            level = record.levelno
            return log_level_to_str(level)
        elif col_index == self.ROW_MESSAGE:
            return record.message
        elif col_index == self.ROW_DATE:
            return str(datetime.datetime.fromtimestamp(record.created))
        else:
            Exception("Unexpected row. Expected 0 or 1, got {0}".format(
                col_index
            ))

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def add(self, item):
        num_items = len(self.items)
        self.beginInsertRows(QtCore.QModelIndex(), num_items, num_items)
        self.items.append(item)
        self.endInsertRows()
        #
        # top = self.createIndex(num_items, 0, 0)
        # bot = self.createIndex(num_items, len(self.header), 0)
        # self.dataChanged.emit(top, bot)

    '''
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.data = sorted(self.data,
                           key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.data.reverse()
        self.emit(SIGNAL("layoutChanged()"))
    '''

class UiLoggerProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super(UiLoggerProxyModel, self).__init__(*args, **kwargs)
        self._log_level_interest = logging.WARNING
        self._log_search_query = None

    def set_loglevel_filter(self, loglevel, update=True):
        self._log_level_interest = loglevel
        if update:
            self.reset()

    def set_log_query(self, query, update=True):
        self._log_search_query = query if query else None
        if update:
            self.reset()

    def filterAcceptsRow(self, source_row, index):
        model = self.sourceModel()
        record = model.items[source_row]

        # Filter using query
        if self._log_search_query:
            query = self._log_search_query.lower()
            if not query in record.message.lower():
                return False

        # Filter using log level
        level = record.levelno
        if level < self._log_level_interest:
            return False

        return True

# class QTreeWidgetItem_CustomTooltip(QtGui.QTreeWidgetItem):
#     """
#     A custom QTreeWidgetItem that implement a tooltip for each individual item.
#     """
#     def __init__(self, *args, **kwargs):
#         super(QTreeWidgetItem_CustomTooltip, self).__init__(*args, **kwargs)
#         self.tooltip = None
#
#     def data(self, column, role):
#         if role == QtCore.Qt.ToolTipRole:
#             return self._tooltip
#         return super(QTreeWidgetItem_CustomTooltip, self).data(column, role)

class AutoRig(QtGui.QMainWindow):
    # http://forums.cgsociety.org/archive/index.php?t-1096914.html
    # Use the intern maya ressources icon
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
        # Try to kill latest Autorig ui window
        try:
            pymel.deleteUI('OpenRiggingToolkit')
        except:
            pass
        if parent is None: parent = getMayaWindow()
        super(AutoRig, self).__init__(parent)
        self.ui = main_window.Ui_OpenRiggingToolkit()
        self.ui.setupUi(self)

        self._is_modifying = False
        self.ui.checkBox_hideAssigned.setCheckState(QtCore.Qt.Checked)
        self.ui.actionCreateModule.setEnabled(False)

        #
        # Configure logging view
        #

        # Used to store the logging handlers
        self._logging_handlers = []
        # Used to store the records so our TableView can filter them
        self._logging_records = []
        # Used to store what log level we are interested.
        # We use a separated value here since we might want to keep other log handlers active (external files, script editor, etc)
        self._logging_level = logging.WARNING

        table_model = UiLoggerModel(self, self._logging_records)
        table_proxy_model = UiLoggerProxyModel(self)
        table_proxy_model.setSourceModel(table_model)
        table_proxy_model.setDynamicSortFilter(False)
        self.ui.tableView_logs.setModel(table_proxy_model)
        #self.ui.tableView_logs.setModel(self._table_log_model)

        self.ui.tableView_logs.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.tableView_logs.horizontalHeader().setStretchLastSection(True)

        self.create_logger_handler()
        log.info('Opened OMTK GUI')

        #
        # First update
        #

        self.import_networks()
        self.update_ui()

        #
        # Connect events
        #

        self.ui.actionBuild.triggered.connect(self.on_build)
        self.ui.actionUnbuild.triggered.connect(self.on_unbuild)
        self.ui.actionRebuild.triggered.connect(self.on_rebuild)
        self.ui.actionImport.triggered.connect(self.on_import)
        self.ui.actionExport.triggered.connect(self.on_export)
        self.ui.actionUpdate.triggered.connect(self.on_update)
        self.ui.actionCreateModule.triggered.connect(self.on_btn_add_pressed)
        self.ui.actionMirrorJntsLToR.triggered.connect(self.on_mirror_influences_l_to_r)
        self.ui.actionMirrorJntsRToL.triggered.connect(self.on_mirror_influences_r_to_l)
        self.ui.actionMirrorSelection.triggered.connect(self.on_mirror_selection)
        self.ui.actionAddNodeToModule.triggered.connect(self.on_addToModule)
        self.ui.actionRemoveNodeFromModule.triggered.connect(self.on_removeFromModule)
        self.ui.actionSelectGrpMeshes.triggered.connect(self.on_SelectGrpMeshes)
        self.ui.actionUpdateModulesView.triggered.connect(self.update_ui_modules)
        self.ui.actionUpdateInfluencesView.triggered.connect(self.update_ui_jnts)
        self.ui.actionUpdateMeshesView.triggered.connect(self.update_ui_meshes)
        self.ui.actionChangeLogLevel.triggered.connect(self.update_log_search_level)
        self.ui.actionUpdateLogSearchQuery.triggered.connect(self.update_log_search_query)
        self.ui.actionClearLogs.triggered.connect(self.on_log_clear)
        self.ui.actionSaveLogs.triggered.connect(self.on_log_save)
        self.ui.actionShowPluginManager.triggered.connect(self.on_show_pluginmanager)

        self.ui.treeWidget.itemSelectionChanged.connect(self.on_module_selection_changed)
        self.ui.treeWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ui.treeWidget.itemChanged.connect(self.on_module_changed)
        self.ui.treeWidget.itemDoubleClicked.connect(self.on_module_double_clicked)
        self.ui.treeWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ui.treeWidget.focusInEvent = self.focus_in_module
        self.ui.treeWidget.setAutoFillBackground(True)
        self.ui.treeWidget.setStyleSheet(self._STYLE_SHEET)

        self.ui.treeWidget_jnts.setStyleSheet(self._STYLE_SHEET)
        self.ui.treeWidget_jnts.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ui.treeWidget_jnts.itemSelectionChanged.connect(self.on_influence_selection_changed)
        self.ui.treeWidget_meshes.itemSelectionChanged.connect(self.on_mesh_selection_changed)

        self.ui.lineEdit_search_jnt.textChanged.connect(self.on_query_changed)
        self.ui.lineEdit_search_modules.textChanged.connect(self.on_module_query_changed)
        self.ui.lineEdit_search_meshes.textChanged.connect(self.on_meshes_query_changed)
        self.ui.checkBox_hideAssigned.stateChanged.connect(self.on_query_changed)

        # Right click menu
        self.ui.treeWidget_jnts.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.ui.treeWidget_jnts, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.on_btn_add_pressed)

        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.ui.treeWidget, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.on_context_menu_request)

        self.callbacks_events = []
        self.callbacks_scene = []
        self.callbacks_nodes = None

        self.create_callbacks()

    def create_callbacks(self):
        self.remove_callbacks()
        # Disable to prevent performance drop when CTRL-Z and the tool is open
        # TODO - Reactivate back when the tool will be stable ?
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
    def _can_build(self, data, verbose=True):
        validate_message = None
        try:
            if isinstance(data, classRig.Rig):
                data.validate()
            elif isinstance(data, classModule.Module):
                data.validate(self.root)
            else:
                raise Exception("Unexpected datatype {0} for {1}".format(type(data), data))
        except Exception, e:
            if verbose:
                validate_message  = str(e)
                pymel.warning("{0} failed validation: {1}".format(data, str(e)))
            return False, validate_message
        return True, validate_message

    _color_invalid = QtGui.QBrush(QtGui.QColor(255, 45, 45))
    _color_valid = QtGui.QBrush(QtGui.QColor(45, 45, 45))
    _color_locked = QtGui.QBrush(QtGui.QColor(125, 125, 125))

    def _set_QTreeWidgetItem_color(self, qItem, module):
        desired_color = None

        # Set QTreeWidgetItem gray if the module fail validation
        if isinstance(module, classModule.Module) and module.locked:
            return self._color_locked

        # Set QTreeWidgetItem red if the module fail validation
        can_build, validation_message = self._can_build(module, verbose=True)
        if not can_build:
            desired_color = self._color_invalid
            msg = 'Validation failed for {0}: {1}'.format(module, validation_message)
            log.warning(msg)
            qItem.setToolTip(0, msg)

        if desired_color:
            qItem.setBackground(0, desired_color)

    def _rig_to_tree_widget(self, module):
        qItem = QtGui.QTreeWidgetItem(0)
        if hasattr(module, '_network'):
            qItem.net = module._network
        else:
            pymel.warning("{0} have no _network attributes".format(module))
        qItem.rig = module

        # Set label
        label = str(module)
        if isinstance(module, classModule.Module) and module.locked:
            label += ' (locked)'
        qItem.setText(0, label)

        # HACK: bypass the stylecheet
        # see: http://forum.qt.io/topic/22219/item-view-stylesheet-bgcolor/12
        # style_sheet_invalid = """
        # QTreeView::item
        # {
        #   background-color: rgb(45,45,45);
        # }"""
        self._set_QTreeWidgetItem_color(qItem, module)

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
        return libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint) or libPymel.isinstance_of_shape(obj,
                                                                                                            pymel.nodetypes.NurbsSurface)

    def _set_icon_from_type(self, obj, qItem):
        if isinstance(obj, pymel.nodetypes.Joint):
            qItem.setIcon(0, QtGui.QIcon(":/pickJointObj.png"))
        elif isinstance(obj, pymel.nodetypes.Transform):
            self._set_icon_from_type(obj.getShape(), qItem)
        elif isinstance(obj, pymel.nodetypes.NurbsCurve):
            qItem.setIcon(0, QtGui.QIcon(":/nurbsCurve.svg"))
        elif isinstance(obj, pymel.nodetypes.NurbsSurface):
            qItem.setIcon(0, QtGui.QIcon(":/nurbsSurface.svg"))
        elif isinstance(obj, pymel.nodetypes.Mesh):
            qItem.setIcon(0, QtGui.QIcon(":/mesh.svg"))
        else:
            qItem.setIcon(0, QtGui.QIcon(":/question.png"))

    def _fill_widget_influences(self, qt_parent, data):
        obj = pymel.PyNode(data.val) if data.val else None
        #obj, children_data = data
        if obj:
            obj_name = obj.stripNamespace()

            fnFilter = lambda x: libSerialization.isNetworkInstanceOfClass(x, 'Module')
            networks = libSerialization.getConnectedNetworks(obj, key=fnFilter)

            textBrush = QtGui.QBrush(QtCore.Qt.white)

            if self._is_influence(obj):  # todo: listen to the Rig class
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

        for child_data in data.children:
            self._fill_widget_influences(qt_parent, child_data)
        #for child_data in children_data:
            #child = child_data[0]
            #if isinstance(child, pymel.nodetypes.Transform):
                #self._fill_widget_influences(qt_parent, child_data)

    def _fill_widget_meshes(self, qt_parent, mesh, influences):
        textBrush = QtGui.QBrush(QtCore.Qt.white)

        # Add mesh
        item_mesh = QtGui.QTreeWidgetItem(0)
        item_mesh.setText(0, str(mesh))
        item_mesh.setForeground(0, textBrush)
        self._set_icon_from_type(mesh.getParent(), item_mesh)
        qt_parent.addChild(item_mesh)

        # Monkey-patch mesh QWidget
        item_mesh.metadata_type = MetadataType.Mesh
        item_mesh.metadata_data = mesh

        # Add influences
        if influences:
            for influence in influences:
                item = QtGui.QTreeWidgetItem(0)
                item.setText(0, str(influence))
                item.setForeground(0, textBrush)
                self._set_icon_from_type(influence, item)
                item_mesh.addChild(item)

                # Monkey-patch influence QWidget
                item.metadata_type = MetadataType.Influece
                item.metadata_data = influence

    def _show_parent_recursive(self, qt_parent_item):
        if qt_parent_item is not None:
            if qt_parent_item.isHidden:
                qt_parent_item.setHidden(False)
            self._show_parent_recursive(qt_parent_item.parent())

    def _can_show_QTreeWidgetItem(self, qItem, query_regex):
        obj = qItem.obj  # Retrieve monkey-patched data
        obj_name = obj.stripNamespace()
        # print obj_name

        if not re.match(query_regex, obj_name, re.IGNORECASE):
            return False

        if self.ui.checkBox_hideAssigned.isChecked():
            if qItem.networks:
                return False

        return True

    def _update_network(self, module, item=None):
        if hasattr(module, "_network"):
            pymel.delete(module._network)
        new_network = libSerialization.export_network(module)  # TODO : Automatic update
        # If needed, update the network item net property to match the new exported network
        if item:
            item.net = new_network

    # Block signals need to be called in a function because if called in a signal, it will block it
    def _set_text_block(self, item, str):
        self.ui.treeWidget.blockSignals(True)
        if hasattr(item, "rig"):
            item.setText(0, str)
        self.ui.treeWidget.blockSignals(False)

    def _add_part(self, cls):
        # part = _cls(pymel.selected())
        self.root.add_module(cls, pymel.selected())
        net = self.export_networks()
        pymel.select(net)
        # Add manually the Rig to the root list instead of importing back all network
        # if not self.root in self.roots:
        #    self.roots.append(self.root)
        # self.updateData()

        # Hack: Delete all cache since adding a module can push other module to validate/unvalidate.
        # ex: FaceAvarGrp need a Head module to work.
        # for module in self.root.modules:
        #     try:
        #         del module._cache
        #     except AttributeError:
        #         pass

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

    @libPython.log_execution_time('export_networks')
    def export_networks(self):
        try:
            pymel.delete(self.root._network)
        except AttributeError:
            pass

        net = libSerialization.export_network(self.root)  # Export part and only part
        return net

    #
    # Publics
    #

    # Will only refresh tree view information without removing any items
    def refresh_ui(self):
        self._refresh_ui_modules_checked()
        self._refresh_ui_modules_visibility()
        self.refresh_ui_jnts()

    # Recreate tree views items
    def update_ui(self, *args, **kwargs):
        self.update_ui_modules()
        self.update_ui_jnts()
        self.update_ui_meshes()

    def update_ui_modules(self, *args, **kwargs):
        self.ui.treeWidget.clear()
        for root in self.roots:
            qItem = self._rig_to_tree_widget(root)
            self.ui.treeWidget.addTopLevelItem(qItem)
            self.ui.treeWidget.expandItem(qItem)

        self.refresh_ui_modules()

    @libPython.log_execution_time('update_ui_jnts')
    def update_ui_jnts(self, *args, **kwargs):
        # Resolve text query
        query_raw = self.ui.lineEdit_search_jnt.text()

        self.ui.treeWidget_jnts.clear()
        all_potential_influences = self.root.get_potential_influences()

        if all_potential_influences:
            data = libPymel.get_tree_from_objs(all_potential_influences, sort=True)

            self._fill_widget_influences(self.ui.treeWidget_jnts.invisibleRootItem(), data)
            self.ui.treeWidget_jnts.sortItems(0, QtCore.Qt.AscendingOrder)

        '''
        if all_jnt_roots:
            for jnt in all_jnt_roots:
                self._fill_widget_influences_recursive(self.ui.treeWidget_jnts.invisibleRootItem(), jnt)
        '''

        self.refresh_ui_jnts()

    def update_ui_meshes(self, *args, **kwargs):
        self.ui.treeWidget_meshes.clear()
        # Hack: force cache to invalidate
        try:
            self.root.get_meshes.func.im_self.cache.clear()
        except Exception, e:
            pass
        all_meshes = self.root.get_meshes()

        if all_meshes:
            widget_root = self.ui.treeWidget_meshes.invisibleRootItem()

            for mesh in all_meshes:
                influences = None
                from omtk.libs import libSkinning
                skincluster = libSkinning.get_skin_cluster(mesh)
                if skincluster:
                    influences = sorted(skincluster.influenceObjects())

                self._fill_widget_meshes(widget_root, mesh, influences)

        self._refresh_ui_meshes_visibility()

    def refresh_ui_jnts(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search_jnt.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        unselectableBrush = QtGui.QBrush(QtCore.Qt.darkGray)
        selectableBrush = QtGui.QBrush(QtCore.Qt.white)
        for qt_item in get_all_QTreeWidgetItem(self.ui.treeWidget_jnts):
            can_show = self._can_show_QTreeWidgetItem(qt_item, query_regex)
            qt_item.setHidden(not can_show)
            if can_show:
                qt_item.setForeground(0, selectableBrush)
                flags = qt_item.flags()
                if not flags & QtCore.Qt.ItemIsSelectable:  # Make selectable
                    flags ^= QtCore.Qt.ItemIsSelectable
                    qt_item.setFlags(flags)
                self._show_parent_recursive(qt_item.parent())
            else:
                qt_item.setForeground(0, unselectableBrush)
                flags = qt_item.flags()
                if flags & QtCore.Qt.ItemIsSelectable:  # Make selectable
                    flags ^= QtCore.Qt.ItemIsSelectable
                    qt_item.setFlags(flags)

        self.ui.treeWidget_jnts.expandAll()

    def refresh_ui_modules(self):
        self._refresh_ui_modules_checked()
        self._refresh_ui_modules_visibility()

    def _refresh_ui_modules_checked(self):
        # Block the signal to make sure that the itemChanged event is not called when adjusting the check state
        self.ui.treeWidget.blockSignals(True)
        for qt_item in get_all_QTreeWidgetItem(self.ui.treeWidget):
            if hasattr(qt_item, "rig"):
                qt_item.setCheckState(0, QtCore.Qt.Checked if qt_item.rig.is_built() else QtCore.Qt.Unchecked)
        self.ui.treeWidget.blockSignals(False)

    def _refresh_ui_modules_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search_modules.text()
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

        # unselectableBrush = QtGui.QBrush(QtCore.Qt.darkGray)
        # selectableBrush = QtGui.QBrush(QtCore.Qt.white)
        for qt_item in get_all_QTreeWidgetItem(self.ui.treeWidget):
            can_show = fn_can_show(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    def _refresh_ui_meshes_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search_meshes.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        def fn_can_show(qItem, query_regex):
            if qItem.metadata_type == MetadataType.Influece:  # Always show influences
                return True

            return not query_regex or re.match(query_regex, qItem.text(0), re.IGNORECASE)

        for qt_item in get_all_QTreeWidgetItem(self.ui.treeWidget_meshes):
            can_show = fn_can_show(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    def _build_module(self, module):
        if module.locked:
            pymel.warning("Can't build locked module {0}".format(module))
            return

        self.root.pre_build()
        module.build(self.root)
        self.root.post_build_module(module)

        return True

    def _unbuild_module(self, module):
        if module.locked:
            pymel.warning("Can't unbuild locked module {0}".format(module))
            return

        module.unbuild(self.root)

        return True

    def _build(self, val):
        if val.is_built():
            pymel.warning("Can't build {0}, already built.".format(val))
            return

        try:
            if isinstance(val, classModule.Module):
                self._build_module(val)
            elif isinstance(val, classRig.Rig):
                val.build()
            else:
                raise Exception("Unexpected datatype {0} for {1}".format(type(val), val))
        except Exception, e:
            log.error("Error building {0}. Received {1}. {2}".format(val, type(e).__name__, str(e).strip()))
            traceback.print_exc()

    def _unbuild(self, val):
        if not val.is_built():
            pymel.warning("Can't unbuild {0}, already unbuilt.".format(val))
            return

        try:
            if isinstance(val, classModule.Module):
                self._unbuild_module(val)
            elif isinstance(val, classRig.Rig):
                val.unbuild()
            else:
                raise Exception("Unexpected datatype {0} for {1}".format(type(val), val))
        except Exception, e:
            log.error("Error building {0}. Received {1}. {2}".format(val, type(e).__name__, str(e).strip()))
            traceback.print_exc()

    #
    # Events
    #

    def on_build(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.rig
            self._build(val)
        self._update_network(self.root)
        self.update_ui()

    def on_unbuild(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.rig
            self._unbuild(val)
        self._update_network(self.root)
        self.update_ui()

    def on_rebuild(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.rig
            self._unbuild(val)
            self._build(val)
        self._update_network(self.root)

    def on_lock(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item.rig
            if isinstance(val, classModule.Module) and not val.locked:
                need_update = True
                val.locked = True
        if need_update:
            self._update_network(self.root)
            self.update_ui_modules()

    def on_unlock(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item.rig
            if isinstance(val, classModule.Module) and val.locked:
                need_update = True
                val.locked = False
        if need_update:
            self._update_network(self.root)
            self.update_ui_modules()

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
        # TODO - Fix the reload problem which cause isinstance function check to fail with an existing network
        import omtk;
        reload(omtk);
        omtk._reload(kill_ui=False)
        self.import_networks()
        self.update_ui()

    def on_module_selection_changed(self):
        pymel.select([item.net for item in self.ui.treeWidget.selectedItems() if hasattr(item, 'net')])

    def on_influence_selection_changed(self):
        pymel.select([item.obj for item in self.ui.treeWidget_jnts.selectedItems() if item.obj.exists()])
        if self.ui.treeWidget_jnts.selectedItems():
            self.ui.actionCreateModule.setEnabled(True)
        else:
            self.ui.actionCreateModule.setEnabled(False)

    def on_mesh_selection_changed(self):
        pymel.select([item.metadata_data.getParent() for item in self.ui.treeWidget_meshes.selectedItems() if
                      item.metadata_data.exists()])

    def on_module_changed(self, item):
        # todo: handle exception
        # Check first if the checkbox have changed
        need_update = False
        new_state = item.checkState(0) == QtCore.Qt.Checked
        new_text = item.text(0)
        module = item.rig
        if item._checked != new_state:
            item._checked = new_state
            # Handle checkbox change
            if new_state:
                self._build(module)
            else:
                self._unbuild(module)
            need_update = True
            self._update_network(self.root, item=item)

        # Check if the name have changed
        if (item._name != new_text):
            item._name = new_text
            module.name = new_text

            # Update directly the network value instead of re-exporting it
            if hasattr(item, "net"):
                name_attr = item.net.attr("name")
                name_attr.set(new_text)

        # Ensure to only refresh the UI and not recreate all
        if need_update:
            self.refresh_ui()

    def on_query_changed(self, *args, **kwargs):
        self.refresh_ui_jnts()

    def on_module_query_changed(self, *args, **kwargs):
        self._refresh_ui_modules_visibility()

    def on_meshes_query_changed(self, *args, **kwargs):
        self._refresh_ui_meshes_visibility()

    def on_module_double_clicked(self, item):
        if hasattr(item, "rig"):
            self._set_text_block(item, item.rig.name)
            self._is_modifying = True  # Flag to know that we are currently modifying the name
            self.ui.treeWidget.editItem(item, 0)

    def on_remove(self):
        for item in self.ui.treeWidget.selectedItems():
            module = item.rig
            # net = item.net if hasattr(item, "net") else None
            try:
                if module.is_built():
                    module.unbuild(self.root)
                self.root.modules.remove(module)
            except Exception, e:
                log.error("Error building {0}. Received {1}. {2}".format(module, type(e).__name__, str(e).strip()))
                traceback.print_exc()
        self.export_networks()
        self.update_ui()

    def on_context_menu_request(self):
        if self.ui.treeWidget.selectedItems():
            menu = QtGui.QMenu()
            actionBuild = menu.addAction("Build")
            actionBuild.triggered.connect(self.on_build)
            actionUnbuild = menu.addAction("Unbuild")
            actionUnbuild.triggered.connect(self.on_unbuild)
            actionRebuild = menu.addAction("Rebuild")
            actionRebuild.triggered.connect(self.on_rebuild)
            menu.addSeparator()
            actionLock = menu.addAction("Lock")
            actionLock.triggered.connect(self.on_lock)
            action_unlock = menu.addAction("Unlock")
            action_unlock.triggered.connect(self.on_unlock)
            menu.addSeparator()
            sel = self.ui.treeWidget.selectedItems()
            if len(sel) == 1:
                actionRemove = menu.addAction("Rename")
                # actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.editItem, sel[0], 0))
                actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.itemDoubleClicked.emit, sel[0], 0))
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
                # if not inspect.ismethod(fn):
                #    return False
                return val.__can_show__()

            functions = inspect.getmembers(module, is_exposed)

            if functions:
                menu.addSeparator()
                for fn_name, fn in functions:

                    # Always pass the rig as the first argument in an exposed module function.
                    if isinstance(module, classModule.Module):
                        fn = functools.partial(fn, self.root)

                    action = menu.addAction(fn_name)
                    action.triggered.connect(fn)

            menu.exec_(QtGui.QCursor.pos())

    def on_btn_add_pressed(self):
        if self.ui.treeWidget_jnts.selectedItems():
            menu = QtGui.QMenu()

            from omtk.plugin_manager import plugin_manager
            for plugin_name, plugin_cls in sorted(plugin_manager.get_plugins('modules').iteritems()):
                if getattr(plugin_cls, 'SHOW_IN_UI', False):
                    action = menu.addAction(plugin_name)
                    action.triggered.connect(functools.partial(self._add_part, plugin_cls))

            menu.exec_(QtGui.QCursor.pos())

    def on_addToModule(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
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
        for item in self.ui.treeWidget.selectedItems():
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

    def _is_l_influence(self, root, inf):
        inf_name = inf.stripNamespace()
        nomenclature = root.nomenclature()
        nomenclature.build_from_string(inf_name)
        return nomenclature.side == nomenclature.SIDE_L

    def _is_r_influence(self, root, inf):
        inf_name = inf.stripNamespace()
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

    def on_mirror_influences_r_to_l(self):
        objs = self._get_r_influences()
        if not objs:
            pymel.warning('No joints found!')
            return
        libSkeleton.mirror_jnts(objs)

    def on_mirror_selection(self):
        objs = pymel.selected(type='joint')
        if not objs:
            pymel.warning('No joints found!')
            return
        libSkeleton.mirror_jnts(objs)

    def on_SelectGrpMeshes(self):
        grp = self.root.grp_geo
        if not grp or not grp.exists():
            pymel.warning("Can't find influence grp!")
        else:
            pymel.select(grp)

    def focus_in_module(self, event):
        # Set back the text with the information about the module in it
        if self._is_modifying:
            sel = self.ui.treeWidget.selectedItems()
            if sel:
                self._set_text_block(sel[0], str(sel[0].rig))
                # sel[0].setText(0, str(sel[0].rig))
            self._is_modifying = False
        self.focusInEvent(event)

    #
    # Logging implementation
    #

    def create_logger_handler(self):
        class QtHandler(logging.Handler):
            def __init__(self):
                logging.Handler.__init__(self)

            def emit(self_, record):
                self._logging_records.append(record)
                self.ui.tableView_logs.model().reset()

        handler = QtHandler()

        # handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
        self._logging_handlers.append(handler)

    def remove_logger_handler(self):
        if self._logging_handlers:
            for handler in self._logging_handlers:
                log.removeHandler(handler)
            self._logging_handlers = []

    def update_log_search_query(self):
        query = self.ui.lineEdit_log_search.text()
        self.ui.tableView_logs.model().set_log_query(query)

    def update_log_search_level(self):
        index = self.ui.comboBox_log_level.currentIndex()
        model = self.ui.tableView_logs.model()
        if index == 0:
            model.set_loglevel_filter(logging.ERROR)
        elif index == 1:
            model.set_loglevel_filter(logging.WARNING)
        elif index == 2:
            model.set_loglevel_filter(logging.INFO)
        elif index == 3:
            model.set_loglevel_filter(logging.DEBUG)

    def _save_logs(self, path):
        with open(path, 'w') as fp:
            # Write header
            fp.write('Date,Level,Message\n')

            # Write content
            for record in self._logging_records:
                fp.write('{0},{1},{2}\n'.format(
                    str(datetime.datetime.fromtimestamp(record.created)),
                    log_level_to_str(record.levelno),
                    record.message
                ))

    def on_log_save(self):
        default_name = datetime.datetime.now().strftime("%Y-%m-%d-%Hh%Mm%S")
        if self.root:
            default_name = '{0}_{1}'.format(default_name, self.root.name)

        path, _ = QtGui.QFileDialog.getSaveFileName(self, "Save logs", '{0}.log'.format(default_name), ".log")
        if path:
            self._save_logs(path)

    def on_log_clear(self):
        del self._logging_records[:]
        self.ui.tableView_logs.model().reset()

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

        self.remove_logger_handler()
        self.remove_callbacks()
        # Sometime calling the super close event cause this event :
        # TypeError: super(type, obj): obj must be an instance or subtype of type
        try:
            super(AutoRig, self).closeEvent(*args, **kwargs)
        except:
            pass

        #
        # Logger handling
        #

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
