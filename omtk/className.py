from libs import libPython


class BaseName(object):
    """
    This class handle the naming of object.
    Store a name as a collection of string 'tokens'.
    Note that since maya don't support compounds and having the same name on multiple nodes can cause issues,
    we need to support multiple number of tokens.
    """
    separator = '_'

    def __init__(self, name, prefix=None, suffix=None):
        self.tokens = self._get_tokens(name)
        # prefix and suffix are automatically handled
        self.prefix = prefix
        self.suffix = suffix

    def _get_tokens(self, name):
        return name.split(self.separator)

    def add_tokens(self, *args):
        self.tokens.extend(args)

    def add_suffix(self, suffix):
        self.tokens.append(suffix)

    def add_prefix(self, prefix):
        self.tokens.insert(0, prefix)

    @libPython.memoized
    def resolve(self, *args):
        tokens = []

        if self.prefix:
            tokens.append(self.prefix)
        tokens.extend(self.tokens)
        tokens.extend(args)
        if self.suffix:
            tokens.append(self.suffix)

        return self.separator.join(tokens)

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


class Name(BaseName):
    def _get_tokens(self, name):
        tokens = super(Name, self)._get_tokens(name)
        return tokens[1:] if tokens else None
