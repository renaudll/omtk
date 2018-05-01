//Maya ASCII 2017ff05 scene
//Name: FK3-0.0.1.ma
//Last modified: Sat, Apr 28, 2018 03:48:17 PM
//Codeset: UTF-8
requires maya "2017ff05";
requires -nodeType "decomposeMatrix" "matrixNodes" "1.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201710312130-1018716";
fileInfo "osv" "Linux 4.13.0-39-generic #44-Ubuntu SMP Thu Apr 5 14:25:01 UTC 2018 x86_64";
fileInfo "license" "student";
fileInfo "omtk.component.author" "Renaud Lessard Larouche";
fileInfo "omtk.component.version" "0.0.1";
fileInfo "omtk.component.uid" "9e3111df-b42f-5f6d-b243-bbfeb645518a";
fileInfo "omtk.component.name" "FK3";
createNode joint -n "out1";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000025A";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" 431.77759 208.20543 ;
createNode joint -n "out2" -p "out1";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000025B";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 431.60065 351.06342 ;
createNode joint -n "out3" -p "out2";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000025C";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 435.78094 539.68756 ;
createNode transform -n "dag";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000025D";
createNode transform -n "root" -p "dag";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000025E";
createNode transform -n "ctrl1_zero" -p "root";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000025F";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 410.24487 -328.61633 ;
createNode transform -n "ctrl1" -p "ctrl1_zero";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000260";
createNode nurbsCurve -n "ctrl1Shape" -p "ctrl1";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000261";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "ctrl2_zero" -p "ctrl1";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000262";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 418.25702 -179.63831 ;
createNode transform -n "arm_fk_infl_02_anm" -p "ctrl2_zero";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000263";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".rz";
createNode nurbsCurve -n "ctrl2" -p "arm_fk_infl_02_anm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000264";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "ctrl3_zero" -p "arm_fk_infl_02_anm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000265";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 410.0069 -15.191317 ;
createNode transform -n "ctrl3" -p "ctrl3_zero";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000266";
createNode nurbsCurve -n "ctrl3Shape" -p "ctrl3";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000267";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode joint -n "inn1";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000268";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".t" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 90 -45 -90 ;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" -572.00122 -41.937538 ;
createNode joint -n "inn2" -p "inn1";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000269";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".t" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr -av ".tx";
	setAttr -av ".ty";
	setAttr -av ".tz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" -562.41504 47.607861 ;
createNode joint -n "inn3" -p "inn2";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000026A";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".t" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" -560.02527 145.99234 ;
createNode transform -s -n "persp";
	rename -uid "32E12980-0000-718A-5AE4-CFF90000037F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 28 21 28 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "32E12980-0000-718A-5AE4-CFF900000380";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "32E12980-0000-718A-5AE4-CFF900000381";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "32E12980-0000-718A-5AE4-CFF900000382";
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
	rename -uid "32E12980-0000-718A-5AE4-CFF900000383";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "32E12980-0000-718A-5AE4-CFF900000384";
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
	rename -uid "32E12980-0000-718A-5AE4-CFF900000385";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "32E12980-0000-718A-5AE4-CFF900000386";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode addDoubleLinear -n "getLimbLength";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000285";
createNode multiplyDivide -n "multiplyDivide10";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000275";
	setAttr ".i2" -type "float3" 3.5355339 0 3.9252311e-16 ;
createNode multiplyDivide -n "multiplyDivide14";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000287";
createNode animCurveTL -n "guide_02_translateX";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000288";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.535533905932736 10 6.3911650194459524;
createNode animCurveTU -n "guide_02_scaleZ";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000291";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode animCurveTA -n "guide_02_rotateZ";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000028E";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode multiplyDivide -n "multiplyDivide13";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000286";
createNode distanceBetween -n "getLimbSegment2Length";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000284";
createNode multiplyDivide -n "multiplyDivide9";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000274";
	setAttr ".i1" -type "float3" 7.0710678 0 0 ;
createNode network -n "Component";
	rename -uid "32E12980-0000-718A-5AE4-CEAE000002A5";
	addAttr -ci true -sn "uid" -ln "uid" -nn "uid" -dt "string";
	addAttr -s false -ci true -sn "grp_inn" -ln "grp_inn" -nn "grp_inn" -at "message";
	addAttr -ci true -sn "author" -ln "author" -nn "author" -dt "string";
	addAttr -s false -ci true -sn "grp_out" -ln "grp_out" -nn "grp_out" -at "message";
	addAttr -ci true -sn "namespace" -ln "namespace" -nn "namespace" -dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "version" -ln "version" -nn "version" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	setAttr ".uid" -type "string" "9e3111df-b42f-5f6d-b243-bbfeb645518a";
	setAttr ".author" -type "string" "Renaud Lessard Larouche";
	setAttr ".namespace" -type "string" "FK3";
	setAttr "._class_module" -type "string" "omtk";
	setAttr ".version" -type "string" "0.0.1";
	setAttr "._class" -type "string" "Entity.Component";
	setAttr ".name" -type "string" "FK3";
createNode multMatrix -n "getGuide03WorldTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000292";
	setAttr -s 2 ".i";
createNode makeNurbCircle -n "makeNurbCircle3";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000277";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 0.72360073488113941;
createNode decomposeMatrix -n "decomposeCtrlFk02DefaultLocalTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000281";
	setAttr ".imat" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 3.535533905932736 0 3.9252311467094363e-16 1;
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
createNode network -n "out";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000027F";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	addAttr -ci true -sn "CtrlFk01_BaseLocalTm" -ln "CtrlFk01_BaseLocalTm" -dt "matrix";
	addAttr -ci true -sn "CtrlFk02_BaseLocalTm" -ln "CtrlFk02_BaseLocalTm" -dt "matrix";
	addAttr -ci true -sn "CtrlFk03_BaseLocalTm" -ln "CtrlFk03_BaseLocalTm" -dt "matrix";
	addAttr -ci true -sn "outCtrlIkBaseWorldTm" -ln "outCtrlIkBaseWorldTm" -dt "matrix";
	addAttr -ci true -sn "outCtrlIkSwivelBaseWorldTm" -ln "outCtrlIkSwivelBaseWorldTm" 
		-dt "matrix";
	addAttr -ci true -sn "outInf01LocalTm" -ln "outInf01LocalTm" -dt "matrix";
	addAttr -ci true -sn "outInf02LocalTm" -ln "outInf02LocalTm" -dt "matrix";
	addAttr -ci true -sn "outInf03LocalTm" -ln "outInf03LocalTm" -dt "matrix";
	setAttr "._graphpos" -type "float2" 1 -1 ;
	setAttr ".outInf01LocalTm" -type "matrix" 0 -0.70710678118654757 0.70710678118654757 0 1.1102230246251568e-16 0.70710678118654746 0.70710678118654757 0
		 -1.0000000000000002 0 1.1102230246251565e-16 0 4.9303806576313249e-32 5 -5.4738221262688167e-48 1;
	setAttr ".outInf02LocalTm" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 3.535533905932736 0 3.9252311467094363e-16 1;
	setAttr ".outInf03LocalTm" -type "matrix" -2.2204460492503131e-16 1 0 0 -1 -2.2204460492503131e-16 0 0
		 0 0 1 0 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 1;
createNode animCurveTL -n "guide_02_translateY";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000289";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 1.8998827256160656e-16;
createNode vectorProduct -n "getKneeDirectionNormalized";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000029C";
	setAttr ".op" 0;
	setAttr ".no" yes;
createNode decomposeMatrix -n "decomposeMatrix3";
	rename -uid "32E12980-0000-718A-5AE4-CE3B000002A1";
	setAttr ".imat" -type "matrix" -2.2204460492503131e-16 1 0 0 -1 -2.2204460492503131e-16 0 0
		 0 0 1 0 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 1;
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
createNode plusMinusAverage -n "getSwivelDefaultPos";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000029E";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode distanceBetween -n "getLimbSegment1Length";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000283";
createNode multiplyDivide -n "getLimbMiddleAim";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000297";
createNode decomposeMatrix -n "decomposeMatrix1";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000029F";
	setAttr ".imat" -type "matrix" 0 -0.70710678118654757 0.70710678118654757 0 1.1102230246251568e-16 0.70710678118654746 0.70710678118654757 0
		 -1.0000000000000002 0 1.1102230246251565e-16 0 4.9303806576313249e-32 5 -5.4738221262688167e-48 1;
	setAttr ".ot" -type "double3" 4.9303806576313249e-32 5 -5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
