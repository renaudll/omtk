import logging

import pymel.core as pymel

from omtk import constants
from omtk.core import preferences
from omtk.factories import factory_datatypes
from omtk.qt_widgets.nodegraph.nodegraph_filter import NodeGraphFilter

if False:
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphPortModel, NodeGraphConnectionModel

log = logging.getLogger('omtk.nodegraph')

_g_decomposematrix_predictable_inputs = {
    'outputTranslate': 'translate',
    'outputTranslateX': 'translateX',
    'outputTranslateY': 'translateY',
    'outputTranslateZ': 'translateZ',
    'outputRotate': 'rotate',
    'outputRotateX': 'rotateX',
    'outputRotateY': 'rotateY',
    'outputRotateZ': 'rotateZ',
    'outputScale': 'scale',
    'outputScaleX': 'scaleX',
    'outputScaleY': 'scaleY',
    'outputScaleZ': 'scaleZ',
}

_g_composematrix_predictable_outputs = {
    'inputTranslate': 'translate',
    'inputTranslateX': 'translateX',
    'inputTranslateY': 'translateY',
    'inputTranslateZ': 'translateZ',
    'inputRotate': 'rotate',
    'inputRotateX': 'rotateX',
    'inputRotateY': 'rotateY',
    'inputRotateZ': 'rotateZ',
    'inputScale': 'scale',
    'inputScaleX': 'scaleX',
    'inputScaleY': 'scaleY',
    'inputScaleZ': 'scaleZ',
}

_g_composematrix_predictable_outputs_inv = {v: k for k, v in _g_composematrix_predictable_outputs.iteritems()}


def is_connection_predictable_from_map(connection, map_):
    attr_src_ = connection.get_source().get_metadata()
    attr_dst_ = connection.get_destination().get_metadata()
    attr_src_name = attr_src_.longName()
    attr_dst_name = attr_dst_.longName()

    def _goal(src, dst):
        return attr_src_name == src and attr_dst_name == dst

    return any(True for src, dst in map_.iteritems() if _goal(src, dst))

def is_decomposematrix_connection_predictable(connection):
    global _g_decomposematrix_predictable_inputs
    return is_connection_predictable_from_map(connection, _g_decomposematrix_predictable_inputs)


def is_composematrix_connection_predictable(connection):
    global _g_composematrix_predictable_outputs_inv
    return is_connection_predictable_from_map(connection, _g_composematrix_predictable_outputs_inv)


