import re

import omtk.ui_shared
import pymel.core as pymel
from omtk.libs import libQt
from omtk.libs import libSkinning
from omtk.qt_widgets.ui import widget_list_meshes
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
from . import widget_list_base


class WidgetListMeshes(widget_list_base.OmtkBaseListWidget):
    def __init__(self, parent=None):
        super(WidgetListMeshes, self).__init__(parent=parent)

        self._rig = None

    def set_rig(self, rig, update=True):
        self._rig = rig
        if update:
            self.update_list()

    def iter_values(self):
        for obj in pymel.ls(type='mesh'):
            yield obj

    def get_treewidgetitem_from_value(self, value):
        item = super(WidgetListMeshes, self).get_treewidgetitem_from_value(value)
        self._get_treewidget_item_from_mesh(item, value)
        return item

    def update_list(self):
        print('!')
        self.ui.treeWidget.clear()

        # Hack: force cache to invalidate
        # try:
        #     self._rig.get_meshes.func.im_self.cache.clear()
        # except Exception, e:
        #     pass
        all_meshes = self._rig.get_shapes()

        if all_meshes:
            widget_root = self.ui.treeWidget.invisibleRootItem()

            for mesh in all_meshes:
                i

        self.update_list_visibility()

    def _get_treewidget_item_from_mesh(self, root, mesh):
        influences = None

        skincluster = libSkinning.get_skin_cluster(mesh)
        if skincluster:
            influences = sorted(skincluster.influenceObjects())
        else:
            return

        self._fill_widget_meshes(root, mesh, influences)

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

        return item_mesh

    """
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

    """

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
