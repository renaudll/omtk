//Maya ASCII 2020 scene
//Name: omtk.AvarInflSurfaceTemplate.ma
//Last modified: Thu, May 07, 2020 09:25:55 PM
//Codeset: 1252
// requires maya "2020";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "E8A5DE2C-48AA-35F2-3836-90A852FD05B6";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "E8A5DE2C-48AA-35F2-3836-90A852FD05B6";
fileInfo "omtk.compound.name" "omtk.AvarInflSurfaceTemplate";
createNode transform -n "root";
	rename -uid "3DD954C8-48D6-2B7E-260F-4B9B65364DAF";
	addAttr -ci true -k true -sn "bendUpp" -ln "bendUpp" -at "double";
	addAttr -ci true -k true -sn "bendLow" -ln "bendLow" -at "double";
	addAttr -ci true -k true -sn "bendSide" -ln "bendSide" -at "double";
	setAttr -k on ".bendUpp";
	setAttr -k on ".bendLow";
	setAttr -k on ".bendSide";
createNode transform -n "Surface" -p "root";
	rename -uid "6FD3613C-415F-9697-8CFF-2DAE73507ABD";
	setAttr ".r" -type "double3" 0 -90 0 ;
createNode nurbsSurface -n "SurfaceShape" -p "Surface";
	rename -uid "0E994ED0-41B1-1CD3-6C81-BCBB2BC1B0FC";
	setAttr -k off ".v";
	setAttr -s 8 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode nurbsSurface -n "SurfaceShape1Orig" -p "Surface";
	rename -uid "F8A1874F-48BA-EAC9-C74A-478C1ADDCC40";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
createNode transform -n "SideBendHandle" -p "root";
	rename -uid "D71E7852-45EA-51CC-1820-BAA1B4AD951A";
	setAttr ".r" -type "double3" 90 90 0 ;
	setAttr ".s" -type "double3" 0.5 0.5 0.5 ;
	setAttr ".smd" 7;
createNode deformBend -n "SideBendHandleShape" -p "SideBendHandle";
	rename -uid "98E706C9-4D8F-D5EF-5E3C-DC874086E53A";
	setAttr -k off ".v";
	setAttr ".dd" -type "doubleArray" 3 -1 1 0 ;
	setAttr ".hw" 0.55;
createNode transform -n "UppBendHandle" -p "root";
	rename -uid "E34B6AD7-4148-0575-5AAE-BCAAD8A5FB41";
	setAttr ".r" -type "double3" 180 90 0 ;
	setAttr ".s" -type "double3" 0.5 0.5 0.5 ;
	setAttr ".smd" 7;
createNode deformBend -n "UppBendHandleShape" -p "UppBendHandle";
	rename -uid "5152226A-4491-1556-ABBF-1DA55716D78F";
	setAttr -k off ".v";
	setAttr ".dd" -type "doubleArray" 3 -1 0 0 ;
	setAttr ".hw" 0.55;
createNode transform -n "LowBendHandle" -p "root";
	rename -uid "DBBBA2E2-4638-7AE1-AC7E-9D9751467B4C";
	setAttr ".r" -type "double3" 180 90 0 ;
	setAttr ".s" -type "double3" 0.5 0.5 0.5 ;
	setAttr ".smd" 7;
createNode deformBend -n "LowBendHandleShape" -p "LowBendHandle";
	rename -uid "1C685FBD-4F20-12BD-584A-C4BC03AA5678";
	setAttr -k off ".v";
	setAttr ".dd" -type "doubleArray" 3 0 1 0 ;
	setAttr ".hw" 0.55;
createNode nonLinear -n "Surface_LowBend";
	rename -uid "7AFA5774-43C1-5BDF-BE93-D48874CF69A8";
	addAttr -is true -ci true -k true -sn "cur" -ln "curvature" -smn -3.14159 -smx 
		3.14159 -at "doubleAngle";
	addAttr -is true -ci true -k true -sn "lb" -ln "lowBound" -dv -1 -max 0 -smn -10 
		-smx 0 -at "double";
	addAttr -is true -ci true -k true -sn "hb" -ln "highBound" -dv 1 -min 0 -smn 0 -smx 
		10 -at "double";
	setAttr -k on ".cur";
	setAttr -k on ".lb" 0;
	setAttr -k on ".hb";
createNode unitConversion -n "unitConversion3";
	rename -uid "092DDFC5-4F56-360A-96C4-D4AB67BCB098";
	setAttr ".cf" 0.017453292519943295;
