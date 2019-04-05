import logging

from omtk import constants
from omtk.component.component_port import ComponentPort
from omtk.core import manager
from omtk.core.entity import Entity
from omtk.core.entity_action import EntityAction
from omtk.libs import libNamespaces
from omtk.vendor import libSerialization

log = logging.getLogger(__name__)


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

        # Normalize the namespace.
        # We don't track if it's a root namespace or not.
        namespace = namespace.strip(':') if namespace else None

        self.namespace = namespace

        self.uid = self.component_id

        # Component can have a definition that define information needed to identify them.
        self.definition = None

        # A component can have a 'inn' node.
        # Each input custom attribute of this object will be exposed outside of the component.
        self.grp_inn = None

        # A component can have an 'out' node.
        # Each output custom attribute of this object will be exposed outside of the component.
        self.grp_out = None

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

    def get_definition(self):
        # type: () -> ComponentDefinition
        """
        Return metadata associated with the component.
        :return: A Component definition object.
        """
        from maya import cmds
        import pymel.core as pymel

        metadata_dagpath = '{0}:metadata'.format(self.namespace)
        if not cmds.objExists(metadata_dagpath):
            return None
        else:
            metadata_node = pymel.PyNode(metadata_dagpath)
            m = manager.get_session()
            component_def = m.import_network(metadata_node)
            return component_def

    def build_interface(self):
        """
        Create the Component input, output and dag hub. Define all public attributes.
        However does not build what between the input and output hub.
        This is separated in it's own method since we might want to set public attributes before building
        the content, especially if the content depend on some attribute value.
        """
        import pymel.core as pymel
        sel = pymel.selected()

        if self.need_grp_inn:
            self.grp_inn = pymel.createNode('network', name='inn')
        if self.need_grp_out:
            self.grp_out = pymel.createNode('network', name='out')

        pymel.select(sel)  # todo: keep_selection decorator

        m = manager.get_session()
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
        from omtk.libs import libAttr
        attrs_inn = set(libAttr.iter_network_contributing_attributes(self.grp_inn))
        attrs_out = set(libAttr.iter_network_contributing_attributes(self.grp_out))
        custom_attrs = set(self.grp_inn.listAttr(userDefined=True)) | set(self.grp_out.listAttr(userDefined=True))
        attrs_inn &= custom_attrs
        attrs_out &= custom_attrs

        attr_by_name = {attr.longName(): attr for attr in attrs_inn | attrs_out}
        for name, attr in attr_by_name.iteritems():
            # yield get_attribute_definition(self, attr)
            yield ComponentPort(self, name, attr)

    def iter_actions(self):
        for action in super(Component, self).iter_actions():
            yield action
        yield ActionShowContentInNodeEditor(self)

    def unbuild(self):
        import pymel.core as pymel
        from maya import cmds

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
        cmds.namespace(mergeNamespaceWithParent=True, removeNamespace=self.namespace)

    def optimize(self):
        """
        Implement optimisation routines. Call before publishing rig to animation.
        There's multiple things that can be done here, here's some idea:
        - Remove the inn and out hub.
        - Check if decomposeMatrix are sent to composeMatrix and vice versa and remove them.

        :return:
        :rtype: bool
        """
        return False

    def is_modified(self):
        """
        Check if a component have been modified since it's construction.

        :rtype: bool
        """
        raise NotImplementedError

    # --- Interface management ---

    def add_input_attr(self, long_name, **kwargs):
        """

        :param str long_name:
        :param kwargs:
        :return:
        :rtype: pymel.Attribute
        """
        from omtk.libs import libAttr
        return libAttr.addAttr(self.grp_inn, long_name, **kwargs)

    def has_input_attr(self, attr_name):
        """
        :param str attr_name:
        :return:
        :rtype: bool
        """
        return self.grp_inn.hasAttr(attr_name)

    def get_input_attr(self, attr_name):
        """
        :param str attr_name:
        :return:
        :rtype: bool
        """
        return self.grp_inn.attr(attr_name)

    def get_input_attributes(self):
        """

        :return:
        :rtype: list of pymel.Attribute
        """
        return self.grp_inn.listAttr(userDefined=True)

    def add_output_attr(self, long_name, **kwargs):
        """

        :param str long_name:
        :param kwargs:
        :return: An attribute
        :rtype: pymel.Attribute
        """
        from omtk.libs import libAttr
        return libAttr.addAttr(self.grp_out, long_name, **kwargs)

    def has_output_attr(self, attr_name):
        """

        :param str attr_name:
        :return:
        :rtype: bool
        """
        # type: (str) -> bool
        return self.grp_out.hasAttr(attr_name)

    def get_output_attr(self, attr_name):
        """

        :param str attr_name:
        :return:
        :rtype: pymel.Attribute
        """
        return self.grp_out.attr(attr_name)

    def get_output_attributes(self):
        """

        :return: List of attributes
        :rtype: list of pymel.Attribute
        """
        return self.grp_out.listAttr(userDefined=True)

    def connect_to_input_attr(self, attr_name, attr_src, **kwargs):
        """

        :param str attr_name:
        :param pymel.Attribute attr_src:
        """
        import pymel.core as pymel
        if not self.grp_inn.hasAttr(attr_name):
            log.warning("Cannot reconnect {0} to {1}. {0} doesnt exist.".format(attr_name, attr_src))
            return
        if not attr_src.exists():
            log.warning("Cannot reconnect {0} to {1}. {1} doesnt exist.".format(attr_name, attr_src))
            return
        attr_dst = self.grp_inn.attr(attr_name)
        log.info("Connecting {0} to {1}".format(attr_src, attr_dst))
        pymel.connectAttr(attr_src, attr_dst)

    def connect_to_output_attr(self, attr_name, attr, **kwargs):
        """

        :param str attr_name:
        :param pymel.Attribute attr:
        :param kwargs:
        """
        import pymel.core as pymel
        if not self.grp_out.hasAttr(attr_name):
            log.warning("Cannot reconnect {0} to {1}. {0} doesnt exist.".format(attr, attr_name))
            return
        if not attr.exists():
            log.warning("Cannot reconnect {0} to {1}. {1} doesnt exist.".format(attr, attr_name))
            return
        attr_src = self.grp_out.attr(attr_name)
        log.info("Connecting {0} to {1}".format(attr_src, attr))
        pymel.connectAttr(attr_src, attr)

    def explode(self):
        """Delete the component and it's hub, remaping the attribute to their original location."""
        if not self.is_built():
            raise Exception("Cannot explode an unbuilt component.")

        def _remap_attr(attr):
            import pymel.core as pymel
            attr_src = next(iter(attr.inputs(plugs=True)), None)
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
        """
        The children of the component are any DgNode that are under our namespace.
        :return:
        :rtype list pymel.nodetypes.DependNode
        """
        import pymel.core as pymel
        return pymel.ls('{0}:*'.format(self.namespace))

    def export(self, path):
        """

        :param str path:
        """
        import pymel.core as pymel
        from maya import cmds
        from omtk.libs.libAttr import context_disconnected_attrs

        children = self.get_children()
        if not children:
            raise Exception("Can't export component, component is empty!")

        # Ensure the component metadata is exported
        m = manager.get_session()
        network = m.export_network(self)

        objs_to_export = set(children) | {self.grp_inn, self.grp_out, network}

        # Hold current file
        current_path = cmds.file(q=True, sn=True)

        # todo: optimise this
        grp_inn_attrs = set(self.grp_inn.listAttr())
        grp_inn_attrs.remove(self.grp_inn.message)
        grp_out_attrs = set(self.grp_out.listAttr())
        grp_out_attrs.remove(self.grp_out.message)

        with context_disconnected_attrs(grp_inn_attrs, hold_inputs=True, hold_outputs=False):
            with context_disconnected_attrs(grp_out_attrs, hold_inputs=False, hold_outputs=True):
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

    def set_definition(self, component_def):
        """

        :param ComponentDefinition component_def:
        :return:
        """
        from maya import cmds
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
        import pymel.core as pymel
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
        from maya import cmds
        old_namespace = self.namespace
        new_namespace = libNamespaces.get_unique_namespace(new_namespace)
        cmds.namespace(addNamespace=new_namespace)
        cmds.namespace(moveNamespace=(self.namespace, new_namespace))
        cmds.namespace(removeNamespace=old_namespace)
        self.namespace = new_namespace

    def delete(self):
        self.unbuild()  # todo: merge methods?

    def update(self, new_def):
        """
        Update a component to a new definition.
        This will try to preserve any attribute connection.

        :param new_def: A component definition
        :return: A new component instance
        """
        old_namespace = self.namespace
        map_inn, map_out = self.get_connections_relative()
        self.delete()

        inst_2 = new_def.instanciate(name=old_namespace)  # todo: rename to namespace
        for attr_name, attr_srcs in map_inn.iteritems():
            for attr_src in attr_srcs:
                inst_2.connect_to_input_attr(attr_name, attr_src)
        for attr_name, attr_dsts in map_out.iteritems():
            for attr_dst in attr_dsts:
                inst_2.connect_to_output_attr(attr_name, attr_dst)

        return inst_2


