//Maya ASCII 2017ff05 scene
//Name: twist_extractor.ma
//Last modified: Tue, Aug 22, 2017 12:09:32 AM
//Codeset: UTF-8
requires maya "2017ff05";
requires -nodeType "decomposeMatrix" -nodeType "inverseMatrix" "matrixNodes" "1.0";
requires -nodeType "quatToEuler" "quatNodes" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201706020738-1017329";
fileInfo "osv" "Linux 3.10.0-514.21.2.el7.x86_64 #1 SMP Tue Jun 20 12:24:47 UTC 2017 x86_64";
fileInfo "omtk.component.author" "";
fileInfo "omtk.component.version" "0.0.0";
fileInfo "omtk.component.uid" "92a19478-4810-491d-bfc2-b9962d54e280";
fileInfo "omtk.component.name" "twistExtractor";
createNode multMatrix -n "getTwistEndTm";
	rename -uid "0FB10900-0000-1BCF-599B-A22A000005F7";
	setAttr -s 3 ".i";
createNode multMatrix -n "getBind3LocalTm";
	rename -uid "0FB10900-0000-1BCF-599B-A30C00000621";
	setAttr -s 2 ".i";
createNode inverseMatrix -n "getInn1InverseWorldTm";
	rename -uid "0FB10900-0000-1BCF-599B-A23A000005F8";
	setAttr ".omat" -type "matrix" 0.89442719099991586 -1.2412670766236363e-16 0.44721359549995782 0 0.44721359549995782 3.1031676915590919e-16 -0.89442719099991597 0
		 -1.2412670766236363e-16 1.0000000000000002 3.1031676915590919e-16 0 0 0 0 1;
createNode inverseMatrix -n "getInn2InverseWorldTm";
	rename -uid "0FB10900-0000-1BCF-599B-A2BB0000061A";
	setAttr ".omat" -type "matrix" 0.89442719099991608 -1.2412670766236371e-16 -0.44721359549995771 0 -0.44721359549995787 3.1031676915590924e-16 -0.89442719099991608 0
		 1.7377739072730916e-16 1.0000000000000002 2.8549142762343654e-16 0 -2.6832815729997495 1.7639466088662016e-31 3.5777087639996634 1;
createNode inverseMatrix -n "getBind3InverseLocalTm";
	rename -uid "0FB10900-0000-1BCF-599B-A31E00000623";
	setAttr ".omat" -type "matrix" 1 0 -7.3955709864469857e-32 0 -4.9303806576313238e-32 1 -4.9303806576313238e-32 0
		 -5.5511151231257864e-17 0 1 0 -4.4721359549995796 2.1803579172388573e-31 -8.8817841970012494e-16 1;
createNode quatToEuler -n "convertTwistEndQuatToEuler";
	rename -uid "0FB10900-0000-1BCF-599B-A36600000627";
createNode decomposeMatrix -n "convertTwistEndTmToQuat";
	rename -uid "0FB10900-0000-1BCF-599B-A250000005F9";
	setAttr ".ot" -type "double3" 8.8817841970012523e-16 0 0 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqw" 1;
createNode multMatrix -n "getTwistStartTm";
	rename -uid "0FB10900-0000-1BCF-599B-A2C70000061B";
	setAttr -s 3 ".i";
createNode inverseMatrix -n "getBind2InverseLocalTm";
	rename -uid "0FB10900-0000-1BCF-599B-A31700000622";
	setAttr ".omat" -type "matrix" 0.60000000000000053 -2.9582283945787958e-32 -0.79999999999999971 0 3.9443045261050582e-32 1 2.9582283945787953e-32 0
		 0.79999999999999982 -3.9443045261050582e-32 0.6000000000000002 0 -2.6832815729997495 2.0625170552943501e-31 3.5777087639996625 1;
createNode unitConversion -n "getTwistStartScalar";
	rename -uid "0FB10900-0000-1BCF-599B-A4250000065C";
	setAttr ".cf" 57.295779513082323;
