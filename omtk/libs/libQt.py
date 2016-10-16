import os
import time

from maya import OpenMayaUI

from omtk.libs import libPython

use_pyside = libPython.does_module_exist('PySide')
use_pyqt4 = libPython.does_module_exist('PyQt4')

print 'pyqt4' if use_pyqt4 else 'pyside'

# Import QtCore, QtGui & uic
if use_pyqt4:
    import sip
    from PyQt4 import QtCore, QtGui

    getMayaWindow = lambda: sip.wrapinstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtCore.QObject)

elif use_pyside:
    from PySide import QtCore, QtGui
    import shiboken

    uic = shiboken
    getMayaWindow = lambda: shiboken.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtGui.QWidget)


# Return true if the .py associated with a .ui file is older or doesn't exist.
def _can_compile_ui(path):
    ui_dir = os.path.basedir(path)
    ui_name, ui_ext = os.path.splitext(path)
    assert (ui_ext == '.ui')

    uic_path = os.path.join(ui_dir, '{0}.py'.format(ui_name))
    if not os.path.exist(uic_path): return True

    # Compile .ui only if more recent than the .py
    timestamp_ui = time.ctime(os.path.getmtime(path))
    timestamp_uic = time.ctime(os.path.getmtime(uic_path))

    return timestamp_ui > timestamp_uic


def compile_ui(path):
    if _can_compile_ui(path):
        print 'Compile ui!'


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
