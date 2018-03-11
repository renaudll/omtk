from omtk.core import entity_attribute
from omtk.factories import factory_datatypes
from omtk.qt_widgets.nodegraph.models.port.port_adaptor_base import NodeGraphPortImpl
from omtk.qt_widgets.nodegraph.models.port.port_adaptor_pymel import PymelAttributeNodeGraphPortImpl
from pymel import core as pymel
from omtk.core import component

class EntityAttributeNodeGraphPortImpl(NodeGraphPortImpl):
    def __init__(self, data, adaptor=None):
        assert (isinstance(data, entity_attribute.EntityAttribute))
        self._data = data

        # Some EntityAttribute points to pymel attributes.
        if adaptor:
            self._pymel_adaptor = adaptor
        else:
            if isinstance(data, entity_attribute.EntityPymelAttribute):
                self._pymel_adaptor = PymelAttributeNodeGraphPortImpl(data.get_raw_data())
            else:
                self._pymel_adaptor = None

    def get_metadata(self):
        return self._data.get_raw_data()

    def get_metatype(self):
        if isinstance(self._data, entity_attribute.EntityPymelAttribute):
            return factory_datatypes.get_attr_datatype(self._data.get_raw_data())
        else:
            return factory_datatypes.get_datatype(self.get_metadata())

    def is_readable(self):
        return self._data.is_output

    def is_writable(self):
        return self._data.is_input

    def is_interesting(self):
        return True

    def is_source(self):
        if self._pymel_adaptor:
            return self._pymel_adaptor.is_source()

        return False

    def is_destination(self):
        if self._pymel_adaptor:
            return self._pymel_adaptor.is_destination()

        val = self._data.get()
        if isinstance(val, list):
            for entry in val:
                datatype = factory_datatypes.get_datatype(entry)
                if datatype in (
                        factory_datatypes.AttributeType.Node,
                        factory_datatypes.AttributeType.Component,
                        factory_datatypes.AttributeType.Module,
                        factory_datatypes.AttributeType.Rig
                ):
                    return True
            if isinstance(val, pymel.PyNode):
                return True
        return bool(val)

    def get_inputs(self):
        if self._pymel_adaptor:
            return self._pymel_adaptor.get_inputs()

        return []

    def get_outputs(self):
        if self._pymel_adaptor:
            return self._pymel_adaptor.get_outputs()

        return []

    def connect_from(self, val):
        if isinstance(self._data, entity_attribute.EntityPymelAttribute):
            self._pymel_adaptor.connect_from(val)
        else:
            raise NotImplementedError

    def connect_to(self, val):
        if isinstance(self._data, entity_attribute.EntityPymelAttribute):
            self._pymel_adaptor.connect_to(val)
        else:
            raise NotImplementedError
