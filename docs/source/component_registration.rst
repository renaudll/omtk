Component Registration
======================

For a network to be eligible for Component registration, you need to make sure that it is isolated between two networks.

.. image:: images/component_raw_network.png

You can then register the component using the following code:

.. code-block:: python

    import pymel.core as pymel
    from omtk.core import classComponent
    from omtk.vendor import libSerialization

    c = classComponent.Component()
    c.name = 'my_component'
    c.grp_inn = pymel.PyNode('inn')
    c.grp_out = pymel.PyNode('out')

    c.export('/home/rll/dev/python/omtk/components/twist_extractor2.ma')  # todo: compute the path automatically?

Here's the desired final API:

.. code-block:: python

    from omtk import component_factory
    component_factory.create_from_networks(
        'my_network',
        pymel.PyNode('inn'),
        pymel.PyNode('out')
    )
    component_factory.publish()