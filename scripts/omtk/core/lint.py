"""
Linter for maya rigging network.
"""
from maya import cmds


class Issue(object):
    pass


class ConnectionRemap(Issue):
    """
    Issue where a connection could be replaced by a more efficient connection.
    """

    def __init__(self, before, after):
        """
        :param before:
        :type before: tuple of str
        :param after:
        :type after: tuple of str
        """
        self.before = before
        self.after = after

    def __str__(self):
        return "%r can be replaced by %r" % (
            " -> ".join(self.before),
            " -> ".join(self.after),
        )

    def fix(self):
        # TODO: Should we manually remove old connection?
        cmds.connectAttr(
            self.after[0], self.after[1], force=True
        )  # TODO: support n-size tuple


class UneededInverseMatrix(ConnectionRemap):
    """
    Issue where a inverseMatrix is not necessary.
    """

    def __init__(self, util, before, after):
        """
        :param util: A node of type inverseMatrix
        """
        self.util = util
        super(UneededInverseMatrix, self).__init__(before, after)

    def fix(self):
        super(UneededInverseMatrix, self).fix()
        cmds.delete(self.util)

    @classmethod
    def _scan(cls, util):
        dst_before = "%s.inputMatrix" % util
        src_before = cmds.connectionInfo(dst_before, sourceFromDestination=True)
        src_before_node, src_attr = src_before.split(".", 1)
        if cmds.nodeType(src_before_node) != "transform":
            return

        try:
            src_after_attr = {
                "matrix": "inverseMatrix",
                "worldMatrix": "inverseWorldMatrix",
            }[src_attr]
        except KeyError:
            return

        src_after = "%s.%s" % (src_before_node, src_after_attr)
        dsts = (
            cmds.connectionInfo("%s.outputMatrix" % util, destinationFromSource=True)
            or []
        )

        for dst in dsts:
            yield cls(util, (src_before, dst_before), (src_after, dst))

    @classmethod
    def scan(cls):
        """
        :return: A generator that yield UneededInverseMatrix
        :rtype: Generator of UneededInverseMatrix
        """
        # Redirect any inverseMatrix done on a node matrix property
        # to it's inverseMatrix counterpart.
        nodes = cmds.ls(type="inverseMatrix")
        for node in nodes:
            for yielded in cls._scan(node):
                yield yielded


def get_issues():
    return tuple(UneededInverseMatrix.scan())


def scan():
    for issue in get_issues():
        print(issue)


def fix():
    for issue in get_issues():
        issue.fix()
