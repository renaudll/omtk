import re
import pymel.core as pymel
from omtk.widgets.ui import widget_list_meshes

from omtk.libs import libSkinning
from omtk.libs import libQt
from omtk.widgets import _utils
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets


class WidgetListMeshes(QtWidgets.QWidget):
    _TEXT_BRUSH = QtGui.QBrush(QtCore.Qt.white)

    def __init__(self, parent=None):
        super(WidgetListMeshes, self).__init__(parent=parent)

        self._rig = None

        self.ui = widget_list_meshes.Ui_Form()
        self.ui.setupUi(self)

        # Connect events
        self.ui.treeWidget.itemSelectionChanged.connect(self.on_mesh_selection_changed)
        self.ui.lineEdit_search.textChanged.connect(self.on_meshes_query_changed)
        self.ui.pushButton_selectGrpMeshes.pressed.connect(self.on_SelectGrpMeshes)
        self.ui.btn_update.pressed.connect(self.update)

    def set_rig(self, rig, update=True):
        self._rig = rig
        if update:
            self.update_list()

    def update_list(self):
        self.ui.treeWidget.clear()

        if self._rig is None:
            return

        all_meshes = self._rig.get_shapes()

        if all_meshes:
            root = self.ui.treeWidget.invisibleRootItem()

            for mesh in all_meshes:
                influences = []

                skincluster = libSkinning.get_skin_cluster(mesh)
                if skincluster:
                    influences = sorted(
                        libSkinning.get_skin_cluster_influence_objects(skincluster)
                    )

                self._fill_widget_meshes(root, mesh, influences)

        self.update_list_visibility()

    def _fill_widget_meshes(self, qt_parent, mesh, influences):
        # Add mesh
        item_mesh = self._create_item_mesh(mesh)
        qt_parent.addChild(item_mesh)

        # Add influences
        for influence in influences:
            item = self._create_item_influence(influence)
            item_mesh.addChild(item)

    def _create_item_mesh(self, mesh):
        """
        Create a QTreeWidgetItem for an influence.

        :param influence: An influence object.
        :type influence: pymel.nodetypes.Transform
        :return: A Qt tree item
        :rtype: QtWidgets.QTreeWidgetItem
        """
        item = QtWidgets.QTreeWidgetItem(0)
        item.setText(0, str(mesh))
        item.setForeground(0, self._TEXT_BRUSH)
        _utils.set_icon_from_type(mesh.getParent(), item)

        # Monkey-patch mesh QWidget
        item.metadata_type = _utils.MetadataType.Mesh
        item.metadata_data = mesh

        return item

    def _create_item_influence(self, influence):
        """
        Create a QTreeWidgetItem for an influence.

        :param influence: An influence object.
        :type influence: pymel.nodetypes.Transform
        :return: A Qt tree item
        :rtype: QtWidgets.QTreeWidgetItem
        """
        item = QtWidgets.QTreeWidgetItem(0)
        item.setText(0, str(influence))
        item.setForeground(0, self._TEXT_BRUSH)
        _utils.set_icon_from_type(influence, item)

        # Monkey-patch influence QWidget
        item.metadata_type = _utils.MetadataType.Influence
        item.metadata_data = influence

        return item

    def update_list_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*%s.*" % query_raw if query_raw else ".*"

        def fn_can_show(qItem, query_regex):
            if (
                qItem.metadata_type == _utils.MetadataType.Influence
            ):  # Always show influences
                return True

            return not query_regex or re.match(
                query_regex, qItem.text(0), re.IGNORECASE
            )

        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            can_show = fn_can_show(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    def get_selection(self):
        result = []
        for item in self.ui.treeWidget.selectedItems():
            if item.metadata_data.exists():
                result.append(item.metadata_data.getParent())
        return result

    #
    # Events
    #

    def on_mesh_selection_changed(self):
        pymel.select(self.get_selection())

    def on_meshes_query_changed(self, *args, **kwargs):
        self.update_list_visibility()

    def on_SelectGrpMeshes(self):
        grp = self._rig.grp_geo
        if not grp or not grp.exists():
            pymel.warning("Can't find influence grp!")
        else:
            pymel.select(grp)
