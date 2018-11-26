import abc
import logging

import omtk.nodegraph.models.port.port_adaptor_entity
import omtk.nodegraph.models.port.port_adaptor_pymel
from omtk.nodegraph.models.port.port_adaptor_pymel import PymelAttributeNodeGraphPortImpl

log = logging.getLogger(__name__)


class PortModel(object):
    """
    Application agnostic interface for a Port.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry, node, name):
        self._name = name
        self._registry = registry
        self._node = node
        self._impl = None

    def __repr__(self):
        return '<Port {0}.{1}>'.format(self.get_parent().get_metadata(), self.get_name())

    def __hash__(self):
        return hash(self.get_path())
        # return hash(self._node) ^ hash(self._name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.get_name() > other.get_name()

    def __lt__(self, other):
        return self.get_name() < other.get_name()

    def dump(self):
        return {
            "name": self._name,
            "connections": self.get_connections(),
        }

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
        """
        By default, an attribute share the same parent than it's node.
        However this is not always true, for example a Compound input hub
        output attribute have the Compound a it's parent. However a Compound
        input hub input attribute have the Compound parent as it's parent.
        :return:
        :rtype: omtk.nodegraph.NodeModel
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
        """
        :return: The type of the attribute as an enum value.
        :rtype: omtk.constants.AttributeType
        """
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
        """
        :return: True if the port is part of a connection.
        :rtype: bool
        """
        return self.impl.is_destination()

    def is_connected(self):
        """
        :return: True if the port is part of a connection.
        :rtype: bool
        """
        return self.is_source() or self.is_destination()

    def is_interesting(self):
        return self.impl.is_interesting()

    def is_user_defined(self):
        return self.impl.is_user_defined()

    # --- Connection related methods --- #

    def get_input_connections(self):
        result = set()

        for val in self.impl.get_inputs():
            model = self._registry.get_port(val)
            inst = self._registry.get_connection(model, self)
            result.add(inst)
        return result

    def get_output_connections(self):
        result = set()
        for val in self.impl.get_outputs():
            model = self._registry.get_port(val)
            inst = self._registry.get_connection(self, model)
            result.add(inst)
        return result

    def get_connections(self):
        """
        ???
        :return:
        :rtype: Set[ConnectionModel]
        """
        inns = self.get_input_connections()
        outs = self.get_output_connections()
        return inns | outs

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
        from omtk.nodegraph.widgets import widget_port as port_widget

        if is_input is None:
            is_input = self.is_writable()
        if is_output is None:
            is_output = self.is_readable()
        # Resolve port class
        if is_input and is_output:
            # raise Exception("{0} cannot be input and output at the same time.".format(attr))

            # In case of ambiguity, we will ask the node model.
            node_value = self.get_parent().get_metadata()
            # model_node = ctrl.get_node_model_from_value(node_value)
            node_model = self._registry.get_node(node_value)
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
        from omtk.factories import factory_datatypes
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


class NodeGraphOpenMaya2PortModel(PortModel):
    pass


class NodeGraphPymelPortModel(PortModel):
    """Define an attribute bound to a PyMel.Attribute datatype."""

    def __init__(self, registry, node, pyattr):
        name = pyattr.longName()
        super(NodeGraphPymelPortModel, self).__init__(registry, node, name)
        self._impl = PymelAttributeNodeGraphPortImpl(pyattr)
        # self._pynode = attr_node if attr_node else pyattr.node()
        # self._pyattr = pyattr

    def __hash__(self):
        # todo: this is so unclean... cleanup reference to private values
        # We use the node hash since the same pymel.Attribute can refer
        # different node when dealing with Compound.
        # print(hash(self._impl._data))
        # return hash(self._node) ^ hash(self._impl)
        return hash(self.get_path())

    # --- Connections related methods --- #

    # todo: move to adaptor?
    def connect_from(self, val):
        import pymel.core as pymel

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
        import pymel.core as pymel

        pymel.connectAttr(self._impl._data, val)

    # todo: move to adaptor
    def disconnect_from(self, val):
        import pymel.core as pymel

        try:
            pymel.disconnectAttr(val, self._impl._data)
        except RuntimeError, e:
            log.warning(e)

    # todo: move to adaptor
    def disconnect_to(self, val):
        import pymel.core as pymel

        pymel.disconnectAttr(self._impl._data, val)


class NodeGraphEntityAttributePortModel(PortModel):
    """Define an attribute bound to an EntityPort instance."""

    def __init__(self, registry, node, attr_def):
        name = attr_def.name
        super(NodeGraphEntityAttributePortModel, self).__init__(registry, node, name)
        self._impl = omtk.nodegraph.models.port.port_adaptor_entity.EntityAttributeNodeGraphPortImpl(
            attr_def)

