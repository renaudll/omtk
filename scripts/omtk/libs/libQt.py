"""
Qt related helper methods
"""
from omtk.vendor.Qt import QtWidgets


def get_all_QTreeWidgetItem(widget, qt_item=None):
    """
    Iterate through all items of a provided QTreeWidgetItem.
    :param widget: The QTreeWidgetItem to iterate through.
    :param qt_item: The starting point of the iteration. If nothing is provided the invisibleRootItem will be used.
    :return: A generator that yield QTreeWidgetItem
    :rtype Generator of QtWidgets.QTreeWidgetItem
    """
    if qt_item is None:
        qt_item = widget.invisibleRootItem()

    num_child = qt_item.childCount()
    for i in reversed(range(num_child)):
        qt_sub_item = qt_item.child(i)
        yield qt_sub_item
        for x in get_all_QTreeWidgetItem(widget, qt_sub_item):
            yield x


def get_maya_window():
    """
    :return : Maya main window
    :rtype: QtWidgets.QWidget
    """
    for obj in QtWidgets.QApplication.instance().topLevelWidgets():
        if obj.objectName() == "MayaWindow":
            return obj
    raise RuntimeError("Could not find MayaWindow instance")


def center_window(gui):
    """
    Move a window to the center of the screen.

    :param gui: A window
    :type gui: QtWidgets.QMainWindow
    """
    frame = gui.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(
        QtWidgets.QApplication.desktop().cursor().pos()
    )
    center = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frame.moveCenter(center)
    gui.move(frame.topLeft())
