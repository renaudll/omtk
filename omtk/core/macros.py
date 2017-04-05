"""
A macro is a simple action that can be in a shelf or in a keyboard shortcut. Nothing fancy.
"""


class BaseMacro(object):
    def run(self):
        raise NotImplementedError
