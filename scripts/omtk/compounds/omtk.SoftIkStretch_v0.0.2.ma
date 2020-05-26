//Maya ASCII 2020 scene
//Name: omtk.SoftIkStretch_v0.0.2.ma
//Last modified: Mon, May 18, 2020 02:28:19 PM
//Codeset: 1252
// requires maya "2020";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "77AC15B0-47A6-367D-CDE1-C7A07CE5B4ED";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.2";
fileInfo "omtk.compound.uid" "a905155e-573e-48b4-86ee-567ec5db471c";
fileInfo "omtk.compound.name" "omtk.SoftIkStretch";
createNode distanceBetween -n "distanceBetween1";
	rename -uid "2BD5770B-4722-FDE4-5C55-F095A526C568";
createNode multiplyDivide -n "multiplyDivide2";
	rename -uid "534CE338-4723-997D-E1FD-668A81D1144B";
createNode plusMinusAverage -n "plusMinusAverage1";
	rename -uid "C9C10883-4B6D-7F59-83D9-C3AD3C7B6A07";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode multiplyDivide -n "multiplyDivide3";
	rename -uid "F3E2AAAC-42FE-FF26-3E6B-40806DC3F3ED";
	setAttr ".op" 2;
createNode multiplyDivide -n "multiplyDivide4";
	rename -uid "7C92B1EE-417F-51D8-128D-F58FCD44041D";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode clamp -n "clamp1";
	rename -uid "097303C7-40FF-CB3C-01E9-DAA5E274AAC0";
	setAttr ".mn" -type "float3" 9.9999997e-05 0 0 ;
	setAttr ".mx" -type "float3" 999 0 0 ;
createNode plusMinusAverage -n "plusMinusAverage2";
	rename -uid "5B3485AC-4704-53B1-8AC8-6CA1966F3CFA";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode network -n "inputs";
	rename -uid "67BFFF9A-46D3-7A0B-920C-7B9491997A51";
	addAttr -ci true -sn "length" -ln "length" -at "float";
	addAttr -ci true -sn "ratio" -ln "ratio" -at "float";
	addAttr -ci true -sn "stretch" -ln "stretch" -at "float";
	addAttr -ci true -sn "start" -ln "start" -dt "matrix";
	addAttr -ci true -sn "end" -ln "end" -dt "matrix";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	addAttr -ci true -sn "startPos" -ln "startPos" -dt "double3";
	addAttr -ci true -sn "endPos" -ln "endPos" -dt "double3";
	setAttr ".length" 7.2111024856567383;
	setAttr ".start" -type "matrix" 7.7715611723760958e-16 -0.8320502943378435 0.55470019622522926 0
		 3.3306690738754696e-16 0.55470019622522937 0.8320502943378435 0 -0.99999999999999989 -3.3306690738754696e-16 7.7715611723760958e-16 0
		 0 7 -2 1;
	setAttr ".end" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 3.1407887410280393e-15 1.0000000000000022 -2.0000000000000013 1;
	setAttr ".nts" -type "string" "author:'Renaud Lessard Larouche'\nversion:'0.0.1'\nuid:'69881719-cc70-4340-a05e-ff919aaaac31'\nname:'omtk.SoftIkStretch'\ndescription:'Inputs:\\n -length\\n -ratio\\n -stretch\\n -start\\n -end\\nOutputs:\\n -ratio\\n -stretch\\n'";
createNode distanceBetween -n "distanceBetween2";
	rename -uid "D3307ED1-49AD-E047-06F5-EF84684C8F5F";
createNode multiplyDivide -n "multiplyDivide6";
	rename -uid "2454A264-4F76-212F-08FD-949C25F6553C";
createNode plusMinusAverage -n "plusMinusAverage3";
	rename -uid "025F7F5D-4969-F90D-D02F-A9A5913DAADC";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  1 inf;
createNode multiplyDivide -n "multiplyDivide5";
	rename -uid "58197C68-480A-CD61-91F4-9280F3E4F57F";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 2.7182817 0 0 ;
createNode multiplyDivide -n "multiplyDivide7";
	rename -uid "BD10E756-465D-ABAB-1083-45A00468B433";
	setAttr ".op" 2;
createNode condition -n "condition2";
	rename -uid "27BDB3A2-4AE7-190B-DC7F-56A0110DEA15";
	setAttr ".op" 2;
