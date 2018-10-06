from omtk.vendor.Qt import QtCore, QtWidgets


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
        self._drag_enabled_buffer = None  # used in mousePressEvent and mouseReleaseEvent
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
        text = ','.join([str(id(item._meta_data)) for item in items])
        self._mimedata = QtCore.QMimeData()
        self._mimedata.setData('omtk', text)
        return self._mimedata

    def mousePressEvent(self, event):
        """
        Our goal is to reproduce the Maya outliner which only create drag event on middle-mouse events.
        This method will temporary disable qt drag and drop if the left-mouse button is used.
        """
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_enabled_buffer = self.dragEnabled()
            if self._drag_enabled_buffer:
                self.setDragEnabled(False)
        super(WidgetExtendedTree, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Our goal is to reproduce the Maya outliner which only create drag event on middle-mouse events.
        This method will re-enable qt drag and drop if it was disabled before.
        """
        if event.button() == QtCore.Qt.LeftButton:
            if self._drag_enabled_buffer:
                self.setDragEnabled(self._drag_enabled_buffer)
        super(WidgetExtendedTree, self).mouseReleaseEvent(event)
