name = 'omtk'

version = '2.0.0a1'

requires = ['libSerialization-0.1+']

def commands():
    env.PYTHONPATH.append('{root}/python')
    env.XBMLANGPATH.append("{root}/shelf/%B")
