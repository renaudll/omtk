//Maya ASCII 2020 scene
//Name: omtk.InteractiveCtrl_v0.0.1.ma
//Last modified: Mon, Apr 27, 2020 11:05:46 AM
//Codeset: 1252
// requires maya "2020";
requires -nodeType "inverseMatrix" "matrixNodes" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "D98A34C0-4A68-93E4-5148-2BA369279EA9";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "6E4D092E-4392-A54E-A7E5-33AE63854593";
fileInfo "omtk.compound.name" "omtk.InteractiveCtrl";
createNode transform -n "dag";
	rename -uid "F2284602-4751-4805-5EF3-41BD67ED2729";
createNode follicle -n "l_cheek_jnt_cheek_follicle_rigShape" -p "dag";
	rename -uid "11C474E0-471F-96B7-73B3-66BA73142B87";
	setAttr -k off ".v";
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -s -n "persp";
	rename -uid "3E88EACF-4FDC-DDC4-44D6-20A6C0823D19";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 28 21 28 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "C279BBD4-4E42-F012-6F71-5094AFD9B544";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "5F595060-4A24-8791-F141-CABAE789CD62";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "C5E2A6F8-4406-D768-5D33-D9BEB77595A2";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "D51B9BA9-40C5-0906-BE73-4CB39EF0158C";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "D06B2141-4AAA-6D2B-2B9B-888D613AD3BE";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "8147FC8A-4A6B-E4A2-1BEA-36AB88E3C126";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "689879D5-4122-8480-33F2-58868E3644F6";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode pointOnSurfaceInfo -n "follicle:pointOnSurfaceInfo1";
	rename -uid "B9FAF25A-4E83-7CEE-BA26-EABC24085CDE";
createNode decomposeMatrix -n "decomposeCtrlLocalTM";
	rename -uid "DCA23430-4E67-4A40-21E7-3D8902C6B572";
createNode decomposeMatrix -n "decomposeMatrix161";
	rename -uid "56334B4A-480E-4101-29EB-DB9DA43FB2A5";
createNode multiplyDivide -n "multiplyDivide46";
	rename -uid "395E2443-4507-F850-7EA8-6D825C685860";
	setAttr ".i2" -type "float3" -1 -1 -1 ;
createNode unitConversion -n "unitConversion52";
	rename -uid "D266D47F-436D-98DA-EE74-BCA33DCE50A7";
	setAttr ".cf" 57.295779513082323;
createNode network -n "inputs";
	rename -uid "40C00AC1-4CED-5994-0406-298A4C60906B";
	addAttr -ci true -sn "bindTM" -ln "bindTM" -dt "matrix";
	addAttr -ci true -sn "mesh" -ln "mesh" -dt "mesh";
	addAttr -ci true -sn "parameterU" -ln "parameterU" -at "float";
	addAttr -ci true -sn "parameterV" -ln "parameterV" -at "float";
	addAttr -ci true -sn "follicleBindTM" -ln "follicleBindTM" -dt "matrix";
	addAttr -ci true -sn "sensitivityX" -ln "sensitivityX" -at "float";
	addAttr -ci true -sn "sensitivityY" -ln "sensitivityY" -at "float";
	addAttr -ci true -sn "sensitivityZ" -ln "sensitivityZ" -at "float";
	addAttr -ci true -sn "ctrlLocalTM" -ln "ctrlLocalTM" -dt "matrix";
	addAttr -ci true -sn "ctrlShapeOrig" -ln "ctrlShapeOrig" -dt "nurbsCurve";
	setAttr ".bindTM" -type "matrix" 1.0000000000000002 0 0 0 0 1.0000000000000004 0 0
		 0 0 1 0 0.44958669403607443 15.900531583857832 1.6920539488665605 1;
	setAttr ".mesh" -type "mesh" 


		"v"	4
		-0.5	0	0.5
		0.5	0	0.5
		-0.5	0	-0.5
		0.5	0	-0.5

		"vt"	4
		0	0
		1	0
		0	1
		1	1

		"e"	4
		0	1	"hard"
		0	2	"hard"
		1	3	"hard"
		2	3	"hard"

		"face"	
		"l"	4	0	2	-4	-2	
		"lt"	4	0	1	3	2	;
	setAttr ".parameterU" 2.7275063991546631;
	setAttr ".parameterV" 0.44066837430000305;
	setAttr ".follicleBindTM" -type "matrix" -0.83969181007605886 -0.115742283892815 0.53058589107746457 0
		 0.025511085612758257 -0.98435251623299314 -0.17435397413490089 0 0.5424636841319892 -0.13286778204309041 0.82950545742201065 0
		 0.44958695769309998 15.900532722473145 1.7304239273071289 1;
	setAttr ".sensitivityX" 0.084827542304992676;
	setAttr ".sensitivityY" 0.042409896850585938;
	setAttr ".sensitivityZ" 0.033930540084838867;
	setAttr ".ctrlLocalTM" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ctrlShapeOrig" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122449 0.7836116248912246 0
		6.7857323231109122e-17 1.1081941875543877 0
		-0.78361162489122449 0.78361162489122438 0
		-1.1081941875543881 5.7448982375248304e-17 0
		-0.78361162489122449 -0.78361162489122449 0
		-1.1100856969603225e-16 -1.1081941875543884 0
		0.78361162489122449 -0.78361162489122438 0
		1.1081941875543881 -1.511240500779959e-16 0
		0.78361162489122449 0.7836116248912246 0
		6.7857323231109122e-17 1.1081941875543877 0
		-0.78361162489122449 0.78361162489122438 0
		;
