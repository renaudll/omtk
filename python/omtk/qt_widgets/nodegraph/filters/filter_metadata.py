import pymel.core as pymel
from omtk.qt_widgets.nodegraph import nodegraph_filter

if False:
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphConnectionModel


class NodeGraphMetadataFilter(nodegraph_filter.NodeGraphFilter):
    """
    Simple filter than let only connection between message attribute pass.
    """
    def can_show_connection(self, connection):
        # type: (NodeGraphConnectionModel) -> bool
        port_src = connection.get_source()
        port_src_data = port_src.get_metadata()
        if not isinstance(port_src_data, pymel.Attribute) or port_src_data.type() != 'message':
            return False

        port_dst = connection.get_destination()
        port_dst_data = port_dst.get_metadata()
        if not isinstance(port_dst_data, pymel.Attribute) or port_dst_data.type() != 'message':
            return False

        return super(NodeGraphMetadataFilter, self).can_show_connection(connection)