createNode decomposeMatrix -n "decomposeMatrix2";
	rename -uid "32E12980-0000-718A-5AE4-CE3B000002A0";
	setAttr ".imat" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 3.535533905932736 0 3.9252311467094363e-16 1;
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
createNode decomposeMatrix -n "decomposeGuide03WorldTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000293";
	setAttr ".ot" -type "double3" -5.8878467200641577e-16 8.8817841970012523e-16 -1.3322676295501878e-15 ;
	setAttr ".or" -type "double3" 90 -45.000000000000028 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818829;
	setAttr ".oqz" -0.27059805007309845;
	setAttr ".oqw" 0.65328148243818829;
createNode plusMinusAverage -n "getLimbAim";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000296";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode animCurveTL -n "guide_02_translateZ";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000028A";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.9252311467094363e-16 10 7.5484373465108625e-17;
createNode multiplyDivide -n "getLimbRatio";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000295";
	setAttr ".op" 2;
createNode animCurveTU -n "guide_02_visibility";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000028B";
	setAttr ".tan" 9;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
createNode decomposeMatrix -n "decomposeCtrlFk01DefaultLocalTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000280";
	setAttr ".imat" -type "matrix" 0 -0.70710678118654757 0.70710678118654757 0 1.1102230246251568e-16 0.70710678118654746 0.70710678118654757 0
		 -1.0000000000000002 0 1.1102230246251565e-16 0 -4.9303806576313249e-32 5 5.4738221262688167e-48 1;
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
createNode animCurveTA -n "guide_02_rotateY";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000028D";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode decomposeMatrix -n "decomposeGuide02WorldTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000029B";
	setAttr ".ot" -type "double3" -3.9252311467094378e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".or" -type "double3" 90 45 -90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.65328148243818818;
	setAttr ".oqy" -0.27059805007309845;
	setAttr ".oqz" -0.65328148243818829;
	setAttr ".oqw" 0.27059805007309851;
createNode multiplyDivide -n "multiplyDivide1";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000273";
	setAttr ".i2" -type "float3" 0.0099999998 1 1 ;
createNode plusMinusAverage -n "getKneeDirection";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000299";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000271";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n"
		+ "            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n"
		+ "            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n"
		+ "            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n"
		+ "            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n"
		+ "            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n"
		+ "            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1165\n            -height 696\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n"
		+ "            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n"
		+ "            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n"
		+ "            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n"
		+ "            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n"
		+ "                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n"
		+ "                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n"
		+ "                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n"
		+ "                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n"
		+ "                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n"
		+ "                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n"
		+ "                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n"
		+ "                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n"
		+ "                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n"
		+ "                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1165\\n    -height 696\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1165\\n    -height 696\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode multMatrix -n "getGuide02WorldTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000029A";
	setAttr -s 2 ".i";
createNode animCurveTU -n "guide_02_scaleY";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000290";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "32E12980-0000-718A-5AE4-CFF90000036C";
createNode network -n "metadata1";
	rename -uid "32E12980-0000-718A-5AE4-CEAE000002A4";
	addAttr -ci true -sn "uid" -ln "uid" -nn "uid" -dt "string";
	addAttr -s false -ci true -sn "grp_inn" -ln "grp_inn" -nn "grp_inn" -at "message";
	addAttr -ci true -sn "author" -ln "author" -nn "author" -dt "string";
	addAttr -s false -ci true -sn "grp_out" -ln "grp_out" -nn "grp_out" -at "message";
	addAttr -ci true -sn "namespace" -ln "namespace" -nn "namespace" -dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "version" -ln "version" -nn "version" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	setAttr ".uid" -type "string" "9e3111df-b42f-5f6d-b243-bbfeb645518a";
	setAttr ".author" -type "string" "Renaud Lessard Larouche";
	setAttr ".namespace" -type "string" "FK3";
	setAttr "._class_module" -type "string" "omtk";
	setAttr ".version" -type "string" "0.0.1";
	setAttr "._class" -type "string" "Entity.Component";
	setAttr ".name" -type "string" "FK3";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000270";
	setAttr ".g" yes;
createNode animCurveTA -n "guide_02_rotateX";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000028C";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode network -n "inn";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000027B";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	addAttr -ci true -sn "Guide01_LocalTm" -ln "Guide01_LocalTm" -dt "matrix";
	addAttr -ci true -sn "Guide02_LocalTm" -ln "Guide02_LocalTm" -dt "matrix";
	addAttr -ci true -sn "Guide03_LocalTm" -ln "Guide03_LocalTm" -dt "matrix";
	addAttr -ci true -sn "swivelDistanceRatio" -ln "swivelDistanceRatio" -dv 0.5 -min 
		0 -max 1 -at "double";
	setAttr "._graphpos" -type "float2" -182.13298 -179.33249 ;
	setAttr ".Guide01_LocalTm" -type "matrix" 0 -0.70710678118654757 0.70710678118654757 0 1.1102230246251568e-16 0.70710678118654746 0.70710678118654757 0
		 -1.0000000000000002 0 1.1102230246251565e-16 0 -4.9303806576313249e-32 5 5.4738221262688167e-48 1;
	setAttr ".Guide02_LocalTm" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 3.535533905932736 0 3.9252311467094363e-16 1;
	setAttr ".Guide03_LocalTm" -type "matrix" -2.2204460492503131e-16 1 0 0 -1 -2.2204460492503131e-16 0 0
		 0 0 1 0 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 1;
	setAttr -k on ".swivelDistanceRatio";
