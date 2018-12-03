import json


class NodePreset(object):
    def __init__(self, map):
        self._map = map

    def apply(self, session, node):
        for name, kwargs in self._map.iteritems():
            try:
                session.create_port(node, name, **kwargs)
            except Exception as e:  # FIXME
                pass

    @classmethod
    def fromDict(cls, map):
        return NodePreset(map)


class NodePresetRegistry(object):
    def __init__(self):
        self._registry = {}

    def register(self, node_type, preset):
        assert (isinstance(preset, NodePreset))

        if node_type in self._registry:
            raise Exception("Preset is already registered.")

        self._registry[node_type] = preset

    def get(self, node_type):
        """
        Return the preset associated with the provided node type.

        :param str node_type: The node type to query.
        :return: The node configuration
        :rtype: NodePreset
        """
        return self._registry.get(node_type)


_path_schema = '/home/rll/dev/python/omtk/python/omtk/vendor/mock_maya/schema.json'

REGISTRY_DEFAULT = NodePresetRegistry()

with open(_path_schema) as fp:
    data = json.load(fp)

    for node_type, attr_data in data.iteritems():
        preset = NodePreset(attr_data)
        REGISTRY_DEFAULT.register(node_type, preset)
