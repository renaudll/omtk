from . import nodegraph_node_model_component

# for type hinting only
if False:
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_node_model_base import NodeGraphNodeModel


class NodeGraphConnectionModel(object):
    def __init__(self, registry, name, attr_src, attr_dst):
        self._registry = registry
        self._attr_src = attr_src
        self._attr_dst = attr_dst

    def __repr__(self):
        return '<NodeGraphConnectionModel {0}.{1} to {2}.{3}>'.format(
            self._attr_src.get_parent(),
            self._attr_src.get_name(),
            self._attr_dst.get_parent(),
            self._attr_dst.get_name()
        )

    def __hash__(self):
        return hash(self._attr_src) ^ hash(self._attr_dst)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        """
        By default, a connection parent is either the same as it's input attribute or it's output attribute.
        This difference is important with Compound nodes.
        :return:
        """
        src_node_model = self._attr_src.get_parent()
        dst_node_model = self._attr_dst.get_parent()

        class enum_PortKind:
            normal = 1
            compound_inn = 2
            compound_out = 3

        class ConnectionKind:
            normal = 1
            normal_to_compound_inn = 2 # src (node is outside the compound)
            normal_to_compound_out = 3 # dst (node is inside the compound)
            compound_inn_to_normal = 4 # src (node is inside the compound)
            compound_out_to_normal = 5 # dst (node is outside the compound)
            compound_inn_to_compound_inn = 6 # dst (destination is inside source)
            compound_inn_to_compound_out = 7 # any (source and destination are inside the same compound)
            compound_out_to_compound_inn = 8 # any (source and destination are inside the same compound)
            compound_out_to_compound_out = 9 # src (source is inside destination)

        def get_connection_kind():
            from omtk.libs import libComponents
            src_role = libComponents.get_metanetwork_role(src_node_model)
            dst_role = libComponents.get_metanetwork_role(dst_node_model)

            src_is_compound_bound = src_role != libComponents.ComponentMetanetworkRole.NoRole
            dst_is_compound_bound = dst_role != libComponents.ComponentMetanetworkRole.NoRole
            # The possibilities are:
            # - Connection from a component out to a component on the same level.
            # - Connection from a component inn to a component inn inside this same component.
            # - Connection from a component out to a parent component out.
            if src_is_compound_bound and dst_is_compound_bound:
                src_is_inn = src_role == libComponents.ComponentMetanetworkRole.Inn
                dst_is_inn = dst_role == libComponents.ComponentMetanetworkRole.Out
                # Connection from a component inn to another component inn.
                # In that case the destination component is a child of the source component.
                if src_is_inn and dst_is_inn:
                    return ConnectionKind.compound_inn_to_compound_inn
                # Connection from a component inn to a component out.
                # In that case the connection is from the same component (or there's something really wrong in the scene).
                # In that case both src and dst are in the same space.
                elif src_is_inn and not dst_is_inn:
                    return ConnectionKind.compound_inn_to_compound_out
                # Connection from a component out to a component inn
                # In that case the source component is a child of the destination component.
                elif not src_is_inn and dst_is_inn:
                    return ConnectionKind.compound_out_to_compound_inn
                # Connection from a component out to a component out
                # In that case the source component is a child of the destination component.
                else:
                    return ConnectionKind.compound_out_to_compound_out

            elif src_is_compound_bound:  # exiting a compounds
                src_is_inn = src_role == libComponents.ComponentMetanetworkRole.Inn
                if src_is_inn:
                    return ConnectionKind.compound_inn_to_normal
                else:
                    return ConnectionKind.compound_out_to_normal
            elif dst_is_compound_bound:  # entering a compound
                dst_is_inn = dst_role == libComponents.ComponentMetanetworkRole.Inn
                if dst_is_inn:
                    return ConnectionKind.normal_to_compound_inn
                else:
                    return ConnectionKind.normal_to_compound_out

        def get_connection_node_model():
            # Define if we should use the source or destination node model to fetch the parent.
            # normal_to_compound_inn = 2  # src (node is outside the compound)
            # normal_to_compound_out = 3  # dst (node is inside the compound)
            # compound_inn_to_normal = 4  # src (node is inside the compound)
            # compound_out_to_normal = 5  # dst (node is outside the compound)
            # compound_inn_to_compound_inn = 6  # dst (destination is inside source)
            # compound_inn_to_compound_out = 7  # any (source and destination are inside the same compound)
            # compound_out_to_compound_inn = 8  # any (source and destination are inside the same compound)
            # compound_out_to_compound_out = 9  # src (source is inside destination)
            connection_kind = get_connection_kind()
            if connection_kind in (
                ConnectionKind.normal_to_compound_inn,
                ConnectionKind.compound_inn_to_normal,
                ConnectionKind.compound_inn_to_compound_inn,
                ConnectionKind.compound_out_to_compound_out,
            ):
                return dst_node_model
            else:
                return src_node_model

        node_model = get_connection_node_model()
        return node_model

    def get_source(self):
        # type: () -> NodeGraphPortModel
        return self._attr_src

    def get_destination(self):
        # type: () -> NodeGraphPortModel
        return self._attr_dst
