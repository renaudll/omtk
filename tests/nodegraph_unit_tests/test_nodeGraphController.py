from unittest import TestCase
from omtk.vendor import mock
from omtk_test import NodeGraphTestCase
from omtk.nodegraph import NodeGraphController, GraphModel

class TestNodeGraphController(NodeGraphTestCase):

    # def test_get_root_model(self):
    #     self.fail()
    #
    # def test_get_nodes(self):
    #     self.fail()
    #
    # def test_get_ports(self):
    #     self.fail()
    #
    # def test_get_model(self):
    #     self.fail()

    def test_set_model(self):
        """Validate that the model we set is the model we get."""
        model = GraphModel(self.registry)
        self.ctrl.set_model(model)
        self.assertIs(model, self.ctrl.get_model())

    def test_set_view(self):
        """Validate that the view we set is the view we get."""
        view = mock.MagicMock()
        self.ctrl.set_view(view)
        self.assertIs(view, self.ctrl.get_view())

    def test_set_filter(self):
        self.fail()

    def test_set_registry(self):
        self.fail()

    def test_get_registry(self):
        self.fail()

    def test__get_port_models_from_connection(self):
        self.fail()

    def test_reset_view(self):
        self.fail()

    def test_collapse_node_attributes(self):
        self.fail()

    def test_iter_node_connections(self):
        self.fail()

    def test_expand_node_connections(self):
        self.fail()

    def test_get_node_widget(self):
        self.fail()

    def test_get_port_widget(self):
        self.fail()

    def test_get_connection_widget(self):
        self.fail()

    def test_is_node_in_view(self):
        self.fail()

    def test_is_port_in_view(self):
        self.fail()

    def test_is_connection_in_view(self):
        self.fail()

    def test_add_node_to_view(self):
        self.fail()

    def test_remove_node_from_view(self):
        self.fail()

    def test_add_port_to_view(self):
        self.fail()

    def test_remove_port_from_view(self):
        self.fail()

    def test_add_connection_to_view(self):
        self.fail()

    def test_remove_connection_from_view(self):
        self.fail()

    def test_on_node_draged_in(self):
        self.fail()

    def test_on_selected_nodes_moved(self):
        self.fail()

    def test_add_nodes(self):
        self.fail()

    def test_add_node(self):
        self.fail()

    def test_remove_node(self):
        self.fail()

    def test_rename_node(self):
        self.fail()

    def test_delete_node(self):
        self.fail()

    def test_get_selected_node_models(self):
        self.fail()

    def test_get_selected_values(self):
        self.fail()

    def test_clear(self):
        self.fail()

    def test_get_level(self):
        self.fail()

    def test_set_level(self):
        self.fail()

    def test_on_right_click(self):
        self.fail()

    def test_add_maya_selection_to_view(self):
        self.fail()

    def test_remove_maya_selection_from_view(self):
        self.fail()

    def test_delete_selected_nodes(self):
        self.fail()

    def test_duplicate_selected_nodes(self):
        self.fail()

    def test_select_all_nodes(self):
        self.fail()
