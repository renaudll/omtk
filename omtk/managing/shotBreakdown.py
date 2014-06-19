"""
This is an open-minded alternative to shotgun software tools app: tk-multi-breakdown application.
Inspired by linux packet managers (rpm, yum), the goal of this module is to be lightweight and simple.
"""

# shotbreakdown.py
import omtk
import logging, re, glob
log = logging.getLogger(__name__)

def _is_path_latest(path):
    can_search = False
    tokens = path.split('.')
    for i, token in enumerate(tokens):
        if re.match('v[0-9]*?}', token):
            token[i] = '*'
            can_search = True

    if can_search:
        search_expr = '.'.join(tokens)
        all_versions = sorted(glob.glob('.'.join(search_expr)))

        if path != all_versions[-1]:
            return False

    # If we don't know, smile at the user and say that everything is correct.
    return True


class Reference(object):
    """
    A reference is a high-level api for any reference type.
    """

    def __init__(self, **kwargs):
        super(self).__init__()
        self.__dict__.update(kwargs)

        # By default we want to know more about our object.
        self.need_update = True


    """
    Return True if the reference needs to by manually updated by the end-user.
    """
    @property
    def needUpdate(self):
        raise NotImplemented

    """
    Change the state of the current scene to update the entity related to the reference.
    """
    def update(self):
        raise NotImplemented

    """
    Called by get_breakdown() to list all reference of this type.
    """
    @staticmethod
    def ls(self):
        raise NotImplemented


class HoudiniAlembic(Reference):
    @staticmethod
    def ls():
        import hou

        #hou.nodes.???

    def needUpdate(self):
        raise NotImplemented

    def update(self):
        raise NotImplemented

class MayaReference(Reference):
    def __init__(self, dagpath):
        import pymel.core as pymel
        self.ref = pymel.PyNode(dagpath)
        #self.path = ??? # todo: get path

    def ls(cls):
        import pymel.core as pymel
        return [MayaReference(ref) for ref in pymel.ls(type='reference')]

    def needUpdate(self):
        return _is_path_latest(self.path)

class MayaAlembic(Reference):
    def __init__(self, *args):
        import pymel.core as pymel
        alembic_nodes = filter(lambda x: isinstance(x, pymel.nodetypes.AlembicNode), args)

        # Ensure we deal with one alembic node at once
        if len(alembic_nodes):
            raise ValueError("Can't assign multiple alembic nodes to a MayaAlembic instance.")

        self.alembic_node = next(iter(alembic_nodes), None)

    def is_plugin_loaded(self):
        return True # todo: implement

    def ls(cls):
        import pymel.core as pymel
        return [MayaAlembic(obj) for obj in pymel.ls(type='alembic')]


'''
class MayaTextureRef(Reference):
    def __init__(self):
        raise NotImplemented

class MayaSettingsRef(Reference):
    def __init__(self):
        raise NotImplemented
'''

def get_scene_breakdown():
    references = []
    engine_name = omtk.get_engine_name()
    if engine_name == 'maya':
        references.extend(MayaReference.ls())
    elif engine_name == 'houdini':
        references.extend(HoudiniAlembic.ls())
    references.extend(MayaReference.ls())
    return references

def update_scene(refs=None, quiet=False):
    import pymel.core as pymel

    if refs is None:
        refs = get_scene_breakdown()

    refs_to_update = (ref for ref in refs if ref.needUpdate())
    num_refs_to_update = len(refs_to_update)

    if (num_refs_to_update > 0):
        anwser = pymel.confirmBox(
            "Warning: Outdated references",
            "The scene contain {x} outdated references!\n\nUpdate? ;)".format(num_refs_to_update),
            ["Yes", "Always", "No"]
        )

        if anwser == "Yes":
            for ref in refs_to_update:
                ref.update()
