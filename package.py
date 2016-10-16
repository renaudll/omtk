name = 'omtk'

version = '0.1.1'

requires = ['libSerialization']

def commands():
    env.PYTHONPATH.append('{root}')