createNode tweak -n "tweak1";
	rename -uid "D870AD1F-49EB-1F0B-FF5C-1A947EFB2F2A";
createNode nonLinear -n "Surface_SideBend";
	rename -uid "3B0D3249-4637-C794-EF1F-2FA32AD023CC";
	addAttr -is true -ci true -k true -sn "cur" -ln "curvature" -smn -3.14159 -smx 
		3.14159 -at "doubleAngle";
	addAttr -is true -ci true -k true -sn "lb" -ln "lowBound" -dv -1 -max 0 -smn -10 
		-smx 0 -at "double";
	addAttr -is true -ci true -k true -sn "hb" -ln "highBound" -dv 1 -min 0 -smn 0 -smx 
		10 -at "double";
	setAttr -k on ".cur";
	setAttr -k on ".lb";
	setAttr -k on ".hb";
createNode unitConversion -n "unitConversion1";
	rename -uid "52F9A617-451C-533D-5D48-FD9CA8B461D0";
	setAttr ".cf" 0.017453292519943295;
createNode nonLinear -n "Surface_UppBend";
	rename -uid "3AFEAE57-4743-2638-DDA7-2B9B9A20F7F4";
	addAttr -is true -ci true -k true -sn "cur" -ln "curvature" -smn -3.14159 -smx 
		3.14159 -at "doubleAngle";
	addAttr -is true -ci true -k true -sn "lb" -ln "lowBound" -dv -1 -max 0 -smn -10 
		-smx 0 -at "double";
	addAttr -is true -ci true -k true -sn "hb" -ln "highBound" -dv 1 -min 0 -smn 0 -smx 
		10 -at "double";
	setAttr -k on ".cur";
	setAttr -k on ".lb";
	setAttr -k on ".hb" 0;
createNode unitConversion -n "unitConversion2";
	rename -uid "AA130113-4EC5-6E11-9EFA-6F99BE2DE9C0";
	setAttr ".cf" 0.017453292519943295;
createNode objectSet -n "tweakSet1";
	rename -uid "AF390CA3-4650-9521-F84B-9E9F44CBFCDA";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode objectSet -n "bend1Set";
	rename -uid "A4352057-4646-D66A-7AD4-B587AEB5B7E1";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode objectSet -n "bend3Set";
	rename -uid "1AEEDFFB-4893-5E8D-BFE9-0095AB115211";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode objectSet -n "bend2Set";
	rename -uid "936304C4-4BAC-4BEC-AE3E-78A8D69DC2B1";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode makeNurbPlane -n "makeNurbPlane1";
	rename -uid "1E1A2258-4670-E99C-A84C-7A88E9A445FB";
	setAttr ".u" 4;
	setAttr ".v" 4;
createNode groupParts -n "bend3GroupParts";
	rename -uid "0CD003DB-4FD2-93DE-C9C1-B084C477DD90";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode groupId -n "bend3GroupId";
	rename -uid "0E39F352-4970-5B5B-BC3E-BBB4907670CF";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	rename -uid "B717AA93-435D-996A-C8B6-5F95B0604123";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode groupId -n "groupId2";
	rename -uid "CB87DAC2-4FDD-1B5D-2CF8-FD89D45CE9FA";
	setAttr ".ihi" 0;
createNode groupId -n "bend1GroupId";
	rename -uid "FEEBB54F-401F-2532-CED0-BC9DD7F1DCC5";
	setAttr ".ihi" 0;
createNode groupId -n "bend2GroupId";
	rename -uid "39675208-4594-FCB6-AEF7-F185325E8D98";
	setAttr ".ihi" 0;
