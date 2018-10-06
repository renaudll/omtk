"""
Utility method for dealing with namespaces.
"""
import contextlib
import itertools

from maya import cmds


def get_parent(name):
    separator = ":"
    return separator.join(name.split(separator)[:-1])


def get_all_namespaces():
    cmds.namespace(setNamespace="::")
    return cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)


def get_unique_namespace(prefix, namespace_format='{0}{1}', enforce_suffix=False, suffix_start=1):
    all_namespaces = get_all_namespaces()
    if not enforce_suffix and prefix not in all_namespaces:
        return prefix
    for i in itertools.count(suffix_start):
        new_namespace = namespace_format.format(prefix, i)
        if new_namespace not in all_namespaces:
            return new_namespace


@contextlib.contextmanager
def with_temporary_namespace(namespace):
    """
    Temporarily change the current namespace. Restore the original namespace afteward.
    :param namespace: The namespace to change to. If will be create if it doesnt exist.
    """
    old_namespace = cmds.namespaceInfo(currentNamespace=True)
    if not cmds.namespace(exists=namespace):
        cmds.namespace(add=namespace)
    cmds.namespace.set(namespace)
    yield
    cmds.namespace(set=old_namespace)


def get_namespace(n):
    def _get(n):
        # type: (object) -> str
        try:
            return n.namespace()
        except:
            return n.namespace
    namespace = _get(n)
    namespace = namespace.rstrip(':')  # sometimes Maya return namespace ending with ':'

    # Todo extract namespace from str if is a str type?

    return namespace


def get_common_namespace(nodes):
    """
    Get the namespace of all provided nodes and find their commont parent.
    It no parent is found, the root namespace is returned.

    >>> class Node(object):
    ...     def __init__(self, name):
    ...        self.namespace = get_parent(name)
    >>> nodes = [Node('parent:child1'), Node('parent:child2')]
    >>> get_common_namespace(nodes)
    'parent'

    :param List[object] nodes: List of objects having a namespace.
    :return: A common namespace.
    :rtype n
    """
    # TODO: Validate
    for node in nodes:
        namespace = get_namespace(node)
        if namespace:
            return namespace
    return None