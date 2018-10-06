//Maya ASCII 2017ff05 scene
//Name: CtrlC-0.0.0.ma
//Last modified: Wed, May 23, 2018 08:29:53 PM
//Codeset: UTF-8
requires maya "2017ff05";
requires -nodeType "decomposeMatrix" -nodeType "composeMatrix" "matrixNodes" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201710312130-1018716";
fileInfo "osv" "Linux 4.13.0-41-generic #46-Ubuntu SMP Wed May 2 13:38:30 UTC 2018 x86_64";
fileInfo "license" "student";
fileInfo "omtk.component.author" "author";
fileInfo "omtk.component.version" "0.0.0";
fileInfo "omtk.component.uid" "7fc6ed36-4217-4741-8c80-fbc582f1378f";
fileInfo "omtk.component.name" "CtrlC";
createNode transform -n "ctrl";
	rename -uid "94181980-0000-3782-5B06-048100000288";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 268.08075 105.27011 ;
createNode nurbsCurve -n "ctrlShape" -p "ctrl";
	rename -uid "94181980-0000-3782-5B06-048100000287";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8
		 9 10
		11
		0.78361162489122504 4.7982373409884682e-17 -0.78361162489122382
		-1.2643170607829326e-16 6.7857323231109134e-17 -1.1081941875543879
		-0.78361162489122427 4.7982373409884713e-17 -0.78361162489122427
		-1.1081941875543879 1.9663354616187859e-32 -3.2112695072372299e-16
		-0.78361162489122449 -4.7982373409884694e-17 0.78361162489122405
		-3.3392053635905195e-16 -6.7857323231109146e-17 1.1081941875543881
		0.78361162489122382 -4.7982373409884719e-17 0.78361162489122438
		1.1081941875543879 -3.6446300679047921e-32 5.9521325992805852e-16
		0.78361162489122504 4.7982373409884682e-17 -0.78361162489122382
		-1.2643170607829326e-16 6.7857323231109134e-17 -1.1081941875543879
		-0.78361162489122427 4.7982373409884713e-17 -0.78361162489122427
		;
	setAttr "._graphpos" -type "float2" -170.50365 232.30508 ;
createNode nurbsCurve -n "ctrlShape1" -p "ctrl";
	rename -uid "94181980-0000-3782-5B06-049C0000028A";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8
		 9 10
		11
		0.78361162489122504 0.78361162489122382 -1.2601436025374895e-16
		-1.2643170607829326e-16 1.1081941875543879 -1.7821121732462098e-16
		-0.78361162489122427 0.78361162489122427 -1.26014360253749e-16
		-1.1081941875543879 3.2112695072372299e-16 -5.1641152288041213e-32
		-0.78361162489122449 -0.78361162489122405 1.2601436025374897e-16
		-3.3392053635905195e-16 -1.1081941875543881 1.78211217324621e-16
		0.78361162489122382 -0.78361162489122438 1.2601436025374902e-16
		1.1081941875543879 -5.9521325992805852e-16 9.5717592467817795e-32
		0.78361162489122504 0.78361162489122382 -1.2601436025374895e-16
		-1.2643170607829326e-16 1.1081941875543879 -1.7821121732462098e-16
		-0.78361162489122427 0.78361162489122427 -1.26014360253749e-16
		;
	setAttr "._graphpos" -type "float2" -449.30042 77.97776 ;
