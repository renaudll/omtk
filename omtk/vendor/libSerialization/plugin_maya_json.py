#
# Define a custom JSON Encoder that can be used to export PyNode and Attribute.
#
from maya import cmds
import pymel.core as pymel
import json
from plugin_json import export_json
from plugin_json import export_json_file
from plugin_json import import_json
from plugin_json import import_json_file
__all__ = (
    'export_json_maya',
    'export_json_file_maya',
    'import_json_maya',
    'import_json_file_maya'
)


# TODO: Add support for matrix and vector datatypes
class PymelJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, pymel.PyNode):
            return {'_class_pymel':'pymel.PyNode', '__melobject__': o.__melobject__()}
        elif isinstance(o, pymel.Attribute):
            return {'_class_pymel':'pymel.Attribute', '__melobject__': o.__melobject__()}
        elif isinstance(o, pymel.datatypes.Matrix):
            return {'_class_pymel':'pymel.datatypes.Matrix', '__melobject__': o.__melobject__()}
        elif isinstance(o, pymel.datatypes.Vector):
            return {'_class_pymel':'pymel.datatypes.Vector', '__melobject__': [o.x, o.y, o.z]}
        elif isinstance(o, pymel.datatypes.Point):
            return {'_class_pymel':'pymel.datatypes.Point', '__melobject__': [o.w, o.x, o.y, o.z]}
        else:
            return super(PymelJSONEncoder, self).default(o)


# TODO: Add support for matrix and vector datatypes
class PymelJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(PymelJSONDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, val):
        if isinstance(val, dict):
            cls = val.get('_class_pymel', None)
            if cls == 'pymel.PyNode':
                dagpath = val.get('__melobject__')
                val = pymel.PyNode(dagpath) if cmds.objExists(dagpath) else None  # TODO: add warning?
            elif cls == 'pymel.Attribute':
                dagpath = val.get('__melobject__')
                val = pymel.Attribute(dagpath) if cmds.objExists(dagpath) else None  # TODO: add warning?
            elif cls == 'pymel.datatypes.Matrix':
                melval = val.get('__melobject__')
                val = pymel.datatypes.Matrix(melval)
            elif cls == 'pymel.datatypes.Vector':
                coords = val.get('__melobject__')
                val = pymel.datatypes.Vector(coords)
            elif cls == 'pymel.datatypes.Point':
                coords = val.get('__melobject__')
                val = pymel.datatypes.Point(coords)
        return val

def export_json_maya(*args, **kwargs):
    return export_json(cls=PymelJSONEncoder, *args, **kwargs)

def export_json_file_maya(*args, **kwargs):
    return export_json_file(cls=PymelJSONEncoder, *args, **kwargs)

def import_json_maya(*args, **kwargs):
    return import_json(cls=PymelJSONDecoder, *args, **kwargs)

def import_json_file_maya(*args, **kwargs):
    return import_json_file(cls=PymelJSONDecoder, *args, **kwargs)