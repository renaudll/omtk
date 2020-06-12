import pymel.core as pymel

__all__ = (
    "iter_connected_networks",
    "get_connected_networks",
    "iter_networks_from_class",
    "get_networks_from_class",
    "is_network_from_class",
)


def is_network_from_class(net, cls_name):
    """
    Inspect a potentially serialized pymel.nodetypes.Network and check if
    if was created from a specific class instance.
    :param net: A pymel.nodetypes.Network to inspect.
    :param cls_name: A string representing a class name.
    :return:
    """
    # HACK: Backward compatibility with the old system.
    # Previously the full namespace was stored in the '_class' attribute.
    try:
        return cls_name in net.getAttr("_class_namespace").split(".")
    except AttributeError:
        pass

    try:
        return cls_name in net.getAttr("_class").split(".")
    except AttributeError:
        pass

    return None


def iter_networks_from_class(cls_name):
    for network in pymel.ls(type="network"):
        if is_network_from_class(network, cls_name):
            yield network


def get_networks_from_class(cls_name):
    """
    Return all networks serialized from a specified base class.
    Note that this don't check if the network itself is deserializable.

    For example, if we are looking for the Rig class and
    the network class is RigElement.Rig but RigElement is not defined,
    this will still return the network.
    However calling libSerialization.import_network will return None.
    # todo: add an option to pre-validate

    :param cls_name: A string representing the name of a class.
    :return: A list of networks
    :rtype: A list of pymel.nodetypes.Network.
    """
    return list(iter_networks_from_class(cls_name))


def iter_connected_networks(objs, key=None, key_skip=None, recursive=True, cache=None):
    """
    Inspect provided dagnode connections in search of serialized networks.

    By providing a function pointer, specific networks can be targeted.
    :param objs: A list of dag nodes to inspect.
    :type objs: list of pymel.nodetypes.DagNode
    :param callable key: A function to filter specific networks.
    :param callable key_skip: A function that receive a network as input and return True
    if the network is blacklisted. If the network is blacklisted,
    it will not be iterated through.
    :param bool recursive: If true, will inspect recursively.
    :param cache: Used internally, do not overwrite.
    :yield: generator of pymel.nodetypes.Networks
    """
    # Initialise the array the first time,
    # we don't want to do it in the function argument as it will keep old values...
    if cache is None:
        cache = []

    # Ensure objects are provided as a list.
    if not hasattr(objs, "__iter__"):
        objs = [objs]

    for obj in objs:
        # Ignore known objects
        if obj in cache:
            continue

        # Remember this object in the cache
        cache.append(obj)

        # Ignore this object if it is blacklisted.
        # However still keep it in the cache in case we encounter it again.
        if key_skip and key_skip(obj):
            continue

        # Ignore any object that don't have a message attribute.
        # This is equivalent to searching for dagnodes only.
        if not obj.hasAttr("message"):
            continue

        for output_obj in obj.message.outputs():
            # Only check pymel.nodetypes.Network
            if not isinstance(output_obj, pymel.nodetypes.Network):
                continue

            # Prevent cyclic dependencies
            if output_obj in cache:
                continue

            # Prevent self referencing
            if output_obj is obj:
                continue

            if key is None or key(output_obj):
                yield output_obj

            if recursive:
                for result in iter_connected_networks(
                    output_obj,
                    key=key,
                    key_skip=key_skip,
                    recursive=recursive,
                    cache=cache,
                ):
                    yield result


def get_connected_networks(objs, key=None, key_skip=None, recursive=True):
    """
    Inspect provided dag node connections in search of serialized networks.
    By providing a function pointer, specific networks can be targeted.

    :param objs: A list of pymel.nodetypes.DagNode to inspect.
    :type objs: list of pymel.nodetypes.DagNode
    :param callable key: A function to filter specific networks
    :param callable key_skip: A function that receive a network as input and return True
    if the network is blacklisted. If the network is blacklisted,
    it will not be iterated through.
    :param recursive: If true, will inspect recursively.
    :return: A list of networks
    :rtype: list of pymel.nodetypes.Network
    """
    return list(
        iter_connected_networks(objs, key=key, key_skip=key_skip, recursive=recursive)
    )
