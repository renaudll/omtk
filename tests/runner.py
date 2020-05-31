from maya import standalone


class PytestMayaPlugin(object):
    """
    Custom pytest runner that initialize and uninitialize maya.
    A plugin is necessary so maya is initialized as soon as possible.
    Otherwise imports in tests will be executed before maya initialization and fail.
    """

    def pytest_sessionstart(self):
        standalone.initialize()

    def pytest_sessionfinish(self):
        standalone.uninitialize()
