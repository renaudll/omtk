from omtk.vendor.Qt import QtCore, QtWidgets

def _set_tree_widget_item_expanded_recursively(item, state):
    if item.isExpanded() != state:
        item.setExpanded(state)
    num_children = item.childCount()
    for i in xrange(num_children):
        child = item.child(i)
        _set_tree_widget_item_expanded_recursively(child, state)


class WidgetComponentTree(QtWidgets.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super(WidgetComponentTree, self).__init__(*args, **kwargs)
        self.itemExpanded.connect(self._on_item_expanded)
        self.itemCollapsed.connect(self._on_item_collapsed)

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

    def mousePressEvent(self, event):
        """Ensure right-clicking don't change the selection."""
        # todo: make it work or remove it!
        if event.button() == QtCore.Qt.RightButton:
            super(WidgetComponentTree, self).mousePressEvent(event)
            self.customContextMenuRequested.emit(event.pos())
        else:
            super(WidgetComponentTree, self).mousePressEvent(event)
