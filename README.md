# libSerialization
Generic serialization library for python that support json and pymel datatypes.

It was originally present as a submodule in omtk.

## Examples
```
import libSerialization

class MyClass(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
foo = MyClass(foo=1, bar=True, foobar="Hello")

# Export to basic datatype
dist_instance = libSerialization.export_dict(foo)
new_dict = libSerialization.import_dict(dist_instance)

# Export to json
path_json = '/tmp/test.json'
libSerialization.export_json_file(path_json, foo)
new_json = libSerialization.import_json_file(path_json)

# Export to maya network datatypes
network = libSerialization.export_network(foo)
new_maya = libSerialization.import_network(network)
```
