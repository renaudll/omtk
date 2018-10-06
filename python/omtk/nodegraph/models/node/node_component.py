import pymel.core as pymel
from omtk import component
from omtk.nodegraph.models.node import node_dg
from omtk.nodegraph.models.node import node_entity
from omtk.nodegraph.models.port import port_base
from omtk.nodegraph.widgets import widget_node
from omtk.vendor.Qt import QtGui
from omtk.nodegraph.models.port import port_adaptor_entity



class NodeGraphComponentPortModel(port_base.NodeGraphEntityAttributePortModel):
    """
    Any port in a NodeGraphComponentModel is simple a normal attribute associated with the inn or out hub.
    However we want to prevent any
    """

    def __init__(self, registry, node, attr_def):
        super(NodeGraphComponentPortModel, self).__init__(registry, node, attr_def)

        name = attr_def.name
        component = node.get_metadata()
        grp_inn = component.grp_inn
        grp_out = component.grp_out
        grp_inn_attr = grp_inn.attr(name) if grp_inn.hasAttr(name) else None
        grp_out_attr = grp_out.attr(name) if grp_out.hasAttr(name) else None

        self._inn_adaptor = port_adaptor_entity.PymelAttributeNodeGraphPortImpl(grp_inn_attr) if grp_inn_attr else None
        self._out_adaptor = port_adaptor_entity.PymelAttributeNodeGraphPortImpl(grp_out_attr) if grp_out_attr else None

    def _can_show_connection(self, connection):
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        node_src = port_src.get_metadata().node()
        node_dst = port_dst.get_metadata().node()

        # If the connection source is the hub inn, this is a private connection. Do not show it.
        if node_src == self._node._entity.grp_inn:
            return False

        # If the connection destination is the hub out, this is a private connection. Do not show it.
        if node_dst == self._node._entity.grp_out:
            return False

        return True

    def get_input_connections(self):
        registry = self._registry
        result = set()

        # grp_inn might not exist
        if not self._inn_adaptor:
            return result

        for val in self._inn_adaptor.get_inputs():
            model = registry.get_port(val)
            inst = registry.get_connection(model, self)
            result.add(inst)
        return result

    def get_output_connections(self):
        registry = self._registry
        result = set()

        # grp_out might not exist
        if not self._out_adaptor:
            return result

        for val in self._out_adaptor.get_outputs():
            model = registry.get_port(val)
            inst = registry.get_connection(self, model)
            result.add(inst)
        return result

    def get_metadata_input(self):
        return self._inn_adaptor.get_metadata()

    def get_metadata_output(self):
        return self._out_adaptor.get_metadata()

    def is_readable(self):
        return self._out_adaptor.is_readable() if self._out_adaptor else False

    def is_writable(self):
        return self._inn_adaptor.is_writable() if self._inn_adaptor else False

    def is_source(self):
        return self._out_adaptor.is_source() if self._out_adaptor else False

    def is_destination(self):
        return self._inn_adaptor.is_source() if self._inn_adaptor else False

    def is_interesting(self):
        return True

    def is_user_defined(self):
        return True  # we'll never receive non-user defined attributes

    def connect_from(self, val):
        """Called when an upstream connection is created using a view."""
        self._inn_adaptor.connect_from(val)

    def connect_to(self, val):
        """Called when a downstream connection is created using a view."""
        self._out_adaptor.connect_to(val)

    def disconnect_from(self, val):
        """Called when an upstream connection is removed using a view."""
        self._inn_adaptor.disconnect_from(val)

    def disconnect_to(self, val):
        """Called when a downstream connection is removed using a view."""
        self._out_adaptor.disconnect_to(val)