createNode nurbsCurve -n "ctrlShape2" -p "ctrl";
	rename -uid "94181980-0000-3782-5B06-049C0000028C";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8
		 9 10
		11
		4.7982373409884947e-17 0.78361162489122382 -0.78361162489122504
		-1.78211217324621e-16 1.1081941875543879 1.2643170607829329e-16
		-3.0001109391738269e-16 0.78361162489122427 0.78361162489122427
		-2.4606854055573016e-16 3.2112695072372299e-16 1.1081941875543879
		-4.7982373409884799e-17 -0.78361162489122405 0.78361162489122449
		1.7821121732462095e-16 -1.1081941875543881 3.3392053635905195e-16
		3.0001109391738264e-16 -0.78361162489122438 -0.78361162489122382
		2.4606854055573021e-16 -5.9521325992805852e-16 -1.1081941875543879
		4.7982373409884947e-17 0.78361162489122382 -0.78361162489122504
		-1.78211217324621e-16 1.1081941875543879 1.2643170607829329e-16
		-3.0001109391738269e-16 0.78361162489122427 0.78361162489122427
		;
	setAttr "._graphpos" -type "float2" -603.09149 -5.9082694 ;
createNode transform -n "offset";
	rename -uid "94181980-0000-3782-5B06-04E5000002AC";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" -861.58533 623.9668 ;
createNode decomposeMatrix -n "decomposeMatrix1";
	rename -uid "94181980-0000-3782-5B06-0502000002B5";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqw" 1;
	setAttr "._graphpos" -type "float2" -1020.3871 309.0672 ;
createNode network -n "Component4";
	rename -uid "94181980-0000-3782-5B06-077600000335";
	addAttr -ci true -sn "version" -ln "version" -nn "version" -dt "string";
	addAttr -s false -ci true -sn "grp_inn" -ln "grp_inn" -nn "grp_inn" -at "message";
	addAttr -ci true -sn "author" -ln "author" -nn "author" -dt "string";
	addAttr -s false -ci true -sn "grp_out" -ln "grp_out" -nn "grp_out" -at "message";
	addAttr -ci true -sn "namespace" -ln "namespace" -nn "namespace" -dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	setAttr ".version" -type "string" "";
	setAttr ".author" -type "string" "";
	setAttr ".namespace" -type "string" "component4";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Entity.Component";
	setAttr ".name" -type "string" "untitled";
createNode network -n "out";
	rename -uid "94181980-0000-3782-5B06-077600000333";
	addAttr -ci true -sn "outputMatrix" -ln "outputMatrix" -nn "outputMatrix" -dt "matrix";
createNode network -n "inn";
	rename -uid "94181980-0000-3782-5B06-077600000332";
	addAttr -ci true -sn "inputMatrix" -ln "inputMatrix" -nn "inputMatrix" -dt "matrix";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" -170.67819 231.42805 ;
createNode network -n "metadata";
	rename -uid "94181980-0000-3782-5B06-078000000338";
	addAttr -ci true -sn "version" -ln "version" -nn "version" -dt "string";
	addAttr -ci true -sn "author" -ln "author" -nn "author" -dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -ci true -sn "uid" -ln "uid" -nn "uid" -dt "string";
	setAttr ".version" -type "string" "0.0.0";
	setAttr ".author" -type "string" "author";
	setAttr "._class_module" -type "string" "omtk";
	setAttr ".name" -type "string" "CtrlC";
	setAttr "._class" -type "string" "ComponentDefinition";
	setAttr ".uid" -type "string" "7fc6ed36-4217-4741-8c80-fbc582f1378f";
createNode composeMatrix -n "composeMatrix1";
	rename -uid "94181980-0000-3782-5B06-07510000032A";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 538.7627 134.46826 ;
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
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "decomposeMatrix1.ot" "offset.t";
connectAttr "decomposeMatrix1.os" "offset.s";
connectAttr "decomposeMatrix1.or" "offset.r";
connectAttr "inn.inputMatrix" "decomposeMatrix1.imat";
connectAttr "inn.msg" "Component4.grp_inn";
connectAttr "out.msg" "Component4.grp_out";
connectAttr "composeMatrix1.omat" "out.outputMatrix";
connectAttr "ctrl.t" "composeMatrix1.it";
connectAttr "ctrl.s" "composeMatrix1.is";
connectAttr "ctrl.r" "composeMatrix1.ir";
// End of CtrlC-0.0.0.ma
