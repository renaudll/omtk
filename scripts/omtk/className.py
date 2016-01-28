from libs import libPython
from maya import cmds

# TODO: Find a way to have different naming for different production.
# Maybe handle it in the rig directly?

class BaseName(object):
    """
    This class handle the naming of object.
    Store a name as a collection of string 'tokens'.
    Note that since maya don't support compounds and having the same name on multiple nodes can cause issues,
    we need to support multiple number of tokens.
    """
    separator = '_'

    type_anm = 'anm'
    type_jnt = 'jnt'
    type_rig = 'rig'

    root_anm_name = 'anms'
    root_geo_name = 'geos'
    root_jnt_name = 'jnts'
    root_rig_name = 'data'

    layer_anm_name = 'layer_anm'
    layer_rig_name = 'layer_rig'
    layer_geo_name = 'layer_geo'

    side_l_tokens = ['l', "left"]
    side_r_tokens = ['r', "right"]

    def __init__(self, name, prefix=None, suffix=None):
        self.tokens = self._get_tokens(name)
        # prefix and suffix are automatically handled
        self.prefix = prefix
        self.suffix = suffix

    def copy(self, name):
        return self.__class__(name, prefix=self.prefix, suffix=self.suffix)

    def _get_tokens(self, name):
        return name.split(self.separator)

    def _join_tokens(self, tokens):
        return self.separator.join(tokens)

    def add_tokens(self, *args):
        self.tokens.extend(args)

    def add_suffix(self, suffix):
        self.tokens.append(suffix)

    def add_prefix(self, prefix):
        self.tokens.insert(0, prefix)

    def get_unique_name(self, name):
        if cmds.objExists(name):
            i = 1
            while cmds.objExists(name + str(i)):
                i += 1
            return name + str(i)
        return name

    def get_side(self):
        for token in self.tokens:
            token_lower = token.lower()
            if any(True for pattern in self.side_l_tokens if token_lower == pattern.lower()):
                return "l"
            elif any(True for pattern in self.side_r_tokens if token_lower == pattern.lower()):
                return "r"
        return None

    @libPython.memoized
    def resolve(self, *args):
        tokens = []

        if self.prefix:
            tokens.append(self.prefix)
        tokens.extend(self.tokens)
        tokens.extend(args)
        if self.suffix:
            tokens.append(self.suffix)

        name = self._join_tokens(tokens)

        # Prevent maya from crashing by guarantying that the name is unique.
        if cmds.objExists(name):
            name_old = name
            name = self.get_unique_name(name)
            cmds.warning("Name {0} already exist, using {1} instead.".format(
                name_old, name
            ))

        return name

    def rename(self, obj, *args):
        name = self.resolve(*args)
        obj.rename(name)

    def rename_may(self, objs, *args):
        args.append(None)  # Reserve space for iterator
        for i, obj in enumerate(objs):
            args[-1] = '%02d' % i
            self.rename(obj, *args)

    def __repr__(self):
        return self.resolve()


class NameRenaud(BaseName):
    def _get_tokens(self, name):
        tokens = super(NameRenaud, self)._get_tokens(name)
        return tokens[1:] if tokens else None
