from omtk.libs import libPython
from maya import cmds
import copy

# TODO: Find a way to have different naming for different production.
# Maybe handle it in the rig directly?

class BaseName(object):
    """
    This class handle the naming of object.
    Store a name as a collection of string 'tokens'.
    Note that since maya don't support compounds and having the same name on multiple nodes can cause issues,
    we need to support multiple number of tokens.
    Also some specific tokens can exist:
    - Side: Generally L/R token
    - Prefix: Always the first token
    - Suffix: Always the last token
    """
    separator = '_'

    type_anm = 'anm'
    type_anm_grp = 'anm_grp'
    type_jnt = 'jnt'
    type_rig = 'rig'
    type_rig_grp = 'data_grp'

    root_anm_name = 'anms'
    root_geo_name = 'geos'
    root_jnt_name = 'jnts'
    root_rig_name = 'data'

    layer_anm_name = 'layer_anm'
    layer_rig_name = 'layer_rig'
    layer_geo_name = 'layer_geo'

    side_l_tokens = ['l', "left"]
    side_r_tokens = ['r', "right"]

    SIDE_L = 'l'
    SIDE_R = 'r'

    def __init__(self, name=None, tokens=None, prefix=None, suffix=None, side=None):
        self.tokens = []
        self.prefix = None
        self.suffix = None
        self.side = None

        if name:
            self.build_from_string(name)

        # Apply manual overrides
        if tokens:
            self.tokens = tokens
        if prefix:
            self.prefix = prefix
        if suffix:
            self.suffix = suffix
        if side:
            self.side = side

    def copy(self):
        inst = self.__class__()
        inst.tokens = copy.copy(self.tokens)
        inst.prefix = self.prefix
        inst.suffix = self.suffix
        return inst

    def rebuild(self, name):
        return self.__class__(name, prefix=self.prefix, suffix=self.suffix)

    def get_basename(self):
        """
        Each name have one single token that represent it's part.
        ex: L_LegUpp_Ik_Ctrl -> LegUpp
        By default it is the first non-side token in the name.
        return: The part name.
        """
        for token in self.tokens:
            if not self._is_side(token):
                return token

    def remove_extra_tokens(self):
        """
        Remove any tokens that is not the base token or a side token.
        :return:
        """
        basename = self.get_basename()
        found_base_token = False

        new_tokens = []
        for token in self.tokens:
            if self._is_side(token):
                new_tokens.append(token)
            elif not found_base_token and token == basename:
                new_tokens.append(token)

        self.tokens = new_tokens

    def _get_tokens(self, name):
        return name.split(self.separator)

    def build_from_string(self, name):
        raw_tokens = name.split(self.separator)
        self.tokens = []
        #self.prefix = None
        #self.suffix = None
        self.side = None

        for token in raw_tokens:
            if self._is_side(token):
                if self._is_side_l(token):
                    self.side = self.SIDE_L
                elif self._is_side_r(token):
                    self.side = self.SIDE_R
            else:
                self.tokens.append(token)

    def _join_tokens(self, tokens):
        return self.separator.join(tokens)

    def add_tokens(self, *args):
        for arg in args:
            for token in arg.split(self.separator):
                self.tokens.append(token)

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

    def _is_side_l(self, token):
        token_lower = token.lower()
        return any(True for pattern in self.side_l_tokens if token_lower == pattern.lower())

    def _is_side_r(self, token):
        token_lower = token.lower()
        return any(True for pattern in self.side_r_tokens if token_lower == pattern.lower())

    def _is_side(self, token):
        return self._is_side_l(token) or self._is_side_r(token)

    def get_tokens(self):
        """
        :return: All token without the side tokens.
        """
        return [token for token in self.tokens if not self._is_side_l(token) and not self._is_side_r(token)]

    def get_side(self):
        for token in self.tokens:
            if self._is_side_l(token):
                return "l"
            elif self._is_side_r(token):
                return "r"
        return None

    def resolve(self, *args):
        tokens = []

        if self.side:
            tokens.append(self.side)

        if self.prefix:
            tokens.append(self.prefix)
        tokens.extend(self.tokens)
        tokens.extend(args)
        if self.suffix:
            tokens.append(self.suffix)

        name = self._join_tokens(tokens)

        # If we have name conflicts, we WILL want to crash.
        '''
        # Prevent maya from crashing by guarantying that the name is unique.
        if cmds.objExists(name):
            name_old = name
            name = self.get_unique_name(name)
            cmds.warning("Name {0} already exist, using {1} instead.".format(
                name_old, name
            ))
        '''

        return name

    def rename(self, obj, *args):
        name = self.resolve(*args)
        obj.rename(name)

    def __repr__(self):
        return self.resolve()
