import functools
from maya import cmds

class AttrData(object):
    def __init__(self, attr=None, **kwargs):
        self.value = None
        self.preInifinity = None
        self.postInfinity = None

        # key properties
        self.times = []
        self.values = []
        self.inAngles = []
        self.outAngles = []
        self.weightedTangent = []
        self.inWeights = []
        self.outWeights = []
        self.inTangentTypes = []
        self.outTangentTypes = []
        self.locks = []
        self.weightLocks = []

        self.__dict__.update(kwargs)  # Alow monkey-patching

        if attr:
            self.build(attr)

    def build(self, attr):
        animCurve = next(iter(attr.inputs()), None)
        if animCurve:
            num_keys = animCurve.numKeys()
            for i in xrange(num_keys):
                self.times.append(animCurve.getTime(i))
                self.values.append(animCurve.getValue(i))
                self.inAngles.append(animCurve.getTangent(i, True))
                self.outAngles.append(animCurve.getTangent(i, False))
                self.inTangentTypes.append(int(animCurve.getInTangentType(i)))
                self.outTangentTypes.append(int(animCurve.getOutTangentType(i)))
                self.locks.append(animCurve.getTangentsLocked(i))
                self.weightLocks.append(animCurve.getWeightsLocked(i))

        # Store static value
        self.value = attr.get()

    def apply(self, attr):
        obj = attr.node()
        obj_mel = obj.__melobject__()
        attr_longName = attr.longName()
        attrMel = attr.__melobject__()
        if len(self.times) > 0:
            for time, value in zip(self.times, self.values):
                cmds.setKeyframe(obj_mel, time=time, attribute=attr_longName, value=value,
                     breakdown=False,  # TODO: Approve
                     hierarchy='none',  # TODO: Approve
                     controlPoints=False,  # TODO: Approve
                     shape=False)  # TODO: Approve

            # set tangents
            cmds.keyTangent(attrMel, edit=True, wt=int(self.weightedTangent))  # todo: approve int cast
            for time, inAngle, outAngle, inWeight, outWeight, inTangentType, outTangentType, lock in zip(
                self.times, self.inAngles, self.outAngles, self.inWeights, self.outWeights, self.inTangentTypes, self.outTangentTypes, self.locks):
                fn_keyTangent = functools.partial(cmds.keyTangent, attrMel, edit=True, time=(time, time))
                fn_keyTangent(inAngle=inAngle,
                    outAngle=outAngle,
                    inWeight=inWeight,
                    outWeight=outWeight)
                fn_keyTangent(inTangentType=inTangentType,outTangentType=outTangentType)
                fn_keyTangent(lock=lock) # TODO: Optimise

            # set infinity
            if self.preInfinity != "constant":
                cmds.setInfinity(obj, attribute=attr_longName, preInfinity=self.preInfinity)
            if self.postInfinity != "constant":
                cmds.setInfinity(obj, attribute=attr_longName, postInfinity=self.postInfinity)
        else:
            attr.set(self.value)

def copy(objs, **kwargs):
    data = []
    for obj in objs:
        attrs = []
        for attr in obj.listAttr(unlocked=True, keyable=True, visible=True, scalar=True, multi=True):
            attrs.append(AttrData(attr))
        data.append(attrs)
    return data

def paste(data, objs):
    """
    docstring
    """
    pass