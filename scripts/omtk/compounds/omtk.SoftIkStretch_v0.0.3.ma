//Maya ASCII 2020 scene
//Name: omtk.SoftIkStretch_v0.0.3.ma
//Last modified: Mon, May 18, 2020 02:36:24 PM
//Codeset: 1252
requires maya "2020";
requires "stereoCamera" "10.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "EBD72779-4F25-DCF8-DD3B-9497364A68B7";
fileInfo "omtk.compound.description" "Inputs:\n -length\n -ratio\n -stretch\n -start\n -end\nOutputs:\n -ratio\n -stretch\n";
fileInfo "omtk.compound.version" "0.0.3";
fileInfo "omtk.compound.uid" "a905155e-573e-48b4-86ee-567ec5db471c";
fileInfo "omtk.compound.name" "omtk.SoftIkStretch";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
createNode blendTwoAttr -n "blendTwoAttr1";
	rename -uid "8B0CD7AC-43E8-D81E-2E08-BB95F987BB26";
	setAttr -s 2 ".i";
	setAttr -s 2 ".i";
createNode blendTwoAttr -n "blendTwoAttr2";
	rename -uid "26BBD026-4176-609C-8EE2-579FF999B9A8";
	setAttr -s 2 ".i[0:1]"  1 1;
createNode clamp -n "clamp1";
	rename -uid "92C321DA-40CE-5A59-D3CB-D5A6BFC5FCF2";
	setAttr ".mn" -type "float3" 9.9999997e-05 0 0 ;
	setAttr ".mx" -type "float3" 999 0 0 ;
createNode condition -n "condition2";
	rename -uid "284CEB9F-417C-D822-755E-D2B35F7EE923";
	setAttr ".op" 2;
createNode condition -n "condition3";
	rename -uid "E88FA03F-447F-CE01-CFDC-1688F066736D";
	setAttr ".op" 2;
createNode distanceBetween -n "distanceBetween2";
	rename -uid "D4074015-44A1-4AD7-3AD3-01828E192B87";
createNode network -n "inputs";
	rename -uid "A61F1D00-4C0B-01A1-5D1E-5F9D2AAAFC25";
	addAttr -ci true -sn "length" -ln "length" -at "float";
	addAttr -ci true -sn "ratio" -ln "ratio" -at "float";
	addAttr -ci true -sn "stretch" -ln "stretch" -at "float";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	addAttr -ci true -sn "start" -ln "start" -dt "double3";
	addAttr -ci true -sn "end" -ln "end" -dt "double3";
	setAttr ".length" 7.2111024856567383;
	setAttr ".ratio" 0.096999995410442352;
	setAttr ".nts" -type "string" "author:'Renaud Lessard Larouche'\nversion:'0.0.3'\nuid:'69881719-cc70-4340-a05e-ff919aaaac31'\nname:'omtk.SoftIkStretch'\ndescription:'Inputs:\\n -length\\n -ratio\\n -stretch\\n -start\\n -end\\nOutputs:\\n -ratio\\n -stretch\\n'";
	setAttr ".start" -type "double3" 3.1513902987550457 7 -2 ;
	setAttr ".end" -type "double3" 3.1513902987550488 1.0000000000000011 -1.9999999999999991 ;
createNode multiplyDivide -n "multiplyDivide2";
	rename -uid "12C7496E-44D2-936C-22AC-31A17AD19391";
createNode multiplyDivide -n "multiplyDivide3";
	rename -uid "5CF20D3B-4C3D-E0B3-888F-B3BE2BF734A4";
	setAttr ".op" 2;
createNode multiplyDivide -n "multiplyDivide4";
	rename -uid "BB7D2B7C-416C-40F0-5541-66B5FDFE81AF";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "multiplyDivide5";
	rename -uid "5E3E4B70-4311-F843-C8C6-E4A6886D2CF5";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 2.7182817 0 0 ;
createNode multiplyDivide -n "multiplyDivide6";
	rename -uid "8DA75187-488C-9867-45E2-75B9194F54DF";
createNode multiplyDivide -n "multiplyDivide7";
	rename -uid "5D14FD27-4889-678E-74F8-30AF6BD12A4B";
	setAttr ".op" 2;
createNode multiplyDivide -n "multiplyDivide8";
	rename -uid "DAA50918-43D4-092C-6C8F-5C9BF8BC10F3";
	setAttr ".op" 2;
createNode network -n "outputs";
	rename -uid "74E31759-42C6-F438-686D-DF9E796E3148";
	addAttr -ci true -sn "stretch" -ln "stretch" -at "float";
	addAttr -ci true -sn "end" -ln "end" -dt "double3";
