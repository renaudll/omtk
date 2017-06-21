# a simple alias
from omtk.libs import libPyflowgraph
from omtk.vendor.Qt import QtWidgets
from ui import widget_node_editor



class WidgetNodeEditor(QtWidgets.QWidget):
    def __init__(self, parent):
        super(WidgetNodeEditor, self).__init__(parent)
        self.ui = widget_node_editor.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.pressed.connect(self.on_add)
        self.ui.pushButton_2.pressed.connect(self.on_del)

        self.ui.widget.endSelectionMoved.connect(self.on_selected_nodes_moved)

    def on_selected_nodes_moved(self):
        for node in self.ui.widget.getSelectedNodes():
            if node._meta_data:
                new_pos = node.pos()  # for x reason, .getGraphPos don't work here
                new_pos = (new_pos.x(), new_pos.y())
                libPyflowgraph.save_node_position(node, new_pos)

    def on_add(self):
        raise NotImplementedError

    def on_del(self):
        graph = self.ui.widget
        graph.deleteSelectedNodes()

# from pyflowgraph.graph_view import GraphView as WidgetNodeEditor
