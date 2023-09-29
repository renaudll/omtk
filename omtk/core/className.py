from maya import cmds
import copy


# todo: make tokens, suffix, prefix and side private. Use getter and setter functions were necessary.
# todo: in add_tokens, reconize what is a suffix and what is a prefix

class BaseName(object):
    """
    This class handle the naming of object.
    Store a name as a list of 'tokens'
    When resolved, the tokens are joinned using a 'separator' (normally an underscore)

    Also some specific properties exists:
    - Side: Generally L/R token
    - Prefix: Always the first token
    - Suffix: Always the last token

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

    You can re-define the 'known_prefix' and 'known_suffix' static properties to ensure that studio-specific
    suffix/prefix are always respected.
    It is re
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
    root_backup_name = 'backup'

    layer_anm_name = 'layer_anm'
    layer_rig_name = 'layer_rig'
    layer_geo_name = 'layer_geo'
    layer_jnt_name = 'layer_jnts'

    KNOWN_PREFIXES = []
    KNOWN_SUFFIXES = []

    SIDE_L = 'l'
    SIDE_R = 'r'

    def __init__(self, name=None, tokens=None, prefix=0, suffix=0, side=0):
        self.tokens = []
        self.prefix = None
        self.suffix = None
        self.side = None

        if name:
            tokens = self.build_from_string(name)

        # Apply manual overrides
        if tokens:
            self.tokens = tokens
        if prefix is not 0:
            self.prefix = prefix
        if suffix is not 0:
            self.suffix = suffix
        if side is not 0:
            self.side = side

    def __add__(self, other):
        """
        Merge two Name instance together.
        :param other: Another Name instance.
        :return: A new Name instance.

        >>> name = BaseName(tokens=['arm'], suffix='ctrl')
        >>> other_name = BaseName(tokens=['armupper'], side=BaseName.SIDE_L)
        >>> (name + other_name).resolve()
        'l_arm_armupper_ctrl'
        """
        result = self.copy()

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
        # self.prefix = None
        # self.suffix = None
        self.side = None

        self.add_tokens(*raw_tokens)

    def _get_tokens(self, val):
        return val.split(self.separator)

    def _join_tokens(self, tokens):
        return self.separator.join(tokens)

    def add_tokens(self, *args):
        for arg in args:
            for token in arg.split(self.separator):
                # Handle side
                side = self.get_side_from_token(token)
                if side:
                    self.side = side
                # Handle suffixes
                elif token in self.KNOWN_SUFFIXES:
                    self.suffix = token
                # Handle prefixes
                elif token in self.KNOWN_PREFIXES:
                    self.prefix = token
                # Handle normal token
                else:
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

    @classmethod
    def get_side_from_token(cls, token):
        token_lower = token.lower()
        if token_lower == cls.SIDE_L.lower():
            return cls.SIDE_L
        if token_lower == cls.SIDE_R.lower():
            return cls.SIDE_R

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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
