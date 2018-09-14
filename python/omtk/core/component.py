import logging
import re

from maya import cmds
from omtk import constants
from omtk.core import session
from omtk.core.entity import Entity
from omtk.core.entity_action import EntityAction
from omtk.core.entity_attribute import EntityAttribute
from omtk.core import component_definition
from omtk.core.entity_attribute import EntityPymelAttribute, EntityPymelAttributeCollection
from omtk.factories import factory_datatypes
from omtk.libs import libAttr
from omtk.libs import libNamespaces
from omtk.libs import libPython
from omtk.vendor import libSerialization
from pymel import core as pymel


log = logging.getLogger('omtk')


if False:  # for type hinting
    from typing import List, Dict
    from omtk.core.component_definition import ComponentDefinition

# todo: create ComponentScripted and ComponentSaved


class ComponentAttribute(EntityAttribute):
    def __init__(self, parent, name, attr, **kwargs):
        super(ComponentAttribute, self).__init__(parent, name=name, **kwargs)
        self.get_attribute_definition(parent, attr, True, True)

        attr_inn = parent.grp_inn.attr(name) if parent.grp_inn and parent.grp_inn.hasAttr(name) else None
        attr_out = parent.grp_out.attr(name) if parent.grp_out and parent.grp_out.hasAttr(name) else None
        self._attr_inn = self.get_attribute_definition(parent, attr_inn) if attr_inn else None
        self._attr_out = self.get_attribute_definition(parent, attr_out) if attr_out else None

    def get_attribute_definition(self, parent, attr, is_input=False, is_output=False):
        valid_types = factory_datatypes.get_attr_datatype(attr)
        if valid_types is None:
            log.warning("Cannot create AttributeDef from {0}".format(attr))
            return None

        if attr.isMulti():
            return EntityPymelAttributeCollection(parent, attr, is_input=is_input, is_output=is_output)
        else:
            return EntityPymelAttribute(parent, attr, is_input=is_input, is_output=is_output)

    def get(self):
        raise NotImplementedError

    def set(self, val):
        raise NotImplementedError

    def connect_from(self, val):
        assert (isinstance(val, pymel.Attribute))
        self._attr_inn.disconnect_from(val)

    def connect_to(self, val):
        assert (isinstance(val, pymel.Attribute))
        self._attr_out.connect_to(val)

    def disconnect_from(self, val):
        assert (isinstance(val, pymel.Attribute))
        self._attr_inn.disconnect_from(val)

    def disconnect_to(self, val):
        assert (isinstance(val, pymel.Attribute))
        self._attr_out.disconnect_to(val)


