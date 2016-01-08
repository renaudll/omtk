import pprint
import pymel.core as pymel
import libSerialization

# Todo: Export

# Todo: Import


def _is_utility_node():
    return True
    # is shading?


class DigitalAsset(object):
    def gen_id(self, name, itt):
        return "%s%02d" % (name, itt)

    def get_unique_id(self, name):
        itt = 1
        while self.gen_id(name, itt) in self._attnames:
            itt +=1
        return self.gen_id(name, itt)

    def get_safe_id(self, name):
        return name.replace('[', '').replace(']', '_')

    def __init__(self, nodes, **kwargs):
        self.name = "DigitalAsset"
        self.inns = []
        self.outs = []
        self.__dict__.update(kwargs)
        self._attnames = []


        for node in nodes:
            for attr in node.listAttr(keyable=True):
                if pymel.attributeQuery(attr, writable=True):
                    attr_name = self.get_unique_id('inn_' + self.get_safe_id(attr.longName()))
                    self._attnames.append(attr_name)
                    setattr(self, attr_name, attr)
                else:
                    attr_name = self.get_unique_id('out_' + self.get_safe_id(attr.longName()))
                    self._attnames.append(attr_name)
                    setattr(self, attr_name, attr)

    '''
            for attr in node.inputs(plugs=True):
                if attr.isKeyable():
                    if attr.node not in nodes:
                        attr_name = self.get_unique_id('inn_' + self.get_safe_id(attr.longName()))
                        self._attnames.append(attr_name)
                        setattr(self, attr_name, attr)
            for attr in node.outputs(plugs=True):
                if attr.isKeyable():
                    if attr.node not in nodes:
                        attr_name = self.get_unique_id('out_' + self.get_safe_id(attr.longName()))
                        self._attnames.append(attr_name)
                        setattr(self, attr_name, attr)
    '''

    def __getattr__(self, name):
        for input in self.inns:
            if input.shortName == name:
                return input
        for output in self.outs:
            if output.shortName == name:
                return output
        raise AttributeError

    def __repr__(self):
        return repr(self.__dict__)

def from_selection():
    import pymel.core as pymel
    da =  DigitalAsset(pymel.selected())
    print da.__repr__()
    libSerialization.export_network(da)
    return da



