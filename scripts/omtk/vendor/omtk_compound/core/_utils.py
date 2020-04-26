""" Various utility methods """
import itertools
import re
from contextlib import contextmanager
import pymel.core as pymel

_REGEX_GROUP_PREFIX = re.compile("(.*[^0-9]+)([0-9]*)$")


def get_unique_key(name, all_names, naming_format="{0}{1}", start=1):
    """

    >>> get_unique_key('v1', ['v1', 'v2'])
    'v3'
    >>> get_unique_key('v', ['v', 'v1', 'v2'])
    'v3'

    :param str name: A start value
    :param all_names: A sequence of existing values
    :type all_names: Sequence[str]
    :param naming_format:
    :param start:
    :return:
    """
    if name not in all_names:
        return name

    name, prefix = _REGEX_GROUP_PREFIX.match(name).groups()
    if prefix:
        start = int(prefix) + 1  # we'll try next

    counter = itertools.count(start)
    while True:
        new_name = naming_format.format(name, next(counter))
        if new_name not in all_names:
            return new_name


def pairwise(iterable):
    """ Consume an iterable by yielded two values at the time.
    Recipe from: https://docs.python.org/2/library/itertools.html

    :param Iterable iterable: An iterable
    :return: A generator that yield two values at once
    :rtype: Generator[object, object]
    """
    iter_a, iter_b = itertools.tee(iterable)
    next(iter_b, None)
    return itertools.izip(iter_a, iter_b)


@contextmanager
def preserve_selection():
    """ Context that preserve the current selection.

    :return: A context
    :rtype: Generator
    """
    sel = pymel.selected()
    yield
    if sel:
        pymel.select(sel)
    else:
        pymel.select(clear=True)
