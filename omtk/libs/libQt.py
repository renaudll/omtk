import imp

def _does_module_exist(_name):
	try:
		imp.find_module(_name)
		return True
	except ImportError:
		return False

use_pyqt4 = _does_module_exist('PyQt4')
use_pyside = _does_module_exist('PySide')

# Import QtCore, QtGui & uic
if use_pyqt4:
	import PyQt4
	import uic
	QtCore = PyQt4.QtCore
	QtGui = PyQt4.QtGui
elif use_pyside:
	import PySide
	import shiboken
	QtCore = PySide.QtCore
	QtGui = PySide.QtGui
	uic = shiboken
else:
	raise Exception