class Component(Entity):
    """
    A Component implement encapsulation in Maya
    Components use namespaces to determine their content.
    This is the simplest design available to us in Maya.
    """
    # These need to be defined in order to register a component.
    component_id = None
    component_name = None

    need_grp_inn = True
    need_grp_out = True

    def __init__(self, namespace=None):
        super(Component, self).__init__()

        # todo: namespace is a keyword argument for compatibility with libSerialization
        # fix libSerialization instead of modifying this code

        self.namespace = namespace

        self.uid = self.component_id

        # Component can have a definition that define informations needed to identify them.
        self.definition = None

        # A component can have a 'inn' node.
        # Each input custom attribute of this object will be exposed outside of the component.
        self.grp_inn = None

        # A component can have an 'out' node.
        # Each output custom attribute of this object will be exposed outside of the component.
        self.grp_out = None

        # Used for dynamic components. Define if a Component content need to be regenerated.
        self._is_dirty_content = True

    def __hash__(self):
        return hash(self.namespace)

    def __contains__(self, item):
        # type: (pymel.nodetypes.DependNode) -> bool
        """
        Check if a pymel.nodetypes.DependNode is inside the component.
        :param item: A pymel.nodetypes.DependNode.
        :return: True if the node is inside the component. False otherwise.
        """
        # todo: do we check recursively?
        return item in self.get_children()

    def get_namespace(self):
        # type: () -> str
        return self.namespace

    @classmethod
    def from_definition(cls, cls_def):
        # type: (component_definition.ComponentDefinition) -> Component
        inst = cls()
        inst.name = cls_def.name
        inst.version = cls_def.version
        inst.author = cls_def.author
        return inst

    def is_dirty_content(self):
        return self._is_dirty_content

    def set_content_dirty(self, state=True):
        self._is_dirty_content = state

    def get_definition(self):
        # type: () -> ComponentDefinition
        """
        Return metadata associated with the component.
        :return: A Component definition object.
        """
        metadata_dagpath = '{0}:metadata'.format(self.namespace)
        if not cmds.objExists(metadata_dagpath):
            return None
        else:
            metadata_node = pymel.PyNode(metadata_dagpath)
            m = session.get_session()
            component_def = m.import_network(metadata_node)
            return component_def

    def build_interface(self):
        """
        Create the Component input, output and dag hub. Define all public attributes.
        However does not build what between the input and output hub.
        This is separated in it's own method since we might want to set public attributes before building
        the content, especially if the content depend on some attribute value.
        """

        sel = pymel.selected()

        if self.need_grp_inn:
            self.grp_inn = pymel.createNode('network', name='inn')
        if self.need_grp_out:
            self.grp_out = pymel.createNode('network', name='out')

        pymel.select(sel)  # todo: keep_selection decorator

        m = session.get_session()
        m.export_network(self)

        # -> any inherited class would want to add input and output attributes here <-

    def build_content(self):
        """
        Build the content between the inn and out hub.
        This is separated in it's own method since in some Component, changing an attribute value can necessitate
        a rebuild of the content but not of the public interface.
        :return:
        """
        raise NotImplementedError

    def build(self, build_content=True):
        """
        Build the Component public interface and private content.
        :param build_content: Set False if you can to build the content yourself, can be usefull if attributes need to be set first.
        :return:
        """
        self.build_interface()
        if build_content:
            self.build_content()

    def is_built_interface(self):
        return \
            self.grp_inn and self.grp_inn.exists() and \
            self.grp_out and self.grp_out.exists()

    def is_built(self):
        return self.is_built_interface()

    def iter_attributes(self):
        attrs_inn = set(libAttr.iter_network_contributing_attributes(self.grp_inn))
        attrs_out = set(libAttr.iter_network_contributing_attributes(self.grp_out))
        custom_attrs = set(self.grp_inn.listAttr(userDefined=True)) | set(self.grp_out.listAttr(userDefined=True))
        attrs_inn &= custom_attrs
        attrs_out &= custom_attrs

        attr_by_name = {attr.longName(): attr for attr in attrs_inn | attrs_out}
        for name, attr in attr_by_name.iteritems():
            # yield get_attribute_definition(self, attr)
            yield ComponentAttribute(self, name, attr)

    def iter_actions(self):
        for action in super(Component, self).iter_actions():
            yield action
        yield ActionShowContentInNodeEditor(self)

    def unbuild(self):
        if not self.is_built():
            return
        objs_to_delete = []
        if self.grp_inn and self.grp_inn.exists():
            objs_to_delete.append(self.grp_inn)
        if self.grp_out and self.grp_out.exists():
            objs_to_delete.append(self.grp_out)
        if objs_to_delete:
            pymel.delete(objs_to_delete)
        self.grp_inn = None
        self.grp_out = None

        # todo: log remaining objects?
        cmds.namespace(deleteNamespaceContent=True, removeNamespace=self.namespace)

    def optimize(self):
        # type: () -> bool
        """
        Implement optimisation routines. Call before publishing rig to animation.
        There's multiple things that can be done here, here's some idea:
        - Remove the inn and out hub.
        - Check if decomposeMatrix are sent to composeMatrix and vice versa and remove them.
        """
        return False

    def is_modified(self):
        # type: () -> bool
        """
        Check if a component have been modified since it's construction.
        todo: implement it, how???
        :return:
        """
        raise NotImplementedError

    # --- Interface management ---

    def add_input_attr(self, long_name, **kwargs):
        # type: (str) -> pymel.Attribute
        return libAttr.addAttr(self.grp_inn, long_name, **kwargs)

    def has_input_attr(self, attr_name):
        # type: (str) -> bool
        return self.grp_inn.hasAttr(attr_name)

    def get_input_attr(self, attr_name):
        # type: (str) -> pymel.Attribute
        return self.grp_inn.attr(attr_name)

    def get_input_attributes(self):
        # type: (str) -> List[pymel.Attribute]
        return self.grp_inn.listAttr()

    def add_output_attr(self, long_name, **kwargs):
        return libAttr.addAttr(self.grp_out, long_name, **kwargs)

    def has_output_attr(self, attr_name):
        # type: (str) -> bool
        return self.grp_out.hasAttr(attr_name)

    def get_output_attr(self, attr_name):
        # type: (str) -> pymel.Attribute
        return self.grp_out.attr(attr_name)

    def get_output_attributes(self):
        # type: (str) -> List[pymel.Attribute]
        return self.grp_out.listAttr()

    def connect_to_input_attr(self, attr_name, attr_src, **kwargs):
        # type: (str, pymel.Attribute) -> None
        if not self.grp_inn.hasAttr(attr_name):
            log.warning("Cannot reconnect {0} to {1}. {0} doesnt exist.".format(attr_name, attr_src))
            return
        if not attr_src.exists():
            log.warning("Cannot reconnect {0} to {1}. {1} doesnt exist.".format(attr_name, attr_src))
            return
        attr_dst = self.grp_inn.attr(attr_name)
        log.info("Connecting {0} to {1}".format(attr_src, attr_dst))
        pymel.connectAttr(attr_src, attr_dst)

    def connect_to_output_attr(self, attr_name, attr_dst, **kwargs):
        # type: (str, pymel.Attribute) -> None
        if not self.grp_out.hasAttr(attr_name):
            log.warning("Cannot reconnect {0} to {1}. {0} doesnt exist.".format(attr_dst, attr_name))
            return
        if not attr_dst.exists():
            log.warning("Cannot reconnect {0} to {1}. {1} doesnt exist.".format(attr_dst, attr_name))
            return
        attr_src = self.grp_out.attr(attr_name)
        log.info("Connecting {0} to {1}".format(attr_src, attr_dst))
        pymel.connectAttr(attr_src, attr_dst)

    def explode(self):
        """Delete the component and it's hub, remaping the attribute to their original location."""
        if not self.is_built():
            raise Exception("Cannot explode an unbuilt component.")

        def _remap_attr(attr):
            attr_src = next(iter(attr.inputs(plugs=True)), None)
            # if not attr_src:
            #     return
            if attr_src:
                pymel.disconnectAttr(attr_src, attr)
            for attr_dst in attr.outputs(plugs=True):
                pymel.disconnectAttr(attr, attr_dst)
                if attr_src:
                    pymel.connectAttr(attr_src, attr_dst, force=True)

        # Explode grp_inn
        for attr in self.get_input_attributes():
            _remap_attr(attr)

        # Explode grp_out
        for attr in self.get_output_attributes():
            _remap_attr(attr)

        self.unbuild()

    def get_children(self):
        # type: () -> List[pymel.nodetypes.DependNode]
        """
        The children of the component are any DgNode that are under our namespace.
        :return:
        """
        return pymel.ls('{0}:*'.format(self.namespace))

    def export(self, path):
        children = self.get_children()
        if not children:
            raise Exception("Can't export component, component is empty!")

        # Ensure the component metadata is exported
        m = session.get_session()
        network = m.export_network(self)

        objs_to_export = set(children) | {self.grp_inn, self.grp_out, network}

        # Hold current file
        current_path = cmds.file(q=True, sn=True)

        # todo: optimise this
        grp_inn_attrs = set(self.grp_inn.listAttr())
        grp_inn_attrs.remove(self.grp_inn.message)
        grp_out_attrs = set(self.grp_out.listAttr())
        grp_out_attrs.remove(self.grp_out.message)

        with libAttr.context_disconnected_attrs(grp_inn_attrs, hold_inputs=True, hold_outputs=False):
            with libAttr.context_disconnected_attrs(grp_out_attrs, hold_inputs=False, hold_outputs=True):

                pymel.select(objs_to_export)
                cmds.file(rename=path)
                cmds.file(force=True, exportSelected=True, type="mayaAscii")

                # Fetch current file
                cmds.file(rename=current_path)

        definition = self.get_definition()
        definition.write_metadata_to_file(path)

        # Hack: If a hub group is in a namespace, we'll want to remove it from the exported file.
        namespace = None
        if self.grp_inn:
            namespace = self.grp_inn.namespace()
        elif self.grp_out:
            namespace = self.grp_out.namespace()
        if namespace:
            from omtk.libs import libComponents  # todo: move the method to another module
            libComponents.remove_namespace_from_file(path, namespace)

        return True

    def set_definition(self, component_def):
        # type: (ComponentDefinition) -> None
        self.name = component_def.name
        self.author = component_def.author
        self.version = component_def.version
        self.uid = component_def.uid

        # Re-export metadata
        network_name = '{0}:{1}'.format(self.namespace, constants.COMPONENT_METANETWORK_NAME)
        if cmds.objExists(network_name):
            cmds.delete(network_name)

        network = libSerialization.export_network(component_def)
        network.rename(network_name)

    def get_connections(self):
        """
        Return two dict(k,v) describing what is connected to the component.
        This help with updating/promoting component.
        """
        map_inn = {}
        map_out = {}
        for attr in self.grp_inn.listAttr(userDefined=True):
            if attr.isDestination():
                map_inn[attr] = attr.inputs(plugs=True)
        for attr in self.grp_out.listAttr(userDefined=True):
            if attr.isSource():
                map_out[attr] = attr.outputs(plugs=True)
        return map_inn, map_out

    def get_connections_relative(self):
        """
        :return: Two dict(k,v) where k is the name of a public attribute and v is a list of outside attributes connected to it.
        """
        old_map_inn, old_map_out = self.get_connections()
        map_inn = {}
        map_out = {}
        for attr, vals in old_map_inn.iteritems():
            map_inn[attr.longName()] = vals
        for attr, vals in old_map_out.iteritems():
            map_out[attr.longName()] = vals
        return map_inn, map_out

    def hold_connections(self):
        map_inn, map_out = self.get_connections_relative()
        for attr_dst_name, attr_srcs in map_inn.iteritems():
            attr_dst = self.grp_inn.attr(attr_dst_name)
            for attr_src in attr_srcs:
                pymel.disconnectAttr(attr_src, attr_dst)
        for attr_src_name, attr_dsts in map_out.iteritems():
            attr_src = self.grp_out.attr(attr_src_name)
            for attr_dst in attr_dsts:
                pymel.disconnectAttr(attr_src, attr_dst)
        return map_inn, map_out

    def fetch_connections(self, map_inn, map_out):
        for attr_name, attr_srcs in map_inn.iteritems():
            for attr_src in attr_srcs:
                self.connect_to_input_attr(attr_name, attr_src)
        for attr_name, attr_dsts in map_out.iteritems():
            for attr_dst in attr_dsts:
                self.connect_to_output_attr(attr_name, attr_dst)

    def rename(self, new_namespace):
        old_namespace = self.namespace
        new_namespace = libNamespaces.get_unique_namespace(new_namespace)
        cmds.namespace(addNamespace=new_namespace)
        cmds.namespace(moveNamespace=(self.namespace, new_namespace))
        cmds.namespace(removeNamespace=old_namespace)
        self.namespace = new_namespace

    def delete(self):
        self.unbuild()  # todo: merge methods?


