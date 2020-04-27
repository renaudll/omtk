//Maya ASCII 2017ff05 scene
//Name: TwistExtractor-0.0.4.ma
//Last modified: Mon, Feb 12, 2018 10:37:00 PM
//Codeset: UTF-8
requires maya "2017ff05";
requires -nodeType "decomposeMatrix" -nodeType "inverseMatrix" "matrixNodes" "1.0";
requires -nodeType "quatToEuler" "quatNodes" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201710312130-1018716";
fileInfo "osv" "Linux 4.13.0-32-generic #35-Ubuntu SMP Thu Jan 25 09:13:46 UTC 2018 x86_64";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "dc3a518c-25d3-4abe-a6e4-7df3efa78d11";
fileInfo "omtk.compound.name" "omtk.TwistExtractor";
createNode quatToEuler -n "convertTwistEndQuatToEuler";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000448";
createNode multMatrix -n "getBind2LocalTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000443";
	setAttr -s 2 ".i";
createNode inverseMatrix -n "getBind1InverseWorldTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000442";
	setAttr ".omat" -type "matrix" 0.89442719099991586 -1.2412670766236363e-16 0.44721359549995782 0 0.44721359549995782 3.1031676915590919e-16 -0.89442719099991597 0
		 -1.2412670766236363e-16 1.0000000000000002 3.1031676915590919e-16 0 0 0 0 1;
createNode inverseMatrix -n "getInn1InverseWorldTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000439";
	setAttr ".omat" -type "matrix" 0.89442719099991586 -1.2412670766236363e-16 0.44721359549995782 0 0.44721359549995782 3.1031676915590919e-16 -0.89442719099991597 0
		 -1.2412670766236363e-16 1.0000000000000002 3.1031676915590919e-16 0 0 0 0 1;
createNode network -n "inputs";
	rename -uid "AACF9980-0000-4B37-5A82-5D540000043B";
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
createNode multMatrix -n "getBind3LocalTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000446";
	setAttr -s 2 ".i";
createNode multMatrix -n "getTwistEndTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D540000043C";
	setAttr -s 3 ".i";
createNode multMatrix -n "getTwistStartTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D540000044A";
	setAttr -s 3 ".i";
createNode inverseMatrix -n "getBind2InverseWorldTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D540000043F";
	setAttr ".omat" -type "matrix" 0.89442719099991608 -1.2412670766236371e-16 -0.44721359549995771 0 -0.44721359549995787 3.1031676915590924e-16 -0.89442719099991608 0
		 1.7377739072730916e-16 1.0000000000000002 2.8549142762343654e-16 0 -2.6832815729997495 1.7639466088662016e-31 3.5777087639996634 1;
createNode network -n "outputs";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000447";
	addAttr -ci true -sn "outTwistS" -ln "outTwistS" -at "double";
	addAttr -ci true -sn "outTwistE" -ln "outTwistE" -at "double";
createNode decomposeMatrix -n "convertTwistEndTmToQuat";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000449";
	setAttr ".ot" -type "double3" 8.8817841970012523e-16 0 0 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqw" 1;
createNode unitConversion -n "getTwistEndScalar";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000438";
	setAttr ".cf" 57.295779513082323;
createNode quatToEuler -n "convertTwistStartQuatToEuler";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000440";
createNode unitConversion -n "getTwistStartScalar";
	rename -uid "AACF9980-0000-4B37-5A82-5D540000043D";
	setAttr ".cf" 57.295779513082323;
createNode inverseMatrix -n "getBind3InverseLocalTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000445";
	setAttr ".omat" -type "matrix" 1 0 -7.3955709864469857e-32 0 -4.9303806576313238e-32 1 -4.9303806576313238e-32 0
		 -5.5511151231257864e-17 0 1 0 -4.4721359549995796 2.1803579172388573e-31 -8.8817841970012494e-16 1;
createNode decomposeMatrix -n "convertTwistStartTmToQuat";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000444";
	setAttr ".or" -type "double3" 0 1.5125511122374552e-31 0 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqw" 1;
