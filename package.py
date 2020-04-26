name = "omtk"

version = "0.6.0"


def commands():
    env = locals()["env"]
    system = locals()["system"]

    env.PYTHONPATH.append("{root}/scripts/python")

    if system.platform == "windows":
        env.XBMLANGPATH.append("{root}/icons/")
    else:
        env.XBMLANGPATH.append("{root}/icons/%B")
