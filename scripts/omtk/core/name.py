"""
This class handle the naming of object.
Store a name as a list of 'tokens'
When resolved, the tokens are joinned using a 'SEPARATOR' (normally an underscore)

Also some specific properties exists:
- Side: Generally L/R token
- Prefix: Always the first token
- Suffix: Always the last token
- Type: A type identifier, can only have one

You can resolve a BaseName instance from a string.
>>> name = BaseName('l_eye_jnt')
>>> name.resolve()
'l_eye_jnt'

You can build a BaseName instance manually.
>>> name = BaseName(tokens=['eye'], suffix='jnt', side=BaseName.SIDE_L)
>>> name.resolve()
'l_eye_jnt'

You can add tokens at any time.
>>> name.add_tokens('upp')
>>> name.resolve()
'l_eye_upp_jnt'

You can override a BaseName public properties.
>>> name = BaseName()
>>> name.tokens = ['eye']
>>> name.resolve()
'eye'
>>> name.suffix = 'jnt'
>>> name.resolve()
'eye_jnt'
>>> name.side = name.SIDE_L
>>> name.resolve()
'l_eye_jnt'

You can re-define the 'known_prefix' and 'known_suffix' static properties
to ensure that studio-specific suffix/prefix are always respected.
>>> class PrefixBasedNomenclature(BaseName):
...     KNOWN_PREFIXES = ['jnt', 'ctrl']
>>> name = PrefixBasedNomenclature('jnt_head')
>>> name.prefix = 'ctrl'
>>> name.resolve()
'ctrl_head'
>>> class SuffixBasedNomenclature(BaseName):
...     KNOWN_SUFFIXES = ['jnt', 'ctrl']
>>> name = SuffixBasedNomenclature('head_jnt')
>>> name.suffix = 'ctrl'
>>> name.resolve()
'head_ctrl'
"""
import copy

from maya import cmds


