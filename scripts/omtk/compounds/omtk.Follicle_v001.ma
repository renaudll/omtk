//Maya ASCII 2020 scene
//Name: omtk.Follicle_v001.ma
//Last modified: Sun, Apr 26, 2020 08:35:48 PM
//Codeset: 1252
// requires maya "2020";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "95FF2CD3-42BE-E1EB-3020-36B28F519D63";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "95FF2CD3-42BE-E1EB-3020-36B28F519D63";
fileInfo "omtk.compound.name" "omtk.Follicle";
createNode pointOnSurfaceInfo -n "pointOnSurfaceInfo1";
	rename -uid "D4649307-4AD9-07CC-8784-13943BEA2DD2";
createNode network -n "inputs";
	rename -uid "0E0D07B7-4904-BC92-1EA4-32BEAC2CE073";
	addAttr -s false -ci true -sn "is" -ln "inputSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "u" -ln "parameterU" -at "double";
	addAttr -ci true -sn "v" -ln "parameterV" -at "double";
createNode fourByFourMatrix -n "fourByFourMatrix1";
	rename -uid "E31D94CB-46DE-3E29-78AA-0BA2E324483A";
createNode network -n "outputs";
	rename -uid "695429D5-4D56-E2C1-D9AA-BC9DC22A2982";
	addAttr -s false -sn "o" -ln "output" -dt "matrix";
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
connectAttr "inputs.is" "pointOnSurfaceInfo1.is";
connectAttr "inputs.u" "pointOnSurfaceInfo1.u";
connectAttr "inputs.v" "pointOnSurfaceInfo1.v";
connectAttr "pointOnSurfaceInfo1.px" "fourByFourMatrix1.i30";
connectAttr "pointOnSurfaceInfo1.py" "fourByFourMatrix1.i31";
connectAttr "pointOnSurfaceInfo1.pz" "fourByFourMatrix1.i32";
connectAttr "pointOnSurfaceInfo1.nx" "fourByFourMatrix1.i00";
connectAttr "pointOnSurfaceInfo1.ny" "fourByFourMatrix1.i01";
connectAttr "pointOnSurfaceInfo1.nz" "fourByFourMatrix1.i02";
connectAttr "pointOnSurfaceInfo1.tux" "fourByFourMatrix1.i10";
connectAttr "pointOnSurfaceInfo1.tuy" "fourByFourMatrix1.i11";
connectAttr "pointOnSurfaceInfo1.tuz" "fourByFourMatrix1.i12";
connectAttr "pointOnSurfaceInfo1.tvx" "fourByFourMatrix1.i20";
connectAttr "pointOnSurfaceInfo1.tvy" "fourByFourMatrix1.i21";
connectAttr "pointOnSurfaceInfo1.tvz" "fourByFourMatrix1.i22";
connectAttr "fourByFourMatrix1.o" "outputs.o";
// End of omtk.Follicle_v001.ma
