from omtk.libs import libAttr
from pymel import core as pymel
from omtk.core.classEntity import Entity
from omtk.core.classEntityAttribute import get_attrdef_from_attr
from omtk.vendor import libSerialization

from omtk import constants


# todo: create ComponentScripted and ComponentSaved

class Component(Entity):
    need_grp_inn = True
    need_grp_out = True
    need_grp_dag = False

    def __init__(self, name=None):
        super(Component, self).__init__()

        # Not sure about this one
        self.name = name

        self.version = None

        # Network object that hold all the input attributes.
        self.grp_inn = None

        # Network object that hold all the output attributes.
        self.grp_out = None

        # Network object to hold any DagNode belonging to the component.
        self.grp_dag = None

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
        for attr in self.grp_inn.listAttr(userDefined=True):
            attr_def = get_attrdef_from_attr(attr, is_input=True, is_output=False)
            if attr_def:
                yield attr_def
        for attr in self.grp_out.listAttr(userDefined=True):
            attr_def = get_attrdef_from_attr(attr, is_input=False, is_output=True)
            if attr_def:
                yield attr_def

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

    def add_input_attr(self, long_name, **kwargs):
        return libAttr.addAttr(self.grp_inn, long_name, **kwargs)

    def add_output_attr(self, long_name, **kwargs):
        return libAttr.addAttr(self.grp_out, long_name, **kwargs)

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
            #if not isolate:
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
            #if not isolate:
            #    pymel.connectAttr(hub_out.attr(attr_name), attr_out)

        inst.grp_inn = hub_inn
        inst.grp_out = hub_out

        libSerialization.export_network(inst)

        return inst

    def get_children(self):
        return (set(self.grp_inn.listHistory()) | set(self.grp_out.listHistory())) - {self.grp_inn, self.grp_out}