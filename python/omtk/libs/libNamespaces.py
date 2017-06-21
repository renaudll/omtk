"""
Utility method for dealing with namespaces.
"""
import itertools

from maya import cmds


def get_all_namespaces():
    cmds.namespace(setNamespace="::")
    return cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)


def get_unique_namespace(prefix, namespace_format='{0}{1:02d}'):
    all_namespaces = get_all_namespaces()
    if prefix not in all_namespaces:
        return prefix
    for i in itertools.count():
        new_namespace = namespace_format.format(prefix, i)
        if new_namespace not in all_namespaces:
            return new_namespace
