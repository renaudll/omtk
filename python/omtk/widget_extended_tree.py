from omtk.vendor.Qt import QtCore, QtWidgets
from omtk.vendor import libSerialization

def _set_tree_widget_item_expanded_recursively(item, state):
    if item.isExpanded() != state:
        item.setExpanded(state)
    num_children = item.childCount()
    for i in xrange(num_children):
        child = item.child(i)
        _set_tree_widget_item_expanded_recursively(child, state)


# todo: remove to ExtendedTreeWidget
class WidgetExtendedTree(QtWidgets.QTreeWidget):
    """
    Customization on top of the standard QTreeWidget to match Maya behavior.
    - Ctrl-click will recursively expand/collapse items.
    - Implement drag signals.
    """
    # todo: ensure that events are bound per instances
    dragEnter = QtCore.Signal(object)
    dragLeave = QtCore.Signal(object)
    dragDrop = QtCore.Signal(object)

    # onDragMove = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        self._mime_data = None  # hack: prevent gc to destroy our mimeData during dragging...
        super(WidgetExtendedTree, self).__init__(*args, **kwargs)
        self.itemExpanded.connect(self._on_item_expanded)
        self.itemCollapsed.connect(self._on_item_collapsed)
        self.setAcceptDrops(True)

    def _on_item_expanded(self, item):
        """Recursively expand sub-items if the shift key is pressed."""
        if QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ShiftModifier:
            _set_tree_widget_item_expanded_recursively(item, True)
        else:
            # Extra: If no metadata is associated with the item, it is an intermediate item, expand it.
            num_children = item.childCount()
            for i in xrange(num_children):
                child = item.child(i)
                if not hasattr(child, 'metadata') and not child.isExpanded():
                    child.setExpanded(True)

    def _on_item_collapsed(self, item):
        """Recursively collapse sub-items if the shift key is pressed."""
        if QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ShiftModifier:
            _set_tree_widget_item_expanded_recursively(item, False)

    # def mousePressEvent(self, event):
    #     """Ensure right-clicking don't change the selection."""
    #     # todo: make it work or remove it!
    #     if event.button() == QtCore.Qt.RightButton:
    #         # super(WidgetExtendedTree, self).mousePressEvent(event)
    #         self.customContextMenuRequested.emit(event.pos())
    #     else:
    #         super(WidgetExtendedTree, self).mousePressEvent(event)

    # --- drag and drop support ---

    def dropMimeData(self, parent, index, data, action):
        print parent, index, data, action
        return True

    def dragEnterEvent(self, event):
        event.accept()
        self.dragEnter.emit(event)

    def dragLeaveEvent(self, event):
        super(WidgetExtendedTree, self).dragLeaveEvent(event)
        self.dragLeave.emit(event)

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        super(WidgetExtendedTree, self).dropEvent(event)
        self.dragDrop.emit(event)

    def mimeTypes(self):
        return ['omtk-influences']

    def mimeData(self, items):
        print "WidgetExtendedTree::mimeData"
        # todo: generic class for our custom TreeWidgetItem?
        text = ','.join([str(id(item.obj)) for item in items])
        self._mimedata = QtCore.QMimeData()
        self._mimedata.setData('omtk', text)
        return self._mimedata
