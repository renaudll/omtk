import logging

import omtk.constants
from maya import cmds
from omtk import constants
from omtk.core import session
from omtk.core.entity import Entity
from omtk.core.entity_action import EntityAction
from omtk.core.entity_attribute import get_attrdef_from_attr
from omtk.libs import libAttr
from omtk.libs import libNamespaces
from omtk.libs import libComponents
from omtk.vendor import libSerialization
from pymel import core as pymel
from . import component_definition

log = logging.getLogger('omtk')


if False:  # for type hinting
    from omtk.core.component_definition import ComponentDefinition

# todo: create ComponentScripted and ComponentSaved


class Component(Entity):
    # These need to be defined in order to register a component.
    component_id = None
    component_name = None

    need_grp_inn = True
    need_grp_out = True
    need_grp_dag = True

    def __init__(self, name=None):
        super(Component, self).__init__()

        self.uid = self.component_id

        # Not sure about this one
        self.name = name if name else self.component_name

        self.version = None

        self.author = ''

        # Network object that hold all the input attributes.
        self.grp_inn = None

        # Network object that hold all the output attributes.
        self.grp_out = None

        # Network object to hold any DagNode belonging to the component.
        self.grp_dag = None

        # Used for dynamic components. Define if a Component content need to be regenerated.
        self._is_dirty_content = True

    def get_name(self):
        # todo: store the instance name in the class?
        # currently we'll use the namespace which is not ideal
        if self.grp_inn:
            return self.grp_inn.namespace().strip(':')
        if self.grp_out:
            return self.grp_out.namespace().strip(':')
        if self.grp_dag:
            return self.grp_dag.namespace().strip(':')

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
        inst = component_definition.ComponentDefinition(
            uid=self.uid,
            name=self.name,
            version=self.version,
            author=self.author
        )
        return inst

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
        if self.need_grp_dag:
            self.grp_dag = pymel.createNode('transform', name='dag')

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
        # Hub inn
        custom_attrs = self.grp_inn.listAttr(userDefined=True)
        for attr in libAttr.iter_network_contributing_attributes(self.grp_inn):
            if attr not in custom_attrs:
                continue
            attr_def = get_attrdef_from_attr(attr, is_input=True, is_output=False)
            if attr_def:
                yield attr_def

        # Hub out
        custom_attrs = self.grp_out.listAttr(userDefined=True)
        for attr in libAttr.iter_network_contributing_attributes(self.grp_out):
            if attr not in custom_attrs:
                continue
            attr_def = get_attrdef_from_attr(attr, is_input=False, is_output=True)
            if attr_def:
                yield attr_def

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
        if self.grp_dag and self.grp_dag.exists():
            objs_to_delete.append(self.grp_dag)
        if objs_to_delete:
            pymel.delete(objs_to_delete)
        self.grp_inn = None
        self.grp_out = None
        self.grp_dag = None

    def optimize(self):
        # type: () -> bool
        """
        Implement optimisation routines. Call before publishing rig to animation.
        :return:
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
        attr_dst = self.grp_inn.attr(attr_name)
        pymel.connectAttr(attr_src, attr_dst)

    def connect_to_output_attr(self, attr_name, attr_dst, **kwargs):
        attr_src = self.grp_out.attr(attr_dst)
        pymel.connectAttr(attr_src, attr_dst)

    # @classmethod
    # def from_attributes(cls, attrs_inn, attrs_out, swap=False):
    #     inst = cls()
    #
    #     hub_inn = pymel.createNode('network', name=constants.COMPONENT_HUB_INN_NAME)
    #     hub_out = pymel.createNode('network', name=constants.COMPONENT_HUB_OUT_NAME)
    #
    #     for attr_inn in attrs_inn:
    #         attr_name = libAttr.get_unique_attr_name(hub_inn, libAttr.escape_attr_name(attr_inn.longName()))
    #         # Check if the attribute exist before transfering it.
    #         # This can happen with build-in attribute like translateX since the hub is a transform.
    #         # It might be more logical to use networks for this, but we'll stick with transforms for now.
    #         data = libAttr.holdAttr(attr_inn, delete=False)
    #         data['node'] = hub_inn
    #         data['longName'] = attr_name
    #         data['shortName'] = attr_name
    #         data['niceName'] = attr_name
    #         libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
    #         hub_inn_attr = hub_inn.attr(attr_name)
    #         libAttr.swapAttr(attr_inn, hub_inn_attr, inputs=False, outputs=swap)
    #         if not swap:
    #             pymel.connectAttr(hub_inn_attr, attr_inn)
    #
    #     for attr_out in attrs_out:
    #         attr_name = libAttr.get_unique_attr_name(hub_out, libAttr.escape_attr_name(attr_out.longName()))
    #         data = libAttr.holdAttr(attr_out, delete=False)
    #         data['node'] = hub_out
    #         data['longName'] = attr_name
    #         data['shortName'] = attr_name
    #         data['niceName'] = attr_name
    #         libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
    #         hub_out_attr = hub_out.attr(attr_name)
    #         libAttr.swapAttr(hub_out_attr, attr_out, inputs=swap, outputs=False)
    #         if not swap:
    #             pymel.connectAttr(attr_out, hub_out_attr)
    #             # if not isolate:
    #             #    pymel.connectAttr(hub_out.attr(attr_name), attr_out)
    #
    #     inst.grp_inn = hub_inn
    #     inst.grp_out = hub_out
    #
    #     if dag_root:
    #         hub_dag = pymel.createNode('transform', name=constants.COMPONENT_HUB_DAG_NAME)
    #         dag_root.setParent(hub_dag)
    #         inst.grp_dag = hub_dag
    #
    #     libSerialization.export_network(inst)
    #
    #     return inst

    @classmethod
    def create(cls, attrs_inn, attrs_out, dagnodes=None):
        """
        Create a Component from existing nodes.
        :param dagnodes: A list of nodes to include in the component.
        :param attrs_inn: A dict(k, v) of public input attributes where k is attr name and v is the reference attribute.
        :param attrs_out: A dict(k, v) of publish output attributes where k is attr name v is the reference attribute.
        :return: Component instance.
        """
        # todo: do we want to force readable or writable attributes? can this fail?
        # Find an available namespace
        # This allow us to make sure that we'll have access to unique name.
        # Note theses namespaces will be removed in any exported file.
        namespace = libNamespaces.get_unique_namespace('component', enforce_suffix=True)
        cmds.namespace(add=namespace)

        inst = cls()

        hub_inn = pymel.createNode('network', name='{0}:{1}'.format(namespace, constants.COMPONENT_HUB_INN_NAME))
        hub_out = pymel.createNode('network', name='{0}:{1}'.format(namespace, constants.COMPONENT_HUB_OUT_NAME))

        # Create the hub_inn attribute.
        for attr_name, attr_ref in attrs_inn.iteritems():
            data = libAttr.AttributeData.from_pymel_attribute(attr_ref, store_inputs=True, store_outputs=True)
            if not data.is_writable:
                raise IOError("Expected a writable attribute as an input reference.")
            data.rename(attr_name)
            hub_attr = data.copy_to_node(hub_inn)
            pymel.connectAttr(hub_attr, attr_ref, force=True)
            data.connect_stored_inputs(hub_inn)

        # Create the hub_out attribute.
        for attr_name, attr_ref in attrs_out.iteritems():
            data = libAttr.AttributeData.from_pymel_attribute(attr_ref, store_inputs=True, store_outputs=True)
            if not data.is_readable:
                raise IOError("Expected a readable attribute as an output reference.")
            data.rename(attr_name)
            hub_attr = data.copy_to_node(hub_out)
            pymel.connectAttr(attr_ref, hub_attr)
            data.connect_stored_outputs(hub_out)

        inst.grp_inn = hub_inn
        inst.grp_out = hub_out

        if dagnodes:
            hub_dag = pymel.createNode('transform', name='{0}:{1}'.format(namespace, constants.COMPONENT_HUB_DAG_NAME))
            dagnodes_set = set(dagnodes)
            for dagnode in dagnodes:
                dagnode.rename('{0}:{1}'.format(namespace, dagnode.nodeName()))

                # We'll only parent to the dag grp provided nodes that are not child of other provided node.
                allparents_set = set(dagnode.getAllParents())
                if not dagnodes_set & allparents_set:
                    dagnode.setParent(hub_dag)
            inst.grp_dag = hub_dag

            libSerialization.export_network(inst)

        return inst

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
        result = (set(self.grp_inn.listHistory(future=True)) & set(self.grp_out.listHistory(future=False))) - {
            self.grp_inn, self.grp_out}
        if self.grp_dag:
            result.add(self.grp_dag)
            result.update(self.grp_dag.listRelatives(allDescendents=True))
        return result

    def export(self, path):
        children = self.get_children()
        if not children:
            raise Exception("Can't export component, component is empty!")

        # Ensure the component metadata is exported
        m = session.get_session()
        network = m.export_network(self)

        objs_to_export = children | {self.grp_inn, self.grp_out, network}
        if self.grp_dag:
            objs_to_export.add(self.grp_dag)

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
        elif self.grp_dag:
            namespace = self.grp_dag.namespace()
        if namespace:
            libComponents.remove_namespace_from_file(path, namespace)

        return True

    def set_definition(self, component_def):
        # type: (ComponentDefinition) -> None
        self.name = component_def.name
        self.author = component_def.author
        self.version = component_def.version
        self.uid = component_def.uid

        # Re-export metadata
        libSerialization.export_network(self)


# todo: create IComponent class?

class ComponentScripted(Component):
    @classmethod
    def get_definition(cls):
        from omtk.core import component_definition

        inst = component_definition.ComponentScriptedDefinition(
            uid=cls.component_id,
            name=cls.component_name,
            version=omtk.constants.get_version(),
        )
        inst.component_cls = cls
        return inst

    def build_content(self):
        """
        Build the content between the inn and out hub.
        This is separated in it's own method since in some Component, changing an attribute value can necessitate
        a rebuild of the content but not of the public interface.
        :return:
        """
        pass

    def build(self):
        self.build_interface()
        self.build_content()

    def is_built_interface(self):
        return \
            self.grp_inn and self.grp_inn.exists() and \
            self.grp_out and self.grp_out.exists()

    def is_built(self):
        return self.is_built_interface()


# --- Actions ---

class ActionShowContentInNodeEditor(EntityAction):
    def get_name(self):
        return 'Show content in Node Editor.md'

    def _create_node_editor(self):
        cmds.window()
        form = cmds.formLayout()
        p = cmds.scriptedPanel(type="nodeEditorPanel", label="Node Editor.md")
        cmds.formLayout(form, e=True, af=[(p, s, 0) for s in ("top", "bottom", "left", "right")])
        cmds.showWindow()
        return p + 'NodeEditorEd'

    def execute(self):
        children = self.component.get_children()
        if not children:
            log.debug('Cannot open NodeEditor to explore {0} content. No children to display!'.format(self.component))
            return
        children.add(self.component.grp_inn)
        children.add(self.component.grp_out)

        node_editor = self._create_node_editor()
        pymel.select(children)
        cmds.nodeEditor(node_editor, e=True, addNode='')
