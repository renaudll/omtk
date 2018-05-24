import abc
import logging

import omtk.qt_widgets.nodegraph.models.port.port_adaptor_entity
import omtk.qt_widgets.nodegraph.models.port.port_adaptor_pymel
import pymel.core as pymel
from omtk.factories import factory_datatypes

log = logging.getLogger('omtk')

if False:
    from omtk.qt_widgets.nodegraph.nodegraph_controller import NodeGraphController
    from omtk.qt_widgets.nodegraph.models.node.node_base import NodeGraphNodeModel

    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
    from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
    from omtk.vendor.pyflowgraph.port import Port as PyflowgraphBasePort


class NodeGraphPortModel(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry, node, name):
        self._name = name
        self._registry = registry
        self._node = node
        self._impl = None

    def __repr__(self):
        return '<Port {0}.{1}>'.format(self.get_parent().get_metadata(), self.get_name())

    def __hash__(self):
        return hash(self._node) ^ hash(self._name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.get_name() > other.get_name()

    def __lt__(self, other):
        return self.get_name() < other.get_name()

    # def __ge__(self, other):
    #     raise Exception("why?")
    #
    # def __le__(self, other):
    #     raise Exception("why?")

    @property
    def impl(self):
        if not self._impl:
            raise Exception("No implementation given.")
        return self._impl

    def get_name(self):
        """Return the unique name relative to the node."""
        return self._name

    def get_path(self):
        """Return the unique path relative to the graph."""
        return self._node.get_name() + '.' + self._name

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

    # --- NodeGraphPortImpl interface methods --- #

    def get_metadata(self):
        return self.impl.get_metadata()

    def get_metadata_input(self):
        """
        :return: The object associated with the port input.
        """
        return self.get_metadata()  # basic port share the same metadata for input and output

    def get_metadata_output(self):
        """
        :return: The object associated with the port output.
        """
        return self.get_metadata()  # basic port share the same metadata for input and output

    def get_metatype(self):
        return self.impl.get_metatype()

    def is_readable(self):
        return self.impl.is_readable()

    def is_writable(self):
        try:
            return self.impl.is_writable()
        except Exception, e:
            log.warning(e)

    def is_source(self):
        return self.impl.is_source()

    def is_destination(self):
        return self.impl.is_destination()

    def is_connected(self):
        return self.is_source() or self.is_destination()

    def is_interesting(self):
        return self.impl.is_interesting()

    def is_user_defined(self):
        return self.impl.is_user_defined()

    # --- Connection related methods --- #

    def get_input_connections(self):
        result = set()

        for val in self.impl.get_inputs():
            model = self._registry.get_port_model_from_value(val)
            inst = self._registry.get_connection_model_from_values(model, self)
            result.add(inst)
        return result

    def get_output_connections(self):
        result = set()
        for val in self.impl.get_outputs():
            model = self._registry.get_port_model_from_value(val)
            inst = self._registry.get_connection_model_from_values(self, model)
            result.add(inst)
        return result

    def get_connections(self):
        return self.get_input_connections() | self.get_output_connections()

    def connect_from(self, val):
        """Called when an upstream connection is created using a view."""
        self.impl.connect_from(val)

    def connect_to(self, val):
        """Called when a downstream connection is created using a view."""
        self.impl.connect_to(val)

    def disconnect_from(self, val):
        """Called when an upstream connection is removed using a view."""
        raise NotImplementedError

    def disconnect_to(self, val):
        """Called when a downstream connection is removed using a view."""
        raise NotImplementedError

    # --- Widget export --- #

    def _get_widget_cls(self, ctrl, is_input=None, is_output=None):
        from omtk.qt_widgets.nodegraph import pyflowgraph_port_widget as port_widget

        if is_input is None:
            is_input = self.is_writable()
        if is_output is None:
            is_output = self.is_readable()
        # Resolve port class
        if is_input and is_output:
            # raise Exception("{0} cannot be input and output at the same time.".format(attr))

            # In case of ambiguity, we will ask the node model.
            node_value = self.get_parent().get_metadata()
            # node_model = ctrl.get_node_model_from_value(node_value)
            node_model = self._registry.get_node_from_value(node_value)
            if is_input and not is_output:
                return port_widget.OmtkNodeGraphPortInWidget
            elif not is_input and is_output:
                return port_widget.OmtkNodeGraphPortOutput
            else:
                return port_widget.OmtkNodeGraphPortIOWidget
        elif not is_input and not is_output:
            raise Exception("{0} is neither an input or an output.".format(self))
        elif is_output:
            return port_widget.OmtkNodeGraphPortOutput
        else:
            return port_widget.OmtkNodeGraphPortInWidget

    def _get_widget_color(self):
        metatype = self.get_metatype()
        return factory_datatypes.get_port_color_from_datatype(metatype)
        # return QtGui.QColor(128, 170, 170, 255)  # todo: use factory_datatypes to get color

    def get_widget(self, ctrl, graph, node, is_input=None, is_output=None):
        # type: (NodeGraphController, PyFlowgraphView, PyFlowgraphNode) -> PyflowgraphBasePort
        cls = self._get_widget_cls(ctrl, is_input=is_input, is_output=is_output)
        color = self._get_widget_color()

        port = cls(
            node, graph,
            self._name,
            color,
            'some-mime-type',
        )
        node.addPort(port)

        # todo: use signals for this?
        port.on_added_to_scene()

        return port


class NodeGraphOpenMaya2PortModel(NodeGraphPortModel):
    pass


class NodeGraphPymelPortModel(NodeGraphPortModel):
    """Define an attribute bound to a PyMel.Attribute datatype."""

    def __init__(self, registry, node, pyattr):
        name = pyattr.longName()
        super(NodeGraphPymelPortModel, self).__init__(registry, node, name)
        self._impl = omtk.qt_widgets.nodegraph.models.port.port_adaptor_pymel.PymelAttributeNodeGraphPortImpl(pyattr)
        # self._pynode = attr_node if attr_node else pyattr.node()
        # self._pyattr = pyattr

    def __hash__(self):
        # todo: this is so unclean... cleanup reference to private values
        # We use the node hash since the same pymel.Attribute can refer
        # different node when dealing with Compound.
        # print(hash(self._impl._data))
        return hash(self._node) ^ hash(self._impl)

    # --- Connections related methods --- #

    # todo: move to adaptor?
    def connect_from(self, val):
        # Multi attributes cannot be directly connected to.
        # We need an available port.
        if self._impl._data.isMulti():
            i = self._impl._data.numElements()
            attr_dst = self._impl._data[i]
        else:
            attr_dst = self._impl._data

        try:
            pymel.connectAttr(val, attr_dst, force=True)
        except RuntimeError, e:
            log.warning(e)

    # todo: move to adaptor
    def connect_to(self, val):
        pymel.connectAttr(self._impl._data, val)

    # todo: move to adaptor
    def disconnect_from(self, val):
        try:
            pymel.disconnectAttr(val, self._impl._data)
        except RuntimeError, e:
            log.warning(e)

    # todo: move to adaptor
    def disconnect_to(self, val):
        pymel.disconnectAttr(self._impl._data, val)

        # --- Widget export --- #

        # def get_widget(self, ctrl, graph, node):
        #     widget = super(NodeGraphPymelPortModel, self).get_widget(ctrl, graph, node)
        #
        #     return widget


class OpenMaya2PortModel(NodeGraphPortModel):
    pass


# todo: replace double inheritence by composition
class NodeGraphEntityAttributePortModel(NodeGraphPortModel):
    """Define an attribute bound to an EntityAttribute instance."""

    def __init__(self, registry, node, attr_def):
        name = attr_def.name
        super(NodeGraphEntityAttributePortModel, self).__init__(registry, node, name)
        self._impl = omtk.qt_widgets.nodegraph.models.port.port_adaptor_entity.EntityAttributeNodeGraphPortImpl(
            attr_def)

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
