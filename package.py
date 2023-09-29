name = 'omtk'

version = '0.6.0'


def commands():
    env.PYTHONPATH.append('{root}/python')

    if system.platform == 'windows':
        env.XBMLANGPATH.append("{root}/images/")
    else:
        env.XBMLANGPATH.append("{root}/images/%B")
