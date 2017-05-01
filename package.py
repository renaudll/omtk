name = 'omtk'

version = '0.4.36'

requires = ['libSerialization-0.1+']

def commands():
    env.PYTHONPATH.append('{root}/python')
    env.XBMLANGPATH.append("{root}/images/%B")
