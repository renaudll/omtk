//Maya ASCII 2019 scene
//Name: omtk.AvarCtrlLinear_v0.0.2.ma
//Last modified: Tue, Jun 09, 2020 08:48:47 PM
//Codeset: UTF-8
requires maya "2019";
requires -nodeType "decomposeMatrix" -nodeType "composeMatrix" "matrixNodes" "1.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2019";
fileInfo "version" "2019";
fileInfo "cutIdentifier" "201812112215-434d8d9c04";
fileInfo "osv" "Linux 3.10.0-1127.8.2.el7.x86_64 #1 SMP Tue May 12 16:57:42 UTC 2020 x86_64";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.2";
fileInfo "omtk.compound.uid" "CDEEFD59-4004-90F6-9762-13B965F3A5DD";
fileInfo "omtk.compound.name" "omtk.AvarCtrlLinear";
createNode network -n "inputs";
	rename -uid "CDEEFD59-4004-90F6-9762-13B965F3A5DD";
	addAttr -ci true -sn "avar" -ln "avar" -at "compound" -nc 9;
	addAttr -ci true -sn "avarLR" -ln "avarLR" -at "double" -p "avar";
	addAttr -ci true -sn "avarUD" -ln "avarUD" -at "double" -p "avar";
	addAttr -ci true -sn "avarFB" -ln "avarFB" -at "double" -p "avar";
	addAttr -ci true -sn "avarYW" -ln "avarYW" -at "double" -p "avar";
	addAttr -ci true -sn "avarPT" -ln "avarPT" -at "double" -p "avar";
	addAttr -ci true -sn "avarRL" -ln "avarRL" -at "double" -p "avar";
	addAttr -ci true -sn "avarScaleLR" -ln "avarScaleLR" -at "double" -p "avar";
	addAttr -ci true -sn "avarScaleUD" -ln "avarScaleUD" -at "double" -p "avar";
	addAttr -ci true -sn "avarScaleFB" -ln "avarScaleFB" -at "double" -p "avar";
	addAttr -ci true -sn "innOffset" -ln "innOffset" -dt "matrix";
	addAttr -ci true -sn "multLr" -ln "multLr" -at "float";
	addAttr -ci true -sn "multFb" -ln "multFb" -at "float";
	addAttr -ci true -sn "multUd" -ln "multUd" -at "float";
	addAttr -ci true -sn "ctrlLocalTM" -ln "ctrlLocalTM" -at "matrix";
	setAttr ".innOffset" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
createNode unitConversion -n "unitConversion6";
	rename -uid "8D97C9C0-0000-0C4B-5ED6-F42F0000033E";
	setAttr ".cf" 0.017453292519943295;
createNode unitConversion -n "unitConversion5";
	rename -uid "8D97C9C0-0000-0C4B-5ED6-F3CE0000033D";
	setAttr ".cf" 0.017453292519943295;
createNode decomposeMatrix -n "decomposeCtrlLocalTM";
	rename -uid "300679C0-0000-0AB0-5EE0-357C00001415";
createNode multiplyDivide -n "applyPosMultiplier";
	rename -uid "89330A1D-4CB7-19CA-B13A-4D8619691BF4";
createNode unitConversion -n "unitConversion7";
	rename -uid "300679C0-0000-0AB0-5EE0-35D60000141B";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion4";
	rename -uid "8D97C9C0-0000-0C4B-5ED6-F3B20000033C";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "getLocalRotInv";
	rename -uid "300679C0-0000-0AB0-5EE0-35D20000141A";
	setAttr ".i2" -type "float3" -1 -1 -1 ;
createNode unitConversion -n "unitConversion8";
	rename -uid "300679C0-0000-0AB0-5EE0-36150000141D";
	setAttr ".cf" 0.017453292519943295;
createNode composeMatrix -n "getAvarTm";
	rename -uid "592F2F89-4D38-7A53-E93F-589F77089DF9";
	setAttr ".omat" -type "matrix" 9.9999999999999998e-13 0 0 0 0 9.9999999999999998e-13 0 0
		 0 0 9.9999999999999998e-13 0 0 0 0 1;
createNode multiplyDivide -n "getLocalScaleInv";
	rename -uid "300679C0-0000-0AB0-5EE0-35DA0000141C";
	setAttr ".op" 2;
	setAttr ".i1" -type "float3" 1 1 1 ;
createNode multMatrix -n "applyOffsetTM";
	rename -uid "66A795DA-478D-A87F-A212-9D8A455B7B5D";
	setAttr -s 3 ".i";
createNode composeMatrix -n "getCtrlLocalTmRotInv";
	rename -uid "300679C0-0000-0AB0-5EE0-359900001417";
	setAttr ".ro" 5;
createNode multMatrix -n "getCtrlInvLocalTm";
	rename -uid "300679C0-0000-0AB0-5EE0-36330000141E";
	setAttr -s 3 ".i";
createNode composeMatrix -n "getCtrlLocalTmSclInv";
	rename -uid "300679C0-0000-0AB0-5EE0-35A400001418";
createNode multiplyDivide -n "getLocalPosInv";
	rename -uid "300679C0-0000-0AB0-5EE0-35CA00001419";
	setAttr ".i2" -type "float3" -1 -1 -1 ;
createNode decomposeMatrix -n "decomposeMatrix1";
	rename -uid "8D97C9C0-0000-0C4B-5ED6-F2AC00000337";
createNode composeMatrix -n "getCtrlLocalTmPosInv";
	rename -uid "300679C0-0000-0AB0-5EE0-358600001416";
