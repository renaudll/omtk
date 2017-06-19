import logging

import pymel.core as pymel

from omtk.core.classEntity import Entity
from omtk.vendor.Qt import QtGui, QtCore, QtWidgets
from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
from omtk.vendor.pyflowgraph.port import InputPort as PyFlowgraphInputPort
from omtk.vendor.pyflowgraph.port import OutputPort as PyFlowgraphOutputPort
from omtk.vendor.pyflowgraph.port import IOPort as PyFlowgraphIOPort
from omtk.core.classEntityAttribute import EntityAttributeTyped, EntityAttributeTypedCollection
from omtk.libs import libAttr
from omtk.libs import libComponents

from omtk import factory_datatypes

log = logging.getLogger('omtk')

__all__ = (
    'get_node',
)


def _get_port_name_from_pymel_attr(attr):
    return libComponents._escape_attr_name(attr.longName())


class NodeIcon(QtWidgets.QGraphicsWidget):
    def __init__(self, icon, parent=None):
        super(NodeIcon, self).__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        layout = QtWidgets.QGraphicsLinearLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        layout.setOrientation(QtCore.Qt.Horizontal)
        self.setLayout(layout)

        self._titleWidget = QtWidgets.QGraphicsPixmapItem(icon.pixmap(QtCore.QSize(20, 20)), self)
        # layout.addItem(self._titleWidget)
        # layout.setAlignment(self._titleWidget, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)


class GraphFactoryModel(object):
    def __init__(self, graph):
        self._graph = graph
        self._cache_node_by_pynode = {}
        self._cache_node_by_component = {}
        self._cache_port_by_pyattr = {}

    def clear_cache(self):
        self._cache_node_by_pynode.clear()
        self._cache_node_by_component.clear()
        self._cache_port_by_pyattr.clear()

    def get_node(self, val):
        """
        Main entry point
        :param graph:
        :param val:
        :return:
        """
        # type: (PyFlowgraphView, object) -> PyFlowgraphNode
        datatype = factory_datatypes.get_component_attribute_type(val)
        if datatype in (
                factory_datatypes.AttributeType.Component,
                factory_datatypes.AttributeType.Module,
                factory_datatypes.AttributeType.Rig
        ):
            return self._get_node_from_component(val)
        elif datatype == factory_datatypes.AttributeType.Node:
            return self._get_node_from_pynode(val)
        raise Exception("Unexpected datatype {0}: {1}".format(datatype, val))

    def _get_port_cls_from_attr(self, attr):
        attr_name = attr.attrName()
        attr_node = attr.node()
        is_inn = pymel.attributeQuery(attr_name, node=attr_node, writable=True)
        is_out = pymel.attributeQuery(attr_name, node=attr_node, readable=True)
        # Resolve port class
        if is_inn and is_out:
            # raise Exception("{0} cannot be input and output at the same time.".format(attr))
            return PyFlowgraphIOPort
        elif not is_inn and not is_out:
            raise Exception("{0} is neither an input or an output.".format(attr))
        elif is_out:
            return PyFlowgraphInputPort
        else:
            return PyFlowgraphOutputPort

    def _get_port_from_attr(self, attr):
        try:
            return self._cache_port_by_pyattr[attr]
        except KeyError:
            pass

        attr_node = attr.node()
        node = self._get_node_from_pynode(attr_node)

        attr_name = _get_port_name_from_pymel_attr(attr)
        port_cls = self._get_port_cls_from_attr(attr)

        port = port_cls(
            node, self._graph,
            attr_name,
            QtGui.QColor(128, 170, 170, 255),
            'something'
        )
        node.addPort(port)
        self._cache_port_by_pyattr[attr] = port
        return port

    def _get_node_from_component(self, component):
        # type: (PyFlowgraphView, Entity) -> PyFlowgraphNode
        try:
            return self._cache_node_by_pynode[component]
        except KeyError:
            pass

        node_label = "   {0} v{1}".format(component.name, component.get_version())
        node = PyFlowgraphNode(self._graph, node_label)

        icon = QtGui.QIcon(":/out_objectSet.png")
        # item = QtWidgets.QGraphicsPixmapItem()
        item = NodeIcon(icon)
        node.layout().insertItem(0, item)

        # Monkey-patch our metadata into the node.
        node._meta_data = component
        node._meta_type = factory_datatypes.AttributeType.Component

        color = factory_datatypes.get_node_color_from_datatype(node._meta_type)
        node.setColor(color)

        # hack
        port_out = PyFlowgraphOutputPort(
            node, self._graph, 'output', color, 'pymel/pynode'
        )
        node.addPort(port_out)

        for attr in component.iter_attributes():
            val = attr.get()

            port = self._get_port_from_attr(attr._attr)
            port_name = port.getName()

            node.addPort(port)

            # Hack: Enable multiple connections
            is_multi = isinstance(val, list)
            if is_multi:
                port.inCircle().setSupportsOnlySingleConnections(False)

            if isinstance(port, (PyFlowgraphInputPort, PyFlowgraphIOPort)):
                for attr_inn in attr._attr.inputs(plugs=True, skipConversionNodes=True):
                    attr_name = _get_port_name_from_pymel_attr(attr_inn)

                    sub_port = self._get_port_from_attr(attr_inn)
                    sub_node = sub_port.getNode()
                    try:
                        self._graph.connectPorts(sub_node, attr_name, node, port_name)
                    except Exception, e:
                        log.warning(e)

            if isinstance(port, (PyFlowgraphOutputPort, PyFlowgraphIOPort)):
                for attr_out in attr._attr.outputs(plugs=True, skipConversionNodes=True):
                    attr_name = _get_port_name_from_pymel_attr(attr_out)

                    sub_port = self._get_port_from_attr(attr_out)
                    sub_node = sub_port.getNode()
                    try:
                        self._graph.connectPorts(node, port_name, sub_node, attr_name)
                    except Exception, e:
                        log.warning(e)

        self._cache_node_by_component[component] = node
        return node

    def _get_node_from_pynode(self, pynode):
        try:
            return self._cache_node_by_pynode[pynode]
        except KeyError:
            pass

        node_label = "   {0}".format(pynode.name())
        node = PyFlowgraphNode(self._graph, node_label)

        icon = QtGui.QIcon(":/out_transform.png")
        item = NodeIcon(icon)
        node.layout().insertItem(0, item)

        # Monkey-patch our metadata into the node.
        node._meta_data = pynode
        node._meta_type = factory_datatypes.AttributeType.Node

        color = factory_datatypes.get_node_color_from_datatype(node._meta_type)
        node.setColor(color)

        # for attr in libAttr.iter_interesting_attributes(pynode):
        #     port = self._get_port_from_attr(node, attr)
        #     node.addPort(port)

        self._graph.addNode(node)

        self._cache_node_by_pynode[pynode] = node
        return node


_g_model_by_graph = {}


# for backward compatibility... for now!
def get_node(graph, val):
    global _g_model_by_graph
    try:
        _g_model_by_graph[graph].get_node(val)
    except KeyError:
        model = GraphFactoryModel(graph)
        _g_model_by_graph[graph] = model
        return model.get_node(val)
