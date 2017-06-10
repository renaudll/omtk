# a simple alias
from omtk.vendor.Qt import QtWidgets
from ui import widget_node_editor


class WidgetNodeEditor(QtWidgets.QWidget):
    def __init__(self, parent):
        super(WidgetNodeEditor, self).__init__(parent)
        self.ui = widget_node_editor.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.pressed.connect(self.on_add)
        self.ui.pushButton_2.pressed.connect(self.on_del)

    def on_add(self):
        raise NotImplementedError

    def on_del(self):
        graph = self.ui.widget
        graph.deleteSelectedNodes()

# from pyflowgraph.graph_view import GraphView as WidgetNodeEditor
