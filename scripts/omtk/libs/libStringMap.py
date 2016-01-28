class StringMap(object):
	def __init__(self, content, **kwargs):
		self.content = content
		self.set_fields(**kwargs)

	def get_fields(self):
		return self.fields

	def set_fields(self, **kwargs):
		new_fields = {}
		for key, val in kwargs.iteritems():
			new_fields['{0}'.format(key)] = val
		self.fields = kwargs

	def __str__(self):
		return self.content.format(**self.fields)

	def __repr__(self):
		return repr(self.fields)

#node_rig_map = StringMap('{type}_{uid}_{tokens}', type='rig')