class NodeGraphIntermediateNodeFilter(NodeGraphFilter):
    """
    Define filtering rules for a NodeGraphController.
    """

    def __init__(self):
        super(NodeGraphIntermediateNodeFilter, self).__init__()
        self.hide_unitconversion_node = True
        self.hide_predictable_decomposematrix_node = True

    def intercept_connection(self, connection):
        # type: (NodeGraphConnectionModel) -> NodeGraphConnectionModel
        model = self.get_model()
        registry = connection._registry
        port_src = connection.get_source()
        port_dst = connection.get_destination()

        node_src = port_src.get_parent()
        node_dst = port_dst.get_parent()

        # todo: remove this?
        attr_src = port_src.get_metadata_output()
        attr_dst = port_dst.get_metadata_input()

        # For now, if any port don't have metadata, don't try anything.
        if attr_src is None or attr_dst is None:
            log.warning("Cannot intercept connection that don't have any metadata! ({0}) Aborting".format(connection))
            yield connection
            return

        pynode_src = attr_src.node()
        pynode_dst = attr_dst.node()

        is_src_node_visible = model.is_node_visible(node_src)
        is_dst_node_visible = model.is_node_visible(node_dst)

        def _intercept_unitconversion_connection():
            if attr_dst.longName() == 'input' and not is_dst_node_visible:
                model_dst = registry.get_port_model_from_value(pynode_dst.output)
                for new_connection in model.get_port_output_connections(model_dst):
                    yield registry.get_connection_model_from_values(port_src, new_connection.get_destination())
                return

            # Redirect anything where the source is a unitConversion.output attribute.
            # EXCEPT if the unitConversion is already shown.
            if attr_src.longName() == 'output' and not is_src_node_visible:
                model_src = registry.get_port_model_from_value(pynode_src.input)
                if not model.is_node_visible(model_src):
                    for new_connection in model.get_port_input_connections(model_src):
                        yield registry.get_connection_model_from_values(new_connection.get_source(), port_dst)
                    return

        def _intercept_decomposematrix_connection():
            # Redirect "[1] -> inputMatrix" to "[1] -> [2]"
            if attr_dst.longName() == 'inputMatrix' and not is_dst_node_visible:
                for sub_connection in self._get_decomposematrix_inputmatrix_output_connections(registry, attr_dst):
                    new_connection = registry.get_connection_model_from_values(port_src, sub_connection)
                    yield new_connection
                return

            # Redirect "output[Translate/Rotate/Scale] -> [1]" to "[2] -> [1]"
            if attr_src.longName() in _g_decomposematrix_predictable_inputs and not is_src_node_visible:
                new_port_src = registry.get_port_model_from_value(pynode_src.attr('inputMatrix'))
                for sub_connection in model.get_port_input_connections(new_port_src):
                    new_connection = registry.get_connection_model_from_values(sub_connection.get_source(), port_dst)
                    yield new_connection
                return
            pass

        def _intercept_composematrix_connection():
            if attr_dst.longName() in _g_composematrix_predictable_outputs and not is_dst_node_visible:
                redirection_port = registry.get_port_model_from_value(pynode_dst.attr('outputMatrix'))
                for sub_connection in model.get_port_output_connections(redirection_port):
                    new_connection = registry.get_connection_model_from_values(attr_src, sub_connection.get_destination())
                    yield new_connection
                return

        if self.hide_unitconversion_node:
            # Redirect anything where destination is a unitConversion.input attribute
            # EXCEPT if the unitConversion is already shown.
            if not model.is_node_visible(node_src) and isinstance(pynode_src, pymel.nodetypes.UnitConversion):
                for yielded in _intercept_unitconversion_connection():
                    yield yielded
                return
            if not model.is_node_visible(node_dst) and isinstance(pynode_dst, pymel.nodetypes.UnitConversion):
                for yielded in _intercept_unitconversion_connection():
                    yield yielded
                return

        if self.hide_predictable_decomposematrix_node:
            # Redirect anything where the destination is a predictable decomposeMatrix.inputMatrix attribute.
            # EXCEPT if the unitConversion is already shown.

            if isinstance(pynode_src, pymel.nodetypes.DecomposeMatrix) and not model.is_node_visible(node_src):
                for yielded in _intercept_decomposematrix_connection():
                    yield yielded
                return

            if isinstance(pynode_dst, pymel.nodetypes.DecomposeMatrix) and not model.is_node_visible(node_dst):
                for yielded in _intercept_decomposematrix_connection():
                    yield yielded
                return

            if isinstance(pynode_src, pymel.nodetypes.ComposeMatrix) and not model.is_node_visible(node_src) and is_composematrix_connection_predictable(connection):
                for yielded in _intercept_composematrix_connection():
                    yield yielded
                return

            if isinstance(pynode_dst, pymel.nodetypes.ComposeMatrix) and not model.is_node_visible(node_dst) and is_composematrix_connection_predictable(connection):
                for yielded in _intercept_composematrix_connection():
                    yield yielded
                return

        yield connection

    def _get_decomposematrix_inputmatrix_output_connections(self, registry, attr):
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

        # attr_inputmatrix_model = self.get_port_mode
        node = attr.node()
        node_model = registry.get_node_from_value(node)

        # We will hold the connections in case we encounter an anormal connection.
        results = []
        for attr_dst in node_model.get_connected_output_ports():
            # Ignore message output connections...
            if attr_dst.get_metatype() == factory_datatypes.AttributeType.AttributeMessage:
                continue

            for connection in model.get_port_output_connections(attr_dst):
                # for connection2 in self.get_port_output_connections(dst_node_model):
                if is_decomposematrix_connection_predictable(connection):
                    new_connection = connection.get_destination()
                    results.append(new_connection)
                else:
                    log.warning("Will no ignore {0} because of an unpredictable connection {1}.".format(node, connection))
                    yield attr
                    return

        for result in results:
            yield result
