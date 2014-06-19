from omtk.rigging.autorig import RigNode

"""
Since Pixar don't seem to want to release the OSD (Open Scene Descriptor) projet, here's my take on the matter.

data = {
    "shots":[
        {
            "location":{
                "type":"Shot",
                "id":001,
                "name":"shotName"
            },
            "frame_range":{
                "start":0,
                "end":100,
                "padding-l":24,
                "padding-r":24,
                "preroll":10,
                "postroll":10
            },
            "assets":[
                {
                    "name": "asset01", # used for reference only
                    "location":{ # shotgun reference
                        "type":"Asset",
                        "id":001,
                        "name":"assetName"
                    },
                    "transforms":{ # animation file
                        "type":"PublishedFile",
                        "id":001
                    }
                },
                {
                    "name": "asset02", # used for reference only
                    "location": "X:/assets/ex.ma",
                    "transforms": [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1] # matrix
                }
            ]
        }
    ]
}
"""

class Attribute(object):
    def __init__(self, value):
        self.value = value

class Asset(object):
    field_type = 'camera'
    locked = False
    pass

class Shot(object):
    pass

class FrameRange(object):
    def __init__(self, start=None, end=None, handle=None, tail=None, preroll=None, postroll=None, **kwargs):
        self.__dict__.update(kwargs)