createNode composeMatrix -n "composeMatrix17";
	rename -uid "102D9A27-4F7C-FE30-AF6D-CA8FF3D42EDA";
createNode multiplyDivide -n "multiplyDivide48";
	rename -uid "342F93DA-43EF-5375-D8E5-FA84C4A2D843";
	setAttr ".i2" -type "float3" -1 -1 -1 ;
createNode multiplyDivide -n "multiplyDivide45";
	rename -uid "2A51F11B-4316-8790-6E6E-30A6357A5A0A";
	setAttr ".op" 2;
	setAttr ".i1" -type "float3" 1 1 1 ;
createNode multiplyDivide -n "multiplyDivide47";
	rename -uid "E1B65D2F-4266-AB65-3BE8-458A2F80C186";
createNode inverseMatrix -n "inverseMatrix12";
	rename -uid "91CE16CE-46FA-0AA5-BBF6-9CB9B315A28F";
createNode plusMinusAverage -n "plusMinusAverage1";
	rename -uid "678BE221-4C26-79F5-E356-15806AEA33CB";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode composeMatrix -n "composeMatrix16";
	rename -uid "15B46336-4071-A7E0-4F0E-398006B7701B";
createNode unitConversion -n "unitConversion53";
	rename -uid "0D1DA7C7-4D52-0E15-5F44-D681841D6323";
	setAttr ".cf" 0.017453292519943295;
createNode multMatrix -n "multMatrix28";
	rename -uid "106BF6D3-4052-C3C4-C9DE-B78EA1223D33";
	setAttr -s 3 ".i";
createNode composeMatrix -n "getInverseTM";
	rename -uid "EF95C869-469E-6F35-ABB2-E583C79688DC";
createNode transformGeometry -n "transformGeometry9";
	rename -uid "8910CB47-4C31-127D-A490-54B8C806F602";
createNode multMatrix -n "multMatrix29";
	rename -uid "C9B9F22F-4173-5129-9453-F1AEFDA8C08B";
createNode network -n "outputs";
	rename -uid "66C3C5D6-4059-5AD2-CFFD-15AABFB2C73A";
	addAttr -ci true -sn "outputTM" -ln "outputTM" -dt "matrix";
	addAttr -ci true -sn "ctrlShapeAdjusted" -ln "ctrlShapeAdjusted" -dt "nurbsCurve";
	addAttr -ci true -sn "folliclePos" -ln "folliclePos" -dt "double3";
createNode displayLayerManager -n "layerManager";
	rename -uid "C7110F97-4F82-1A3F-D6D9-CEAF127146FD";
	setAttr -s 23 ".dli[1:22]"  23 3 4 2 5 6 7 8 
		9 10 11 12 13 14 15 16 17 18 19 20 21 22;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "7152A971-4F46-0EE0-0D5E-E68CD37EFCB0";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "6763084E-4B64-6218-4001-0A8465FDC34F";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "BCA500A4-4ADF-761E-B99C-AF97A0DB326F";
