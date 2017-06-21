"""
A ComponentAttribute is the link between internal data and the gui.
It deal with typing and validation (used for drag and drop events for now)
"""
import logging
import pymel.core as pymel

log = logging.getLogger('omtk')

_ENTITY_ATTR_TYPE_BY_MAYA_ATTR_TYPE = {
    'bool': bool,
    'long': int,
    'short': int,
    'byte': int,
    'char': str,
    'enum': int,
    'float': float,
    'double': float,
    'doubleAngle': float,
    'doubleLinear': float,
    'string': str,
    'stringArray': str,
    'time': float,
    'matrix': pymel.datatypes.Matrix,
    'fltMatrix': pymel.datatypes.Matrix,
    'float2': float,  # ???,  # ???
    'float3': pymel.datatypes.Vector,
    'double2': float,  # ???, # ???
    'double3': pymel.datatypes.Vector,
    'long2': int,  # ???,  # ???
    'long3': pymel.datatypes.Vector,
    'short2': pymel.datatypes.Vector,
    'short3': pymel.datatypes.Vector,
    'doubleArray': float,
    'Int32Array': int,
    'vectorArray': pymel.datatypes.Vector,
    'nurbsCurve': pymel.nodetypes.NurbsCurve,
    'nurbsSurface': pymel.nodetypes.NurbsSurface,
    'mesh': pymel.nodetypes.Mesh,
    'lattice': pymel.nodetypes.Lattice,
}


class EntityAttribute(object):
    def __init__(self, name, is_input=True, is_output=True, fn_get=None, fn_set=None, val=None):
        self.name = name
        self._val = val
        self.is_input = is_input
        self.is_output = is_output
        self._fn_get = fn_get
        self._fn_set = fn_set

    def get(self):
        if self._fn_get:
            return self._fn_get()
        log.warning("Attribute {0} have not getter defined!".format(self))
        return None
        # raise Exception("Attribute {0} have not getter defined!".format(self))

    def set(self, val):
        if self._fn_set:
            return self._fn_set()
        raise Exception("Attribute {0} have no setter defined!".format(self))

    def validate(self, val):
        """
        Check if a provided value can be set on this EntityAttribute.
        :param val: An object instance or a basic value.
        :return: True if the value can be set. False otherwise.
        """
        return True


class EntityAttributeTyped(EntityAttribute):
    def __init__(self, attr, **kwargs):
        self._attr = attr
        self._valid_types = _ENTITY_ATTR_TYPE_BY_MAYA_ATTR_TYPE[attr.type()]
        super(EntityAttributeTyped, self).__init__(
            name=attr.attrName(),
            fn_get=attr.get,
            fn_set=attr.set,
            **kwargs
        )

    def validate(self, val):
        print val, self._valid_types
        return isinstance(val, self._valid_types)


class EntityAttributeTypedCollection(EntityAttributeTyped):
    def validate(self, val):
        # Validate iterable values
        if isinstance(val, (list, tuple, set)):
            return all(super(EntityAttributeTypedCollection, self).validate(entry) for entry in val)
        # Otherwise validate single values
        else:
            return super(EntityAttributeTypedCollection, self).validate(val)


def get_attrdef_from_attr(attr, is_input=False, is_output=False):
    valid_types = _ENTITY_ATTR_TYPE_BY_MAYA_ATTR_TYPE.get(attr.type())
    if valid_types is None:
        log.warning("Cannot create AttributeDef from {0}".format(attr))
        return None

    if attr.isMulti():
        return EntityAttributeTypedCollection(attr, is_input=is_input, is_output=is_output)
    else:
        return EntityAttributeTyped(attr, is_input=is_input, is_output=is_output)