createNode quatToEuler -n "convertTwistStartQuatToEuler";
	rename -uid "0FB10900-0000-1BCF-599B-A37300000628";
createNode inverseMatrix -n "getBind1InverseWorldTm";
	rename -uid "0FB10900-0000-1BCF-599B-A2F700000620";
	setAttr ".omat" -type "matrix" 0.89442719099991586 -1.2412670766236363e-16 0.44721359549995782 0 0.44721359549995782 3.1031676915590919e-16 -0.89442719099991597 0
		 -1.2412670766236363e-16 1.0000000000000002 3.1031676915590919e-16 0 0 0 0 1;
createNode inverseMatrix -n "getBind2InverseWorldTm";
	rename -uid "0FB10900-0000-1BCF-599B-A2F40000061F";
	setAttr ".omat" -type "matrix" 0.89442719099991608 -1.2412670766236371e-16 -0.44721359549995771 0 -0.44721359549995787 3.1031676915590924e-16 -0.89442719099991608 0
		 1.7377739072730916e-16 1.0000000000000002 2.8549142762343654e-16 0 -2.6832815729997495 1.7639466088662016e-31 3.5777087639996634 1;
createNode multMatrix -n "getBind2LocalTm";
	rename -uid "0FB10900-0000-1BCF-599B-A2E90000061E";
	setAttr -s 2 ".i";
createNode decomposeMatrix -n "convertTwistStartTmToQuat";
	rename -uid "0FB10900-0000-1BCF-599B-A33100000624";
	setAttr ".or" -type "double3" 0 1.5125511122374552e-31 0 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqw" 1;
createNode unitConversion -n "getTwistEndScalar";
	rename -uid "0FB10900-0000-1BCF-599B-A41F0000065B";
	setAttr ".cf" 57.295779513082323;
createNode network -n "inn";
	rename -uid "0FB10900-0000-1BCF-599B-A14C000005F6";
	addAttr -ci true -sn "bind1" -ln "bind1" -at "matrix";
	addAttr -ci true -sn "bind2" -ln "bind2" -at "matrix";
	addAttr -ci true -sn "bind3" -ln "bind3" -at "matrix";
	addAttr -ci true -sn "inn1" -ln "inn1" -at "matrix";
	addAttr -ci true -sn "inn2" -ln "inn2" -at "matrix";
	addAttr -ci true -sn "inn3" -ln "inn3" -at "matrix";
	setAttr ".bind1" -type "matrix" 0.89442719099991597 0.44721359549995787 -2.7755575615628914e-17 0 -2.7755575615628914e-17 3.3306690738754696e-16 0.99999999999999989 0
		 0.44721359549995787 -0.89442719099991586 3.3306690738754696e-16 0 0 0 0 1;
	setAttr ".bind2" -type "matrix" 0.89442719099991597 -0.44721359549995765 2.4980018054066017e-16 0 -2.7755575615628914e-17 3.3306690738754696e-16 0.99999999999999989 0
		 -0.44721359549995776 -0.89442719099991597 2.2204460492503141e-16 0 4.0000000000000009 2 -1.241267076623638e-16 1;
	setAttr ".bind3" -type "matrix" 0.89442719099991597 -0.44721359549995765 2.4980018054066017e-16 0 -2.7755575615628914e-17 3.3306690738754696e-16 0.99999999999999989 0
		 -0.44721359549995776 -0.89442719099991597 2.2204460492503141e-16 0 8 8.8817841970012523e-16 9.9301366129890885e-16 1;
	setAttr ".inn1" -type "matrix" 0.89442719099991597 0.44721359549995787 -2.7755575615628914e-17 0 -2.7755575615628914e-17 3.3306690738754696e-16 0.99999999999999989 0
		 0.44721359549995787 -0.89442719099991586 3.3306690738754696e-16 0 0 0 0 1;
	setAttr ".inn2" -type "matrix" 0.89442719099991597 -0.44721359549995765 2.4980018054066017e-16 0 -2.7755575615628914e-17 3.3306690738754696e-16 0.99999999999999989 0
		 -0.44721359549995776 -0.89442719099991597 2.2204460492503141e-16 0 4.0000000000000009 2 -1.241267076623638e-16 1;
	setAttr ".inn3" -type "matrix" 0.89442719099991597 -0.44721359549995765 2.4980018054066017e-16 0 -2.7755575615628914e-17 3.3306690738754696e-16 0.99999999999999989 0
		 -0.44721359549995776 -0.89442719099991597 2.2204460492503141e-16 0 8 8.8817841970012523e-16 9.9301366129890885e-16 1;
