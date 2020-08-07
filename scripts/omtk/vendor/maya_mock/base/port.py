"""A mocked Maya port"""
import fnmatch

import six

from . import _abstract
from .constants import EnumAttrTypes


class MockedPort(_abstract.BaseDagObject):  # pylint: disable=too-many-instance-attributes
    """
    A mocked Maya port.
    """

    def __init__(
        self,
        node,
        name,
        port_type="long",
        short_name=None,
        nice_name=None,
        value=0,
        readable=True,
        writable=True,
        interesting=True,
        user_defined=True,
        parent=None,
    ):  # pylint: disable=too-many-arguments
        """
        Create a Maya port mock.

        :param MockedNode node: The node associated with the port.
        :param name: The name of the port.
        :param port_type: The type of the port. See maya_mock.constants.EnumAttrTypes
        :param str short_name: The 'short' name of the port. (ex: transform.t)
        :param str nice_name: The 'nice' name of the port. (ex: transform.translateMcTranslate)
        :param object value: The value of the port.
        :param readable: 1
        :param writable:
        :param interesting:
        :param bool user_defined: Is the port is not standard for this type of node?
        :param parent: An optional parent to the attribute. Parent need to exist.
        :type parent: str or None
        """
        super(MockedPort, self).__init__()

        # Ensure provided name is unicode
        name = six.text_type(name) if name else None
        short_name = six.text_type(short_name) if short_name else None
        nice_name = six.text_type(nice_name) if nice_name else None

        self.node = node
        self.name = name
        self.short_name = short_name or name
        self.nice_name = nice_name or name
        self._type = getattr(EnumAttrTypes, port_type)
        self.value = value
        self.readable = readable
        self.writable = writable
        self.interesting = interesting
        self.user_defined = user_defined
        self.parent = parent

    def __repr__(self):
        return '<Mocked Port "{}.{}">'.format(self.node.name, self.name)

    def __melobject__(self):
        return "{}.{}".format(self.node.__melobject__(), self.name)

    @property
    def type(self):
        """
        rtype: EnumAttrTypes
        """
        return self._type

    def match(self, pattern):
        """
        Check if the node match a certain pattern.
        The pattern can be a fully qualified dagpath or a name.

        - `child.foo`
        - `child*.foo`
        - `|child`

        :param pattern:
        :return:
        """
        # No pattern always match
        if pattern is None:
            return True

        # Match fully qualified dagpath
        # TODO: Make more solid
        dagpath = self.dagpath
        if dagpath == "|" + pattern:
            return True

        dagpath_short = self.dagpath_short
        if dagpath_short == "|" + pattern:
            return True

        port_name = self.name
        port_short_name = self.short_name

        # Match attribute name
        if port_name == pattern or fnmatch.fnmatch(port_name, pattern):
            return True

        if port_short_name == pattern or fnmatch.fnmatch(port_short_name, pattern):
            return True

        return False

    @property
    def dagpath(self):
        """
        Resolve the port dagpath.

        :return: A fully qualified dagpath to the port.
        :rtype: str
        """
        return "{}.{}".format(self.node.dagpath, self.name)

    @property
    def dagpath_short(self):
        """
        Resolve a dagpath from the port short name.

        :return: A fully qualified dagpath to the port.
        :rtype: str
        """
        return "{}.{}".format(self.node.dagpath, self.short_name)
