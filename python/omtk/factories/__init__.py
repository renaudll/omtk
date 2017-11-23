import logging


log = logging.getLogger('omtk')


def reload_():
    log.debug('Reloading factory_datatypes')
    from omtk.factories import factory_datatypes
    reload(factory_datatypes)

    log.debug('Reloading factory_tree_widget_item')
    from omtk.factories import factory_tree_widget_item
    reload(factory_tree_widget_item)

    log.debug('Reloading factory_rc_menu')
    from omtk.factories import factory_rc_menu
    reload(factory_rc_menu)
