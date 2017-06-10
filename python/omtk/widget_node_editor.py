# a simple alias
from omtk.vendor.Qt import QtWidgets
from ui import widget_node_editor


class WidgetNodeEditor(QtWidgets.QWidget):
    def __init__(self, parent):
        super(WidgetNodeEditor, self).__init__(parent)
        self.ui = widget_node_editor.Ui_Form()
        self.ui.setupUi(self)

# from pyflowgraph.graph_view import GraphView as WidgetNodeEditor
