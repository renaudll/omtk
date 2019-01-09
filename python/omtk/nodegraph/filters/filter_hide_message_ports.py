from omtk.nodegraph import filter_
from omtk.factories import factory_datatypes


class NodeGraphMessagePortFilter(filter_.NodeGraphFilter):
    """
    Simple filter than let only connection between message attribute pass.
    """
    def can_show_port(self, port):
        """
        Check if a port is displayable according to the filter.
        :param PortModel port: The port to inspect.
        :return: True if we can display this port.
        :rtype: bool
        """
        port_type = port.get_metatype()
        if port_type != factory_datatypes.AttributeType.AttributeMessage:
            return False

        return super(NodeGraphMessagePortFilter, self).can_show_port(port)