createNode decomposeMatrix -n "decomposeGuide01LocalTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000027C";
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
createNode makeNurbCircle -n "makeNurbCircle2";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000276";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 1.1477089008538313;
createNode decomposeMatrix -n "decomposeCtrlFk03DefaultLocalTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000282";
	setAttr ".imat" -type "matrix" -2.2204460492503131e-16 1 0 0 -1 -2.2204460492503131e-16 0 0
		 0 0 1 0 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 1;
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000272";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode makeNurbCircle -n "makeNurbCircle4";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000278";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 0.72360073488113941;
createNode plusMinusAverage -n "getKneePosProjectedOnLimbDir";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000298";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode animCurveTU -n "guide_02_scaleX";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000028F";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode decomposeMatrix -n "decomposeGuide03LocalTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000027E";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode multiplyDivide -n "getSwivelDistance";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000294";
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "32E12980-0000-718A-5AE4-CE3B000002A2";
	setAttr ".def" no;
	setAttr -s 7 ".tgi";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -3739.9723788593819 -4397.6188728734051 ;
	setAttr ".tgi[0].vh" -type "double2" 2914.9724116419275 -2595.2379921126339 ;
	setAttr -s 33 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -2608.571533203125;
	setAttr ".tgi[0].ni[0].y" -2138.571533203125;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" -3317.874267578125;
	setAttr ".tgi[0].ni[1].y" -1844.968994140625;
	setAttr ".tgi[0].ni[1].nvs" 18312;
	setAttr ".tgi[0].ni[2].x" -1372.857177734375;
	setAttr ".tgi[0].ni[2].y" -2048.571533203125;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" -3557.593505859375;
	setAttr ".tgi[0].ni[3].y" -1010.6516723632812;
	setAttr ".tgi[0].ni[3].nvs" 1931;
	setAttr ".tgi[0].ni[4].x" -84.285713195800781;
	setAttr ".tgi[0].ni[4].y" -2127.142822265625;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 714.28570556640625;
	setAttr ".tgi[0].ni[5].y" -2797.142822265625;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" -3180.7255859375;
	setAttr ".tgi[0].ni[6].y" -1443.1690673828125;
	setAttr ".tgi[0].ni[6].nvs" 18306;
	setAttr ".tgi[0].ni[7].x" -2608.571533203125;
	setAttr ".tgi[0].ni[7].y" -1744.2857666015625;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" -1625.73779296875;
	setAttr ".tgi[0].ni[8].y" -2420.765380859375;
	setAttr ".tgi[0].ni[8].nvs" 18314;
	setAttr ".tgi[0].ni[9].x" -3317.874267578125;
	setAttr ".tgi[0].ni[9].y" -2000.0814208984375;
	setAttr ".tgi[0].ni[9].nvs" 18314;
	setAttr ".tgi[0].ni[10].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[10].y" 284.30282592773438;
	setAttr ".tgi[0].ni[10].nvs" 18314;
	setAttr ".tgi[0].ni[11].x" 344.28570556640625;
	setAttr ".tgi[0].ni[11].y" -2397.142822265625;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" -3559.94384765625;
	setAttr ".tgi[0].ni[12].y" -792.08404541015625;
	setAttr ".tgi[0].ni[12].nvs" 1931;
	setAttr ".tgi[0].ni[13].x" -2608.571533203125;
	setAttr ".tgi[0].ni[13].y" -2040;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" -2608.571533203125;
	setAttr ".tgi[0].ni[14].y" -1350;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" -4220.34716796875;
	setAttr ".tgi[0].ni[15].y" -1645.202880859375;
	setAttr ".tgi[0].ni[15].nvs" 18313;
	setAttr ".tgi[0].ni[16].x" -2282.696533203125;
	setAttr ".tgi[0].ni[16].y" -3022.0634765625;
	setAttr ".tgi[0].ni[16].nvs" 1923;
	setAttr ".tgi[0].ni[17].x" -4220.34716796875;
	setAttr ".tgi[0].ni[17].y" -1245.670654296875;
	setAttr ".tgi[0].ni[17].nvs" 18313;
	setAttr ".tgi[0].ni[18].x" -1992.3165283203125;
	setAttr ".tgi[0].ni[18].y" -2653.79296875;
	setAttr ".tgi[0].ni[18].nvs" 1923;
	setAttr ".tgi[0].ni[19].x" -3568.920654296875;
	setAttr ".tgi[0].ni[19].y" -1715.50048828125;
	setAttr ".tgi[0].ni[19].nvs" 18306;
	setAttr ".tgi[0].ni[20].x" -1684.191650390625;
	setAttr ".tgi[0].ni[20].y" -2916.984130859375;
	setAttr ".tgi[0].ni[20].nvs" 18306;
	setAttr ".tgi[0].ni[21].x" 344.28570556640625;
	setAttr ".tgi[0].ni[21].y" -2895.71435546875;
	setAttr ".tgi[0].ni[21].nvs" 18304;
	setAttr ".tgi[0].ni[22].x" -2948.89453125;
	setAttr ".tgi[0].ni[22].y" -1946.027099609375;
	setAttr ".tgi[0].ni[22].nvs" 18312;
	setAttr ".tgi[0].ni[23].x" -3910.1220703125;
	setAttr ".tgi[0].ni[23].y" -1473.6390380859375;
	setAttr ".tgi[0].ni[23].nvs" 18314;
	setAttr ".tgi[0].ni[24].x" -2608.571533203125;
	setAttr ".tgi[0].ni[24].y" -1448.5714111328125;
	setAttr ".tgi[0].ni[24].nvs" 18304;
	setAttr ".tgi[0].ni[25].x" -1342.2041015625;
	setAttr ".tgi[0].ni[25].y" -3234.176025390625;
	setAttr ".tgi[0].ni[25].nvs" 18306;
	setAttr ".tgi[0].ni[26].x" -3125.15478515625;
	setAttr ".tgi[0].ni[26].y" -2569.7314453125;
	setAttr ".tgi[0].ni[26].nvs" 18314;
	setAttr ".tgi[0].ni[27].x" 714.28570556640625;
	setAttr ".tgi[0].ni[27].y" -2895.71435546875;
	setAttr ".tgi[0].ni[27].nvs" 18304;
	setAttr ".tgi[0].ni[28].x" -2791.646240234375;
	setAttr ".tgi[0].ni[28].y" -2204.69677734375;
	setAttr ".tgi[0].ni[28].nvs" 1931;
	setAttr ".tgi[0].ni[29].x" -4222.697265625;
	setAttr ".tgi[0].ni[29].y" -1379.6314697265625;
	setAttr ".tgi[0].ni[29].nvs" 18313;
	setAttr ".tgi[0].ni[30].x" -3632.42724609375;
	setAttr ".tgi[0].ni[30].y" -1477.7398681640625;
	setAttr ".tgi[0].ni[30].nvs" 18306;
	setAttr ".tgi[0].ni[31].x" 344.28570556640625;
	setAttr ".tgi[0].ni[31].y" -1784.2857666015625;
	setAttr ".tgi[0].ni[31].nvs" 18304;
	setAttr ".tgi[0].ni[32].x" 714.28570556640625;
	setAttr ".tgi[0].ni[32].y" -1784.2857666015625;
	setAttr ".tgi[0].ni[32].nvs" 18304;
	setAttr ".tgi[1].tn" -type "string" "Untitled_2";
	setAttr ".tgi[1].vl" -type "double2" -1452.5182573004249 -682.14283003693629 ;
	setAttr ".tgi[1].vh" -type "double2" 3558.4705545697802 674.99997317791087 ;
	setAttr -s 14 ".tgi[1].ni";
	setAttr ".tgi[1].ni[0].x" 440.24679565429688;
	setAttr ".tgi[1].ni[0].y" 493.32656860351562;
	setAttr ".tgi[1].ni[0].nvs" 18313;
	setAttr ".tgi[1].ni[1].x" 128.57142639160156;
	setAttr ".tgi[1].ni[1].y" 494.28570556640625;
	setAttr ".tgi[1].ni[1].nvs" 18312;
	setAttr ".tgi[1].ni[2].x" 1775.695556640625;
	setAttr ".tgi[1].ni[2].y" 414.17254638671875;
	setAttr ".tgi[1].ni[2].nvs" 18306;
	setAttr ".tgi[1].ni[3].x" 2377.003662109375;
	setAttr ".tgi[1].ni[3].y" -456.60031127929688;
	setAttr ".tgi[1].ni[3].nvs" 18314;
	setAttr ".tgi[1].ni[4].x" 1171.720703125;
	setAttr ".tgi[1].ni[4].y" -470.35821533203125;
	setAttr ".tgi[1].ni[4].nvs" 1931;
	setAttr ".tgi[1].ni[5].x" 777.67034912109375;
	setAttr ".tgi[1].ni[5].y" 346.83428955078125;
	setAttr ".tgi[1].ni[5].nvs" 18314;
	setAttr ".tgi[1].ni[6].x" 128.57142639160156;
	setAttr ".tgi[1].ni[6].y" 592.85711669921875;
	setAttr ".tgi[1].ni[6].nvs" 18312;
	setAttr ".tgi[1].ni[7].x" 2902.684326171875;
	setAttr ".tgi[1].ni[7].y" -622.25701904296875;
	setAttr ".tgi[1].ni[7].nvs" 1931;
	setAttr ".tgi[1].ni[8].x" 1171.720703125;
	setAttr ".tgi[1].ni[8].y" -329.415283203125;
	setAttr ".tgi[1].ni[8].nvs" 1931;
	setAttr ".tgi[1].ni[9].x" 128.57142639160156;
	setAttr ".tgi[1].ni[9].y" 691.4285888671875;
	setAttr ".tgi[1].ni[9].nvs" 18312;
	setAttr ".tgi[1].ni[10].x" 2906.5791015625;
	setAttr ".tgi[1].ni[10].y" -384.2847900390625;
	setAttr ".tgi[1].ni[10].nvs" 1931;
	setAttr ".tgi[1].ni[11].x" 2605.094970703125;
	setAttr ".tgi[1].ni[11].y" -352.89810180664062;
	setAttr ".tgi[1].ni[11].nvs" 1931;
	setAttr ".tgi[1].ni[12].x" 5058.5712890625;
	setAttr ".tgi[1].ni[12].y" -765.71429443359375;
	setAttr ".tgi[1].ni[12].nvs" 18304;
	setAttr ".tgi[1].ni[13].x" 1794.710205078125;
	setAttr ".tgi[1].ni[13].y" 692.2615966796875;
	setAttr ".tgi[1].ni[13].nvs" 18306;
	setAttr ".tgi[2].tn" -type "string" "Untitled_3";
	setAttr ".tgi[2].vl" -type "double2" -8842.49049112184 814.28568192890828 ;
	setAttr ".tgi[2].vh" -type "double2" -5119.4137159866959 1822.6189751946765 ;
	setAttr -s 2 ".tgi[2].ni";
	setAttr ".tgi[2].ni[0].x" -2984.28564453125;
	setAttr ".tgi[2].ni[0].y" 1490;
	setAttr ".tgi[2].ni[0].nvs" 18304;
	setAttr ".tgi[2].ni[1].x" -7416.857421875;
	setAttr ".tgi[2].ni[1].y" 1527.61865234375;
	setAttr ".tgi[2].ni[1].nvs" 18305;
	setAttr ".tgi[3].tn" -type "string" "Untitled_4";
	setAttr ".tgi[3].vl" -type "double2" -5797.7561798742599 -773.8094930610971 ;
	setAttr ".tgi[3].vh" -type "double2" -1701.0530459593201 335.71427237419903 ;
	setAttr -s 9 ".tgi[3].ni";
	setAttr ".tgi[3].ni[0].x" -5244.28564453125;
	setAttr ".tgi[3].ni[0].y" -364.28570556640625;
	setAttr ".tgi[3].ni[0].nvs" 18304;
	setAttr ".tgi[3].ni[1].x" -4630;
	setAttr ".tgi[3].ni[1].y" -364.28570556640625;
	setAttr ".tgi[3].ni[1].nvs" 18304;
	setAttr ".tgi[3].ni[2].x" -4008.571533203125;
	setAttr ".tgi[3].ni[2].y" -58.571430206298828;
	setAttr ".tgi[3].ni[2].nvs" 18304;
	setAttr ".tgi[3].ni[3].x" -5244.28564453125;
	setAttr ".tgi[3].ni[3].y" -265.71429443359375;
	setAttr ".tgi[3].ni[3].nvs" 18304;
	setAttr ".tgi[3].ni[4].x" -4008.571533203125;
	setAttr ".tgi[3].ni[4].y" -274.28570556640625;
	setAttr ".tgi[3].ni[4].nvs" 18304;
	setAttr ".tgi[3].ni[5].x" -4315.71435546875;
	setAttr ".tgi[3].ni[5].y" -232.85714721679688;
	setAttr ".tgi[3].ni[5].nvs" 18304;
	setAttr ".tgi[3].ni[6].x" -4630;
	setAttr ".tgi[3].ni[6].y" -167.14285278320312;
	setAttr ".tgi[3].ni[6].nvs" 18304;
	setAttr ".tgi[3].ni[7].x" -4315.71435546875;
	setAttr ".tgi[3].ni[7].y" -331.42855834960938;
	setAttr ".tgi[3].ni[7].nvs" 18304;
	setAttr ".tgi[3].ni[8].x" -4937.14306640625;
	setAttr ".tgi[3].ni[8].y" -265.71429443359375;
	setAttr ".tgi[3].ni[8].nvs" 18304;
	setAttr ".tgi[4].tn" -type "string" "Untitled_5";
	setAttr ".tgi[4].vl" -type "double2" -10739.560012808668 -1855.9523072034626 ;
	setAttr ".tgi[4].vh" -type "double2" -6717.5821506496868 -766.6666362020718 ;
	setAttr -s 20 ".tgi[4].ni";
	setAttr ".tgi[4].ni[0].x" -10155.7138671875;
	setAttr ".tgi[4].ni[0].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[0].nvs" 18304;
	setAttr ".tgi[4].ni[1].x" -9848.5712890625;
	setAttr ".tgi[4].ni[1].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[1].nvs" 18304;
	setAttr ".tgi[4].ni[2].x" -9848.5712890625;
	setAttr ".tgi[4].ni[2].y" -912.85711669921875;
	setAttr ".tgi[4].ni[2].nvs" 18304;
	setAttr ".tgi[4].ni[3].x" -2717.142822265625;
	setAttr ".tgi[4].ni[3].y" -1185.7142333984375;
	setAttr ".tgi[4].ni[3].nvs" 18304;
	setAttr ".tgi[4].ni[4].x" -10155.7138671875;
	setAttr ".tgi[4].ni[4].y" -1110;
	setAttr ".tgi[4].ni[4].nvs" 18304;
	setAttr ".tgi[4].ni[5].x" -9848.5712890625;
	setAttr ".tgi[4].ni[5].y" -1110;
	setAttr ".tgi[4].ni[5].nvs" 18304;
	setAttr ".tgi[4].ni[6].x" -4005.71435546875;
	setAttr ".tgi[4].ni[6].y" -1008.5714111328125;
	setAttr ".tgi[4].ni[6].nvs" 18304;
	setAttr ".tgi[4].ni[7].x" -10155.7138671875;
	setAttr ".tgi[4].ni[7].y" -1405.7142333984375;
	setAttr ".tgi[4].ni[7].nvs" 18304;
	setAttr ".tgi[4].ni[8].x" -1692.857177734375;
	setAttr ".tgi[4].ni[8].y" -762.85711669921875;
	setAttr ".tgi[4].ni[8].nvs" 18304;
	setAttr ".tgi[4].ni[9].x" -10155.7138671875;
	setAttr ".tgi[4].ni[9].y" -912.85711669921875;
	setAttr ".tgi[4].ni[9].nvs" 18304;
	setAttr ".tgi[4].ni[10].x" -8945.8779296875;
	setAttr ".tgi[4].ni[10].y" -1389.3060302734375;
	setAttr ".tgi[4].ni[10].nvs" 18306;
	setAttr ".tgi[4].ni[11].x" -8920;
	setAttr ".tgi[4].ni[11].y" -1061.4285888671875;
	setAttr ".tgi[4].ni[11].nvs" 18304;
	setAttr ".tgi[4].ni[12].x" -9542.23828125;
	setAttr ".tgi[4].ni[12].y" -1033.5311279296875;
	setAttr ".tgi[4].ni[12].nvs" 18306;
	setAttr ".tgi[4].ni[13].x" -10155.7138671875;
	setAttr ".tgi[4].ni[13].y" -1307.142822265625;
	setAttr ".tgi[4].ni[13].nvs" 18304;
	setAttr ".tgi[4].ni[14].x" -957.14288330078125;
	setAttr ".tgi[4].ni[14].y" -465.71429443359375;
	setAttr ".tgi[4].ni[14].nvs" 18304;
	setAttr ".tgi[4].ni[15].x" -10155.7138671875;
	setAttr ".tgi[4].ni[15].y" -1208.5714111328125;
	setAttr ".tgi[4].ni[15].nvs" 18304;
	setAttr ".tgi[4].ni[16].x" -10155.7138671875;
	setAttr ".tgi[4].ni[16].y" -617.14288330078125;
	setAttr ".tgi[4].ni[16].nvs" 18304;
	setAttr ".tgi[4].ni[17].x" -957.14288330078125;
	setAttr ".tgi[4].ni[17].y" -564.28570556640625;
	setAttr ".tgi[4].ni[17].nvs" 18304;
	setAttr ".tgi[4].ni[18].x" -1692.857177734375;
	setAttr ".tgi[4].ni[18].y" -1017.1428833007812;
	setAttr ".tgi[4].ni[18].nvs" 18304;
	setAttr ".tgi[4].ni[19].x" -8614.15234375;
	setAttr ".tgi[4].ni[19].y" -1219.30224609375;
	setAttr ".tgi[4].ni[19].nvs" 18306;
	setAttr ".tgi[5].tn" -type "string" "Untitled_6";
	setAttr ".tgi[5].vl" -type "double2" -3649.2214667145759 -3032.1427366563157 ;
	setAttr ".tgi[5].vh" -type "double2" 2755.1738831932234 -1297.618996056287 ;
	setAttr -s 33 ".tgi[5].ni";
	setAttr ".tgi[5].ni[0].x" -1096.7374267578125;
	setAttr ".tgi[5].ni[0].y" -2203.770263671875;
	setAttr ".tgi[5].ni[0].nvs" 18306;
	setAttr ".tgi[5].ni[1].x" -3545.71435546875;
	setAttr ".tgi[5].ni[1].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[1].nvs" 18304;
	setAttr ".tgi[5].ni[2].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[2].y" -1814.2857666015625;
	setAttr ".tgi[5].ni[2].nvs" 1923;
	setAttr ".tgi[5].ni[3].x" -3545.71435546875;
	setAttr ".tgi[5].ni[3].y" -1000;
	setAttr ".tgi[5].ni[3].nvs" 18304;
	setAttr ".tgi[5].ni[4].x" -3238.571533203125;
	setAttr ".tgi[5].ni[4].y" -1000;
	setAttr ".tgi[5].ni[4].nvs" 18304;
	setAttr ".tgi[5].ni[5].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[5].y" -1388.5714111328125;
	setAttr ".tgi[5].ni[5].nvs" 18304;
	setAttr ".tgi[5].ni[6].x" -3545.71435546875;
	setAttr ".tgi[5].ni[6].y" -901.4285888671875;
	setAttr ".tgi[5].ni[6].nvs" 18304;
	setAttr ".tgi[5].ni[7].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[7].y" -1715.7142333984375;
	setAttr ".tgi[5].ni[7].nvs" 18304;
	setAttr ".tgi[5].ni[8].x" -3238.571533203125;
	setAttr ".tgi[5].ni[8].y" -1197.142822265625;
	setAttr ".tgi[5].ni[8].nvs" 18304;
	setAttr ".tgi[5].ni[9].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[9].y" -941.4285888671875;
	setAttr ".tgi[5].ni[9].nvs" 18304;
	setAttr ".tgi[5].ni[10].x" -717.14288330078125;
	setAttr ".tgi[5].ni[10].y" -1872.857177734375;
	setAttr ".tgi[5].ni[10].nvs" 18304;
	setAttr ".tgi[5].ni[11].x" -717.14288330078125;
	setAttr ".tgi[5].ni[11].y" -1577.142822265625;
	setAttr ".tgi[5].ni[11].nvs" 18304;
	setAttr ".tgi[5].ni[12].x" -3545.71435546875;
	setAttr ".tgi[5].ni[12].y" -1394.2857666015625;
	setAttr ".tgi[5].ni[12].nvs" 18304;
	setAttr ".tgi[5].ni[13].x" -3545.71435546875;
	setAttr ".tgi[5].ni[13].y" -802.85711669921875;
	setAttr ".tgi[5].ni[13].nvs" 18304;
	setAttr ".tgi[5].ni[14].x" -1982.1771240234375;
	setAttr ".tgi[5].ni[14].y" -1443.332763671875;
	setAttr ".tgi[5].ni[14].nvs" 18306;
	setAttr ".tgi[5].ni[15].x" -717.14288330078125;
	setAttr ".tgi[5].ni[15].y" -794.28570556640625;
	setAttr ".tgi[5].ni[15].nvs" 18304;
	setAttr ".tgi[5].ni[16].x" -3545.71435546875;
	setAttr ".tgi[5].ni[16].y" -704.28570556640625;
	setAttr ".tgi[5].ni[16].nvs" 18304;
	setAttr ".tgi[5].ni[17].x" -3545.71435546875;
	setAttr ".tgi[5].ni[17].y" -1295.7142333984375;
	setAttr ".tgi[5].ni[17].nvs" 18304;
	setAttr ".tgi[5].ni[18].x" -2931.428466796875;
	setAttr ".tgi[5].ni[18].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[18].nvs" 18304;
	setAttr ".tgi[5].ni[19].x" -3545.71435546875;
	setAttr ".tgi[5].ni[19].y" -1197.142822265625;
	setAttr ".tgi[5].ni[19].nvs" 18304;
	setAttr ".tgi[5].ni[20].x" -717.14288330078125;
	setAttr ".tgi[5].ni[20].y" -1127.142822265625;
	setAttr ".tgi[5].ni[20].nvs" 18304;
	setAttr ".tgi[5].ni[21].x" -717.14288330078125;
	setAttr ".tgi[5].ni[21].y" -1225.7142333984375;
	setAttr ".tgi[5].ni[21].nvs" 18304;
	setAttr ".tgi[5].ni[22].x" -3238.571533203125;
	setAttr ".tgi[5].ni[22].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[22].nvs" 18304;
	setAttr ".tgi[5].ni[23].x" -1388.5714111328125;
	setAttr ".tgi[5].ni[23].y" -1200;
	setAttr ".tgi[5].ni[23].nvs" 18304;
	setAttr ".tgi[5].ni[24].x" -2280.754150390625;
	setAttr ".tgi[5].ni[24].y" -1337.3529052734375;
	setAttr ".tgi[5].ni[24].nvs" 18306;
	setAttr ".tgi[5].ni[25].x" -2624.28564453125;
	setAttr ".tgi[5].ni[25].y" -1058.5714111328125;
	setAttr ".tgi[5].ni[25].nvs" 18304;
	setAttr ".tgi[5].ni[26].x" -717.14288330078125;
	setAttr ".tgi[5].ni[26].y" -1028.5714111328125;
	setAttr ".tgi[5].ni[26].nvs" 18304;
	setAttr ".tgi[5].ni[27].x" -717.14288330078125;
	setAttr ".tgi[5].ni[27].y" -1774.2857666015625;
	setAttr ".tgi[5].ni[27].nvs" 18304;
	setAttr ".tgi[5].ni[28].x" -2660.843017578125;
	setAttr ".tgi[5].ni[28].y" -1198.5745849609375;
	setAttr ".tgi[5].ni[28].nvs" 18306;
	setAttr ".tgi[5].ni[29].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[29].y" -1040;
	setAttr ".tgi[5].ni[29].nvs" 18304;
	setAttr ".tgi[5].ni[30].x" -2649.8759765625;
	setAttr ".tgi[5].ni[30].y" -767.46453857421875;
	setAttr ".tgi[5].ni[30].nvs" 18306;
	setAttr ".tgi[5].ni[31].x" -2268.605224609375;
	setAttr ".tgi[5].ni[31].y" -1083.2686767578125;
	setAttr ".tgi[5].ni[31].nvs" 18306;
	setAttr ".tgi[5].ni[32].x" -3545.71435546875;
	setAttr ".tgi[5].ni[32].y" -605.71429443359375;
	setAttr ".tgi[5].ni[32].nvs" 18304;
	setAttr ".tgi[6].tn" -type "string" "Untitled_7";
	setAttr ".tgi[6].vl" -type "double2" 2208.9239667947518 -2084.9783602515836 ;
	setAttr ".tgi[6].vh" -type "double2" 6950.237362770913 -381.53478952744376 ;
	setAttr -s 49 ".tgi[6].ni";
	setAttr ".tgi[6].ni[0].x" 4582.85693359375;
	setAttr ".tgi[6].ni[0].y" -967.14288330078125;
	setAttr ".tgi[6].ni[0].nvs" 18304;
	setAttr ".tgi[6].ni[1].x" -350;
	setAttr ".tgi[6].ni[1].y" -1251.4285888671875;
	setAttr ".tgi[6].ni[1].nvs" 18304;
	setAttr ".tgi[6].ni[2].x" 5910;
	setAttr ".tgi[6].ni[2].y" -652.85711669921875;
	setAttr ".tgi[6].ni[2].nvs" 18304;
	setAttr ".tgi[6].ni[3].x" 5910;
	setAttr ".tgi[6].ni[3].y" -751.4285888671875;
	setAttr ".tgi[6].ni[3].nvs" 18304;
	setAttr ".tgi[6].ni[4].x" 5231.4287109375;
	setAttr ".tgi[6].ni[4].y" -1227.142822265625;
	setAttr ".tgi[6].ni[4].nvs" 18304;
	setAttr ".tgi[6].ni[5].x" 571.4285888671875;
	setAttr ".tgi[6].ni[5].y" -1025.7142333984375;
	setAttr ".tgi[6].ni[5].nvs" 18304;
	setAttr ".tgi[6].ni[6].x" -350;
	setAttr ".tgi[6].ni[6].y" -1350;
	setAttr ".tgi[6].ni[6].nvs" 18304;
	setAttr ".tgi[6].ni[7].x" 5910;
	setAttr ".tgi[6].ni[7].y" -962.85711669921875;
	setAttr ".tgi[6].ni[7].nvs" 18304;
	setAttr ".tgi[6].ni[8].x" -350;
	setAttr ".tgi[6].ni[8].y" -660;
	setAttr ".tgi[6].ni[8].nvs" 18304;
	setAttr ".tgi[6].ni[9].x" 5545.71435546875;
	setAttr ".tgi[6].ni[9].y" -721.4285888671875;
	setAttr ".tgi[6].ni[9].nvs" 18304;
	setAttr ".tgi[6].ni[10].x" 4275.71435546875;
	setAttr ".tgi[6].ni[10].y" -975.71429443359375;
	setAttr ".tgi[6].ni[10].nvs" 18304;
	setAttr ".tgi[6].ni[11].x" 3342.857177734375;
	setAttr ".tgi[6].ni[11].y" -920;
	setAttr ".tgi[6].ni[11].nvs" 18304;
	setAttr ".tgi[6].ni[12].x" 5910;
	setAttr ".tgi[6].ni[12].y" -1170;
	setAttr ".tgi[6].ni[12].nvs" 18304;
	setAttr ".tgi[6].ni[13].x" -42.857143402099609;
	setAttr ".tgi[6].ni[13].y" -1054.2857666015625;
	setAttr ".tgi[6].ni[13].nvs" 18304;
	setAttr ".tgi[6].ni[14].x" 5231.4287109375;
	setAttr ".tgi[6].ni[14].y" -967.14288330078125;
	setAttr ".tgi[6].ni[14].nvs" 18304;
	setAttr ".tgi[6].ni[15].x" 4580.99365234375;
	setAttr ".tgi[6].ni[15].y" -1048.225341796875;
	setAttr ".tgi[6].ni[15].nvs" 18306;
	setAttr ".tgi[6].ni[16].x" 3650;
	setAttr ".tgi[6].ni[16].y" -841.4285888671875;
	setAttr ".tgi[6].ni[16].nvs" 18304;
	setAttr ".tgi[6].ni[17].x" -350;
	setAttr ".tgi[6].ni[17].y" -758.5714111328125;
	setAttr ".tgi[6].ni[17].nvs" 18304;
	setAttr ".tgi[6].ni[18].x" 1192.857177734375;
	setAttr ".tgi[6].ni[18].y" -1090;
	setAttr ".tgi[6].ni[18].nvs" 18304;
	setAttr ".tgi[6].ni[19].x" 885.71429443359375;
	setAttr ".tgi[6].ni[19].y" -994.28570556640625;
	setAttr ".tgi[6].ni[19].nvs" 18304;
	setAttr ".tgi[6].ni[20].x" -42.857143402099609;
	setAttr ".tgi[6].ni[20].y" -955.71429443359375;
	setAttr ".tgi[6].ni[20].nvs" 18304;
	setAttr ".tgi[6].ni[21].x" 5231.4287109375;
	setAttr ".tgi[6].ni[21].y" -1065.7142333984375;
	setAttr ".tgi[6].ni[21].nvs" 18304;
	setAttr ".tgi[6].ni[22].x" 4924.28564453125;
	setAttr ".tgi[6].ni[22].y" -1227.142822265625;
	setAttr ".tgi[6].ni[22].nvs" 18304;
	setAttr ".tgi[6].ni[23].x" 3968.571533203125;
	setAttr ".tgi[6].ni[23].y" -1028.5714111328125;
	setAttr ".tgi[6].ni[23].nvs" 18304;
	setAttr ".tgi[6].ni[24].x" 885.71429443359375;
	setAttr ".tgi[6].ni[24].y" -1092.857177734375;
	setAttr ".tgi[6].ni[24].nvs" 18304;
	setAttr ".tgi[6].ni[25].x" -350;
	setAttr ".tgi[6].ni[25].y" -955.71429443359375;
	setAttr ".tgi[6].ni[25].nvs" 18304;
	setAttr ".tgi[6].ni[26].x" -350;
	setAttr ".tgi[6].ni[26].y" -1054.2857666015625;
	setAttr ".tgi[6].ni[26].nvs" 18304;
	setAttr ".tgi[6].ni[27].x" 571.4285888671875;
	setAttr ".tgi[6].ni[27].y" -1124.2857666015625;
	setAttr ".tgi[6].ni[27].nvs" 18304;
	setAttr ".tgi[6].ni[28].x" 5545.71435546875;
	setAttr ".tgi[6].ni[28].y" -1170;
	setAttr ".tgi[6].ni[28].nvs" 18304;
	setAttr ".tgi[6].ni[29].x" 5545.71435546875;
	setAttr ".tgi[6].ni[29].y" -1398.5714111328125;
	setAttr ".tgi[6].ni[29].nvs" 18304;
	setAttr ".tgi[6].ni[30].x" 5545.71435546875;
	setAttr ".tgi[6].ni[30].y" -1300;
	setAttr ".tgi[6].ni[30].nvs" 18304;
	setAttr ".tgi[6].ni[31].x" 5231.4287109375;
	setAttr ".tgi[6].ni[31].y" -1325.7142333984375;
	setAttr ".tgi[6].ni[31].nvs" 18304;
	setAttr ".tgi[6].ni[32].x" 5910;
	setAttr ".tgi[6].ni[32].y" -1350;
	setAttr ".tgi[6].ni[32].nvs" 18304;
	setAttr ".tgi[6].ni[33].x" 5545.71435546875;
	setAttr ".tgi[6].ni[33].y" -991.4285888671875;
	setAttr ".tgi[6].ni[33].nvs" 18304;
	setAttr ".tgi[6].ni[34].x" 3650;
	setAttr ".tgi[6].ni[34].y" -940;
	setAttr ".tgi[6].ni[34].nvs" 18304;
	setAttr ".tgi[6].ni[35].x" 4924.28564453125;
	setAttr ".tgi[6].ni[35].y" -957.14288330078125;
	setAttr ".tgi[6].ni[35].nvs" 18304;
	setAttr ".tgi[6].ni[36].x" 4582.85693359375;
	setAttr ".tgi[6].ni[36].y" -868.5714111328125;
	setAttr ".tgi[6].ni[36].nvs" 18304;
	setAttr ".tgi[6].ni[37].x" -350;
	setAttr ".tgi[6].ni[37].y" -561.4285888671875;
	setAttr ".tgi[6].ni[37].nvs" 18304;
	setAttr ".tgi[6].ni[38].x" -42.857143402099609;
	setAttr ".tgi[6].ni[38].y" -857.14288330078125;
	setAttr ".tgi[6].ni[38].nvs" 18304;
	setAttr ".tgi[6].ni[39].x" 5545.71435546875;
	setAttr ".tgi[6].ni[39].y" -1702.857177734375;
	setAttr ".tgi[6].ni[39].nvs" 18304;
	setAttr ".tgi[6].ni[40].x" 3968.571533203125;
	setAttr ".tgi[6].ni[40].y" -930;
	setAttr ".tgi[6].ni[40].nvs" 18304;
	setAttr ".tgi[6].ni[41].x" 264.28570556640625;
	setAttr ".tgi[6].ni[41].y" -955.71429443359375;
	setAttr ".tgi[6].ni[41].nvs" 18306;
	setAttr ".tgi[6].ni[42].x" 3035.71435546875;
	setAttr ".tgi[6].ni[42].y" -845.71429443359375;
	setAttr ".tgi[6].ni[42].nvs" 18304;
	setAttr ".tgi[6].ni[43].x" -350;
	setAttr ".tgi[6].ni[43].y" -857.14288330078125;
	setAttr ".tgi[6].ni[43].nvs" 18304;
	setAttr ".tgi[6].ni[44].x" 5910;
	setAttr ".tgi[6].ni[44].y" -1538.5714111328125;
	setAttr ".tgi[6].ni[44].nvs" 18304;
	setAttr ".tgi[6].ni[45].x" -350;
	setAttr ".tgi[6].ni[45].y" -1152.857177734375;
	setAttr ".tgi[6].ni[45].nvs" 18304;
	setAttr ".tgi[6].ni[46].x" 1500;
	setAttr ".tgi[6].ni[46].y" -1244.2857666015625;
	setAttr ".tgi[6].ni[46].nvs" 18304;
	setAttr ".tgi[6].ni[47].x" 5910;
	setAttr ".tgi[6].ni[47].y" -1637.142822265625;
	setAttr ".tgi[6].ni[47].nvs" 18304;
	setAttr ".tgi[6].ni[48].x" 5910;
	setAttr ".tgi[6].ni[48].y" -1735.7142333984375;
	setAttr ".tgi[6].ni[48].nvs" 18304;
