import yaml
import os
import core

__all__ = (
	'export_yaml',
    'export_yaml_file',
    'import_yaml',
    'import_yaml_file'
)

def export_yaml(data, **kwargs):
	dicData = core.export_dict(data)
	return yaml.dump(dicData, **kwargs)

def export_yaml_file(data, path, mkdir=True, **kwargs):
	if mkdir: 
		os.makedirs(path)

	dicData = core.export_dict(data)

	with open(path, 'w') as fp:
		yaml.dump(dicData, fp)

	return True

def import_yaml(str_, **kwargs):
	data = yaml.load(str_)
	return core.import_dict(data)

def import_yaml_file(path, **kwargs):
	if not os.path.exists(path):
		raise Exception("Can't importFromYamlFile, file does not exist! {0}".format(path))

	with open(path, 'r') as fp:
		data = yaml.load(fp)
	return core.import_dict(data)
