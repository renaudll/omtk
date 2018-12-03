"""
Factory module to create NodeModel, PortModel and ConnectionModel.
# TODO: DEPRECATE ALL OF THIS!!! Composition over inheritance
"""
import omtk.nodegraph.models._deprecated.port_entityattribute
import omtk.nodegraph.models._deprecated.port_pymel
import omtk.nodegraph.models.port
from omtk.core import entity_attribute


# TODO: Deprecate pymel?

# def get_node_from_value(registry, val):
#     """
#     Factory method to NodeModel
#
#     :param omtk.nodegraph.NodeGraphRegistry registry:
#     :param object val: A value associated with the node. (str, PyNode, etc)
#     :return: A ``NodeModel`` instance
#     :rtype: omtk.nodegraph.NodeModel
#     """
#     from omtk.factories import factory_datatypes
#
#     session = registry.session
#
#     data_type = factory_datatypes.get_datatype(val)
#     if data_type == factory_datatypes.AttributeType.Component:
#         from omtk.nodegraph.models.node._deprecated import node_component
#
#         node = node_component.NodeGraphComponentModel(registry, val)
#
#         # Hack: Force registration of all component children.
#         # This will ensure that node deletion signal get propagated.
#         node.get_children()
#
#         return node
#
#     if data_type == factory_datatypes.AttributeType.Node:
#         import pymel.core as pymel
#         if isinstance(val, pymel.nodetypes.DagNode):
#             from omtk.nodegraph.models.node._deprecated import node_dag
#             node = node_dag.NodeGraphDagNodeModel(registry, val)
#         else:
#             from omtk.nodegraph.models.node._deprecated import node_dg
#             node = node_dg.NodeGraphDgNodeModel(registry, val)
#         if session:
#             session.add_node_callbacks(node)
#         return node
#
#     if data_type == factory_datatypes.AttributeType.Module:
#         from omtk.nodegraph.models.node._deprecated import node_module
#         return node_module.NodeGraphModuleModel(registry, val)
#
#     if data_type == factory_datatypes.AttributeType.Rig:
#         from omtk.nodegraph.models.node._deprecated import node_rig
#         return node_rig.NodeGraphNodeRigModel(registry, val)
#
#     raise Exception("Unsupported value {0} of type {1}".format(
#         val, data_type
#     ))


def get_port_from_value(registry, val):
    """
    Factory method for PortModel

    :param omtk.nodegraph.Registry registry: The REGISTRY_DEFAULT
    :param object val: A value associated with a port (str, pymel.Attribute)
    :return: A ``PortModel`` instance
    :rtype: omtk.nodegraph.PortModel
    """
    from omtk.nodegraph.models.port import port_base
    import pymel.core as pymel
    from omtk.factories import factory_datatypes

    if isinstance(val, entity_attribute.EntityPymelPort):
        node_value = val.parent
        node_model = registry.get_node(node_value)
        inst = omtk.nodegraph.models._deprecated.port_entityattribute.NodeGraphEntityAttributePortModel(registry, node_model, val)
        return inst

    if isinstance(val, entity_attribute.EntityPort):
        node_value = val.parent
        node_model = registry.get_node(node_value)
        # model_node = REGISTRY_DEFAULT.get_node(val.parent)
        inst = omtk.nodegraph.models._deprecated.port_entityattribute.NodeGraphEntityAttributePortModel(registry, node_model, val)
        return inst

    # pymel Attribute
    if isinstance(val, pymel.Attribute):
        node_value = val.node()
        node_model = registry.get_node(node_value)
        inst = omtk.nodegraph.models._deprecated.port_pymel.NodeGraphPymelPortModel(registry, node_model, val)
        return inst

    # OMTK node
    datatype = factory_datatypes.get_datatype(val)
    if datatype == factory_datatypes.AttributeType.Node:
        node_model = registry.get_node(val)
        inst = omtk.nodegraph.models._deprecated.port_pymel.NodeGraphPymelPortModel(registry, node_model, val.message)
        return inst

    # OMTK module
    if isinstance(val, module.Module):  # todo: use factory_datatypes?
        # node_value = val.rig
        node_model = registry.get_node(val.rig)
        val = val.rig.get_attribute_by_name('modules')
        inst = omtk.nodegraph.models._deprecated.port_entityattribute.NodeGraphEntityAttributePortModel(registry, node_model, val)
        return inst

    # pymel PyNode
    node_model = registry.get_node(val.node())
    inst = omtk.nodegraph.models._deprecated.port_pymel.NodeGraphPymelPortModel(registry, node_model, val)

    return inst


def get_connection_from_value(registry, port_src, port_dst):
    """
    Get a connection object from two ports.

    :param omtk.nodegraph.NodeGraphRegistry registry: The REGISTRY_DEFAULT
    :param omtk.nodegraph.PortModel port_src: The source port
    :param omtk.nodegraph.PortModel port_dst: The destination port
    :return: A ``ConnectionModel`` instance
    :rtype: omtk.nodegraph.ConnectionModel
    """
    from omtk.nodegraph.models import connection

    if not isinstance(port_src, omtk.nodegraph.models.port.PortModel):
        port_src = registry.get_port(port_src)

    if not isinstance(port_dst, omtk.nodegraph.models.port.PortModel):
        port_dst = registry.get_port(port_dst)

    inst = connection.ConnectionModel(registry, port_src, port_dst)
    return inst