createNode multiplyDivide -n "getKneeDirectionOffset";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000029D";
createNode decomposeMatrix -n "decomposeGuide02LocalTm";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000027D";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
createNode network -n "ik:softik:metadata";
	rename -uid "32E12980-0000-718A-5AE4-CE3B0000027A";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "locked" -ln "locked" -nn "locked" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -s false -ci true -sn "grp_inn" -ln "grp_inn" -nn "grp_inn" -at "message";
	addAttr -s false -ci true -sn "grp_out" -ln "grp_out" -nn "grp_out" -at "message";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -ci true -sn "version" -ln "version" -dt "string";
	setAttr "._uid" -2147483648;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "untitled";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Component.Module2";
	setAttr ".version" -type "string" "1.0.1";
createNode network -n "ik:softik:inn";
	rename -uid "32E12980-0000-718A-5AE4-CE3B00000279";
	addAttr -ci true -sn "inMatrixE" -ln "inMatrixE" -nn "inMatrixE" -dt "matrix";
	addAttr -ci true -sn "inMatrixS" -ln "inMatrixS" -nn "inMatrixS" -dt "matrix";
	addAttr -ci true -sn "inStretch" -ln "inStretch" -nn "inStretch" -at "float";
	addAttr -ci true -sn "inChainLength" -ln "inChainLength" -nn "inChainLength" -at "float";
	addAttr -ci true -sn "inRatio" -ln "inRatio" -nn "inRatio" -at "float";
	setAttr ".inMatrixE" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -5.8878467200641567e-16 1.7763568394002505e-15 -1.3322676295501878e-15 1;
	setAttr ".inMatrixS" -type "matrix" 0 -0.70710678118654757 0.70710678118654757 0 1.1102230246251568e-16 0.70710678118654746 0.70710678118654757 0
		 -1.0000000000000002 0 1.1102230246251565e-16 0 -4.9303806576313249e-32 5 5.4738221262688167e-48 1;
	setAttr ".inStretch" 1;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "32E12980-0000-718A-5AE4-CFF900000387";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "32E12980-0000-718A-5AE4-CFF900000388";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "32E12980-0000-718A-5AE4-CFF900000389";