class AbstractName(object):
    """
    Implementation for naming.
    """
    SEPARATOR = "_"
    KNOWN_PREFIXES = []
    KNOWN_SUFFIXES = []
    KNOWN_TYPES = {}  # TODO: Better type registry
    SIDE_L = None
    SIDE_R = None
    SIDE_C = None
    SIDE_V_UPP = None
    SIDE_V_LOW = None
    SIDE_V_MID = None

    def __init__(self, name=None, tokens=None, prefix=0, suffix=0, side=0):
        self.tokens = tokens or []
        self.prefix = None
        self.suffix = None
        self.side = None
        self.side_v = None
        self._type = None

        if name:
            self.build_from_string(name)

        # Apply manual overrides
        if tokens:
            self.tokens = tokens
        if prefix is not 0:
            self.prefix = prefix
        if suffix is not 0:
            self.suffix = suffix
        if side is not 0:
            self.side = side

    def __repr__(self):  # TODO: This should be __str__
        return self.resolve()

    def __add__(self, other):
        """
        Merge two Name instance together.
        :param other: Another Name instance.
        :return: A new Name instance.

        >>> name = BaseName(tokens=['arm'], suffix='ctrl')
        >>> other_name = BaseName(tokens=['armupper'], side=BaseName.SIDE_L)
        >>> (name + other_name).resolve()
        'l_arm_armupper_ctrl'

        >>> name = BaseName(tokens=['arm'], suffix='ctrl')
        >>> (name + "armupper").resolve()
        'l_arm_armupper_ctrl'
        """
        result = self.copy()

        # Handle addition to a simple string
        if isinstance(other, basestring):
            result.tokens.append(other)
            return result

        # Merge tokens
        for token in other.tokens:
            result.tokens.append(token)

        # Merge side, prefix and suffix
        if other.prefix and not result.prefix:
            result.prefix = other.prefix
        if other.suffix and not result.suffix:
            result.suffix = other.suffix
        if other.side and not result.side:
            result.side = other.side

        return result

    @classmethod
    def from_string(cls, value):
        return cls(value)  # TODO: Deprecate name from constructor

    @property
    def type(self):
        """
        :return: The naming type
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, value):
        """
        Set the naming type

        :param str value: The naming type
        """
        if value and value not in self.KNOWN_TYPES:
            raise ValueError("Unrecognized type %r" % value)
        old_type = self.type
        if old_type in self.KNOWN_PREFIXES and self.prefix == old_type:
            self.prefix = None
        if old_type in self.KNOWN_SUFFIXES and self.suffix == old_type:
            self.suffix = None
        if value in self.KNOWN_PREFIXES:
            self.prefix = value
        elif value in self.KNOWN_SUFFIXES:
            self.suffix = value

    def copy(self):
        """
        Return a copy of the name object.
        """
        inst = self.__class__()
        inst.tokens = copy.copy(self.tokens)
        inst.prefix = self.prefix
        inst.suffix = self.suffix
        inst.side = self.side
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
            if not self.get_side_from_token(token):
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
            if self.get_side_from_token(token):
                new_tokens.append(token)
            elif not found_base_token and token == basename:
                new_tokens.append(token)

        self.tokens = new_tokens

    def build_from_string(self, name):
        raw_tokens = self._get_tokens(name)
        self.tokens = []
        self.side = None

        self.add_tokens(*raw_tokens)

    def _get_tokens(self, val):
        return val.split(self.SEPARATOR)

    def _join_tokens(self, tokens):
        return self.SEPARATOR.join(tokens)

    def add_tokens(self, *args):
        found_token = False
        for arg in args:
            for token in arg.split(self.SEPARATOR):
                # Handle side
                side = self.get_side_from_token(token)
                side_v = self.get_v_side_from_token(token)
                if side:
                    self.side = side
                elif side_v:
                    self.side_v = side_v
                # Handle suffixes
                elif token in self.KNOWN_SUFFIXES:
                    self.suffix = token
                # Handle prefixes
                elif token in self.KNOWN_PREFIXES and not found_token:
                    self.prefix = token
                # Handle normal token
                else:
                    self.tokens.append(token)
                    found_token = True

    def add_suffix(self, suffix):
        self.tokens.append(suffix)

    def add_prefix(self, prefix):
        self.tokens.insert(0, prefix)

    def get_unique_name(self, name):  # TODO: Move this outside of the class
        if cmds.objExists(name):
            i = 1
            while cmds.objExists(name + str(i)):
                i += 1
            return name + str(i)
        return name

    @classmethod
    def get_side_from_token(cls, token):
        token = token.lower()  # TODO: Why?
        for side in (cls.SIDE_L, cls.SIDE_R, cls.SIDE_C):
            if side and side.lower() == token:
                return side

    @classmethod
    def get_v_side_from_token(cls, token):
        token = token.lower()  # TODO: Why?
        for side in (cls.SIDE_V_UPP, cls.SIDE_V_MID, cls.SIDE_V_LOW):
            if side and side.lower() == token:
                return side

    def get_tokens(self):
        """
        :return: All token without the side tokens.
        """
        return [token for token in self.tokens if not self.get_side_from_token(token)]

    def resolve(self, *args):
        tokens = []

        if self.prefix:
            tokens.append(self.prefix)

        if self.side:
            tokens.append(self.side)

        tokens.extend(self.tokens)
        tokens.extend(args)
        if self.suffix:
            tokens.append(self.suffix)

        name = self._join_tokens(tokens)

        return name

    def rename(self, obj, *args):
        name = self.resolve(*args)
        obj.rename(name)


class BaseName(AbstractName):
    """
    Base name for development.
    """
    SEPARATOR = "_"

    type_anm = "anm"
    type_anm_grp = "anmgrp"
    type_jnt = "jnt"
    type_rig = "rig"
    type_rig_grp = "riggrp"

    root_anm_name = "anms"
    root_anm_master_name = "anm_all"
    root_geo_name = "geos"
    root_jnt_name = "jnts"
    root_rig_name = "data"
    root_backup_name = "backup"

    layer_anm_name = "layer_anm"
    layer_rig_name = "layer_rig"
    layer_geo_name = "layer_geo"
    layer_jnt_name = "layer_jnts"

    KNOWN_PREFIXES = ["anm", "grp", "jnt", "rig"]
    KNOWN_SUFFIXES = []
    KNOWN_TYPES = {"anm", "grp", "jnt", "rig", "anmgrp", "riggrp"}

    SIDE_L = "l"
    SIDE_R = "r"
    SIDE_C = None
    SIDE_V_UPP = "upp"
    SIDE_V_LOW = "low"
    SIDE_V_MID = "mid"

if __name__ == "__main__":
    import doctest

    doctest.testmod()
