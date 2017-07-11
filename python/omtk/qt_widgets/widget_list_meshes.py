import re
import pymel.core as pymel
from omtk.ui import widget_list_meshes

from omtk.libs import libSkinning
from omtk.libs import libQt

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

import omtk.ui_shared


class WidgetListMeshes(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WidgetListMeshes, self).__init__(parent=parent)

        self._rig = None

        self.ui = widget_list_meshes.Ui_Form()
        self.ui.setupUi(self)

        # Connect events
        self.ui.treeWidget.itemSelectionChanged.connect(self.on_mesh_selection_changed)
        self.ui.lineEdit_search.textChanged.connect(self.on_meshes_query_changed)
        self.ui.btn_update.pressed.connect(self.update)

    def set_rig(self, rig, update=True):
        self._rig = rig
        if update:
            self.update_list()

    def update_list(self):
        self.ui.treeWidget.clear()

        if self._rig is None:
            return

        # Hack: force cache to invalidate
        # try:
        #     self._rig.get_meshes.func.im_self.cache.clear()
        # except Exception, e:
        #     pass
        all_meshes = self._rig.get_shapes()

        if all_meshes:
            widget_root = self.ui.treeWidget.invisibleRootItem()

            for mesh in all_meshes:
                influences = None

                skincluster = libSkinning.get_skin_cluster(mesh)
                if skincluster:
                    influences = sorted(skincluster.influenceObjects())

                self._fill_widget_meshes(widget_root, mesh, influences)

        self.update_list_visibility()

    def _fill_widget_meshes(self, qt_parent, mesh, influences):
        textBrush = QtGui.QBrush(QtCore.Qt.white)

        # Add mesh
        item_mesh = QtWidgets.QTreeWidgetItem(0)
        item_mesh.setText(0, str(mesh))
        item_mesh.setForeground(0, textBrush)
        omtk.ui_shared._set_icon_from_type(mesh.getParent(), item_mesh)
        qt_parent.addChild(item_mesh)

        # Monkey-patch mesh QWidget
        item_mesh._meta_data_type = omtk.ui_shared.MimeTypes.Mesh
        item_mesh._meta_data_data = mesh

        # Add influences
        if influences:
            for influence in influences:
                item = QtWidgets.QTreeWidgetItem(0)
                item.setText(0, str(influence))
                item.setForeground(0, textBrush)
                omtk.ui_shared._set_icon_from_type(influence, item)
                item_mesh.addChild(item)

                # Monkey-patch influence QWidget
                item._meta_data_type = omtk.ui_shared.MimeTypes.Influence
                item._meta_data_data = influence

    def update_list_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        def fn_can_show(qItem, query_regex):
            if qItem._meta_data_type == omtk.ui_shared.MimeTypes.Influence:  # Always show influences
                return True

            return not query_regex or re.match(query_regex, qItem.text(0), re.IGNORECASE)

        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            can_show = fn_can_show(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    def get_selection(self):
        result = []
        for item in self.ui.treeWidget.selectedItems():
            if item._meta_data_data.exists():
                result.append(item._meta_data_data.getParent())
        return result

    #
    # Events
    #

    def on_mesh_selection_changed(self):
        pymel.select(self.get_selection())

    def on_meshes_query_changed(self, *args, **kwargs):
        self.update_list_visibility()