createNode displayLayerManager -n "layerManager";
	rename -uid "32E12980-0000-718A-5AE4-CFF90000038A";
createNode displayLayer -n "defaultLayer";
	rename -uid "32E12980-0000-718A-5AE4-CFF90000038B";
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
	setAttr -s 27 ".u";
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
connectAttr "decomposeMatrix1.ot" "out1.t";
connectAttr "decomposeMatrix1.or" "out1.r";
connectAttr "decomposeMatrix1.os" "out1.s";
connectAttr "out1.s" "out2.is";
connectAttr "decomposeMatrix2.ot" "out2.t";
connectAttr "decomposeMatrix2.or" "out2.r";
connectAttr "decomposeMatrix2.os" "out2.s";
connectAttr "out2.s" "out3.is";
connectAttr "decomposeMatrix3.ot" "out3.t";
connectAttr "decomposeMatrix3.or" "out3.r";
connectAttr "decomposeMatrix3.os" "out3.s";
connectAttr "decomposeCtrlFk01DefaultLocalTm.ot" "ctrl1_zero.t";
connectAttr "decomposeCtrlFk01DefaultLocalTm.or" "ctrl1_zero.r";
connectAttr "decomposeCtrlFk01DefaultLocalTm.os" "ctrl1_zero.s";
connectAttr "makeNurbCircle2.oc" "ctrl1Shape.cr";
connectAttr "decomposeCtrlFk02DefaultLocalTm.ot" "ctrl2_zero.t";
connectAttr "decomposeCtrlFk02DefaultLocalTm.or" "ctrl2_zero.r";
connectAttr "decomposeCtrlFk02DefaultLocalTm.os" "ctrl2_zero.s";
connectAttr "makeNurbCircle3.oc" "ctrl2.cr";
connectAttr "decomposeCtrlFk03DefaultLocalTm.ot" "ctrl3_zero.t";
connectAttr "decomposeCtrlFk03DefaultLocalTm.or" "ctrl3_zero.r";
connectAttr "decomposeCtrlFk03DefaultLocalTm.os" "ctrl3_zero.s";
connectAttr "makeNurbCircle4.oc" "ctrl3Shape.cr";
connectAttr "guide_02_translateX.o" "inn2.tx";
connectAttr "guide_02_translateY.o" "inn2.ty";
connectAttr "guide_02_translateZ.o" "inn2.tz";
connectAttr "guide_02_visibility.o" "inn2.v";
connectAttr "guide_02_rotateX.o" "inn2.rx";
connectAttr "guide_02_rotateY.o" "inn2.ry";
connectAttr "guide_02_rotateZ.o" "inn2.rz";
connectAttr "guide_02_scaleX.o" "inn2.sx";
connectAttr "guide_02_scaleY.o" "inn2.sy";
connectAttr "guide_02_scaleZ.o" "inn2.sz";
connectAttr "getLimbSegment1Length.d" "getLimbLength.i1";
connectAttr "getLimbSegment2Length.d" "getLimbLength.i2";
connectAttr "decomposeGuide03LocalTm.ot" "multiplyDivide14.i1";
connectAttr "decomposeGuide02LocalTm.ot" "multiplyDivide13.i1";
connectAttr "decomposeGuide03LocalTm.ot" "getLimbSegment2Length.p2";
connectAttr "inn.msg" "Component.grp_inn";
connectAttr "out.msg" "Component.grp_out";
connectAttr "inn.Guide03_LocalTm" "getGuide03WorldTm.i[0]";
connectAttr "getGuide02WorldTm.o" "getGuide03WorldTm.i[1]";
connectAttr "inn.Guide01_LocalTm" "out.CtrlFk01_BaseLocalTm";
connectAttr "inn.Guide02_LocalTm" "out.CtrlFk02_BaseLocalTm";
connectAttr "inn.Guide03_LocalTm" "out.CtrlFk03_BaseLocalTm";
connectAttr "getKneeDirection.o3" "getKneeDirectionNormalized.i1";
connectAttr "decomposeGuide02WorldTm.ot" "getSwivelDefaultPos.i3[0]";
connectAttr "getKneeDirectionOffset.o" "getSwivelDefaultPos.i3[1]";
connectAttr "decomposeGuide02LocalTm.ot" "getLimbSegment1Length.p2";
connectAttr "getLimbRatio.ox" "getLimbMiddleAim.i2x";
connectAttr "getLimbRatio.ox" "getLimbMiddleAim.i2y";
connectAttr "getLimbRatio.ox" "getLimbMiddleAim.i2z";
connectAttr "getLimbAim.o3" "getLimbMiddleAim.i1";
connectAttr "getGuide03WorldTm.o" "decomposeGuide03WorldTm.imat";
connectAttr "decomposeGuide03WorldTm.ot" "getLimbAim.i3[0]";
connectAttr "decomposeGuide01LocalTm.ot" "getLimbAim.i3[1]";
connectAttr "getLimbSegment1Length.d" "getLimbRatio.i1x";
connectAttr "getLimbLength.o" "getLimbRatio.i2x";
connectAttr "getGuide02WorldTm.o" "decomposeGuide02WorldTm.imat";
connectAttr "decomposeGuide02WorldTm.ot" "getKneeDirection.i3[0]";
connectAttr "getKneePosProjectedOnLimbDir.o3" "getKneeDirection.i3[1]";
connectAttr "inn.Guide02_LocalTm" "getGuide02WorldTm.i[0]";
connectAttr "inn.Guide01_LocalTm" "getGuide02WorldTm.i[1]";
connectAttr "inn.msg" "metadata1.grp_inn";
connectAttr "out.msg" "metadata1.grp_out";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "inn.Guide01_LocalTm" "decomposeGuide01LocalTm.imat";
connectAttr "decomposeGuide01LocalTm.ot" "getKneePosProjectedOnLimbDir.i3[0]";
connectAttr "getLimbMiddleAim.o" "getKneePosProjectedOnLimbDir.i3[1]";
connectAttr "inn.Guide03_LocalTm" "decomposeGuide03LocalTm.imat";
connectAttr "getLimbLength.o" "getSwivelDistance.i1x";
connectAttr "inn.swivelDistanceRatio" "getSwivelDistance.i2x";
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn";
connectAttr "ctrl2_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn";
connectAttr "decomposeGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn";
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "out3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn";
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn"
		;
