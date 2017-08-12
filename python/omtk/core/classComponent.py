import logging

from maya import cmds
from omtk import constants
from omtk.core.classEntity import Entity
from omtk.core.classEntityAction import EntityAction
from omtk.core.classEntityAttribute import get_attrdef_from_attr
from omtk.libs import libAttr
from omtk.vendor import libSerialization
from pymel import core as pymel
from omtk import manager

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

        # Used for dynamic components. Define if a Component content need to be regenerated.
        self._is_dirty_content = True

    def is_dirty_content(self):
        return self._is_dirty_content

    def set_content_dirty(self, state=True):
        self._is_dirty_content = state

    def get_definition(self):
        from omtk.core import classComponentDefinition

        inst = classComponentDefinition.ComponentDefinition(
            uid=self.uid,
            name=self.name,
            version=self.name,
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
        # Not needed
        pass

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

    def is_modified(self):
        # type: () -> bool
        """
        Check if a component have been modified since it's construction.
        todo: implement it, how???
        :return:
        """
        raise NotImplementedError

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
        # type: (str) -> pymel.Attribute
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

    @classmethod
    def from_attributes(cls, attrs_inn, attrs_out):
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
            libAttr.swapAttr(attr_inn, hub_inn.attr(attr_name), inputs=False, outputs=True)
            # if not isolate:
            #    pymel.connectAttr(attr_inn, hub_inn.attr(attr_name))

        for attr_out in attrs_out:
            attr_name = libAttr.get_unique_attr_name(hub_out, libAttr.escape_attr_name(attr_out.longName()))
            data = libAttr.holdAttr(attr_out, delete=False)
            data['node'] = hub_out
            data['longName'] = attr_name
            data['shortName'] = attr_name
            data['niceName'] = attr_name
            libAttr.fetchAttr(data, reconnect_inputs=False, reconnect_outputs=False)
            libAttr.swapAttr(hub_out.attr(attr_name), attr_out, inputs=True, outputs=False)
            # if not isolate:
            #    pymel.connectAttr(hub_out.attr(attr_name), attr_out)

        inst.grp_inn = hub_inn
        inst.grp_out = hub_out

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
        return (set(self.grp_inn.listHistory(future=True)) & set(self.grp_out.listHistory(future=False))) - {
            self.grp_inn, self.grp_out}

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

    def build_interface(self):
        """
        Create the Component input, output and dag hub. Define all public attributes.
        However does not build what between the input and output hub.
        This is separated in it's own method since we might want to set public attributes before building
        the content, especially if the content depend on some attribute value.
        """
        if self.need_grp_inn:
            self.grp_inn = pymel.createNode('network', name='inn')
        if self.need_grp_out:
            self.grp_out = pymel.createNode('network', name='out')
        if self.need_grp_dag:
            self.grp_dag = pymel.createNode('transform', name='dag')

        m = manager.get_manager()
        m.export_network(self)

        # -> any inherited class would want to add input and output attributes here <-

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
