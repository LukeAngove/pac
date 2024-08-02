from reachable import getVersion
from collections import namedtuple

def test_getVersion():
    tflags = namedtuple("tflags", ["hasKey"])
    flags = tflags(True)
    target_scene = {
        "targets": {
            "hasKey": "init2",
            "default": "init",
        },
        "versions": {
            "init": {},
            "init2": {},
        },
    }

    res = getVersion(target_scene, flags)
    assert(res == "init2")

