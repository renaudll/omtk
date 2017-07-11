import pymel.core as pymel
from omtk.core import api
from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore


class AutoRigManager(QtCore.QObject):
    """
    Manager class than handle possible user actions in omtk.
    """
    # todo: move AutoRig class logic to the manager and implement unit tests

    # Used when a new Rig instance is added to the scene.
    onRigCreated = QtCore.Signal(object)

    def __init__(self):
        super(AutoRigManager, self).__init__()
        self._root = None
        self._roots = []

        # Initialize libSerialization cache.
        # This will allow to re-use data.
        # Note that we will reset the cache at each import.
        from omtk.vendor.libSerialization import cache
        self._serialization_cache = cache.Cache()

    def _add_rig(self, rig):
        self._roots.append(rig)
        if self._root is None:
            self._root = next(iter(self._roots), None)
        libSerialization.export_network(rig, cache=self._serialization_cache)

    def import_networks(self):
        """
        Re-import everything from the scene.
        Warning, this is a SLOW operation.
        :return:
        """
        from omtk.vendor.libSerialization import cache
        self._serialization_cache = cache.Cache()
        self._roots = api.find(cache=self._serialization_cache)
        self._root = next(iter(self._roots), None)

    def export_networks(self):
        """
        Re-export everything in the scene.
        Warning, this is a SLOW operation.
        :return:
        """
        for root in self._roots:
            try:
                network = root._network
                if network and network.exists():
                    pymel.delete(network)
            except AttributeError:
                pass

        for root in self._roots:
            libSerialization.export_network(root, cache=self._serialization_cache)

    def create_rig(self, rig_type=None):
        if rig_type is None:
            # todo: get default rig definition
            raise NotImplementedError
        # rig_type = self.get_selected_rig_definition()

        # Initialize the scene
        rig = api.create(cls=rig_type)
        rig.build()
        self._add_rig(rig)
        libSerialization.export_network(rig)

        self.onRigCreated.emit(rig)

        return rig