class NodeGraphComponentModel(node_entity.NodeGraphEntityModel):
    """
    Define the data model for a Node representing a Component.
    A Component is a special OMTK datatypes that consist of an input network, an output network and one or multiple
    maya nodes sandwitched in between.
    """

    def __init__(self, registry, entity):
        assert (isinstance(entity, component.Component))
        super(NodeGraphComponentModel, self).__init__(registry, entity)
        self._name = entity.namespace

    def __hash__(self):
        return super(NodeGraphComponentModel, self).__hash__() + 1  # magic number hack :(

    def rename(self, new_name):
        component = self.get_metadata()
        component.rename(new_name)

    def delete(self):
        # todo: verify it work
        pymel.delete(self._entity.get_children())

    def get_parent(self):
        # The parent of a component is either None or another component.
        # To retreive the parent of a component, check one of it's connections?
        # todo: use libComponents?
        from omtk.core import manager
        s = manager.get_session()
        current_namespace = self._entity.namespace
        tokens = current_namespace.split(':')
        if len(tokens) == 1:
            return None
        else:
            parent_namespace = ':'.join(tokens[1:])
            parent_component = s.get_component_from_namespace(parent_namespace)
            if parent_component:
                model = self._registry.get_node(parent_component)
                return model
        # for connection in self.get_input_connections():
        #     node = connection.get_source().get_parent()
        #     return node.get_parent()
        # for connection in self.get_output_connections():
        #     node = connection.get_destination().get_parent()
        #     return node.get_parent()
        return None

    def get_children(self):
        return [
            self._registry.get_node(pynode)
            for pynode in self._entity.get_children()
        ]

    def get_nodes(self):
        return self._entity.get_children()

    def scan_ports(self):
        """
        ???
        :return:
        :rtype: omtk.nodegraph.PortModel
        """

        if not self._entity.is_built():
            return

        for attr_def in self.get_ports_metadata():
            yield NodeGraphComponentPortModel(self._registry, self, attr_def)

    def _get_widget_cls(self):
        return widget_node.OmtkNodeGraphComponentNodeWidget


class NodeGraphComponentBoundBaseModel(node_dg.NodeGraphDgNodeModel):
    """
    Since dagnode contain input and output network that define their bound, it is usefull for us
    to have access to a dedicated model for the bounds that point to the compound model.
    """

    def __init__(self, registry, pynode, component):
        """
        :param omtk.nodegraph.NodeGraphRegistry registry:
        :param pymel.PyNode pynode:
        :param PortModel component:
        """
        super(NodeGraphComponentBoundBaseModel, self).__init__(registry, pynode)
        self._component = component

    def scan_ports(self):
        # Only show userDefined ports.
        for port in super(NodeGraphComponentBoundBaseModel, self).scan_ports():
            if port.is_user_defined():
                yield port

    def get_parent(self):
        """

        :return:
        :rtype: omtk.nodegraph.PortModel
        """
        return self._component


class NodeGraphComponentInnBoundModel(NodeGraphComponentBoundBaseModel):
    _widget_background_color = QtGui.QColor(0, 195, 227)

    def scan_ports(self):
        for port in super(NodeGraphComponentInnBoundModel, self).scan_ports():
            # hack: prevent us from reading input connections
            # todo: make it cleaner!
            def _hack():
                return []
            port.get_input_connections = _hack
            yield port

    def get_input_ports(self):
        """Return nothing. A InnBound have no visible input connection."""
        # Can only have output connections
        return []

    def get_widget(self, graph, ctrl):
        # debugging
        widget = super(NodeGraphComponentBoundBaseModel, self).get_widget(graph, ctrl)
        color = self._widget_background_color
        widget.setColor(color)
        return widget


class NodeGraphComponentOutBoundModel(NodeGraphComponentBoundBaseModel):
    _widget_background_color = QtGui.QColor(255, 69, 84)

    def scan_ports(self):
        for port in super(NodeGraphComponentOutBoundModel, self).scan_ports():
            # hack: prevent us from reading input connections
            # todo: make it cleaner!
            def _hack():
                return []
            port.get_output_connections = _hack
            yield port

    def get_input_ports(self):
        """
        ???
        :return:
        :rtype: List[PortModel]
        """
        # type: () -> list[PortModel]
        # Can only have input connections
        return []

    def get_widget(self, graph, ctrl):
        # debugging
        widget = super(NodeGraphComponentBoundBaseModel, self).get_widget(graph, ctrl)
        color = self._widget_background_color
        widget.setColor(color)
        return widget
