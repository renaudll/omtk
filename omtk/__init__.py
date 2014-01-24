import animation
import rigging
import libs

def _reload():
	reload(animation); animation._reload()
	reload(libs); libs._reload()
	reload(rigging); rigging._reload()