class MockedPort(object):
    """
    Pymel.Attribute mock.
    """
    def __init__(self, node, name):
        self.node = node
        self.name = name

    def __repr__(self):
        return '<Mocked Port "{}">'.format(self.dagpath)

    @property
    def dagpath(self):
        "{}.{}".format(self.node.dagpath, self.name)
