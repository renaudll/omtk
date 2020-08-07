"""
Abstract classes
"""


class BaseDagObject(object):
    """
    Base class for an object that can be represented with a dag path.
    """

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __gt__(self, other):
        return self.dagpath > other.dagapth

    def __lt__(self, other):
        return self.dagpath < other.dagpath

    def __ge__(self, other):
        return self.dagpath >= other.dagpath

    def __le__(self, other):
        return self.dagpath <= other.dagpath

    def __hash__(self):
        return hash(self.dagpath)

    @property
    def dagpath(self):
        """
        :return: The object fully qualified dagpath
        :rtype: str
        """
        raise NotImplementedError