createNode network -n "out";
	rename -uid "0FB10900-0000-1BCF-599B-A3EB00000656";
	addAttr -ci true -sn "outTwistS" -ln "outTwistS" -at "double";
	addAttr -ci true -sn "outTwistE" -ln "outTwistE" -at "double";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 14 ".u";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "inn.inn2" "getTwistEndTm.i[0]";
connectAttr "getInn1InverseWorldTm.omat" "getTwistEndTm.i[1]";
connectAttr "getBind2InverseLocalTm.omat" "getTwistEndTm.i[2]";
connectAttr "inn.bind3" "getBind3LocalTm.i[0]";
connectAttr "getBind2InverseWorldTm.omat" "getBind3LocalTm.i[1]";
connectAttr "inn.inn1" "getInn1InverseWorldTm.imat";
connectAttr "inn.inn2" "getInn2InverseWorldTm.imat";
connectAttr "getBind3LocalTm.o" "getBind3InverseLocalTm.imat";
connectAttr "convertTwistEndTmToQuat.oqw" "convertTwistEndQuatToEuler.iqw";
connectAttr "convertTwistEndTmToQuat.oqx" "convertTwistEndQuatToEuler.iqx";
connectAttr "getTwistEndTm.o" "convertTwistEndTmToQuat.imat";
connectAttr "inn.inn3" "getTwistStartTm.i[0]";
connectAttr "getInn2InverseWorldTm.omat" "getTwistStartTm.i[1]";
connectAttr "getBind3InverseLocalTm.omat" "getTwistStartTm.i[2]";
connectAttr "getBind2LocalTm.o" "getBind2InverseLocalTm.imat";
connectAttr "convertTwistStartQuatToEuler.orx" "getTwistStartScalar.i";
connectAttr "convertTwistStartTmToQuat.oqx" "convertTwistStartQuatToEuler.iqx";
connectAttr "convertTwistStartTmToQuat.oqw" "convertTwistStartQuatToEuler.iqw";
connectAttr "inn.bind1" "getBind1InverseWorldTm.imat";
connectAttr "inn.bind2" "getBind2InverseWorldTm.imat";
connectAttr "inn.bind2" "getBind2LocalTm.i[0]";
connectAttr "getBind1InverseWorldTm.omat" "getBind2LocalTm.i[1]";
connectAttr "getTwistStartTm.o" "convertTwistStartTmToQuat.imat";
connectAttr "convertTwistEndQuatToEuler.orx" "getTwistEndScalar.i";
connectAttr "getTwistEndScalar.o" "out.outTwistS";
connectAttr "getTwistStartScalar.o" "out.outTwistE";
connectAttr "getTwistEndTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getInn1InverseWorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "convertTwistEndTmToQuat.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getInn2InverseWorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getTwistStartTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getBind2LocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getBind2InverseWorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getBind1InverseWorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getBind3LocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getBind2InverseLocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getBind3InverseLocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "convertTwistStartTmToQuat.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "convertTwistEndQuatToEuler.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "convertTwistStartQuatToEuler.msg" ":defaultRenderUtilityList1.u" -na
		;
// End of twist_extractor.ma
