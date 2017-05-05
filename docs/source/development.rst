Development
~~~~~~~~~~~

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
