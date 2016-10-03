import pkgutil
import pprint

print 'modules.__path__ before:'
pprint.pprint(__path__)
print

__path__ = pkgutil.extend_path(__path__, __name__)

print 'modules.__path__ after:'
pprint.pprint(__path__)
print