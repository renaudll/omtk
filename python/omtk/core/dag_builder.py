from omtk import decorators
from omtk.libs import libPython, libRigging
from pymel import core as pymel


class DagBuilder(object):
    """
    A ComponentBuilder is an Helper class than provide methods and caching for scripted Component creation.
    It is important than one DagBuilder is instanciated for each Component since we don't want to leave
    the Component sandbox.
    """

    @decorators.memoized_instancemethod
    def create_utility_node(self, *args, **kwargs):
        """
        Wrapper around libRigging.create_utility_node that cache results to ease rig optimisation at creation time.
        This mean that even if create_utility_node is called multiple time, only one utility node is truly used.
        :param args: Any arguments are fowarded to libRigging.create_utility_node
        :param kwargs: Any keyword arguments are fowarded to libRigging.create_utility_node
        :return: A pymel.nodetypes.DagNode instance.
        """
        return libRigging.create_utility_node(*args, **kwargs)

    def constraint_obj_to_tm(self, obj, tm, compensate_parent=False):
        if compensate_parent and obj.getParent():
            tm = self.create_utility_node(
                'multMatrix',
                matrixIn=(tm, obj.parentInverseMatrix)
            ).matrixSum
        u = self.create_utility_node(
            'decomposeMatrix',
            inputMatrix=tm
        )
        pymel.connectAttr(u.outputTranslate, obj.translate)
        pymel.connectAttr(u.outputRotate, obj.rotate)
        pymel.connectAttr(u.outputScale, obj.scale)

    def get_world_translate(self, obj):
        return self.create_utility_node(
            'decomposeMatrix',
            inputMatrix=obj.worldMatrix
        ).outputTranslate

    def get_world_rotate(self, obj):
        return self.create_utility_node(
            'decomposeMatrix',
            inputMatrix=obj.worldMatrix
        ).outputRotate

    def get_world_scale(self, obj):
        return self.create_utility_node(
            'decomposeMatrix',
            inputMatrix=obj.worldMatrix
        ).outputScale

    def get_attr_inverted_tm(self, attr_tm):
        # todo: if attr_tm come from worldMatrix, parentMatrix, matrix, use the shortcut.
        return self.create_utility_node(
            'inverseMatrix',
            inputMatrix=attr_tm
        ).outputMatrix

    def get_local_tm(self, attr_child_tm, attr_parent_tm):
        return self.create_utility_node(
            'multMatrix',
            matrixIn=(
                attr_child_tm,
                self.get_attr_inverted_tm(attr_parent_tm)
            )
        ).matrixSum

    def get_chain_tms(self, attr_tms):
        """
        Provided a list of n objects, return an n-1 list of local matrix attribute
        representing each objects matrix related to each other (as if they are parented together).
        :param attr_tms: A list of pymel.nodetypes.Transform instances.
        :return: A list of pymel.Attribute instances.
        """

        def _fn(objs):
            yield objs[0]
            for attr_parent_tm, attr_child_tm in libPython.pairwise(objs):
                yield self.get_local_tm(attr_child_tm, attr_parent_tm)

        return list(_fn(attr_tms))

    # todo: make abstract.
    def build(self):
        raise Exception