createNode inverseMatrix -n "getInn2InverseWorldTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D5400000441";
	setAttr ".omat" -type "matrix" 0.89442719099991608 -1.2412670766236371e-16 -0.44721359549995771 0 -0.44721359549995787 3.1031676915590924e-16 -0.89442719099991608 0
		 1.7377739072730916e-16 1.0000000000000002 2.8549142762343654e-16 0 -2.6832815729997495 1.7639466088662016e-31 3.5777087639996634 1;
createNode inverseMatrix -n "getBind2InverseLocalTm";
	rename -uid "AACF9980-0000-4B37-5A82-5D540000043E";
	setAttr ".omat" -type "matrix" 0.60000000000000053 -2.9582283945787958e-32 -0.79999999999999971 0 3.9443045261050582e-32 1 2.9582283945787953e-32 0
		 0.79999999999999982 -3.9443045261050582e-32 0.6000000000000002 0 -2.6832815729997495 2.0625170552943501e-31 3.5777087639996625 1;
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
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "convertTwistEndTmToQuat.oqw" "convertTwistEndQuatToEuler.iqw"
		;
connectAttr "convertTwistEndTmToQuat.oqx" "convertTwistEndQuatToEuler.iqx"
		;
connectAttr "inputs.bind2" "getBind2LocalTm.i[0]";
connectAttr "getBind1InverseWorldTm.omat" "getBind2LocalTm.i[1]"
		;
connectAttr "inputs.bind1" "getBind1InverseWorldTm.imat"
		;
connectAttr "inputs.inn1" "getInn1InverseWorldTm.imat"
		;
connectAttr "inputs.bind3" "getBind3LocalTm.i[0]";
connectAttr "getBind2InverseWorldTm.omat" "getBind3LocalTm.i[1]"
		;
connectAttr "inputs.inn2" "getTwistEndTm.i[0]";
connectAttr "getInn1InverseWorldTm.omat" "getTwistEndTm.i[1]"
		;
connectAttr "getBind2InverseLocalTm.omat" "getTwistEndTm.i[2]"
		;
connectAttr "inputs.inn3" "getTwistStartTm.i[0]";
connectAttr "getInn2InverseWorldTm.omat" "getTwistStartTm.i[1]"
		;
connectAttr "getBind3InverseLocalTm.omat" "getTwistStartTm.i[2]"
		;
connectAttr "inputs.bind2" "getBind2InverseWorldTm.imat"
		;
connectAttr "getTwistEndScalar.o" "outputs.outTwistS";
connectAttr "getTwistStartScalar.o" "outputs.outTwistE"
		;
connectAttr "getTwistEndTm.o" "convertTwistEndTmToQuat.imat"
		;
connectAttr "convertTwistEndQuatToEuler.orx" "getTwistEndScalar.i"
		;
connectAttr "convertTwistStartTmToQuat.oqx" "convertTwistStartQuatToEuler.iqx"
		;
connectAttr "convertTwistStartTmToQuat.oqw" "convertTwistStartQuatToEuler.iqw"
		;
connectAttr "convertTwistStartQuatToEuler.orx" "getTwistStartScalar.i"
		;
connectAttr "getBind3LocalTm.o" "getBind3InverseLocalTm.imat"
		;
connectAttr "getTwistStartTm.o" "convertTwistStartTmToQuat.imat"
		;
connectAttr "inputs.inn2" "getInn2InverseWorldTm.imat"
		;
connectAttr "getBind2LocalTm.o" "getBind2InverseLocalTm.imat"
		;
connectAttr "getTwistEndTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "getInn1InverseWorldTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "convertTwistEndTmToQuat.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getInn2InverseWorldTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getTwistStartTm.msg" ":defaultRenderUtilityList1.u" 
		-na;
connectAttr "getBind2LocalTm.msg" ":defaultRenderUtilityList1.u" 
		-na;
connectAttr "getBind2InverseWorldTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getBind1InverseWorldTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getBind3LocalTm.msg" ":defaultRenderUtilityList1.u" 
		-na;
connectAttr "getBind2InverseLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getBind3InverseLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "convertTwistStartTmToQuat.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "convertTwistEndQuatToEuler.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "convertTwistStartQuatToEuler.msg" ":defaultRenderUtilityList1.u"
		 -na;
// End of TwistExtractor-0.0.4.ma