createNode plusMinusAverage -n "plusMinusAverage4";
	rename -uid "7467FAA0-4EAC-4FE6-89D2-EB8372D57B70";
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode blendTwoAttr -n "blendTwoAttr1";
	rename -uid "84C4F59A-4405-E3BF-CE87-83B5B840F4D3";
	setAttr -s 2 ".i";
	setAttr -s 2 ".i";
createNode condition -n "condition3";
	rename -uid "CDD3DFD4-4CC3-3BA0-BDCB-5C9567C2C6CD";
	setAttr ".op" 2;
createNode blendTwoAttr -n "blendTwoAttr2";
	rename -uid "43B537D5-41A3-850A-2CCB-0CA82A093AFB";
	setAttr -s 2 ".i[0:1]"  1 1;
createNode multiplyDivide -n "multiplyDivide8";
	rename -uid "A8AC73B5-4B04-F0C9-5968-3A8C11B56DEF";
	setAttr ".op" 2;
createNode pairBlend -n "pairBlend1";
	rename -uid "91E8C3BD-4080-7012-207A-A6B7C83B2CED";
createNode network -n "outputs";
	rename -uid "0826A5CC-4C01-795D-8E24-428D30B77215";
	addAttr -ci true -sn "ratio" -ln "ratio" -at "float";
	addAttr -ci true -sn "stretch" -ln "stretch" -at "float";
	addAttr -ci true -sn "pos" -ln "pos" -dt "double3";
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
connectAttr "inputs.end" "distanceBetween1.im2";
connectAttr "inputs.start" "distanceBetween1.im1";
connectAttr "inputs.length" "multiplyDivide2.i1x";
connectAttr "inputs.ratio" "multiplyDivide2.i2x";
connectAttr "inputs.length" "plusMinusAverage1.i1[0]";
connectAttr "multiplyDivide2.ox" "plusMinusAverage1.i1[1]";
connectAttr "plusMinusAverage2.o1" "multiplyDivide3.i1x";
connectAttr "clamp1.opr" "multiplyDivide3.i2x";
connectAttr "multiplyDivide3.ox" "multiplyDivide4.i1x";
connectAttr "multiplyDivide2.ox" "clamp1.ipr";
connectAttr "distanceBetween1.d" "plusMinusAverage2.i1[0]";
connectAttr "plusMinusAverage1.o1" "plusMinusAverage2.i1[1]";
connectAttr "inputs.startPos" "distanceBetween2.p1";
connectAttr "inputs.endPos" "distanceBetween2.p2";
connectAttr "multiplyDivide2.ox" "multiplyDivide6.i1x";
connectAttr "plusMinusAverage3.o1" "multiplyDivide6.i2x";
connectAttr "multiplyDivide5.ox" "plusMinusAverage3.i1[1]";
connectAttr "multiplyDivide4.ox" "multiplyDivide5.i2x";
connectAttr "distanceBetween1.d" "multiplyDivide7.i1x";
connectAttr "plusMinusAverage4.o1" "multiplyDivide7.i2x";
connectAttr "plusMinusAverage4.o1" "condition2.ctr";
connectAttr "distanceBetween1.d" "condition2.cfr";
connectAttr "multiplyDivide3.ox" "condition2.ft";
connectAttr "multiplyDivide6.ox" "plusMinusAverage4.i1[0]";
connectAttr "plusMinusAverage1.o1" "plusMinusAverage4.i1[1]";
connectAttr "inputs.stretch" "blendTwoAttr1.ab";
connectAttr "condition2.ocr" "blendTwoAttr1.i[0]";
connectAttr "distanceBetween1.d" "blendTwoAttr1.i[1]";
connectAttr "plusMinusAverage1.o1" "condition3.st";
connectAttr "multiplyDivide7.ox" "condition3.ctr";
connectAttr "distanceBetween1.d" "condition3.ft";
connectAttr "inputs.stretch" "blendTwoAttr2.ab";
connectAttr "condition3.ocr" "blendTwoAttr2.i[1]";
connectAttr "blendTwoAttr1.o" "multiplyDivide8.i1x";
connectAttr "distanceBetween1.d" "multiplyDivide8.i2x";
connectAttr "inputs.startPos" "pairBlend1.it1";
connectAttr "inputs.endPos" "pairBlend1.it2";
connectAttr "multiplyDivide8.ox" "pairBlend1.w";
connectAttr "multiplyDivide8.ox" "outputs.ratio";
connectAttr "blendTwoAttr2.o" "outputs.stretch";
connectAttr "pairBlend1.ot" "outputs.pos";
connectAttr "distanceBetween2.msg" ":defaultRenderUtilityList1.u" -na;
// End of omtk.SoftIkStretch_v0.0.2.ma