createNode displayLayer -n "defaultLayer";
	rename -uid "6AB40272-4ADC-322D-39B5-17B4C9E55EA2";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "3C0D8E08-45F9-737E-1231-D998813A15AB";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "61132F00-4C1F-A78A-D161-8A9EBA62AC31";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "8AF40E5B-4B95-1D27-BC3C-2298EB004AC4";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 120 -ast 0 -aet 200 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "B9DD1EF5-49E4-880A-FCD8-EA8AD4D72096";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -667.56526188114947 -851.93699343808021 ;
	setAttr ".tgi[0].vh" -type "double2" 1339.1573709074271 736.49497832027464 ;
	setAttr -s 6 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 581.4285888671875;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" -695.71429443359375;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 904.6595458984375;
	setAttr ".tgi[0].ni[2].y" -3.2176203727722168;
	setAttr ".tgi[0].ni[2].nvs" 18306;
	setAttr ".tgi[0].ni[3].x" 274.28570556640625;
	setAttr ".tgi[0].ni[3].y" -51.428569793701172;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" -388.57144165039063;
	setAttr ".tgi[0].ni[4].y" 97.142860412597656;
	setAttr ".tgi[0].ni[4].nvs" 18305;
	setAttr ".tgi[0].ni[5].x" -55.380485534667969;
	setAttr ".tgi[0].ni[5].y" 78.963027954101563;
	setAttr ".tgi[0].ni[5].nvs" 18305;
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
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".etmr" no;
	setAttr ".tmr" 4096;
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
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
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
connectAttr "inputs.mesh" "l_cheek_jnt_cheek_follicle_rigShape.inm";
connectAttr "inputs.parameterU" "l_cheek_jnt_cheek_follicle_rigShape.pu";
connectAttr "inputs.parameterV" "l_cheek_jnt_cheek_follicle_rigShape.pv";
connectAttr "inputs.ctrlLocalTM" "decomposeCtrlLocalTM.imat";
connectAttr "inputs.ctrlLocalTM" "decomposeMatrix161.imat";
connectAttr "decomposeCtrlLocalTM.ot" "multiplyDivide46.i1";
connectAttr "decomposeCtrlLocalTM.or" "unitConversion52.i";
connectAttr "decomposeMatrix161.or" "composeMatrix17.ir";
connectAttr "unitConversion52.o" "multiplyDivide48.i1";
connectAttr "inputs.sensitivityY" "multiplyDivide45.i2y";
connectAttr "inputs.sensitivityX" "multiplyDivide45.i2x";
connectAttr "inputs.sensitivityZ" "multiplyDivide45.i2z";
connectAttr "multiplyDivide46.o" "multiplyDivide47.i1";
connectAttr "composeMatrix17.omat" "inverseMatrix12.imat";
connectAttr "multiplyDivide47.o" "plusMinusAverage1.i3[0]";
connectAttr "l_cheek_jnt_cheek_follicle_rigShape.ot" "plusMinusAverage1.i3[1]";
connectAttr "multiplyDivide45.oy" "composeMatrix16.isy";
connectAttr "multiplyDivide45.ox" "composeMatrix16.isx";
connectAttr "multiplyDivide45.oz" "composeMatrix16.isz";
connectAttr "multiplyDivide48.o" "unitConversion53.i";
connectAttr "composeMatrix17.omat" "multMatrix28.i[0]";
connectAttr "composeMatrix16.omat" "multMatrix28.i[1]";
connectAttr "inverseMatrix12.omat" "multMatrix28.i[2]";
connectAttr "unitConversion53.o" "getInverseTM.ir";
connectAttr "plusMinusAverage1.o3" "getInverseTM.it";
connectAttr "inputs.ctrlShapeOrig" "transformGeometry9.ig";
connectAttr "multMatrix28.o" "transformGeometry9.txf";
connectAttr "getInverseTM.omat" "multMatrix29.i[0]";
connectAttr "multMatrix29.o" "outputs.outputTM";
connectAttr "transformGeometry9.og" "outputs.ctrlShapeAdjusted";
connectAttr "l_cheek_jnt_cheek_follicle_rigShape.ot" "outputs.folliclePos";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "multMatrix29.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "inputs.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn";
connectAttr "outputs.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "getInverseTM.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "l_cheek_jnt_cheek_follicle_rigShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "plusMinusAverage1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of omtk.InteractiveCtrl_v0.0.1.ma