connectAttr "guide_02_translateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn"
		;
connectAttr "inn3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn";
connectAttr "decomposeGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "inn1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn";
connectAttr "getKneePosProjectedOnLimbDir.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn"
		;
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn"
		;
connectAttr "getKneeDirection.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[22].dn";
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[23].dn";
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[24].dn"
		;
connectAttr "getKneeDirectionNormalized.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn"
		;
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[26].dn";
connectAttr "ctrl3_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[27].dn";
connectAttr "getLimbAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[28].dn";
connectAttr "inn2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[29].dn";
connectAttr "getGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[30].dn"
		;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[31].dn"
		;
connectAttr "ctrl1_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[32].dn";
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[0].dn";
connectAttr "inn1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[1].dn";
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[2].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[3].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[4].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[5].dn"
		;
connectAttr "inn3.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[6].dn";
connectAttr "ctrl2_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[7].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[8].dn"
		;
connectAttr "inn2.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[9].dn";
connectAttr "ctrl1_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[10].dn";
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[11].dn"
		;
connectAttr "out3.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[12].dn";
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[13].dn"
		;
connectAttr "ik:softik:metadata.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[0].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[1].dn";
connectAttr "inn2.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[0].dn";
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[1].dn"
		;
connectAttr "multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[2].dn";
connectAttr "inn3.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[3].dn";
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[4].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[5].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[6].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[7].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[8].dn";
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[0].dn";
connectAttr "inn2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[1].dn";
connectAttr "inn1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[2].dn";
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[3].dn"
		;
