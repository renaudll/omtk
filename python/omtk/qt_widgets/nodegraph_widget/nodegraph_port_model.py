import omtk.factory_datatypes
from maya import cmds
import pymel.core as pymel
from omtk.libs import libPython
from omtk.vendor.Qt import QtGui
from omtk.vendor.pyflowgraph.port import IOPort as PyFlowgraphIOPort
from omtk.vendor.pyflowgraph.port import InputPort as PyFlowgraphInputPort
from omtk.vendor.pyflowgraph.port import OutputPort as PyFlowgraphOutputPort
from omtk import factory_datatypes

if False:
    from .nodegraph_node_model import NodeGraphNodeModel
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView


class NodeGraphPortModel(object):
    def __init__(self, registry, node, name):
        self._name = name
        self._registry = registry
        self._node = node

    def __repr__(self):
        return '<NodeGraphPortModel {0}>'.format(self._name)

    def get_metadata(self):
        return None

    def get_metatype(self):
        return None

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

    def is_readable(self):
        return False

    def is_writable(self):
        return False

    def is_source(self):
        return False

    def is_destination(self):
        return False

    def is_connected(self):
        return self.is_source() or self.is_destination()

    @libPython.memoized_instancemethod
    def is_interesting(self):
        if self.is_readable() and self.is_source():
            return True
        if self.is_writable() and self.is_destination():
            return True
        return False

    # --- Connection related methods --- #

    def get_input_connections(self):
        return set()

    def get_output_connections(self):
        return set()

    def get_connections(self):
        return self.get_input_connections() | self.get_output_connections()

    def connect_from(self, val):
        """Called when an upstream connection is created using a view."""
        raise NotImplementedError

    def connect_to(self, val):
        """Called when a downstream connection is created using a view."""
        raise NotImplementedError

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
            node_model = self.get_parent()
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
        return QtGui.QColor(128, 170, 170, 255)  # todo: use factory_datatypes to get color

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
        self._pynode = attr_node if attr_node else pyattr.node()
        self._pyattr = pyattr

    # todo: move in a base class?
    def get_metadata(self):
        return self._pyattr

    # todo: move in a base class?
    def get_metatype(self):
        native_type = factory_datatypes.get_component_attribute_type(self._pyattr)
        result = factory_datatypes.get_component_attribute_type(native_type)
        return result

    @libPython.memoized_instancemethod
    def _attr_name(self):
        return self._pyattr.attrName()

    @libPython.memoized_instancemethod
    def is_readable(self):
        return pymel.attributeQuery(self._attr_name(), node=self._pynode, readable=True)

    @libPython.memoized_instancemethod
    def is_writable(self):
        return pymel.attributeQuery(self._attr_name(), node=self._pynode, writable=True)

    def is_source(self):
        return self._pyattr.isSource()

    def is_destination(self):
        return self._pyattr.isDestination()

    @libPython.memoized_instancemethod
    def _list_parent_user_defined_attrs(self):
        # We use cmds instead of pymel since we want to equivalent of pymel.Attribute.attrName().
        result = cmds.listAttr(self._pynode.__melobject__(), userDefined=True)
        # However, cmds.listAttr can return None...
        if not result:
            return []
        return result

    @libPython.memoized_instancemethod
    def is_interesting(self):
        if super(NodeGraphPymelPortModel, self).is_interesting():
            return True
        # Any attributes not defined in the base MPxNode is interesting
        if self._attr_name() in self._list_parent_user_defined_attrs():
            return True
        # Any keyable attribute is interesting
        if self._pyattr.isKeyable():
            return True
        return False

    # --- Connections related methods --- #

    @libPython.memoized_instancemethod
    def get_input_connections(self):
        result = set()
        for attr_src in self._pyattr.inputs(plugs=True):
            attr_src_model = self._registry.get_port_model_from_value(attr_src)
            inst = self._registry.get_connection_model_from_values(attr_src_model, self)
            result.add(inst)
        return result

    @libPython.memoized_instancemethod
    def get_output_connections(self):
        result = set()
        for attr_dst in self._pyattr.outputs(plugs=True):
            attr_dst_model = self._registry.get_port_model_from_value(attr_dst)
            inst = self._registry.get_connection_model_from_values(self, attr_dst_model)
            result.add(inst)
        return result

    def connect_from(self, val):
        pymel.connectAttr(val, self._pyattr)

    def connect_to(self, val):
        pymel.connectAttr(self._pyattr, val)

    def disconnect_from(self, val):
        pymel.disconnectAttr(val, self._pyattr)

    def disconnect_to(self, val):
        pymel.disconnectAttr(self._pyattr, val)

    # --- Widget export --- #

    def get_widget(self, ctrl, graph, node):
        widget = super(NodeGraphPymelPortModel, self).get_widget(ctrl, graph, node)

        # Hack: Enable multiple connections in PyFlowgraph if we encounter a multi attribute.
        # if self._pyattr.isMulti():
        #     widget.inCircle().setSupportsOnlySingleConnections(False)

        return widget

    def __hash__(self):
        return hash(self._node) ^ hash(self._pyattr)


# todo: replace double inheritence by composition
class NodeGraphEntityAttributePortModel(NodeGraphPortModel):
    """Define an attribute bound to an EntityAttribute instance."""

    def __init__(self, registry, node, attr_def):
        name = attr_def.name
        super(NodeGraphEntityAttributePortModel, self).__init__(registry, node, name)
        self._attr_def = attr_def

    def get_metadata(self):
        return self._attr_def._attr

    def is_readable(self):
        return self._attr_def.is_output

    def is_writable(self):
        return self._attr_def.is_input

    def is_interesting(self):
        return True

    def _get_widget_color(self):
        datatype = self.get_metatype()
        return factory_datatypes.get_port_color_from_datatype(datatype)


# todo: replace double inheritence by composition
class NodeGraphEntityPymelAttributePortModel(NodeGraphPymelPortModel):
    def __init__(self, registry, node, attr_def):
        name = attr_def.name
        super(NodeGraphEntityPymelAttributePortModel, self).__init__(registry, node, attr_def._attr)
        self._attr_def = attr_def

    def get_metadata(self):
        return self._attr_def._attr

    def is_readable(self):
        return self._attr_def.is_output

    def is_writable(self):
        return self._attr_def.is_input

    def is_interesting(self):
        return True
