//Maya ASCII 2020 scene
//Name: omtk.AvarInflModelLinear_v0.0.1.ma
//Last modified: Wed, May 06, 2020 06:59:24 PM
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
fileInfo "UUID" "0259D062-490F-533B-4ADE-069C8F5AB621";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "0259D062-490F-533B-4ADE-069C8F5AB621";
fileInfo "omtk.compound.name" "omtk.AvarInflLinear";
createNode network -n "inputs";
	rename -uid "CDEEFD59-4004-90F6-9762-13B965F3A5DD";
	addAttr -ci true -sn "innAvarFb" -ln "innAvarFb" -at "double";
	addAttr -ci true -sn "innAvarLr" -ln "innAvarLr" -at "double";
	addAttr -ci true -sn "innAvarPt" -ln "innAvarPt" -at "double";
	addAttr -ci true -sn "innAvarRl" -ln "innAvarRl" -at "double";
	addAttr -ci true -sn "innAvarSx" -ln "innAvarSx" -at "double";
	addAttr -ci true -sn "innAvarSy" -ln "innAvarSy" -at "double";
	addAttr -ci true -sn "innAvarSz" -ln "innAvarSz" -at "double";
	addAttr -ci true -sn "innAvarUd" -ln "innAvarUd" -at "double";
	addAttr -ci true -sn "innAvarYw" -ln "innAvarYw" -at "double";
	addAttr -ci true -sn "innOffset" -ln "innOffset" -dt "matrix";
	addAttr -dcb 1 -ci true -k true -sn "i2x" -ln "blendTx" -dv 1 -at "float";
	addAttr -dcb 1 -ci true -k true -sn "i2y" -ln "blendTy" -dv 1 -at "float";
	addAttr -dcb 1 -ci true -k true -sn "i2z" -ln "blendTz" -dv 1 -at "float";
	addAttr -dcb 1 -ci true -k true -sn "i2x1" -ln "blendRx" -dv 1 -at "float";
	addAttr -dcb 1 -ci true -k true -sn "i2y1" -ln "blendRy" -dv 1 -at "float";
	addAttr -dcb 1 -ci true -k true -sn "i2z1" -ln "blendRz" -dv 1 -at "float";
	addAttr -dcb 1 -ci true -k true -sn "i2x2" -ln "blendSx" -dv 1 -at "float";
	addAttr -dcb 1 -ci true -k true -sn "i2y2" -ln "affectSy" -dv 1 -at "float";
	addAttr -dcb 1 -ci true -k true -sn "i2z2" -ln "blendSz" -dv 1 -at "float";
	addAttr -ci true -sn "multLr" -ln "multLr" -at "float";
	addAttr -ci true -sn "multFb" -ln "multFb" -at "float";
	addAttr -ci true -sn "multUd" -ln "multUd" -at "float";
	setAttr ".innAvarSx" 1;
	setAttr ".innAvarSy" 1;
	setAttr ".innAvarSz" 1;
	setAttr ".innOffset" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 5.5511151231257827e-17 0 0.50613270285737955 1;
	setAttr -k on ".i2x";
	setAttr -k on ".i2y";
	setAttr -k on ".i2z";
	setAttr -k on ".i2x1";
	setAttr -k on ".i2y1";
	setAttr -k on ".i2z1";
	setAttr -k on ".i2x2";
	setAttr -k on ".i2y2";
	setAttr -k on ".i2z2";
createNode multiplyDivide -n "applyPosMultiplier";
	rename -uid "89330A1D-4CB7-19CA-B13A-4D8619691BF4";
createNode multiplyDivide -n "applyRotBlend";
	rename -uid "928E8045-49FE-514D-9201-4FB0815D4C6D";
createNode multiplyDivide -n "applyPosBlend";
	rename -uid "FC668766-452A-2D47-C6F5-2DAF4DD9AC87";
createNode unitConversion -n "unitConversion61";
	rename -uid "5966EA51-42E6-4A11-D084-2394FD0ACCE3";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "applySclBlend";
	rename -uid "594D5E24-45C3-B8A0-E926-40B63863AA64";
createNode composeMatrix -n "getLocalTM";
	rename -uid "592F2F89-4D38-7A53-E93F-589F77089DF9";
createNode multMatrix -n "applyOffsetTM";
	rename -uid "66A795DA-478D-A87F-A212-9D8A455B7B5D";
	setAttr -s 2 ".i";
createNode network -n "outputs";
	rename -uid "5AEE8C87-4E52-58EE-E6F0-2A8CDD23DFA9";
	addAttr -s false -ci true -sn "omat" -ln "outputMatrix" -at "matrix";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 0;
	setAttr -av ".unw";
	setAttr -k on ".etw";
	setAttr -k on ".tps";
	setAttr -k on ".tms";
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
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".u";
select -ne :defaultRenderingList1;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".dss" -type "string" "lambert1";
connectAttr "inputs.multUd" "applyPosMultiplier.i2y";
connectAttr "inputs.multLr" "applyPosMultiplier.i2x";
connectAttr "inputs.multFb" "applyPosMultiplier.i2z";
connectAttr "inputs.innAvarLr" "applyPosMultiplier.i1x";
connectAttr "inputs.innAvarUd" "applyPosMultiplier.i1y";
connectAttr "inputs.innAvarFb" "applyPosMultiplier.i1z";
connectAttr "inputs.i2x1" "applyRotBlend.i2x";
connectAttr "inputs.i2y1" "applyRotBlend.i2y";
connectAttr "inputs.i2z1" "applyRotBlend.i2z";
connectAttr "inputs.innAvarPt" "applyRotBlend.i1x";
connectAttr "inputs.innAvarYw" "applyRotBlend.i1y";
connectAttr "inputs.innAvarRl" "applyRotBlend.i1z";
connectAttr "applyPosMultiplier.o" "applyPosBlend.i1";
connectAttr "inputs.i2x" "applyPosBlend.i2x";
connectAttr "inputs.i2y" "applyPosBlend.i2y";
connectAttr "inputs.i2z" "applyPosBlend.i2z";
connectAttr "applyRotBlend.o" "unitConversion61.i";
connectAttr "inputs.i2x2" "applySclBlend.i2x";
connectAttr "inputs.i2z2" "applySclBlend.i2z";
connectAttr "inputs.i2y2" "applySclBlend.i2y";
connectAttr "inputs.innAvarSx" "applySclBlend.i1x";
connectAttr "inputs.innAvarSy" "applySclBlend.i1y";
connectAttr "inputs.innAvarSz" "applySclBlend.i1z";
connectAttr "applyPosBlend.o" "getLocalTM.it";
connectAttr "unitConversion61.o" "getLocalTM.ir";
connectAttr "applySclBlend.o" "getLocalTM.is";
connectAttr "getLocalTM.omat" "applyOffsetTM.i[0]";
connectAttr "inputs.innOffset" "applyOffsetTM.i[1]";
connectAttr "applyOffsetTM.o" "outputs.omat";
connectAttr "applyOffsetTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyPosBlend.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyRotBlend.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applySclBlend.msg" ":defaultRenderUtilityList1.u" -na;
// End of omtk.AvarInflModelLinear_v0.0.1.ma
