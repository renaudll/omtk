name = 'omtk'

version = '0.4.41'

requires = ['libSerialization-0.1+']

def commands():
    env.PYTHONPATH.append('{root}/python')
    # Because windows...
    if system.platform == 'windows':
    	env.XBMLANGPATH.append("{root}/images/")
    else:
    	env.XBMLANGPATH.append("{root}/images/%B")