createNode groupParts -n "bend1GroupParts";
	rename -uid "9651A4B2-4F15-A648-21C3-D6BEFDC550A1";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode groupParts -n "bend2GroupParts";
	rename -uid "F822284D-49FC-E5DF-6B6C-84AF87E78D5C";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
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
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "bend1GroupId.id" "SurfaceShape.iog.og[0].gid";
connectAttr "bend1Set.mwc" "SurfaceShape.iog.og[0].gco";
connectAttr "groupId2.id" "SurfaceShape.iog.og[1].gid";
connectAttr "tweakSet1.mwc" "SurfaceShape.iog.og[1].gco";
connectAttr "bend2GroupId.id" "SurfaceShape.iog.og[2].gid";
connectAttr "bend2Set.mwc" "SurfaceShape.iog.og[2].gco";
connectAttr "bend3GroupId.id" "SurfaceShape.iog.og[3].gid";
connectAttr "bend3Set.mwc" "SurfaceShape.iog.og[3].gco";
connectAttr "Surface_LowBend.og[0]" "SurfaceShape.cr";
connectAttr "tweak1.pl[0].cp[0]" "SurfaceShape.twl";
connectAttr "makeNurbPlane1.os" "SurfaceShape1Orig.cr";
connectAttr "Surface_SideBend.msg" "SideBendHandle.sml";
connectAttr "Surface_SideBend.cur" "SideBendHandleShape.cur";
connectAttr "Surface_SideBend.lb" "SideBendHandleShape.lb";
connectAttr "Surface_SideBend.hb" "SideBendHandleShape.hb";
connectAttr "Surface_UppBend.msg" "UppBendHandle.sml";
connectAttr "Surface_UppBend.cur" "UppBendHandleShape.cur";
connectAttr "Surface_UppBend.lb" "UppBendHandleShape.lb";
connectAttr "Surface_UppBend.hb" "UppBendHandleShape.hb";
connectAttr "Surface_LowBend.msg" "LowBendHandle.sml";
connectAttr "Surface_LowBend.cur" "LowBendHandleShape.cur";
connectAttr "Surface_LowBend.lb" "LowBendHandleShape.lb";
connectAttr "Surface_LowBend.hb" "LowBendHandleShape.hb";
connectAttr "bend3GroupParts.og" "Surface_LowBend.ip[0].ig";
connectAttr "bend3GroupId.id" "Surface_LowBend.ip[0].gi";
connectAttr "unitConversion3.o" "Surface_LowBend.cur";
connectAttr "LowBendHandleShape.dd" "Surface_LowBend.dd";
connectAttr "LowBendHandle.wm" "Surface_LowBend.ma";
connectAttr "root.bendLow" "unitConversion3.i";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "bend1GroupParts.og" "Surface_SideBend.ip[0].ig";
connectAttr "bend1GroupId.id" "Surface_SideBend.ip[0].gi";
connectAttr "unitConversion1.o" "Surface_SideBend.cur";
connectAttr "SideBendHandleShape.dd" "Surface_SideBend.dd";
connectAttr "SideBendHandle.wm" "Surface_SideBend.ma";
connectAttr "root.bendSide" "unitConversion1.i";
connectAttr "bend2GroupParts.og" "Surface_UppBend.ip[0].ig";
connectAttr "bend2GroupId.id" "Surface_UppBend.ip[0].gi";
connectAttr "unitConversion2.o" "Surface_UppBend.cur";
connectAttr "UppBendHandleShape.dd" "Surface_UppBend.dd";
connectAttr "UppBendHandle.wm" "Surface_UppBend.ma";
connectAttr "root.bendUpp" "unitConversion2.i";
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "SurfaceShape.iog.og[1]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "bend1GroupId.msg" "bend1Set.gn" -na;
connectAttr "SurfaceShape.iog.og[0]" "bend1Set.dsm" -na;
connectAttr "Surface_SideBend.msg" "bend1Set.ub[0]";
connectAttr "bend3GroupId.msg" "bend3Set.gn" -na;
connectAttr "SurfaceShape.iog.og[3]" "bend3Set.dsm" -na;
connectAttr "Surface_LowBend.msg" "bend3Set.ub[0]";
connectAttr "bend2GroupId.msg" "bend2Set.gn" -na;
connectAttr "SurfaceShape.iog.og[2]" "bend2Set.dsm" -na;
connectAttr "Surface_UppBend.msg" "bend2Set.ub[0]";
connectAttr "Surface_UppBend.og[0]" "bend3GroupParts.ig";
connectAttr "bend3GroupId.id" "bend3GroupParts.gi";
connectAttr "SurfaceShape1Orig.ws" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "tweak1.og[0]" "bend1GroupParts.ig";
connectAttr "bend1GroupId.id" "bend1GroupParts.gi";
connectAttr "Surface_SideBend.og[0]" "bend2GroupParts.ig";
connectAttr "bend2GroupId.id" "bend2GroupParts.gi";
connectAttr "SurfaceShape.iog" ":initialShadingGroup.dsm" -na;
// End of omtk.AvarInflSurfaceTemplate.ma
