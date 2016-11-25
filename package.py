name = 'omtk'

version = '0.3.0'

requires = ['libSerialization-0.1+']

def commands():
    env.PYTHONPATH.append('{root}')