createNode pairBlend -n "pairBlend1";
	rename -uid "EAF4EF84-4705-1542-92BB-83A11D87601C";
createNode plusMinusAverage -n "plusMinusAverage1";
	rename -uid "FEC9FDC7-4D3F-24DB-36C3-70BD5A292450";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode plusMinusAverage -n "plusMinusAverage2";
	rename -uid "CE06FC62-4301-DC59-3C1C-D4BD817E2D24";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode plusMinusAverage -n "plusMinusAverage3";
	rename -uid "4756FACE-4C55-5F6B-E5FB-FFB85632C80E";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  1 2.078072071;
createNode plusMinusAverage -n "plusMinusAverage4";
	rename -uid "F5C16F86-4EE4-5853-C4B1-12880DDC125D";
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr -av ".unw" 1;
	setAttr -k on ".etw";
	setAttr -k on ".tps";
	setAttr -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".etmr" no;
	setAttr ".tmr" 4096;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 2 ".u";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -cb on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -cb on ".isu";
	setAttr -cb on ".pdu";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off ".ctrs" 256;
	setAttr -av -k off ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "inputs.stretch" "blendTwoAttr1.ab"
		;
connectAttr "condition2.ocr" "blendTwoAttr1.i[0]"
		;
connectAttr "distanceBetween2.d" "blendTwoAttr1.i[1]"
		;
connectAttr "inputs.stretch" "blendTwoAttr2.ab"
		;
connectAttr "condition3.ocr" "blendTwoAttr2.i[1]"
		;
connectAttr "multiplyDivide2.ox" "clamp1.ipr"
		;
connectAttr "plusMinusAverage4.o1" "condition2.ctr"
		;
connectAttr "distanceBetween2.d" "condition2.cfr"
		;
connectAttr "multiplyDivide3.ox" "condition2.ft"
		;
connectAttr "plusMinusAverage1.o1" "condition3.st"
		;
connectAttr "multiplyDivide7.ox" "condition3.ctr"
		;
connectAttr "distanceBetween2.d" "condition3.ft"
		;
connectAttr "inputs.start" "distanceBetween2.p1"
		;
connectAttr "inputs.end" "distanceBetween2.p2"
		;
connectAttr "inputs.length" "multiplyDivide2.i1x"
		;
connectAttr "inputs.ratio" "multiplyDivide2.i2x"
		;
connectAttr "plusMinusAverage2.o1" "multiplyDivide3.i1x"
		;
connectAttr "clamp1.opr" "multiplyDivide3.i2x"
		;
connectAttr "multiplyDivide3.ox" "multiplyDivide4.i1x"
		;
connectAttr "multiplyDivide4.ox" "multiplyDivide5.i2x"
		;
connectAttr "multiplyDivide2.ox" "multiplyDivide6.i1x"
		;
connectAttr "plusMinusAverage3.o1" "multiplyDivide6.i2x"
		;
connectAttr "distanceBetween2.d" "multiplyDivide7.i1x"
		;
connectAttr "plusMinusAverage4.o1" "multiplyDivide7.i2x"
		;
connectAttr "blendTwoAttr1.o" "multiplyDivide8.i1x"
		;
connectAttr "distanceBetween2.d" "multiplyDivide8.i2x"
		;
connectAttr "blendTwoAttr2.o" "outputs.stretch"
		;
connectAttr "pairBlend1.ot" "outputs.end"
		;
connectAttr "inputs.start" "pairBlend1.it1"
		;
connectAttr "inputs.end" "pairBlend1.it2"
		;
connectAttr "multiplyDivide8.ox" "pairBlend1.w"
		;
connectAttr "inputs.length" "plusMinusAverage1.i1[0]"
		;
connectAttr "multiplyDivide2.ox" "plusMinusAverage1.i1[1]"
		;
connectAttr "distanceBetween2.d" "plusMinusAverage2.i1[0]"
		;
connectAttr "plusMinusAverage1.o1" "plusMinusAverage2.i1[1]"
		;
connectAttr "multiplyDivide5.ox" "plusMinusAverage3.i1[1]"
		;
connectAttr "multiplyDivide6.ox" "plusMinusAverage4.i1[0]"
		;
connectAttr "plusMinusAverage1.o1" "plusMinusAverage4.i1[1]"
		;
connectAttr "distanceBetween2.msg" ":defaultRenderUtilityList1.u"
		 -na;
// End of omtk.SoftIkStretch_v0.0.3.ma
