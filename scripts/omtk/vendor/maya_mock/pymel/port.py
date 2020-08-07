"""Mock for pymel.core.Attribute"""


class MockedPymelPort(object):
    """
    Port adaptor for a pymel.Attribute object.

    https://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.general/pymel.core.general.Attribute.html#pymel.core.general.Attribute
    """

    def __init__(self, session, port):
        """
        :param maya_mock.MockedSession session: A mocked session
        :param maya_mock.MockedPort, port: The port to translate.
        """
        self.__session = session
        self._port = port

    def __str__(self):
        return self.__melobject__()

    def __repr__(self):
        # We use the `u` prefix as we don't know yet
        # what this will be in a python-3 based maya.
        return "Attribute(u%r)" % str(self.__melobject__())

    def __melobject__(self):
        return u"{}.{}".format(self._port.node.__melobject__(), self._port.name)

    def name(self):
        """
        :return: The attribute name
        :rtype: str
        """
        return self.__melobject__()

    def longName(self):  # pylint: disable=invalid-name
        """
        https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.general/pymel.core.general.Attribute.html#pymel.core.general.Attribute.longName

        :return: The attribute long name
        :rtype: str
        """
        return self._port.name

    def shortName(self):  # pylint: disable=invalid-name
        """
        https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.general/pymel.core.general.Attribute.html#pymel.core.general.Attribute.shortName

        :return: The attribute short name
        :rtype: str
        """
        return self._port.short_name

    def get(self):
        """
        https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.general/pymel.core.general.Attribute.html#pymel.core.general.Attribute.get

        :return: The value attribute value
        :rtype: object
        """
        return self._port.value

    def set(self, value):
        """
        Set the attribute value

        https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.general/pymel.core.general.Attribute.html#pymel.core.general.Attribute.set

        :param object value: The attribute new value
        """
        self._port.value = value
