import logging
from collections import defaultdict
import functools
import pymel.core as pymel
from maya import OpenMaya
from omtk import decorators
from omtk.libs import libAttr, libPyflowgraph
from omtk.vendor.Qt import QtCore

from . import node_base
from omtk.qt_widgets.nodegraph import pyflowgraph_node_widget

log = logging.getLogger('omtk.nodegraph')


def _analayse_callback_message(msg):
    if msg & OpenMaya.MNodeMessage.kConnectionMade:
        yield 'kConnectionMade'
    if msg & OpenMaya.MNodeMessage.kConnectionBroken:
        yield 'kConnectionBroken'
    if msg & OpenMaya.MNodeMessage.kAttributeEval:
        yield 'kAttributeEval'
    if msg & OpenMaya.MNodeMessage.kAttributeSet:
        yield 'kAttributeSet'
    if msg & OpenMaya.MNodeMessage.kAttributeLocked:
        yield 'kAttributeLocked'
    if msg & OpenMaya.MNodeMessage.kAttributeUnlocked:
        yield 'kAttributeUnlocked'
    if msg & OpenMaya.MNodeMessage.kAttributeAdded:
        yield 'kAttributeAdded'
    if msg & OpenMaya.MNodeMessage.kAttributeRemoved:
        yield 'kAttributeRemoved'
    if msg & OpenMaya.MNodeMessage.kAttributeRenamed:
        yield 'kAttributeRenamed'
    if msg & OpenMaya.MNodeMessage.kAttributeKeyable:
        yield 'kAttributeKeyable'
    if msg & OpenMaya.MNodeMessage.kAttributeUnkeyable:
        yield 'kAttributeUnkeyable'
    if msg & OpenMaya.MNodeMessage.kIncomingDirection:
        yield 'kIncomingDirection'
    if msg & OpenMaya.MNodeMessage.kAttributeArrayAdded:
        yield 'kAttributeArrayAdded'
    if msg & OpenMaya.MNodeMessage.kAttributeArrayRemoved:
        yield 'kAttributeArrayRemoved'
    if msg & OpenMaya.MNodeMessage.kOtherPlugSet:
        yield 'kOtherPlugSet'