createNode network -n "outputs";
	rename -uid "5AEE8C87-4E52-58EE-E6F0-2A8CDD23DFA9";
	addAttr -ci true -sn "ctrlOffsetTranslate" -ln "ctrlOffsetTranslate" -at "double3" 
		-nc 3;
	addAttr -ci true -sn "ctrlOffsetTranslateX" -ln "ctrlOffsetTranslateX" -at "double" 
		-p "ctrlOffsetTranslate";
	addAttr -ci true -sn "ctrlOffsetTranslateY" -ln "ctrlOffsetTranslateY" -at "double" 
		-p "ctrlOffsetTranslate";
	addAttr -ci true -sn "ctrlOffsetTranslateZ" -ln "ctrlOffsetTranslateZ" -at "double" 
		-p "ctrlOffsetTranslate";
	addAttr -ci true -sn "ctrlOffsetRotate" -ln "ctrlOffsetRotate" -at "double3" -nc 
		3;
	addAttr -ci true -sn "ctrlOffsetRotateX" -ln "ctrlOffsetRotateX" -at "doubleAngle" 
		-p "ctrlOffsetRotate";
	addAttr -ci true -sn "ctrlOffsetRotateY" -ln "ctrlOffsetRotateY" -at "doubleAngle" 
		-p "ctrlOffsetRotate";
	addAttr -ci true -sn "ctrlOffsetRotateZ" -ln "ctrlOffsetRotateZ" -at "doubleAngle" 
		-p "ctrlOffsetRotate";
	addAttr -ci true -sn "ctrlOffsetScale" -ln "ctrlOffsetScale" -at "float3" -nc 3;
	addAttr -ci true -sn "ctrlOffsetScaleX" -ln "ctrlOffsetScaleX" -at "float" -p "ctrlOffsetScale";
	addAttr -ci true -sn "ctrlOffsetScaleY" -ln "ctrlOffsetScaleY" -at "float" -p "ctrlOffsetScale";
	addAttr -ci true -sn "ctrlOffsetScaleZ" -ln "ctrlOffsetScaleZ" -at "float" -p "ctrlOffsetScale";
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
	setAttr -s 4 ".s";
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
	setAttr -s 10 ".u";
select -ne :defaultRenderingList1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
connectAttr "inputs.avarRL" "unitConversion6.i";
connectAttr "inputs.avarYW" "unitConversion5.i";
connectAttr "inputs.ctrlLocalTM" "decomposeCtrlLocalTM.imat";
connectAttr "inputs.multUd" "applyPosMultiplier.i2y";
connectAttr "inputs.multLr" "applyPosMultiplier.i2x";
connectAttr "inputs.multFb" "applyPosMultiplier.i2z";
connectAttr "inputs.avarLR" "applyPosMultiplier.i1x";
connectAttr "inputs.avarUD" "applyPosMultiplier.i1y";
connectAttr "inputs.avarFB" "applyPosMultiplier.i1z";
connectAttr "decomposeCtrlLocalTM.or" "unitConversion7.i";
connectAttr "inputs.avarPT" "unitConversion4.i";
connectAttr "unitConversion7.o" "getLocalRotInv.i1";
connectAttr "getLocalRotInv.o" "unitConversion8.i";
connectAttr "applyPosMultiplier.o" "getAvarTm.it";
connectAttr "unitConversion5.o" "getAvarTm.iry";
connectAttr "unitConversion6.o" "getAvarTm.irz";
connectAttr "unitConversion4.o" "getAvarTm.irx";
connectAttr "inputs.avarScaleUD" "getAvarTm.isy";
connectAttr "inputs.avarScaleFB" "getAvarTm.isz";
connectAttr "inputs.avarScaleLR" "getAvarTm.isx";
connectAttr "decomposeCtrlLocalTM.os" "getLocalScaleInv.i2";
connectAttr "getCtrlInvLocalTm.o" "applyOffsetTM.i[0]";
connectAttr "getAvarTm.omat" "applyOffsetTM.i[1]";
connectAttr "inputs.innOffset" "applyOffsetTM.i[2]";
connectAttr "unitConversion8.o" "getCtrlLocalTmRotInv.ir";
connectAttr "getCtrlLocalTmPosInv.omat" "getCtrlInvLocalTm.i[0]";
connectAttr "getCtrlLocalTmRotInv.omat" "getCtrlInvLocalTm.i[1]";
connectAttr "getCtrlLocalTmSclInv.omat" "getCtrlInvLocalTm.i[2]";
connectAttr "getLocalScaleInv.o" "getCtrlLocalTmSclInv.is";
connectAttr "decomposeCtrlLocalTM.ot" "getLocalPosInv.i1";
connectAttr "applyOffsetTM.o" "decomposeMatrix1.imat";
connectAttr "getLocalPosInv.o" "getCtrlLocalTmPosInv.it";
connectAttr "decomposeMatrix1.ot" "outputs.ctrlOffsetTranslate";
connectAttr "decomposeMatrix1.os" "outputs.ctrlOffsetScale";
connectAttr "decomposeMatrix1.or" "outputs.ctrlOffsetRotate";
connectAttr "applyOffsetTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeMatrix1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeCtrlLocalTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getCtrlLocalTmPosInv.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getCtrlLocalTmRotInv.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getCtrlLocalTmSclInv.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLocalPosInv.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLocalRotInv.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLocalScaleInv.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getCtrlInvLocalTm.msg" ":defaultRenderUtilityList1.u" -na;
// End of omtk.AvarCtrlLinear_v0.0.2.ma
