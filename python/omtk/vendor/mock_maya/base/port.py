from omtk.vendor.Qt import QtCore

class MockedPort(QtCore.QObject):
    """
    Pymel.Attribute mock.
    """
    def __init__(self, node, name):
        super(MockedPort, self).__init__()
        self.node = node
        self.name = name

    def __repr__(self):
        return '<Mocked Port "{}">'.format(self.name)

    @property
    def dagpath(self):
        "{}.{}".format(self.node.dagpath, self.name)
