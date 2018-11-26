
class MockedPymelPort(object):
    """
    Port adaptor for a pymel.Attribute object.

    :param MockedPort, port: The port to translate.
    """
    def __init__(self, registry, port):
        self.__registry = registry
        self._port = port

    def __repr__(self):
        return '<Mocked pymel.Attribute "{0}">'.format(self._port.name)

    def __melobject__(self):
        return self._port.dagpath

    def name(self):
        return self._port.name