# --- Actions ---

class ActionShowContentInNodeEditor(EntityAction):
    def get_name(self):
        return 'Show in Maya Node Editor'

    def _create_node_editor(self):
        from maya import cmds
        cmds.window()
        form = cmds.formLayout()
        p = cmds.scriptedPanel(type="nodeEditorPanel", label="Node Editor.md")
        cmds.formLayout(form, e=True, af=[(p, s, 0) for s in ("top", "bottom", "left", "right")])
        cmds.showWindow()
        return p + 'NodeEditorEd'

    def execute(self):
        from maya import cmds
        import pymel.core as pymel

        children = set(self.component.get_children())
        if not children:
            log.debug('Cannot open NodeEditor to explore {0} content. No children to display!'.format(self.component))
            return
        children.add(self.component.grp_inn)
        children.add(self.component.grp_out)

        node_editor = self._create_node_editor()
        pymel.select(children)
        cmds.nodeEditor(node_editor, e=True, addNode='')


def __get_namespace(n):
    try:
        return n.namespace()
    except AttributeError:
        return n.namespace


def _get_parent_namespace(nodes):
    """
    Resolve the parent namespace.
    This allow a component to be inside another component.
    However we don't want to have nodes in our component that don't share the same namespace since
    a component cannot logically have multiple parents.
    """

    namespaces = {__get_namespace(node).strip(':') for node in nodes}
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