# --- Actions ---

class ActionShowContentInNodeEditor(EntityAction):
    def get_name(self):
        return 'Show in Maya Node Editor'

    def _create_node_editor(self):
        cmds.window()
        form = cmds.formLayout()
        p = cmds.scriptedPanel(type="nodeEditorPanel", label="Node Editor.md")
        cmds.formLayout(form, e=True, af=[(p, s, 0) for s in ("top", "bottom", "left", "right")])
        cmds.showWindow()
        return p + 'NodeEditorEd'

    def execute(self):
        children = set(self.component.get_children())
        if not children:
            log.debug('Cannot open NodeEditor to explore {0} content. No children to display!'.format(self.component))
            return
        children.add(self.component.grp_inn)
        children.add(self.component.grp_out)

        node_editor = self._create_node_editor()
        pymel.select(children)
        cmds.nodeEditor(node_editor, e=True, addNode='')

def _get_parent_namespace(nodes):
    """
    Resolve the parent namespace.
    This allow a component to be inside another component.
    However we don't want to have nodes in our component that don't share the same namespace since
    a component cannot logically have multiple parents.
    """
    def _get_namespace(n):
        if isinstance(n, pymel.PyNode):
            return n.namespace()
        else:
            return n.namespace
    namespaces = {_get_namespace(node).strip(':') for node in nodes}
    if len(namespaces) > 1:
        raise Exception("Cannot create component from nodes. Nodes don't share the same namespace.")
    return next(iter(namespaces), None)

