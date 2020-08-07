"""
Various utility functions
"""


def handle_arguments(**mapping):
    """
    Decorator that will remap keyword arguments.
    Useful to support maya "short" and "long" form for function arguments.
    ex: `cmds.ls(selection=True)` and `cmds.ls(sl=True)` are equivalent.

    :param mapping: A mapping of argument short name by their long name.
    :type mapping: dict[str, str]
    :return: A decorated function
    :rtype: callable
    """

    def _deco(func):
        def _wrapper(*args, **kwargs):
            kwargs_conformed = {}
            for attr, alias in mapping.items():
                if attr in kwargs:
                    kwargs_conformed[attr] = kwargs.pop(attr)
                if alias in kwargs:
                    kwargs_conformed[attr] = kwargs.pop(alias)

            if kwargs:
                raise NotImplementedError(
                    "Not implemented keyword argument{s}: {keys}".format(
                        s="s" if len(kwargs) > 1 else "", keys=", ".join(kwargs.keys())
                    )
                )

            return func(*args, **kwargs_conformed)

        return _wrapper

    return _deco


def redirect_method_args_to_arg(func):
    """
    Workaround python-2 specific issue with optional positional arguments and keyword arguments.
    see: https://www.python.org/dev/peps/pep-3102/

    This can be explained with an example:

       >>> def foo(self, kwarg1=None, *args, **kwargs):
       ...     print(args, kwargs, kwarg1)
       ...
       >>> foo(None, "arg1", "arg2")
       ('arg2',) {} arg1

    As you can see, in this case we want `kwarg1` to be a keyword-only argument.
    However it is not possible as `kwarg1` eat the first positional argument.

    A solution is to NOT use optional positional argument at all.
    Using this decorator as a wrapper, we can redirect
    optional positional arguments to the first argument.

       >>> @redirect_method_args_to_arg
       ... def foo(self, args, kwarg1=None, **kwargs):
       ...     print(args, kwargs, kwarg1)
       ...
       >>> foo(None, "arg1", "arg2")
       ('arg1', 'arg2') {} None

    :param callable func: A method to wrap.
    :return: A wrapped method
    :rtype: callable
    """

    def _wrapper(self, *args, **kwargs):
        return func(self, args, **kwargs)

    return _wrapper