class NodeGraphDgNodeModel(node_base.NodeGraphNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def __init__(self, registry, pynode):
        name = pynode.nodeName()
        self._pynode = pynode
        self._callback_id_by_node_model = defaultdict(set)
        super(NodeGraphDgNodeModel, self).__init__(registry, name)

    def __hash__(self):
        return hash(self._pynode)

    def rename(self, new_name):
        self._pynode.rename(new_name)
        # Fetch the nodeName in case of name clash Maya
        # will give the node another name
        self._name = self._pynode.nodeName()

    def delete(self):
        if not self._pynode.exists():
            log.warning("Can't delete already deleted node! {0}".format(self._pynode))
            return

        pymel.delete(self._pynode)

    # @decorators.memoized_instancemethod
    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        # todo: move out of node_dg?
        from omtk.core import session as session_
        session = session_.get_session()
        component = session.get_component_from_obj(self._pynode)
        if component:
            return self._registry.get_node_from_value(component)

    def get_metadata(self):
        return self._pynode

    def get_nodes(self):
        return [self.get_metadata()]

    # @decorators.memoized_instancemethod
    def get_ports_metadata(self):
        return list(libAttr.iter_contributing_attributes(self._pynode))
        # return list(libAttr.iter_contributing_attributes_openmaya2(self._pynode.__melobject__()))

    def iter_ports(self):
        for attr in self.get_ports_metadata():
            inst = self._registry.get_port_model_from_value(attr)
            # inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr)
            # self._registry._register_attribute(inst)
            yield inst

            # Note: Multi-attribute are disabled for now, we might want to handle 'free' item
            # if a special way before re-activating this.
            # Otherwise we might have strange side effects.
            # n = pymel.createNode('transform')
            # n.worldMatrix.numElements()  # -> 0
            # n.worldMatrix.type()
            # n.worldMatrix.numElements() # -> 1, wtf
            # n.worldMatrix[1]  # if we try to use the free index directly
            # n.worldMatrix.numElements() # -> 2, wtf

            # If the attribute is a multi attribute, we'll want to expose the first available.
            # if attr.isMulti():
            #     next_available_index = attr.numElements() if attr.numElements() else 0
            #     attr_available = attr[next_available_index]
            #     inst = self._registry.get_port_model_from_value(attr_available)
            #     yield inst

            # if attr.isMulti():
            #     num_elements = attr.numElements()
            #     for i in xrange(num_elements):
            #         attr_child = attr.elementByLogicalIndex(i)
            #     # for attr_child in attr:
            #         inst = self._registry.get_port_model_from_value(attr_child)
            #         # inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr_child)
            #         # self._registry._register_attribute(inst)
            #         yield inst

    def _get_widget_cls(self):
        return pyflowgraph_node_widget.OmtkNodeGraphDagNodeWidget

    def get_widget(self, graph, ctrl):
        node = super(NodeGraphDgNodeModel, self).get_widget(graph, ctrl)

        # Set position
        pos = libPyflowgraph.get_node_position(node)
        if pos:
            pos = QtCore.QPointF(*pos)
            node.setGraphPos(pos)

        return node

    # --- Callbacks ---

    # def delete(self):
    #     self.remove_callbacks()
    #     super(NodeGraphDgNodeModel, self).delete()

    def add_callbacks(self):
        self.remove_callbacks()

        metadata = self.get_metadata()

        # Add attribute added callback
        callback_id = OpenMaya.MNodeMessage.addAttributeAddedOrRemovedCallback(
            metadata.__apimobject__(),
            self.callback_attribute_added
        )
        self._callback_id_by_node_model[metadata].add(callback_id)

        # Add attribute changed (connected)
        # callback_id = OpenMaya.MNodeMessage.addAttributeChangedCallback(
        #     metadata.__apimobject__(),
        #     self.callback_attribute_changed
        # )
        # self._callback_id_by_node_model[metadata].add(callback_id)

        # Add node deleted callback
        callback_id = OpenMaya.MNodeMessage.addNodeAboutToDeleteCallback(
            metadata.__apimobject__(),
            functools.partial(self.callback_node_deleted, metadata)
        )
        self._callback_id_by_node_model[metadata].add(callback_id)

    def remove_callbacks(self):
        for _, ids in self._callback_id_by_node_model.iteritems():
            for id_ in ids:
                OpenMaya.MNodeMessage.removeCallback(id_)
        self._callback_id_by_node_model.clear()

    def callback_attribute_added(self, callback_id, mplug, _):
        # return  # todo: make it work
        from omtk.qt_widgets.nodegraph.filters import filter_standard

        attr_dagpath = mplug.name()
        attr_name = attr_dagpath.split('.')[-1]

        # todo: make it cleaner
        if attr_name in filter_standard._attr_name_blacklist:
            log.info('Ignoring callback on {0}'.format(attr_dagpath))
            return

        attr_mobj = mplug.node()
        mfn = OpenMaya.MFnDependencyNode(attr_mobj)
        obj_name = mfn.name()
        log.info('Attribute {0} added on {1}'.format(attr_name, obj_name))

        # print attr_dagpath
        attr = pymel.Attribute(attr_dagpath)


        port = self._registry.get_port_model_from_value(attr)
        self.onAttributeAdded.emit(port)

        # self._ctrl.on_attribute_unexpectedly_added(attr)  # todo: make it work

    # @decorators.log_info
    def callback_attribute_changed(self, msg, plug, *args, **kwargs):
        """
        Called when an attribute related to the node change in Maya.
        :param msg:
        :param plug:
        :param args:
        :param kwargs:
        :return:
        """
        # return  # todo: make it work
        from maya import OpenMaya
        # print(' + '.join(self._analayse_callback_message(msg)))

        if msg & OpenMaya.MNodeMessage.kAttributeArrayAdded:
            attr_dagpath = plug.name()
            # attr = pymel.Attribute(attr_dagpath)
            self.onAttributeAdded.emit(attr_dagpath)
            # print attr
            # self._ctrl.callback_attribute_array_added(attr_dagpath)

    @decorators.log_info
    def callback_node_deleted(self, pynode, *args, **kwargs):
        """
        Called when the node is deleted in Maya.
        :param pynode: The pynode that is being deleted
        :param args: Absorb the OpenMaya callback arguments
        :param kwargs: Absorb the OpenMaya callback keyword arguments
        """
        # todo: unregister node
        log.debug("Removing {0} from nodegraph_tests".format(pynode))
        # self.remove_callbacks()
        self.onDeleted.emit(self)
        # if pynode:
        #
        #     self._ctrl.callback_node_deleted(self._model)
            # widget = self._ctrl.get_node_widget(pynode)
            # widget.disconnectAllPorts()
            # self._view.removeNode(widget)

    def on_added_to_scene(self):
        """
        Called when the node is added to a view (scene).
        :return:
        """
        super(NodeGraphDgNodeModel, self).on_added_to_scene()
        self.add_callbacks()

    def on_removed_from_scene(self):
        """
        Called when the node is removed from the view (scene).
        :return:
        """
        super(NodeGraphDgNodeModel, self).on_removed_from_scene()
        self.remove_callbacks()
