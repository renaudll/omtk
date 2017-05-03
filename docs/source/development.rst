Development
~~~~~~~~~~~

Nomenclature Class
==================

.. TODO: Rename add_tokens to add_token
.. TODO: Rename BaseName to Nomenclature

The Nomenclature class handle the parsing and generation of object name in OMTK.
You might want to subclass your own Nomenclature definition to match your needs.

Internals
---------
To name objects, omtk use *tokens* separated using a *separator* (generally ``_``).

.. code-block:: python

    >>> name = Nomenclature('nose')
    >>> name
    'nose'
    >>> name.add_tokens('jnt')
    >>> print(name)
    'nose_jnt'

The number of token is variable and is a good way of suggesting encapsulation.

.. TODO: Example?

Note that hyerarchy in Maya can also suggest encapsulation, however it is often used for other purpose like organization and controlling transforms.

Prefix and Suffixes
-------------------
It is common to see a studio nomenclature where specific tokens are always at the start or the end of a string.
By defining the ``KNOWN_SUFFIXES`` static property, recognised tokens will always be before normal tokens.

    .. code-block:: python

        class MyNomenclature(Nomenclature):
            KNOWN_SUFFIXES = ('ctrl', 'geo', 'jnt')

        >>> name = MyNomenclature('nose')
        >>> name.add_tokens('jnt')
        >>> name.add_tokens('tweak')
        >>> print(name)
        'nose_tweak_jnt'

By defining the ``KNOWN_PREFIXES`` static property, recognised tokens will always be after normal tokens.

    .. code-block:: python

        class MyNomenclature(Nomenclature):
            KNOWN_PREFIX = ('ctrl', 'geo', 'jnt')

        >>> name = MyNomenclature('nose')
        >>> name.add_tokens('jnt')
        >>> name.add_tokens('tweak')
        >>> print(name)
        'jnt_nose_tweak'

Finally, you can always define one-time suffix using the ``add_suffix`` or ``add_prefix`` method.

    .. code-block:: python

        >>> name = Nomenclature('nose')
        >>> name.add_suffix('jnt')
        >>> name.add_prefix('global')
        >>> print(name)
        'global_nose_jnt'

Side
----
Side is a special token that is handled by the implementation of Nomenclature.
It is generally defined as left or right but can also support any other variation like middle/upp/low/etc.
When subclassing BaseClass to implement new side, you'll want to look at get_side_from_token().

Here's an example of subclass that implement the 'M' side for 'Middle':

    >>> class CustomName(Nomenclature):
    ...     SIDE_L = 'l'
    ...     SIDE_R = 'r'
    ...     SIDE_M = 'm'
    ...     KNOWN_SIDES = [SIDE_L, SIDE_R, SIDE_M]
    ...
    >>> nomenclature = CustomName(tokens=('spine', 'ik'), side=CustomName.SIDE_L)
    >>> nomenclature.resolve('locator')
    'spine_ik_locator_l'

Separators
----------

TODO

Here's an example of a subclass that implement separators using PascalCase.

Plugin Management
=================
OMTK feature a Plugin Manager that allow studios to create and manage their own plugins without needing to hijack the core or distribute them. The Plugin Manager is simple and use the pkgutil Python module as fundation.

Creating Plugins
--------------
You can currently create two types of plugins.

- Modules
- Rigs

Simply create the following hierarchy somewhere on a location on disk:

- omtk
    - modules
        - __init__.py
    - rigs
        - __init__.py

Then, add the path to the path to that location to the OMTK_PLUGINS environment variable.
Any modules or rigs that you will define in this hierarchy will be added to OMTK library.
Here's the most basic example of a module implementation.

Located at {location}/omtk/modules/FlyingSaucer.py

.. code-block:: python
   :linenos:

   from omtk.core.classModule import Module
   
   class FlyingSaucer(Module):
       pass

   def register_plugin():
       return FlyingSaucer

Defining a register_plugin function that return your module class definition is the only prerequisite to have your plugin running.

Debugging Plugins
-----------------

Do see if your plugin is loaded correctly, you can use the GUI or run the following command:

    >>> from omtk.core import plugin_manager
    >>> pm = plugin_manager.plugin_manager
    >>> pm.get_summary()

When you do changes to your code, you can either re-open the GUI or run the following command:

    >>> from omtk.core import plugin_manager
    >>> pm = plugin_manager.plugin_manager
    >>> pm.reload_all(force=True)
