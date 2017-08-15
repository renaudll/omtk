import logging

from maya import cmds
from omtk import constants
from omtk.core.classEntity import Entity
from omtk.core.classEntityAction import EntityAction
from omtk.core.classEntityAttribute import get_attrdef_from_attr
from omtk.libs import libAttr
from omtk.libs import libNamespaces
from omtk.vendor import libSerialization
from pymel import core as pymel

log = logging.getLogger('omtk')


# todo: create ComponentScripted and ComponentSaved

class Component(Entity):
    # These need to be defined in order to register a component.
    component_id = None
    component_name = None

    need_grp_inn = True
    need_grp_out = True
    need_grp_dag = False

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

    def get_definition(self):
        from omtk.core import classComponentDefinition

        inst = classComponentDefinition.ComponentDefinition(
            uid=self.uid,
            name=self.name,
            version=self.name,
            author=self.author
        )
        return inst

    def get_namespace(self):
        if self.grp_inn and self.grp_inn.exists():
            return self.grp_inn.namespace().strip(':')
        if self.grp_out and self.grp_out.exists():
            return self.grp_out.namespace().strip(':')
        # We don't want to take the chance to look at the grp_dag namespace as it is visible by the user.
        raise Exception("Cannot resolve namespace for {0}".format(self))

    def build(self):
        if self.need_grp_inn:
            self.grp_inn = pymel.createNode('network', name='inn')
        if self.need_grp_out:
            self.grp_out = pymel.createNode('network', name='out')
        if self.need_grp_dag:
            self.grp_dag = pymel.createNode('transform', name='dag')
        libSerialization.export_network(self)

    def is_built(self):
        return \
            self.grp_inn and self.grp_inn.exists() and \
            self.grp_out and self.grp_out.exists()

    def iter_attributes(self):
        # todo: use factory?
        for attr in self.grp_inn.listAttr(topLevel=True, userDefined=True):
            attr_def = get_attrdef_from_attr(attr, is_input=True, is_output=False)
            if attr_def:
                yield attr_def
        for attr in self.grp_out.listAttr(topLevel=True, userDefined=True):
            attr_def = get_attrdef_from_attr(attr, is_input=False, is_output=True)
            if attr_def:
                yield attr_def

    def iter_actions(self):
        for action in super(Component, self).iter_actions():
            yield action
        yield ActionShowContentInNodeEditor(self)

    def unbuild(self):
        raise NotImplementedError

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
        return libAttr.addAttr(self.grp_inn, long_name, **kwargs)

    def rename_input_attr(self, old_name, new_name):
        # type: (str, str) -> None
        cmds.renameAttr("{0}.{1}".format(self.grp_inn.__melobject__(), old_name), new_name)

    def connect_to_input_attr(self, attr_name, attr_src, **kwargs):
        attr_dst = self.grp_inn.attr(attr_name)
        pymel.connectAttr(attr_src, attr_dst)

    def add_output_attr(self, long_name, **kwargs):
        return libAttr.addAttr(self.grp_out, long_name, **kwargs)

    def rename_output_attr(self, old_name, new_name):
        # type: (str, str) -> None
        cmds.renameAttr("{0}.{1}".format(self.grp_out.__melobject__(), old_name), new_name)

    def connect_to_output_attr(self, attr_name, attr_dst, **kwargs):
        attr_src = self.grp_out.attr(attr_dst)
        pymel.connectAttr(attr_src, attr_dst)

    @classmethod
    def from_attributes(cls, attrs_inn, attrs_out, dag_root=None, swap=True):
        inst = cls()

        hub_inn = pymel.createNode('network', name=constants.COMPONENT_HUB_INN_NAME)
        hub_out = pymel.createNode('network', name=constants.COMPONENT_HUB_OUT_NAME)

        for attr_inn in attrs_inn:
            attr_name = libAttr.get_unique_attr_name(hub_inn, libAttr.escape_attr_name(attr_inn.longName()))
            # Check if the attribute exist before transfering it.
            # This can happen with build-in attribute like translateX since the hub is a transform.
            # It might be more logical to use networks for this, but we'll stick with transforms for now.
            data = libAttr.holdAttr(attr_inn, delete=False)
            data['node'] = hub_inn
            data['longName'] = attr_name
            data['shortName'] = attr_name
            data['niceName'] = attr_name
            libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
            hub_inn_attr = hub_inn.attr(attr_name)
            libAttr.swapAttr(attr_inn, hub_inn_attr, inputs=False, outputs=swap)
            if not swap:
                pymel.connectAttr(hub_inn_attr, attr_inn)

        for attr_out in attrs_out:
            attr_name = libAttr.get_unique_attr_name(hub_out, libAttr.escape_attr_name(attr_out.longName()))
            data = libAttr.holdAttr(attr_out, delete=False)
            data['node'] = hub_out
            data['longName'] = attr_name
            data['shortName'] = attr_name
            data['niceName'] = attr_name
            libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
            hub_out_attr = hub_out.attr(attr_name)
            libAttr.swapAttr(hub_out_attr, attr_out, inputs=swap, outputs=False)
            if not swap:
                pymel.connectAttr(attr_out, hub_out_attr)
                # if not isolate:
                #    pymel.connectAttr(hub_out.attr(attr_name), attr_out)

        inst.grp_inn = hub_inn
        inst.grp_out = hub_out

        if dag_root:
            hub_dag = pymel.createNode('transform', name=constants.COMPONENT_HUB_DAG_NAME)
            dag_root.setParent(hub_dag)
            inst.grp_dag = hub_dag

        libSerialization.export_network(inst)

        return inst

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

    def get_children(self):
        result = (set(self.grp_inn.listHistory(future=True)) & set(self.grp_out.listHistory(future=False))) - {
            self.grp_inn, self.grp_out}
        if self.grp_dag:
            result.add(self.grp_dag)
            result.update(self.grp_dag.listRelatives(allDescendents=True))
        return result

    def export(self, path):
        children = self.get_children() | {self.grp_inn, self.grp_out}
        if not children:
            raise Exception("Can't export component, component is empty!")

        # Hold current file
        current_path = cmds.file(q=True, sn=True)

        # todo: disconnect hub

        pymel.select(children)
        cmds.file(rename=path)
        cmds.file(force=True, exportSelected=True, type="mayaAscii")

        # Fetch current file
        cmds.file(rename=current_path)

        # todo: reconnect hub

        definition = self.get_definition()
        definition.write_metadata_to_file(path)

        return True


class ComponentScripted(Component):
    @classmethod
    def get_definition(cls):
        from omtk.core import classComponentDefinition
        from omtk.core import api

        inst = classComponentDefinition.ComponentScriptedDefinition(
            uid=cls.component_id,
            name=cls.component_name,
            version=api.get_version(),
        )
        inst.component_cls = cls
        return inst


# --- Actions ---

class ActionShowContentInNodeEditor(EntityAction):
    def get_name(self):
        return 'Show content in Node Editor'

    def _create_node_editor(self):
        cmds.window()
        form = cmds.formLayout()
        p = cmds.scriptedPanel(type="nodeEditorPanel", label="Node Editor")
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
