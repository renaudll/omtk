"""
Utility method for dealing with namespaces.
"""
import contextlib
import itertools

from maya import cmds


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
