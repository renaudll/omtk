import imp
from maya import OpenMayaUI

def _does_module_exist(_name):
	try:
		imp.find_module(_name)
		return True
	except ImportError:
		return False

use_pyqt4 = _does_module_exist('PyQt4')
use_pyside = _does_module_exist('PySide')

print 'pyqt4' if use_pyqt4 else 'pyside'

# Import QtCore, QtGui & uic
if use_pyqt4:
	import sip
	from PyQt4 import QtCore, QtGui
	getMayaWindow = lambda: sip.wrapinstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtCore.QObject)

elif use_pyside:
	import PySide
	import shiboken
	QtCore = PySide.QtCore
	QtGui = PySide.QtGui
	uic = shiboken
	getMayaWindow = lambda: shiboken.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtGui.QWidget)
	raise Exception
