import abc

import pymel.core as pymel
from omtk.factories import factory_datatypes
from omtk.vendor.pyflowgraph.port import IOPort as PyFlowgraphIOPort
from omtk.vendor.pyflowgraph.port import InputPort as PyFlowgraphInputPort
from omtk.vendor.pyflowgraph.port import OutputPort as PyFlowgraphOutputPort

from . import nodegraph_port_adaptor

if False:
    from .nodegraph_node_model_base import NodeGraphNodeModel
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView


class NodeGraphPortModel(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry, node, name):
        self._name = name
        self._registry = registry
        self._node = node
        self._adaptor = None

    def __repr__(self):
        return '<NodeGraphPortModel {0}.{1}>'.format(self.get_parent(), self.get_name())

    def get_name(self):
        """Return the unique name relative to the node."""
        return self._name

    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        """
        By default, an attribute share the same parent than it's node.
        However this is not always true, for example a Compound input hub
        output attribute have the Compound a it's parent. However a Compound
        input hub input attribute have the Compound parent as it's parent.
        :return:
        """
        return self._node

    # --- PortAdaptor interface methods --- #

    def get_metadata(self):
        return self._adaptor.get_metadata()

    def get_metatype(self):
        return self._adaptor.get_metatype()

    def is_readable(self):
        return self._adaptor.is_readable()

    def is_writable(self):
        return self._adaptor.is_writable()

    def is_source(self):
        return self._adaptor.is_source()

    def is_destination(self):
        return self._adaptor.is_destination()

    def is_connected(self):
        return self.is_source() or self.is_destination()

    def is_interesting(self):
        return self._adaptor.is_interesting()

    # --- Connection related methods --- #

    def get_input_connections(self):
        result = set()
        for val in self._adaptor.get_inputs():
            model = self._registry.get_port_model_from_value(val)
            inst = self._registry.get_connection_model_from_values(model, self)
            result.add(inst)
        return result

    def get_output_connections(self):
        result = set()
        for val in self._adaptor.get_outputs():
            model = self._registry.get_port_model_from_value(val)
            inst = self._registry.get_connection_model_from_values(self, model)
            result.add(inst)
        return result

    def get_connections(self):
        return self.get_input_connections() | self.get_output_connections()

    def connect_from(self, val):
        """Called when an upstream connection is created using a view."""
        self._adaptor.connect_from(val)

    def connect_to(self, val):
        """Called when a downstream connection is created using a view."""
        self._adaptor.connect_to(val)

    def disconnect_from(self, val):
        """Called when an upstream connection is removed using a view."""
        raise NotImplementedError

    def disconnect_to(self, val):
        """Called when a downstream connection is removed using a view."""
        raise NotImplementedError

    # --- Widget export --- #

    def _get_widget_cls(self, ctrl):
        is_readable = self.is_readable()
        is_writable = self.is_writable()
        # Resolve port class
        if is_readable and is_writable:
            # raise Exception("{0} cannot be input and output at the same time.".format(attr))

            # In case of ambiguity, we will ask the node model.
            node_value = self.get_parent()
            node_model = ctrl.get_node_model_from_value(node_value)
            is_writable = node_model.allow_input_port_display(self, ctrl)
            is_readable = node_model.allow_output_port_display(self, ctrl)
            if is_readable and not is_writable:
                return PyFlowgraphInputPort
            elif not is_readable and is_writable:
                return PyFlowgraphOutputPort
            else:
                return PyFlowgraphIOPort
        elif not is_readable and not is_writable:
            raise Exception("{0} is neither an input or an output.".format(self))
        elif is_writable:
            return PyFlowgraphInputPort
        else:
            return PyFlowgraphOutputPort

    def _get_widget_color(self):
        metatype = self.get_metatype()
        return factory_datatypes.get_port_color_from_datatype(metatype)
        # return QtGui.QColor(128, 170, 170, 255)  # todo: use factory_datatypes to get color

    def get_widget(self, ctrl, graph, node):
        # type: (NodeGraphController, PyFlowgraphView, PyFlowgraphNode) -> PyflowgraphBasePort
        cls = self._get_widget_cls(ctrl)
        color = self._get_widget_color()

        port = cls(
            node, graph,
            self._name,
            color,
            'some-mime-type'
        )
        node.addPort(port)

        return port


class NodeGraphPymelPortModel(NodeGraphPortModel):
    """Define an attribute bound to a PyMel.Attribute datatype."""

    def __init__(self, registry, node, pyattr, attr_node=None):
        name = pyattr.longName()
        super(NodeGraphPymelPortModel, self).__init__(registry, node, name)
        self._adaptor = nodegraph_port_adaptor.PymelAttributePortAdaptor(pyattr)
        # self._pynode = attr_node if attr_node else pyattr.node()
        # self._pyattr = pyattr

    # --- Connections related methods --- #

    # todo: move to adaptor?
    def connect_from(self, val):
        # Multi attributes cannot be directly connected to.
        # We need an available port.
        if self._adaptor._data.isMulti():
            i = self._adaptor._data.numElements()
            attr_dst = self._adaptor._data[i]
        else:
            attr_dst = self._adaptor._data

        pymel.connectAttr(val, attr_dst)

    # todo: move to adaptor
    def connect_to(self, val):
        pymel.connectAttr(self._adaptor._data, val)

    # todo: move to adaptor
    def disconnect_from(self, val):
        pymel.disconnectAttr(val, self._adaptor._data)

    # todo: move to adaptor
    def disconnect_to(self, val):
        pymel.disconnectAttr(self._adaptor._data, val)

        # --- Widget export --- #

        # def get_widget(self, ctrl, graph, node):
        #     widget = super(NodeGraphPymelPortModel, self).get_widget(ctrl, graph, node)
        #
        #     return widget

        # todo: uncomment and fix
        # def __hash__(self):
        #     return hash(self._node) ^ hash(self._pyattr)


# todo: replace double inheritence by composition
class NodeGraphEntityAttributePortModel(NodeGraphPortModel):
    """Define an attribute bound to an EntityAttribute instance."""

    def __init__(self, registry, node, attr_def):
        name = attr_def.name
        super(NodeGraphEntityAttributePortModel, self).__init__(registry, node, name)
        self._adaptor = nodegraph_port_adaptor.EntityAttributePortAdaptor(attr_def)

# # todo: replace double inheritence by composition
# class NodeGraphEntityPymelAttributePortModel(NodeGraphPymelPortModel):
#     def __init__(self, registry, node, attr_def):
#         name = attr_def.name
#         super(NodeGraphEntityPymelAttributePortModel, self).__init__(registry, node, attr_def._attr)
#         self._attr_def = attr_def
#
#     def get_metadata(self):
#         return self._attr_def._attr
#
#     def is_readable(self):
#         return self._attr_def.is_output
#
#     def is_writable(self):
#         return self._attr_def.is_input
#
#     def is_interesting(self):
#         return True
#
#     def _get_widget_color(self):
#         datatype = self.get_metatype()
#         return factory_datatypes.get_port_color_from_datatype(datatype)
#
#         # What was the issue again?
#         # We needed to support:
#         # -  Entity (ex: module name)
#         # -  Entity that point to pymel attribute (ex: module inputs)
#         # -  Pymel attribute (ex: any node attr)
#         # -  Pymel multi attribute (ex: any node attr)
