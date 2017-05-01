name = 'omtk'

version = '0.5.0'

requires = ['libSerialization-0.1+']

def commands():
    env.PYTHONPATH.append('{root}/python')