connectAttr "guide_02_rotateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[4].dn"
		;
connectAttr "inn3.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[5].dn";
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[6].dn"
		;
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[7].dn";
connectAttr "out2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[8].dn";
connectAttr "guide_02_rotateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[9].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[10].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[11].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[12].dn";
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[13].dn"
		;
connectAttr "multiplyDivide10.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[14].dn"
		;
connectAttr "guide_02_scaleX.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[15].dn"
		;
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[16].dn"
		;
connectAttr "ik:softik:metadata.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[17].dn"
		;
connectAttr "out3.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[18].dn";
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[19].dn";
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[0].dn"
		;
connectAttr "guide_02_translateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[1].dn"
		;
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[2].dn";
connectAttr "guide_02_scaleX.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[3].dn";
connectAttr "inn2.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[4].dn";
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[5].dn"
		;
connectAttr "guide_02_rotateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[6].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[7].dn"
		;
connectAttr "inn1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[8].dn";
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[9].dn"
		;
connectAttr ":defaultRenderUtilityList1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[10].dn"
		;
connectAttr "ctrl1_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[11].dn";
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[12].dn"
		;
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[13].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[14].dn";
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[15].dn"
		;
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[16].dn"
		;
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[17].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[18].dn";
connectAttr "guide_02_rotateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[19].dn"
		;
