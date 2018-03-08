import logging

import pymel.core as pymel

from omtk import constants
from omtk.core import preferences
from omtk.qt_widgets.nodegraph.nodegraph_filter import NodeGraphFilter

if False:
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphPortModel, NodeGraphConnectionModel

log = logging.getLogger('omtk.nodegraph')

# Hide the attributes we are ourself creating
# todo: where to put this?
_attr_name_blacklist = (
    constants.PyFlowGraphMetadataKeys.Position,
    constants.PyFlowGraphMetadataKeys.Position + 'X',
    constants.PyFlowGraphMetadataKeys.Position + 'Y',
    constants.PyFlowGraphMetadataKeys.Position + 'Z',
)
_g_preferences = preferences.get_preferences()


def _is_port_model_name_blacklisted(port_name):
    return port_name in _attr_name_blacklist


class NodeGraphStandardFilter(NodeGraphFilter):
    """
    Define filtering rules for a NodeGraphController.
    """

    def __init__(self):
        super(NodeGraphStandardFilter, self).__init__()
        self.hide_libserialization_network = False
        self.hide_unitconversion_node = True
        self.hide_message_attribute_type = True
        self.hide_predictable_decomposematrix_node = True

    def can_show_node(self, node_model):
        # type: (NodeGraphNodeModel) -> bool
        # Some DagNode types might be blacklisted.
        global _g_preferences
        from omtk.qt_widgets.nodegraph.models.node import node_dg

        if isinstance(node_model, node_dg.NodeGraphDgNodeModel):
            blacklist = _g_preferences.get_nodegraph_blacklisted_nodetypes()
            node = node_model.get_metadata()
            nodetype = node.type()
            if nodetype in blacklist:
                return False
        return True

    def can_show_port(self, port):
        # type: (NodeGraphPortModel) -> bool
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param port: The port to inspect.
        :return: True if we can display this port.
        """
        # Some attributes (like omtk metadata) are blacklisted by default.
        if _is_port_model_name_blacklisted(port.get_name()):
            return False

        if self.hide_message_attribute_type:
            port_data = port.get_metadata()
            # Warning: Calling .type() on an array attribute with 0 elements will create one element!
            if isinstance(port_data, pymel.Attribute) and port_data.type() == 'message':
                return False

        return port.is_interesting()

    def can_show_connection(self, connection):
        # type: (NodeGraphConnectionModel) -> bool

        port_src = connection.get_source()
        if not self.can_show_port(port_src):
            return False

        port_dst = connection.get_destination()
        if not self.can_show_port(port_dst):
            return False

        # libSerialization is leaving network everywhere.
        # Theses network are used as metadata, there's no reason we might want to see them instead for debugging.
        if self.hide_libserialization_network:
            port_dst_model = connection.get_destination()
            node_dst = port_dst_model.get_parent().get_metadata()
            if node_dst.hasAttr('_class'):
                return False
        return True

    def intercept_connection(self, connection):
        # type: (NodeGraphConnectionModel) -> NodeGraphConnectionModel
        model = self.get_model()
        registry = connection._registry
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        attr_src = port_src.get_metadata()
        attr_dst = port_dst.get_metadata()
        node_src = attr_src.node()
        node_dst = attr_dst.node()

        if self.hide_unitconversion_node:
            # Redirect anything where destination is a unitConversion.input attribute.
            if isinstance(node_dst, pymel.nodetypes.UnitConversion) and attr_dst.longName() == 'input':
                model_dst = registry.get_port_model_from_value(node_dst.output)
                for new_connection in model.get_port_output_connections(model_dst):
                    yield registry.get_connection_model_from_values(self.get_model(), new_connection.get_destination())
                return

            # Redirect anything where the source is a unitConversion.output attribute.
            if isinstance(node_src, pymel.nodetypes.UnitConversion) and attr_src.longName() == 'output':
                model_src = registry.get_port_model_from_value(node_src.input)
                for new_connection in model.get_port_input_connections(model_src):
                    yield registry.get_connection_model_from_values(new_connection.get_source(), port_dst)
                return

        if self.hide_predictable_decomposematrix_node:
            # Redirect anything where the destination is a predictable decomposeMatrix.inputMatrix attribute.
            if isinstance(node_dst, pymel.nodetypes.DecomposeMatrix) and attr_dst.longName() == 'inputMatrix':
                for real_attr_dst in self._get_decomposematrix_inputmatrix_output_connections(attr_dst):
                    new_connection = registry.get_connection_model_from_values(model, real_attr_dst)
                    yield new_connection
                return

            # Redirect anything where the source is a predictable decomposeMatrix.output[Translate/Rotate/Scale] attribute.
            if isinstance(node_src, pymel.nodetypes.DecomposeMatrix) and attr_src.longName() in (
                    'outputTranslate', 'outputRotate', 'outputScale'):
                inputmatrix_model = registry.get_port_model_from_value(node_src.attr('inputMatrix'))
                for sub_connection in model.get_port_input_connections(inputmatrix_model):
                    new_connection = self._model.get_connection_model_from_values(sub_connection.get_source(),
                                                                                  port_dst)
                    yield new_connection
                return

        yield connection

    def _get_decomposematrix_inputmatrix_output_connections(self, attr):
        """
        To call when encountering a decomposeMatrix.inputMatrix attribute.
        This is used to skip previsible decomposeMatrix in the NodeGraph.
        This will yield the inputMatrix attribute if the decomposeMatrix have non-previsible connections.
        Otherwise it will yield all destination port of the decomposeMatrix.
        A previsible connection it either:
        - outputTranslate to translate
        - outputRotate to rotate
        - outputScale to scale
        :param attr: A pymel.Attribute instance representing a decomposeMatrix.inputMatrix attribute.
        """
        model = self.get_model()
        registry = model.get_registry()

        def _is_predictable(connection_):
            attr_src_ = connection_.get_source().get_metadata()
            attr_dst_ = connection_.get_destination().get_metadata()
            attr_src_name = attr_src_.longName()
            attr_dst_name = attr_dst_.longName()
            if attr_src_name == 'outputTranslate':  # and attr_dst_name == 'translate':
                return True
            if attr_src_name == 'outputRotate':  # and attr_dst_name == 'rotate':
                return True
            if attr_src_name == 'outputScale':  # and attr_dst_name == 'scale':
                return True
            return False

        # attr_inputmatrix_model = self.get_port_mode
        node = attr.node()
        node_model = registry.get_node_model_from_value(node)

        # We will hold the connections in case we encounter an anormal connection.
        results = []
        for attr_dst in node_model.get_connected_output_ports(self):
            for connection in model.get_port_output_connections(attr_dst):
                # for connection2 in self.get_port_output_connections(dst_node_model):
                if _is_predictable(connection):
                    new_connection = connection.get_destination()
                    results.append(new_connection)
                else:
                    log.warning("Will no ignore {0} because of an unprevisible connection {1}.".format(node, connection))
                    yield attr
                    return

        for result in results:
            yield result