def _get_nodes_from_attributes(attrs_inn, attrs_out):
    """
    Determine the common history between attributes that would be used to create a component.
    """
    hist_inn = set()
    hist_out = set()
    for attr_inn in attrs_inn:
        hist_inn.update(attr_inn.listHistory(future=True))
    for attr_out in attrs_out:
        hist_out.update(attr_out.listHistory(future=False))
    return hist_inn & hist_out


def create_empty(namespace='component'):
    # type: (str) -> Component
    """
    Create an empty component.
    :param namespace:
    :return:
    """
    namespace = libNamespaces.get_unique_namespace(namespace, enforce_suffix=True)
    cmds.namespace(add=namespace)
    inst = Component(namespace)
    return inst


def from_nodes(objs, connections=True, namespace='component'):
    # type: (List[pymel.nodetypes.DependNode], str) -> Component
    """
    Create a component from a set of nodes.
    This will move these nodes into a unique namespace and return a Component instance.
    :param objs: A list of pymel.nodetypes.DependNode.
    :param namespace: The desired namespace. If not unique, a suffix will be added.
    :return: A Component instance.
    """
    parent_namespace = _get_parent_namespace(objs)
    if parent_namespace:
        namespace = '{0}:{1}'.format(parent_namespace, namespace)
    namespace = libNamespaces.get_unique_namespace(namespace, enforce_suffix=True)
    cmds.namespace(add=namespace)

    for obj in objs:
        old_name = obj.stripNamespace().nodeName()
        new_name = '{0}:{1}'.format(namespace, old_name)
        obj.rename(new_name)

    inst = Component(namespace)

    # We need an hub in and hub_out
    # However we don't known about which attributes to expose so we'll just create the objects.
    # todo: do we want to automatically populate the hubs?
    hub_inn_dagpath = '{0}:{1}'.format(namespace, constants.COMPONENT_HUB_INN_NAME)
    hub_out_dagpath = '{0}:{1}'.format(namespace, constants.COMPONENT_HUB_OUT_NAME)
    hub_inn = pymel.PyNode(hub_inn_dagpath) if cmds.objExists(hub_inn_dagpath) else pymel.createNode('network', name=hub_inn_dagpath)
    hub_out = pymel.PyNode(hub_out_dagpath) if cmds.objExists(hub_out_dagpath) else pymel.createNode('network', name=hub_out_dagpath)
    inst.grp_inn = hub_inn
    inst.grp_out = hub_out

    return inst


