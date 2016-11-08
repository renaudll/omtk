name = 'omtk'

version = '0.2.3'

requires = ['libSerialization-0.1+']

def commands():
    env.PYTHONPATH.append('{root}')
