from collections import defaultdict


class NodeGraphWidgetCache(object):
    """
    Cache object that keep track of widgets associated with model and widgets.
    """
    def __init__(self):
        # Cache to access model-widget relationship
        self._cache_node_widget_by_model = {}
        self._cache_node_model_by_widget = {}

        self._cache_port_widget_by_model = {}
        self._cache_port_model_by_widget = {}

        self._cache_connection_widget_by_model = {}
        self._cache_connection_model_by_widget = {}

        self._cache_connections_by_port = defaultdict(set)

        self._cache_node_by_port = {}
        self._cache_ports_by_node = defaultdict(set)

    def register_node(self, node, widget):
        """
        Cache a node.
        :param omtk.nodegraph.NodeModel node: The node register.
        :param widget: The widget to associate with the node.
        """
        self._cache_node_widget_by_model[node] = widget
        self._cache_node_model_by_widget[widget] = node

    def unregister_node(self, node, recursive=True):
        """
        Remove a node from the cache.
        :param omtk.nodegraph.NodeModel node: The node to unregister.
        :param bool recursive: If True, all ports associated with the node will be unregistered.
        :return: The widget that was associated with the node.
        :rtype: OmtkNodeGraphNodeWidget
        """
        # Unregister ports
        if recursive:
            ports = self._cache_ports_by_node.pop(node, None)
            if ports:
                for port in ports:
                    self.unregister_port(port)

        # Unregister widget
        widget = self._cache_node_widget_by_model.pop(node, None)
        if widget:
            # Unregister node
            self._cache_node_model_by_widget.pop(widget, None)

        return widget

    def get_widget_from_node(self, node):
        """
        Get the widget associated with the provided node.
        :param omtk.nodegraph.NodeModel node: The node associated with the widget.
        :return: The widget associated with the node.
        :rtype: OmtkNodeGraphNodeWidget
        """
        return self._cache_node_widget_by_model.get(node)

    def get_node_from_widget(self, widget):
        """
        Get the node associated with the provided node widget.
        :param omtk.nodegraph.NodeWidget widget: The widget to consider.
        :return: The node associated with the widget.
        :type: NodeModel
        """
        return self._cache_node_model_by_widget.get(widget)

    def register_port(self, port, widget):
        """
        Cache a port.
        :param omtk.nodegraph.PortModel port: The port to register.
        :param widget: The widget to associate with the port.
        """
        # Update the cache
        self._cache_port_widget_by_model[port] = widget
        self._cache_port_model_by_widget[widget] = port

        # Update the node cache
        node = port.get_parent()
        self._cache_ports_by_node[node].add(port)
        self._cache_node_by_port[port] = node

    def unregister_port(self, port):
        """
        Remove a port from the cache.
        :param omtk.nodegraph.PortModel port: The port to unregister.
        :return:
        """
        # Clear Model <-> Widget cache
        widget = self._cache_port_widget_by_model.pop(port)
        self._cache_port_model_by_widget.pop(widget)

        # Clear Node <-> Port cache
        node = self._cache_node_by_port.pop(port)
        self._cache_ports_by_node[node].discard(port)

        return widget

    def get_port_from_widget(self, widget):
        return self._cache_port_model_by_widget.get(widget)

    def get_widget_from_port(self, port):
        return self._cache_port_widget_by_model.get(port)

    def register_connection(self, connection, widget):
        """
        Cache a connetion.
        :param omtk.nodegraph.ConnectionModel connection: The connection to register.
        :param QtWidgets.QWidget widget: The widget to associate with the connection.
        """
        # Register widget
        self._cache_connection_widget_by_model[connection] = widget

        # Register model
        self._cache_connection_model_by_widget[widget] = connection

    def unregister_connection(self, connection):
        """
        Remove a connection from the cache.
        :param omtk.nodegraph.ConnectionModel connection: The connection to unregister
        """
        # Unregister widget
        widget = self._cache_connection_widget_by_model.pop(connection)

        # Unregister model
        self._cache_connection_model_by_widget.pop(widget)

    def get_widget_from_connection(self, connection):
        """
        Retrieve the widget associated with the connection.
        :param omtk.nodegraph.ConnectionModel connection: A connection
        :return: A widget. None if the connection is not associated with a widget.
        :rtype: QtWidgets.QWidget or None
        """
        return self._cache_connection_widget_by_model.get(connection)

    def get_connection_from_widget(self, widget):
        """
        Retrieve the connected associated with the provided widget.
        :param QtWidgets.QWidget widget: The widget associated with the connection.
        :return: A connection. None if the widget does not represent an existing connection.
        :rtype: omtk.nodegraph.ConnectionModel or None
        """
        return self._cache_connection_model_by_widget.get(widget)
