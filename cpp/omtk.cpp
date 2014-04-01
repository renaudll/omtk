#include <string.h>
#include <maya/MGlobal.h>
#include <maya/MPxCommand.h>
#include <maya/MPxNode.h> 
#include <maya/MString.h> 
#include <maya/MTypeId.h> 
#include <maya/MPlug.h>

#include <maya/MFnPlugin.h>

// Export command
class cmd_exportToNetwork : public MPxCommand 
{
	public:
		cmd_exportToNetwork() {};
		virtual MStatus doIt(const MArgList&)
		{
			MGlobal::displayInfo("Hello World!");
  			return MS::kSuccess;
		}
		static void* creator()
		{
			return new cmd_exportToNetwork;
		}
};

// Import command
class cmd_importFromNetwork : public MPxCommand 
{
	public:
		cmd_importFromNetwork() {};
		virtual MStatus doIt(const MArgList&)
		{
			MGlobal::displayInfo("Hello World!");
  			return MS::kSuccess;
		}
		static void* creator() { return new cmd_importFromNetwork; }
};


MStatus initializePlugin ( MObject obj )
{ 
	MStatus   status;
	MFnPlugin plugin( obj, PLUGIN_COMPANY, "4.5", "Any");

	status = plugin.registerCommand("exportToNetwork", cmd_exportToNetwork::creator);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	status = plugin.registerCommand("importFromNetwork", cmd_importFromNetwork::creator);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	return status;
}

MStatus uninitializePlugin( MObject obj)
{
	MStatus   status;
	MFnPlugin plugin( obj );

	plugin.deregisterCommand("exportToNetwork");
	CHECK_MSTATUS_AND_RETURN_IT(status);
	plugin.deregisterCommand("importFromNetwork");
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return status;
}
