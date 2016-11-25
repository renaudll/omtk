"""
In omtk 0.3.0, the FaceLids module was renamed to FaceEyeLids to prevent
confusion with the FaceLips module.
Run this script to convert a pre-0.3.0 scene.
"""

import libSerialization

cls_rename_map = (
    ('FaceLids', 'FaceEyeLids'),
    ('CtrlLidUpp', 'CtrlEyeLidUpp'),
    ('CtrlLidLow', 'CtrlEyeLidLow'),
    ('AvarGrpAreaOnSurface', 'AvarGrpOnSurface')
)
affected_attr_names = ('_class', '_class_namespace')

for old_name, new_name in cls_rename_map:
    for net in libSerialization.get_networks_from_class(old_name):
        for attr_name in affected_attr_names:
            if not net.hasAttr(attr_name):
                print("Missing attribute {} on {}".format(attr_name, net))
                continue
            print("Renaming {}".format(net))
            attr = net.attr(attr_name)
            attr.set('.'.join((token.replace(old_name, new_name) for token in attr.get().split('.'))))