connectAttr "decomposeGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[20].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[21].dn"
		;
connectAttr "inn3.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[22].dn";
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[23].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[24].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[25].dn"
		;
connectAttr "ctrl2_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[26].dn";
connectAttr "ctrl3_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[27].dn";
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[28].dn"
		;
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[29].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[30].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[31].dn"
		;
connectAttr "guide_02_translateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[32].dn"
		;
connectAttr "getKneePosProjectedOnLimbDir.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[0].dn"
		;
connectAttr "guide_02_translateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[1].dn"
		;
connectAttr "multiplyDivide10.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[2].dn"
		;
connectAttr "ctrl1_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[3].dn";
connectAttr "out1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[4].dn";
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[5].dn"
		;
connectAttr "guide_02_rotateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[6].dn"
		;
connectAttr "getSwivelDefaultPos.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[7].dn"
		;
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[8].dn";
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[9].dn"
		;
connectAttr "getLimbMiddleAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[10].dn"
		;
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[11].dn"
		;
connectAttr "ctrl3_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[12].dn";
connectAttr "inn3.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[13].dn";
connectAttr "getKneeDirectionNormalized.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[14].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[15].dn";
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[16].dn"
		;
connectAttr "guide_02_scaleX.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[17].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[18].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[19].dn"
		;
connectAttr "inn2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[20].dn";
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[21].dn"
		;
connectAttr "decomposeMatrix1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[22].dn"
		;
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[23].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[24].dn"
		;
connectAttr "guide_02_translateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[25].dn"
		;
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[26].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[27].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[28].dn"
		;
connectAttr "decomposeMatrix3.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[29].dn"
		;
connectAttr "out2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[30].dn";
connectAttr "decomposeMatrix2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[31].dn"
		;
connectAttr "out3.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[32].dn";
connectAttr "getKneeDirectionOffset.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[33].dn"
		;
connectAttr "decomposeGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[34].dn"
		;
connectAttr "getKneeDirection.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[35].dn"
		;
connectAttr "decomposeGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[36].dn"
		;
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[37].dn"
		;
connectAttr "inn1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[38].dn";
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[39].dn"
		;
connectAttr "getLimbAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[40].dn";
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[41].dn";
connectAttr "getGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[42].dn"
		;
connectAttr "guide_02_rotateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[43].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[44].dn"
		;
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[45].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[46].dn";
connectAttr "ctrl2_zero.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[47].dn";
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[48].dn"
		;
connectAttr "getKneeDirectionNormalized.o" "getKneeDirectionOffset.i1";
connectAttr "getSwivelDistance.ox" "getKneeDirectionOffset.i2x";
connectAttr "getSwivelDistance.ox" "getKneeDirectionOffset.i2y";
connectAttr "getSwivelDistance.ox" "getKneeDirectionOffset.i2z";
connectAttr "inn.Guide02_LocalTm" "decomposeGuide02LocalTm.imat";
connectAttr "ik:softik:inn.msg" "ik:softik:metadata.grp_inn";
connectAttr "getLimbLength.o" "ik:softik:inn.inChainLength";
connectAttr "multiplyDivide1.ox" "ik:softik:inn.inRatio";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "decomposeGuide01LocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeGuide02LocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeGuide03LocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getLimbSegment1Length.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLimbSegment2Length.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLimbLength.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide13.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide14.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getGuide03WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeGuide03WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getSwivelDistance.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLimbRatio.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLimbAim.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLimbMiddleAim.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getKneePosProjectedOnLimbDir.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "getKneeDirection.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getGuide02WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeGuide02WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getKneeDirectionNormalized.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getKneeDirectionOffset.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getSwivelDefaultPos.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeMatrix1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeMatrix2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeMatrix3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of FK3-0.0.1.ma
