"""
Utility method for dealing with namespaces.
"""
import contextlib

import re


def get_parent(namespace):
    """
    Query the parent namespace of provided namespace

    >>> get_parent('a:b')
    'a'
    >>> get_parent('a')
    ''

    :param str namespace: The child namespace
    :return: The parent namespace
    :rtype: str
    """
    separator = ":"
    return separator.join(namespace.split(separator)[:-1])


def get_all_namespaces():
    """
    :return: List of all namespaces in the current Maya session
    :rtype: list(str)
    """
    from maya import cmds

    cmds.namespace(setNamespace="::")
    return cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)


def join_namespace(*args):
    """

    :param args:
    :return:
    """
    return ":".join((arg.rstrip(":") for arg in args))


def relative_namespace(namespace, parent_namespace):
    """

    :param str namespace:
    :param str parent_namespace:
    :return:
    """
    parent_namespace = parent_namespace or ""  # temporary
    prefix = parent_namespace.rstrip(":") + ":"
    if namespace.startswith(prefix):
        return namespace[len(prefix) :]
    return namespace


def get_unique_namespace(namespace, pool=None):
    """
    :param str namespace: The start namespace
    :return: A unique namespace
    :rtype namespace
    """
    pool = pool or get_all_namespaces()
    prefix, suffix = re.match(
        r"^(?P<prefix>[\w:]*?)(?P<suffix>\d*)$", namespace
    ).groups()
    suffix = int(suffix) if suffix else 0
    guess = namespace
    while guess in pool:
        suffix += 1
        guess = prefix + str(suffix)
    return guess


@contextlib.contextmanager
def with_temporary_namespace(namespace):
    """
    Temporarily change the current namespace. Restore the original namespace afterward.
    :param namespace: The namespace to change to. If will be create if it doesnt exist.
    """
    from maya import cmds

    old_namespace = cmds.namespaceInfo(currentNamespace=True)
    if not cmds.namespace(exists=namespace):
        cmds.namespace(add=namespace)
    cmds.namespace.set(namespace)
    yield
    cmds.namespace(set=old_namespace)


def get_namespace(value):
    """ Get a namespace from an arbitrary value_.

    :param object value: A value to extract a namespace from
    :return: A namespace
    :rtype: str
    """
    # TODO: Deprecate this, we should alway use strings.
    def _get(value_):
        # type: (object) -> str
        try:
            return value_.namespace()
        except Exception:  # pylint: disable=broad-except
            pass

        try:
            return value_.namespace
        except AttributeError:
            pass

        return value_.rsplit(":", 1)[0] if ":" in value_ else ":"

    namespace = _get(value)
    namespace = ":" + namespace.rstrip(":")
    return namespace


def get_common_namespace(nodes):
    """
    Get the namespace of all provided nodes and find their common parent.
    It no parent is found, the root namespace is returned.

    :param List[object] nodes: List of objects having a namespace.
    :return: A common namespace.
    :rtype n
    """
    common_namespaces = None
    # TODO: Validate
    for node in nodes:
        namespace = get_namespace(node)
        if namespace:
            tokens = namespace.split(":")
            possibilities = {":".join(tokens[: i + 1]) for i in range(len(tokens))}
            if not common_namespaces:
                common_namespaces = possibilities
            else:
                common_namespaces &= possibilities

    if common_namespaces:
        return sorted(common_namespaces)[-1].strip(":") or None
    return None


def is_child_of(child, parent):
    """
    :param str child:
    :param str parent:
    :return:
    """
    if not child:
        return False
    child_parent = get_parent(child)
    if child_parent == parent:
        return True
    return is_child_of(child_parent, parent)