_g_regex_prefix = re.compile('(.*[^0-9]+)([0-9]*)$')


def from_attributes(attrs_inn, attrs_out, dagnodes=None, namespace='component'):
    # type: (List[pymel.Attribute], List[pymel.Attribute], str) -> Component
    attrs_inn_map = {}
    attrs_out_map = {}

    for attr in attrs_inn:
        if attr in attrs_inn_map:
            continue
        attr_name = libPython.get_unique_key(attr.longName(), attrs_inn_map)
        attrs_inn_map[attr_name] = attr

    for attr in attrs_out:
        if attr in attrs_out_map:
            continue
        attr_name = libPython.get_unique_key(attr.longName(), attrs_out_map)
        attrs_out_map[attr_name] = attr

    inst = from_attributes_map(attrs_inn_map, attrs_out_map, dagnodes=dagnodes, namespace=namespace)
    return inst


def from_attributes_map(attrs_inn, attrs_out, dagnodes=None, namespace='component'):
    # type: (Dict[str, pymel.Attribute], Dict[str, pymel.Attribute], List[pymel.PyNode], str) -> Component
    """
    Create a Component from existing nodes.
    :param attrs_inn: A dict(k, v) of public input attributes where k is attr name and v is the reference attribute.
    :param attrs_out: A dict(k, v) of publish output attributes where k is attr name v is the reference attribute.
    :param dagnodes: A list of nodes to include in the component.
    :param namespace: A str for the created component namespace.
    :return: Component instance.
    """
    # Determine the parent namespace
    if dagnodes is None:
        dagnodes = set()
    else:
        dagnodes = set(dagnodes)  # enforce set for now...
    additional_dagnodes = _get_nodes_from_attributes(attrs_inn.values(), attrs_out.values())
    dagnodes.update(additional_dagnodes)

    # todo: do we want to force readable or writable attributes? can this fail?
    # Find an available namespace
    # This allow us to make sure that we'll have access to unique name.
    # Note theses namespaces will be removed in any exported file.
    from omtk.libs import libNamespaces
    namespace = libNamespaces.get_unique_namespace(namespace, enforce_suffix=True)
    cmds.namespace(add=namespace)

    inst = Component(namespace)

    hub_inn = pymel.createNode('network', name='{0}:{1}'.format(namespace, constants.COMPONENT_HUB_INN_NAME))
    hub_out = pymel.createNode('network', name='{0}:{1}'.format(namespace, constants.COMPONENT_HUB_OUT_NAME))

    def _escape_attr_name(attr_name):
        return attr_name.replace('[', '').replace(']', '')  # todo: find a better way

    # Create the hub_inn attribute.
    for attr_name, attr_ref in attrs_inn.iteritems():
        data = libAttr.AttributeData.from_pymel_attribute(attr_ref, store_inputs=True, store_outputs=True)
        if not data.is_writable:
            raise IOError("Expected a writable attribute as an input reference.")

        attr_name = _escape_attr_name(attr_name)

        data.rename(attr_name)
        hub_attr = data.copy_to_node(hub_inn)
        pymel.connectAttr(hub_attr, attr_ref, force=True)
        data.connect_stored_inputs(hub_inn)

    # Create the hub_out attribute.
    for attr_name, attr_ref in attrs_out.iteritems():
        data = libAttr.AttributeData.from_pymel_attribute(attr_ref, store_inputs=True, store_outputs=True)
        if not data.is_readable:
            raise IOError("Expected a readable attribute as an output reference.")

        attr_name = _escape_attr_name(attr_name)

        data.rename(attr_name)
        hub_attr = data.copy_to_node(hub_out)
        pymel.connectAttr(attr_ref, hub_attr)
        data.connect_stored_outputs(hub_out)

    # Resolve the objects between the hubs
    dagnodes = set(dagnodes) if dagnodes else set()
    dagnodes |= set(hub_inn.listHistory(future=True)) & set(hub_out.listHistory(future=False))

    dagnodes.discard(hub_inn)  # already correctly named
    dagnodes.discard(hub_out)  # already correctly named

    inst.grp_inn = hub_inn
    inst.grp_out = hub_out


    def _get_name(n):
        try:  # pynodes
            return n.nodeName()
        except:  # component
            return n.namespace

    if dagnodes:
        for dagnode in dagnodes:
            from omtk.libs import libNamespaces
            dagnode.rename('{0}:{1}'.format(namespace, _get_name(dagnode).split(':')[-1]))

    libSerialization.export_network(inst)

    return inst