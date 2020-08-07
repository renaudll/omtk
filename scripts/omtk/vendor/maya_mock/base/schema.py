"""
Schema related classes.
A schema hold information about maya default state, including default node types.
"""
import copy
import logging
import json

_LOG = logging.getLogger(__name__)


def get_namespace_parent(namespace):
    """
    From a provided namespace, return it's parent or None if there's no parent.

    >>> get_namespace_parent('org.foo.bar')
    'org.foo'
    >>> get_namespace_parent('org') is None
    True

    :param str namespace: The namespace to namespace.
    :return: The parent namespace
    :rtype: str
    """
    return namespace.rsplit(".", 1)[0] if "." in namespace else None


def get_namespace_leaf(namespace):
    """
    From a provided namespace, return it's leaf.

    >>> get_namespace_leaf('foo.bar')
    'bar'
    >>> get_namespace_leaf('foo')
    'foo'

    :param namespace:
    :return:
    """
    return namespace.rsplit(".", 1)[-1]


def iter_namespaces(namespaces):
    """
    From a list of namespace, yield all namespaces including their parent in hierarchy order.

    >>> tuple(iter_namespaces(['a.b', 'a.b.c', 'd.e']))
    ('a', 'a.b', 'a.b.c', 'd', 'd.e')

    :param namespaces: A list of namespaces.
    :type namespaces: list(str)
    :return: A namespace generator
    :rtype: generator(str)
    """
    known = set()

    def _subroutine(namespace):
        # Don't yield the same node twice
        if namespace in known:
            return

        # Recursively yield parent first
        parent_namespace = get_namespace_parent(namespace)
        if parent_namespace:
            for yielded in _subroutine(parent_namespace):
                yield yielded

        # Yield
        known.add(namespace)
        yield namespace

    for namespace in namespaces:
        for yielded in _subroutine(namespace):
            yield yielded


class NodeTypeDef(object):
    """
    Object that hold information about a specific node type.
    """

    def __init__(
        self, namespace, data, classification, abstract=False, parent=None
    ):  # pylint: disable=too-many-arguments
        """
        :param str namespace: The node namespace.
        ex: "containerBase.entity.dagNode.shape.camera"
        :param dict(str, dict) data: A dict(k,v) where:
        - k is a standard a port name for this type
        - v is a dict containing the necessary information to build this port
        :param tuple(str) classification: The classification of the type.
        As returned by cmds.getClassification.
        """
        # Don't store the same attribute twice
        if parent:
            for key in parent.data.keys():
                if key not in data:
                    _LOG.debug("Cannot find %r in %r", key, parent)
                    continue
                data.pop(key)

        self.parent = parent
        self.namespace = namespace
        self.type = get_namespace_leaf(namespace)
        self._data = data
        self.classification = classification
        self.abstract = abstract

    def __repr__(self):
        return "<NodeTypeDef %r>" % self.type

    @property
    def data(self):
        """
        Fully qualified dict of all the attributes associated with this node in the form of:

        {
            'attributeA':
            {

            },
            'attributeB:
            (...)
        }

        :return:
        :rtype: dict(str, dict)
        """
        # TODO: memoize
        if self.parent:
            result = copy.copy(self._data)
            result.update(self.parent.data)
            return result
        return self._data

    def apply(self, session, node):
        """
        Create the ports on a provided mocked node.

        :param maya_mock.MockedSession session: The mocked session.
        :param maya_mock.MockedNode node: The node to add ports to.
        """
        for port_name, port_data in self.data.items():
            session.create_port(node, port_name, user_defined=False, **port_data)

    def to_dict(self):
        """
        :return: A serialization python dict version of this instance.
        :rtype: dict
        """
        return {
            "namespace": self.namespace,
            "attributes": self._data,
            "classification": self.classification,
            "abstract": self.abstract,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Construct an instance from a data dict.

        :param dict data: A dict
        :return: An instance
        :rtype: NodeTypeDef
        """
        namespace = data["namespace"]
        attributes = data["attributes"]
        classification = data["classification"]
        abstract = data.get("abstract", False)
        return cls(namespace, attributes, classification, abstract=abstract)


class MockedSessionSchema(object):
    """
    Hold information about known nodes and their ports.
    """

    def __init__(self, nodes=None, default_state=None):
        """
        :param nodes: An optional dict(k,v) for registered nodes where:
        - k is the name of the node type
        - v is the node type definition.
        :type nodes: dict(str, NodeTypeDef) or None
        :param default_state: An optional dict(k,v) for default nodes in an empty scene where:
        - k is the name of the node
        - v is the type of the node
        :type default_state: dict(str, str) or None
        """
        if nodes and not isinstance(nodes, dict):
            raise ValueError("Cannot initialize a schema from %s: %r" % (type(nodes), nodes))
        self.nodes = nodes or {}
        self.default_state = default_state or {}

    def register_node(self, node):
        """
        :param NodeTypeDef node: The node type to register.
        """
        if node.type in self.nodes:
            raise Exception("Node type %r is already registered!" % node.type)

        self.nodes[node.type] = node

    def get(self, node_type):
        """
        Get the node definition for a specific type.

        :param node_type: A node type
        :return: A node definition or None if type is unknown
        :rtype: NodeTypeDef or None
        """
        # TODO: rethink
        return self.nodes.get(node_type)

    def get_node_by_namespace(self, namespace):
        """
        Get a node definition by it's namespace.

        :param str namespace: The node namespace
        :return: A node definition or None if namespace is unknown
        :rtype: NodeTypeDef or None
        """
        return next(
            (node for namespace_, node in self.nodes.items() if namespace == namespace_), None,
        )

    def get_known_node_types(self):
        """
        :return: All the known node types.
        :rtype: list[str]
        """
        return list(self.nodes.keys())

    # Serialization methods

    def to_dict(self):
        """
        Serialize the schema to a JSON compatible dict.

        :return: A JSON compatible dict
        :rtype dict
        """
        return {
            "nodes": {node_type: node_def.to_dict() for node_type, node_def in self.nodes.items()},
            "default_state": self.default_state,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Load a Schema from a raw dict.

        :param dict data: A dict, generally obtained from a JSON file.
        :return: A new Schema instance
        :rtype: MockedSessionSchema
        """
        nodes = data.get("nodes") or {}
        default_state = data.get("default_state") or {}

        nodes = {
            node_name: NodeTypeDef.from_dict(node_data) for node_name, node_data in nodes.items()
        }

        inst = cls(nodes=nodes, default_state=default_state)

        return inst

    @classmethod
    def from_json_file(cls, path):
        """
        Load a Schema from a json file.

        :param str path: The absolute path to a json file.
        :return: A new MockedSessionSchema instance
        :rtype: MockedSessionSchema
        """
        with open(path) as stream:
            data = json.load(stream)

        return cls.from_dict(data)

    def to_json_file(self, path, indent=1, sort_keys=True, **kwargs):
        """
        Export the schema to a json file.

        :param str path: The path to the json file to save to
        :param int indent: The indent to use. Default is 1
        :param bool sort_keys: Should we sort the keys? Default is True
        :param kwargs: Any keyword arguments are passed to `json.dump`
        """
        data = self.to_dict()
        with open(path, "w") as stream:
            json.dump(data, stream, sort_keys=sort_keys, indent=indent, **kwargs)
