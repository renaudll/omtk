import pymel.core as pymel
import libSerialization

def run():
    nets = pymel.ls(type='network')
    net_rig = next(iter(net for net in nets if libSerialization.is_network_from_class(net, 'Rig')), None)

    for net in nets:
        if not libSerialization.is_network_from_class(net, 'Module'):
            continue
        if not net.hasAttr('rig'):
            print("Adding attribute 'rig' on {0}".format(net))
            pymel.addAttr(net, longName='rig', niceName='rig', attributeType='message')
        if not net.rig.isDestination():
            print("Connecting attribute 'rig' on {0}".format(net))
            pymel.connectAttr(net_rig.message, net.rig)
