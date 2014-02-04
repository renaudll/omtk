import pymel.core as pymel
import logging
from classNameMap import NameMap

'''
This is the baseclass for anything that can be Build/Unbuild
'''
class RigPart(object):

    # Allow self.PostInputSet() to be called automaticly when self.aInput is set.
    @property
    def aInput(self):
        return self.__dict__['aInput']

    @aInput.setter
    def aInput(self, val):
        self.__dict__['aInput'] = val
        self.PostInputSet()

    def __init__(self, _aInput=[], *args, **kwargs):
        self.aInput = _aInput
        self.iCtrlIndex = 2
        self.oGrpAnm = None
        self.oGrpRig = None

    # Even when nothing is build, it's usefull to access properties like namemaps.
    # This method is called automaticly when self.aInput is changed. 
    def PostInputSet(self):
        oRef = next(iter(self.aInput), None)
        if oRef is not None:
            self._pNameMapAnm = NameMap(oRef, _sType='anm')
            self._pNameMapRig = NameMap(oRef, _sType='rig')
            self._oParent = oRef.getParent() if oRef is not None else None

    def Build(self, _bCreateGrpAnm=True, _bCreateGrpRig=True, *args, **kwargs):
        assert(hasattr(self, '_pNameMapAnm') and self._pNameMapAnm is not None)
        assert(hasattr(self, '_pNameMapRig') and self._pNameMapRig is not None)

        logging.info('Building {0}'.format(self._pNameMapRig.Serialize()))

        if len(self.aInput) == 0:
            logging.error("[RigPart:Build] Can't build, aInput is empty"); return False

        if _bCreateGrpAnm:
            self.oGrpAnm = pymel.createNode('transform', name=self._pNameMapAnm.Serialize(self.__class__.__name__.lower(), _sType='anms'))
        if _bCreateGrpRig:
            self.oGrpRig = pymel.createNode('transform', name=self._pNameMapRig.Serialize(self.__class__.__name__.lower(), _sType='rigs'))

    def Unbuild(self):
        if self.oGrpAnm is not None:
            pymel.delete(self.oGrpAnm)
            self.oGrpAnm = None
        if self.oGrpRig is not None:
            pymel.delete(self.oGrpRig)
            self.oGrpRig = None

    def _isAnm(self, _obj):
        return any((s for s in _obj.getShapes() if isinstance(s, pymel.nodetypes.NurbsCurve)))

    def getAnmObjs(self, _fnFilter=None):
        if _fnFilter is None: _fnFilter = self._isAnm # Default filter
        iterable = iter(pymel.listRelatives(self.oGrpAnm, allDescendents=True, type='transform'))
        return filter(_fnFilter, iterable)

    def getRigObjs(self, _fnFilter=None):
        iterable = iter(pymel.listRelatives(self.oGrpRig, allDescendents=True, type='transform'))
        return filter(_fnFilter, iterable)

    def __getNetworkName__(self):
        return self._pNameMapRig.Serialize(self.__class__.__name__, _sType='net')

    # Overwritten from Serializable
    def __createMayaNetwork__(self):
        return pymel.createNode('network', name=self._pNameMapAnm.Serialize(_sType='net'))
