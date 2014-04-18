#include <string.h>
#include <maya/MGlobal.h>
#include <maya/MPxCommand.h>
#include <maya/MPxNode.h> 
#include <maya/MString.h> 
#include <maya/MTypeId.h> 
#include <maya/MPlug.h>
#include <maya/MFnPlugin.h>

#include <Python.h>


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

////////////////////////////////////////////////////////////////////////////////
/* Example of embedding Python in another program */

#include "Python.h"

void init_libSerialization(void); /* Forward */

int main(int argc, char **argv)
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);
    
    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();
    
    /* Add a static module */
    init_libSerialization();
    
    /* Define sys.argv.  It is up to the application if you
     want this; you can also let it undefined (since the Python
     code is generally not a main program it has no business
     touching sys.argv...) */
    PySys_SetArgv(argc, argv);
    
    /* Do some application specific code */
    printf("Hello, brave new world\n\n");
    
    /* Execute some Python statements (in module __main__) */
    PyRun_SimpleString("import sys\n");
    PyRun_SimpleString("print sys.builtin_module_names\n");
    PyRun_SimpleString("print sys.modules.keys()\n");
    PyRun_SimpleString("print sys.executable\n");
    PyRun_SimpleString("print sys.argv\n");
    
    /* Note that you can call any public function of the Python
     interpreter here, e.g. call_object(). */
    
    /* Some more application specific code */
    printf("\nGoodbye, cruel world\n");
    
    /* Exit, cleaning up the interpreter */
    Py_Exit(0);
    /*NOTREACHED*/
}

/* A static module */

/* 'self' is not used */
static PyObject *
libSerialization_foo(PyObject *self, PyObject* args)
{
    return PyInt_FromLong(42L);
}

static PyMethodDef libSerialization_methods[] = {
    {"foo",         libSerialization_foo,      METH_NOARGS,
        "Return the meaning of everything."},
    {NULL,          NULL}           /* sentinel */
};

void init_libSerialization(void)
{
    PyImport_AddModule("libSerialization");
    Py_InitModule("libSerialization", libSerialization_methods);
}