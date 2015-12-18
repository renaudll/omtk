import pymel.core as pymel
import re
from libs import libPython


class Name(object):
    """
    This class handle the naming of object.
    Store a name as a collection of string 'tokens'.
    Note that since maya don't support compounds, we need to handle multiple number of tokens.
    """
    separator = '_'

    def __init__(self, name, prefix=None, suffix=None):
        # prefix and suffix are automatically handled
        self.prefix = prefix
        self.suffix = suffix
        self.tokens = name.split(self.separator)

    def add_suffix(self, suffix):
        self.tokens.append(suffix)

    def add_prefix(self, prefix):
        self.tokens.insert(0, prefix)

    @libPython.memoized
    def resolve(self, *args):
        tokens = []

        if self.prefix:
            tokens.append(self.prefix)
        tokens.extend(args)
        if self.suffix:
            tokens.append(self.suffix)

        return self.separator.join(tokens)

    def __repr__(self):
        return self.resolve()
