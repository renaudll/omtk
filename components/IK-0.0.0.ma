//Maya ASCII 2017ff05 scene
//Name: ik.ma
//Last modified: Thu, Apr 19, 2018 11:30:44 PM
//Codeset: UTF-8
requires maya "2017ff05";
requires -nodeType "decomposeMatrix" -nodeType "composeMatrix" "matrixNodes" "1.0";
requires "stereoCamera" "10.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201710312130-1018716";
fileInfo "osv" "Linux 4.13.0-38-generic #43-Ubuntu SMP Wed Mar 14 15:20:44 UTC 2018 x86_64";
fileInfo "license" "student";
fileInfo "omtk.component.author" "Renaud Lessard Larouche";
fileInfo "omtk.component.version" "0.0.0";
fileInfo "omtk.component.uid" "9e38b6df-b42c-5f6d-b243-bbfeb645599a";
fileInfo "omtk.component.name" "IK3";
createNode transform -s -n "persp";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000917";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 25.659861602208593 7.2135083492985999 18.288393394815245 ;
	setAttr ".r" -type "double3" -9.9383527296052421 50.600000000004776 -2.5054370439965773e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000918";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 31.916396595880087;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -4.9960036108132044e-16 2.0971816858077239 0.61494863832237145 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000919";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "699D7980-0000-0F71-5AB5-BDA90000091A";
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
	rename -uid "699D7980-0000-0F71-5AB5-BDA90000091B";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "699D7980-0000-0F71-5AB5-BDA90000091C";
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
	rename -uid "699D7980-0000-0F71-5AB5-BDA90000091D";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "699D7980-0000-0F71-5AB5-BDA90000091E";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode joint -n "out1";
	rename -uid "699D7980-0000-0F71-5AB5-BDAA00000926";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" 8451.4287 -1574.2858 ;
createNode joint -n "out2" -p "out1";
	rename -uid "699D7980-0000-0F71-5AB5-BDAA00000927";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".is" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 7068.5713 -1351.4286 ;
createNode joint -n "out3" -p "out2";
	rename -uid "699D7980-0000-0F71-5AB5-BDAA00000928";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 8451.4287 -2865.7144 ;
createNode transform -n "anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002E8";
createNode transform -n "arm_elbow01_anm_offset" -p "anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000401";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".t" -type "double3" -3.9252311467094368e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".r" -type "double3" 89.999999999999986 44.999999999999986 -90.000000000000057 ;
	setAttr "._graphpos" -type "float2" -348.5932 -2362.9514 ;
createNode transform -n "arm_elbow01_anm" -p "arm_elbow01_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000400";
	setAttr -k on ".ro";
createNode nurbsCurve -n "arm_elbow01_anmShape" -p "arm_elbow01_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003FF";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 12 0 no 3
		13 0 1 2 3 4 5 6 7 8 9 10
		 11 12
		13
		0 -0.41113678118246555 0.41113678118246555
		0 -0.41113678118246555 0.8222735623649311
		0 0.41113678118246555 0.8222735623649311
		0 0.41113678118246555 0.41113678118246555
		0 0.8222735623649311 0.41113678118246555
		0 0.8222735623649311 -0.41113678118246555
		0 0.41113678118246555 -0.41113678118246555
		0 0.41113678118246555 -0.8222735623649311
		0 -0.41113678118246555 -0.8222735623649311
		0 -0.41113678118246555 -0.41113678118246555
		0 -0.8222735623649311 -0.41113678118246555
		0 -0.8222735623649311 0.41113678118246555
		0 -0.41113678118246555 0.41113678118246555
		;
createNode transform -n "ik:arm_ik_anm_grp" -p "anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EB";
createNode transform -n "ik:arm_ik_anm_offset" -p "ik:arm_ik_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F9";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 8451.4287 -871.42859 ;
createNode transform -n "ik:arm_ik_anm" -p "ik:arm_ik_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F8";
	addAttr -ci true -k true -sn "softIkRatio" -ln "softIkRatio" -nn "SoftIK" -min 
		0 -max 50 -at "double";
	addAttr -ci true -k true -sn "stretch" -ln "stretch" -nn "Stretch" -min 0 -max 1 
		-at "double";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".r" -type "double3" 180 -45 -90 ;
	setAttr -k on ".ro";
	setAttr -k on ".softIkRatio";
	setAttr -k on ".stretch" 1;
	setAttr "._graphpos" -type "float2" 5337.1934 881.39252 ;
createNode nurbsCurve -n "ik:arm_ik_anmShape" -p "ik:arm_ik_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F7";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 15 0 no 3
		16 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15
		16
		0 -0.5 0.5
		0 0.5 0.5
		1 0.5 0.5
		1 -0.5 0.5
		0 -0.5 0.5
		0 -0.5 -0.5
		0 0.5 -0.5
		0 0.5 0.5
		1 0.5 0.5
		1 0.5 -0.5
		1 -0.5 -0.5
		1 -0.5 0.5
		1 -0.5 -0.5
		0 -0.5 -0.5
		0 0.5 -0.5
		1 0.5 -0.5
		;
createNode transform -n "ik:arm_ik_swivel_anm_offset" -p "ik:arm_ik_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000317";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".t" -type "double3" -5.3130099264878626e-16 2.5 6.0355339050292969 ;
	setAttr "._graphpos" -type "float2" 2561.4634 -803.40222 ;
createNode transform -n "ik:arm_ik_swivel_anm" -p "ik:arm_ik_swivel_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000316";
	addAttr -ci true -k true -sn "space" -ln "space" -min -2 -max 0 -en "World=-2:arm=0" 
		-at "enum";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -k on ".space" -2;
	setAttr "._graphpos" -type "float2" -705.38379 45.508633 ;
createNode nurbsCurve -n "ik:arm_ik_swivel_anmShape" -p "ik:arm_ik_swivel_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000315";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "ik:arm_ik_swivelLineLoc_anm" -p "ik:arm_ik_swivel_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000318";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".v" no;
	setAttr "._graphpos" -type "float2" 8451.4287 -1340 ;
createNode locator -n "ik:arm_ik_swivelLineLoc_anmShape" -p "ik:arm_ik_swivelLineLoc_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000319";
	setAttr -k off ".v";
createNode pointConstraint -n "ik:locator1_pointConstraint1" -p "ik:arm_ik_swivelLineLoc_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000031A";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "infl_02W0" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" -3.9252311467094378e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr -k on ".w0";
	setAttr "._graphpos" -type "float2" 7682.8569 -1320 ;
createNode annotationShape -n "ik:arm_ik_swivelLineAnn_anm" -p "ik:arm_ik_swivel_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000031B";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -k off ".v";
	setAttr "._graphpos" -type "float2" 13697.143 -3185.7144 ;
createNode transform -n "dag";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002E9";
	addAttr -ci true -sn "globalScale" -ln "globalScale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "fkIk" -ln "fkIk" -dv 1 -min 0 -max 1 -at "double";
	setAttr ".v" no;
	setAttr -k on ".fkIk";
createNode transform -n "ik:arm_ik_data_grp" -p "dag";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EC";
	addAttr -ci true -sn "globalScale" -ln "globalScale" -dv 1 -at "double";
createNode transform -n "ik:arm_ik_ikChain_rig" -p "ik:arm_ik_data_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EA";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 7068.5713 -2785.7144 ;
createNode ikHandle -n "ik:arm_ik_ikHandle_rig" -p "ik:arm_ik_ikChain_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F5";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".r" -type "double3" -45.000000000000007 90 0 ;
	setAttr ".s" -type "double3" 0.99999999999999956 1 1 ;
	setAttr ".roc" yes;
	setAttr "._graphpos" -type "float2" 8451.4287 -2631.4285 ;
createNode pointConstraint -n "ik:arm_ik_ikHandle_rig_softIkConstraint1" -p "ik:arm_ik_ikHandle_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000311";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_ik_ikHandleTarget_rigW0" -dv 
		1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "arm_ik_ikChain_rigW1" -dv 1 -min 0 
		-at "double";
	addAttr -dcb 0 -ci true -k true -sn "w2" -ln "arm_ik_anmW2" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 3 ".tg";
	setAttr ".rst" -type "double3" 3.5355339059327355 -3.5355339059327373 1.9626155733547179e-16 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
	setAttr -k on ".w2";
	setAttr "._graphpos" -type "float2" 7682.8569 -2845.7144 ;
createNode poleVectorConstraint -n "ik:arm_ik_ikHandle_rig_poleVectorConstraint1" 
		-p "ik:arm_ik_ikHandle_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000320";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_ik_swivel_anmW0" -dv 1 -min 0 
		-at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 6.7677669516887091 3.2322330457559731 9.3079804692383041e-16 ;
	setAttr -k on ".w0";
createNode transform -n "ik:arm_ik_ikHandleTarget_rig" -p "ik:arm_ik_data_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002FA";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 5953.6719 1068.634 ;
createNode pointConstraint -n "ik:arm_ik_ikHandleTarget_rig_pointConstraint1" -p "ik:arm_ik_ikHandleTarget_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002FB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_ik_anmW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" -5.8878467200641567e-16 1.7763568394002505e-15 -1.3322676295501878e-15 ;
	setAttr -k on ".w0";
createNode joint -n "ik:arm_ik_01_rig" -p "ik:arm_ik_data_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002ED";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".t" -type "double3" 0 5.0000000000000009 5.4738221262688167e-48 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 90 -45 -90 ;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" 2124.6069 1005.2448 ;
createNode joint -n "ik:arm_ik_02_rig" -p "ik:arm_ik_01_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EE";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".r" -type "double3" 2.5532751999517907e-24 1.0647817771260892e-21 4.5995716956306424e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 8451.4287 -3274.2856 ;
createNode joint -n "ik:arm_ik_03_rig" -p "ik:arm_ik_02_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EF";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 8451.4287 -1105.7142 ;
createNode orientConstraint -n "ik:arm_ik_03_rig_orientConstraint1" -p "ik:arm_ik_03_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000321";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_ik_anmW0" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".lr" -type "double3" 90 0 -8.9959671327898901e-15 ;
	setAttr ".o" -type "double3" -89.999999999999986 0 0 ;
	setAttr -k on ".w0";
	setAttr "._graphpos" -type "float2" 386.3093 11.795704 ;
createNode ikEffector -n "ik:arm_ik_ikEffector_rig" -p "ik:arm_ik_02_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F0";
	setAttr ".v" no;
	setAttr ".hd" yes;
createNode joint -n "inn1";
	rename -uid "9830B980-0000-24DE-5AB5-C4D6000005FE";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".t" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 90 -45.000000000000007 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" -4731.4287 -1842.8572 ;
createNode joint -n "inn2" -p "inn1";
	rename -uid "9830B980-0000-24DE-5AB5-C4D6000005FF";
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
	setAttr "._graphpos" -type "float2" -4731.4287 -1645.7142 ;
createNode joint -n "inn3" -p "inn2";
	rename -uid "9830B980-0000-24DE-5AB5-C4D600000600";
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
	setAttr "._graphpos" -type "float2" -4731.4287 -1448.5714 ;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "4A343980-0000-3530-5AD9-5E6100000284";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "4A343980-0000-3530-5AD9-5E6100000285";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "4A343980-0000-3530-5AD9-5E6100000286";
createNode displayLayerManager -n "layerManager";
	rename -uid "4A343980-0000-3530-5AD9-5E6100000287";
createNode displayLayer -n "defaultLayer";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000923";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "4A343980-0000-3530-5AD9-5E6100000289";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000925";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "699D7980-0000-0F71-5AB5-BDD500000932";
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
		+ "        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n"
		+ "            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n"
		+ "            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n"
		+ "            -shadows 0\n            -captureSequenceNumber -1\n            -width 1247\n            -height 696\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n"
		+ "            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 0\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n"
		+ "            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n"
		+ "            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 0\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n"
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
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n"
		+ "                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n"
		+ "                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1247\\n    -height 696\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1247\\n    -height 696\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "699D7980-0000-0F71-5AB5-BDD500000933";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode ikRPsolver -n "ikRPsolver";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F2";
createNode multiplyDivide -n "multiplyDivide1";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002FC";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".i2" -type "float3" 0.0099999998 1 1 ;
	setAttr "._graphpos" -type "float2" 5951.4785 398.53543 ;
createNode multiplyDivide -n "multiplyDivide9";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000030F";
	setAttr ".i1" -type "float3" 7.0710678 0 0 ;
createNode reverse -n "reverse1";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000310";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 7068.5713 -3020 ;
createNode makeNurbCircle -n "makeNurbCircle1";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000314";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".d" 1;
	setAttr ".s" 4;
createNode network -n "ik:softik:inn";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D5";
	addAttr -ci true -sn "inMatrixE" -ln "inMatrixE" -nn "inMatrixE" -dt "matrix";
	addAttr -ci true -sn "inMatrixS" -ln "inMatrixS" -nn "inMatrixS" -dt "matrix";
	addAttr -ci true -sn "inStretch" -ln "inStretch" -nn "inStretch" -at "float";
	addAttr -ci true -sn "inChainLength" -ln "inChainLength" -nn "inChainLength" -at "float";
	addAttr -ci true -sn "inRatio" -ln "inRatio" -nn "inRatio" -at "float";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" -1645.7142 -1974.2858 ;
createNode multiplyDivide -n "ik:softik:multiplyDivide4";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D7";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 2.7182817 0 0 ;
	setAttr "._graphpos" -type "float2" 2040 -2337.1428 ;
createNode multiplyDivide -n "ik:softik:multiplyDivide3";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D8";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".i2" -type "float3" -1 1 1 ;
	setAttr "._graphpos" -type "float2" 1425.7142 -2291.4285 ;
createNode plusMinusAverage -n "ik:softik:plusMinusAverage4";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D9";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
	setAttr "._graphpos" -type "float2" 3905.7144 -2700 ;
createNode distanceBetween -n "ik:softik:distanceBetween1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DA";
createNode condition -n "ik:softik:condition2";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DB";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr "._graphpos" -type "float2" 5157.1431 -2608.5715 ;
createNode clamp -n "ik:softik:clamp1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DC";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mn" -type "float3" 9.9999997e-05 0 0 ;
	setAttr ".mx" -type "float3" 999 0 0 ;
	setAttr "._graphpos" -type "float2" 197.14285 -2265.7144 ;
createNode plusMinusAverage -n "ik:softik:plusMinusAverage3";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DD";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  1 inf;
	setAttr "._graphpos" -type "float2" 2677.1428 -2388.5715 ;
createNode blendTwoAttr -n "ik:softik:blendTwoAttr2";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DE";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -s 2 ".i[0:1]"  1 1;
	setAttr "._graphpos" -type "float2" 5771.4287 -2600 ;
createNode multiplyDivide -n "ik:softik:multiplyDivide5";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DF";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 3291.4285 -2540 ;
createNode network -n "ik:softik:out";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E0";
	addAttr -ci true -sn "outStretch" -ln "outStretch" -nn "outStretch" -at "float";
	addAttr -ci true -sn "outRatio" -ln "outRatio" -nn "outRatio" -at "float";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 6385.7144 -2657.1428 ;
createNode multiplyDivide -n "ik:softik:multiplyDivide1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E1";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" -1031.4286 -1974.2858 ;
createNode plusMinusAverage -n "ik:softik:plusMinusAverage1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E2";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
	setAttr "._graphpos" -type "float2" -417.14285 -2294.2856 ;
createNode condition -n "ik:softik:condition1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E3";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr "._graphpos" -type "float2" 4520 -2942.8572 ;
createNode multiplyDivide -n "ik:softik:multiplyDivide2";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E4";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr "._graphpos" -type "float2" 811.42859 -2474.2856 ;
createNode multiplyDivide -n "ik:softik:multiplyDivide7";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E5";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr "._graphpos" -type "float2" 5771.4287 -2871.4285 ;
createNode plusMinusAverage -n "ik:softik:plusMinusAverage2";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E6";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
	setAttr "._graphpos" -type "float2" 197.14285 -2537.1428 ;
createNode blendTwoAttr -n "ik:softik:blendTwoAttr1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E7";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -s 2 ".i";
	setAttr -s 2 ".i";
	setAttr "._graphpos" -type "float2" 5157.1431 -2880 ;
createNode multiplyDivide -n "ik:softik:multiplyDivide6";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E8";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr "._graphpos" -type "float2" 4520 -2671.4285 ;
createNode network -n "inn";
	rename -uid "9830B980-0000-24DE-5AB5-C5100000062A";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	addAttr -ci true -sn "Guide01_LocalTm" -ln "Guide01_LocalTm" -dt "matrix";
	addAttr -ci true -sn "Guide02_LocalTm" -ln "Guide02_LocalTm" -dt "matrix";
	addAttr -ci true -sn "Guide03_LocalTm" -ln "Guide03_LocalTm" -dt "matrix";
	addAttr -ci true -sn "swivelDistanceRatio" -ln "swivelDistanceRatio" -dv 0.5 -min 
		0 -max 1 -at "double";
	setAttr "._graphpos" -type "float2" -4117.1431 -1645.7142 ;
	setAttr -k on ".swivelDistanceRatio";
createNode decomposeMatrix -n "decomposeGuide01LocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C59B0000062B";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
	setAttr "._graphpos" -type "float2" 4520 -2017.1428 ;
createNode decomposeMatrix -n "decomposeGuide02LocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C59C0000062C";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
	setAttr "._graphpos" -type "float2" -3502.8572 -1634.2858 ;
createNode decomposeMatrix -n "decomposeGuide03LocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C59D0000062D";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
	setAttr "._graphpos" -type "float2" -3502.8572 -1322.8572 ;
createNode network -n "out";
	rename -uid "9830B980-0000-24DE-5AB5-C94500000818";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	addAttr -ci true -sn "outCtrlIkBaseWorldTm" -ln "outCtrlIkBaseWorldTm" -dt "matrix";
	addAttr -ci true -sn "outCtrlIkSwivelBaseWorldTm" -ln "outCtrlIkSwivelBaseWorldTm" 
		-dt "matrix";
	addAttr -ci true -sn "outInf01LocalTm" -ln "outInf01LocalTm" -dt "matrix";
	addAttr -ci true -sn "outInf02LocalTm" -ln "outInf02LocalTm" -dt "matrix";
	addAttr -ci true -sn "outInf03LocalTm" -ln "outInf03LocalTm" -dt "matrix";
	addAttr -ci true -sn "outCtrlSwivelOffsetTm" -ln "outCtrlSwivelOffsetTm" -dt "matrix";
	addAttr -ci true -sn "outCtrlIkOffsetTm" -ln "outCtrlIkOffsetTm" -dt "matrix";
	setAttr "._graphpos" -type "float2" 3905.7144 -1702.8572 ;
	setAttr ".outInf01LocalTm" -type "matrix" 0 -0.70710678118654757 0.70710678118654757 0 1.1102230246251568e-16 0.70710678118654746 0.70710678118654757 0
		 -1.0000000000000002 0 1.1102230246251565e-16 0 0 5 0 1;
	setAttr ".outInf02LocalTm" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 3.535533905932736 0 3.9252311467094368e-16 1;
	setAttr ".outInf03LocalTm" -type "matrix" -2.2204460492503131e-16 1 0 0 -1 -2.2204460492503131e-16 0 0
		 0 0 1 0 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 1;
createNode decomposeMatrix -n "decomposeCtrlFk01DefaultLocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C9A400000819";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".imat" -type "matrix" 0 -0.70710678118654757 0.70710678118654757 0 1.1102230246251568e-16 0.70710678118654746 0.70710678118654757 0
		 -1.0000000000000002 0 1.1102230246251565e-16 0 -4.9303806576313249e-32 5 5.4738221262688167e-48 1;
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
	setAttr "._graphpos" -type "float2" 130.12289 -666.87982 ;
createNode decomposeMatrix -n "decomposeCtrlFk03DefaultLocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C9B60000081B";
	setAttr ".imat" -type "matrix" -2.2204460492503131e-16 1 0 0 -1 -2.2204460492503131e-16 0 0
		 0 0 1 0 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 1;
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode distanceBetween -n "getLimbSegment1Length";
	rename -uid "8CE2E980-0000-3155-5AB5-CE5000000678";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" -2874.2856 -1300 ;
createNode distanceBetween -n "getLimbSegment2Length";
	rename -uid "8CE2E980-0000-3155-5AB5-CE5D00000679";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" -2874.2856 -1611.4286 ;
createNode addDoubleLinear -n "getLimbLength";
	rename -uid "8CE2E980-0000-3155-5AB5-CE8C0000067A";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" -2260 -1534.2858 ;
createNode multiplyDivide -n "multiplyDivide13";
	rename -uid "8CE2E980-0000-3155-5AB5-D0870000091D";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 7682.8569 -3274.2856 ;
createNode multiplyDivide -n "multiplyDivide14";
	rename -uid "8CE2E980-0000-3155-5AB5-D08B0000091E";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 7682.8569 -1122.8572 ;
createNode animCurveTL -n "guide_02_translateX";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C3";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.535533905932736 10 6.3911650194459524;
	setAttr ".osr" -type "doubleArray" 0 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -2040 ;
createNode animCurveTL -n "guide_02_translateY";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C4";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 1.8998827256160656e-16;
	setAttr ".osr" -type "doubleArray" 2 -65358361939.163658 0.41666666666666669 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -1448.5714 ;
createNode animCurveTL -n "guide_02_translateZ";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C5";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.9252311467094363e-16 10 7.5484373465108625e-17;
	setAttr ".osr" -type "doubleArray" 0 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -2237.1428 ;
createNode animCurveTU -n "guide_02_visibility";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C6";
	setAttr ".tan" 9;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
createNode animCurveTA -n "guide_02_rotateX";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C7";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
	setAttr ".osr" -type "doubleArray" 2 -65358361939.163658 65358361939.163658 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -1251.4286 ;
createNode animCurveTA -n "guide_02_rotateY";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C8";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
	setAttr ".osr" -type "doubleArray" 2 -65358361939.163658 65358361939.163658 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -1054.2858 ;
createNode animCurveTA -n "guide_02_rotateZ";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C9";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
	setAttr ".osr" -type "doubleArray" 2 -65358361939.163658 65358361939.163658 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -857.14288 ;
createNode animCurveTU -n "guide_02_scaleX";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005CA";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr ".osr" -type "doubleArray" 0 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -2434.2856 ;
createNode animCurveTU -n "guide_02_scaleY";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005CB";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr ".osr" -type "doubleArray" 0 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -1842.8572 ;
createNode animCurveTU -n "guide_02_scaleZ";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005CC";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr ".osr" -type "doubleArray" 0 ;
	setAttr "._graphpos" -type "float2" -5345.7144 -1645.7142 ;
createNode multMatrix -n "getGuide03WorldTm";
	rename -uid "8C391980-0000-426F-5AD6-9C3B000005EB";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -s 2 ".i";
	setAttr "._graphpos" -type "float2" 3291.4285 -1511.4286 ;
createNode decomposeMatrix -n "decomposeMatrix4";
	rename -uid "8C391980-0000-426F-5AD6-9C63000005F0";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".ot" -type "double3" -5.8878467200641577e-16 8.8817841970012523e-16 -1.3322676295501878e-15 ;
	setAttr ".or" -type "double3" 90 -45.000000000000028 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818829;
	setAttr ".oqz" -0.27059805007309845;
	setAttr ".oqw" 0.65328148243818829;
	setAttr "._graphpos" -type "float2" 4520 -1362.8572 ;
createNode multiplyDivide -n "getSwivelDistance";
	rename -uid "8C391980-0000-426F-5AD6-9E3000000613";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 1425.7142 -1642.8572 ;
createNode multiplyDivide -n "getLimbRatio";
	rename -uid "8C391980-0000-426F-5AD6-9E6100000616";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr "._graphpos" -type "float2" 5157.1431 -1954.2858 ;
createNode plusMinusAverage -n "getLimbAim";
	rename -uid "8C391980-0000-426F-5AD6-9F5400000623";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
	setAttr "._graphpos" -type "float2" 5157.1431 -1757.1428 ;
createNode multiplyDivide -n "getLimbMiddleAim";
	rename -uid "8C391980-0000-426F-5AD6-9FD600000624";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 5771.4287 -1805.7142 ;
createNode plusMinusAverage -n "getKneePosProjectedOnLimbDir";
	rename -uid "8C391980-0000-426F-5AD6-9FF900000626";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
	setAttr "._graphpos" -type "float2" 6385.7144 -1751.4286 ;
createNode plusMinusAverage -n "getKneeDirection";
	rename -uid "8C391980-0000-426F-5AD6-A08A00000634";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
	setAttr "._graphpos" -type "float2" 7068.5713 -1785.7142 ;
createNode multMatrix -n "getGuide02WorldTm";
	rename -uid "8C391980-0000-426F-5AD6-A09C00000635";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -s 2 ".i";
	setAttr "._graphpos" -type "float2" 1425.7142 -1445.7142 ;
createNode decomposeMatrix -n "decomposeGuide02WorldTm";
	rename -uid "8C391980-0000-426F-5AD6-A0CF00000636";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".ot" -type "double3" -3.9252311467094378e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".or" -type "double3" 90 45 -90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.65328148243818818;
	setAttr ".oqy" -0.27059805007309845;
	setAttr ".oqz" -0.65328148243818829;
	setAttr ".oqw" 0.27059805007309851;
	setAttr "._graphpos" -type "float2" 2040 -1728.5714 ;
createNode vectorProduct -n "getKneeDirectionNormalized";
	rename -uid "8C391980-0000-426F-5AD6-A11700000639";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".op" 0;
	setAttr ".no" yes;
	setAttr "._graphpos" -type "float2" 7682.8569 -1751.4286 ;
createNode multiplyDivide -n "getKneeDirectionOffset";
	rename -uid "8C391980-0000-426F-5AD6-A1370000063C";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr "._graphpos" -type "float2" 2040 -1531.4286 ;
createNode plusMinusAverage -n "getSwivelDefaultPos";
	rename -uid "8C391980-0000-426F-5AD6-A1640000063D";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
	setAttr "._graphpos" -type "float2" 2677.1428 -1665.7142 ;
createNode decomposeMatrix -n "decomposeMatrix1";
	rename -uid "F4C8C980-0000-752C-5AD6-B690000003FA";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".ot" -type "double3" 0 5 0 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
	setAttr "._graphpos" -type "float2" 7682.8569 -1554.2858 ;
createNode decomposeMatrix -n "decomposeMatrix2";
	rename -uid "F4C8C980-0000-752C-5AD6-B694000003FB";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094368e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
	setAttr "._graphpos" -type "float2" 6385.7144 -1274.2858 ;
createNode decomposeMatrix -n "decomposeMatrix3";
	rename -uid "F4C8C980-0000-752C-5AD6-B697000003FC";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
	setAttr "._graphpos" -type "float2" 7682.8569 -2648.5715 ;
createNode composeMatrix -n "composeMatrix1";
	rename -uid "D295E980-0000-2369-5AD9-5C60000002DA";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".omat" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -5.3130099264878626e-16 2.5 6.0355339050292969 1;
	setAttr "._graphpos" -type "float2" 3291.4285 -1708.5714 ;
createNode decomposeMatrix -n "decomposeGuide03WorldTm1";
	rename -uid "4A343980-0000-3530-5AD9-5E9E000002CF";
	setAttr ".ot" -type "double3" -5.8878467200641577e-16 8.8817841970012523e-16 -1.3322676295501878e-15 ;
	setAttr ".or" -type "double3" 90 -45.000000000000021 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818829;
	setAttr ".oqz" -0.27059805007309845;
	setAttr ".oqw" 0.65328148243818829;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "4A343980-0000-3530-5AD9-5EE2000002D0";
	setAttr ".tgi[0].tn" -type "string" "Untitled_6";
	setAttr ".tgi[0].vl" -type "double2" -1860.6819118834524 -110.85441361266444 ;
	setAttr ".tgi[0].vh" -type "double2" -413.3119753146525 617.05439689907621 ;
	setAttr -s 70 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 4940;
	setAttr ".tgi[0].ni[0].y" 584.28570556640625;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 3020;
	setAttr ".tgi[0].ni[1].y" -1814.2857666015625;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" -1041.4285888671875;
	setAttr ".tgi[0].ni[2].y" 435.71429443359375;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 3327.142822265625;
	setAttr ".tgi[0].ni[3].y" -1925.7142333984375;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 4555.71435546875;
	setAttr ".tgi[0].ni[4].y" 580;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 4248.5712890625;
	setAttr ".tgi[0].ni[5].y" -2967.142822265625;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" -420;
	setAttr ".tgi[0].ni[6].y" -51.428569793701172;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" 4940;
	setAttr ".tgi[0].ni[7].y" 485.71429443359375;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" 2091.428466796875;
	setAttr ".tgi[0].ni[8].y" -890;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" 501.42855834960938;
	setAttr ".tgi[0].ni[9].y" -202.85714721679688;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" 4940;
	setAttr ".tgi[0].ni[10].y" 387.14285278320312;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" -1962.857177734375;
	setAttr ".tgi[0].ni[11].y" 151.42857360839844;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" -112.85713958740234;
	setAttr ".tgi[0].ni[12].y" -461.42855834960938;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" 3634.28564453125;
	setAttr ".tgi[0].ni[13].y" -2125.71435546875;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" -1962.857177734375;
	setAttr ".tgi[0].ni[14].y" 447.14285278320312;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" -1655.7142333984375;
	setAttr ".tgi[0].ni[15].y" 250;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" -1962.857177734375;
	setAttr ".tgi[0].ni[16].y" 742.85711669921875;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" 808.5714111328125;
	setAttr ".tgi[0].ni[17].y" -1145.7142333984375;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" -1655.7142333984375;
	setAttr ".tgi[0].ni[18].y" 348.57144165039062;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" 3941.428466796875;
	setAttr ".tgi[0].ni[19].y" -2100;
	setAttr ".tgi[0].ni[19].nvs" 18304;
	setAttr ".tgi[0].ni[20].x" 3327.142822265625;
	setAttr ".tgi[0].ni[20].y" -2061.428466796875;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" -1962.857177734375;
	setAttr ".tgi[0].ni[21].y" 644.28570556640625;
	setAttr ".tgi[0].ni[21].nvs" 18304;
	setAttr ".tgi[0].ni[22].x" 4555.71435546875;
	setAttr ".tgi[0].ni[22].y" 481.42855834960938;
	setAttr ".tgi[0].ni[22].nvs" 18304;
	setAttr ".tgi[0].ni[23].x" 3020;
	setAttr ".tgi[0].ni[23].y" -1487.142822265625;
	setAttr ".tgi[0].ni[23].nvs" 18304;
	setAttr ".tgi[0].ni[24].x" 1135.7142333984375;
	setAttr ".tgi[0].ni[24].y" -905.71429443359375;
	setAttr ".tgi[0].ni[24].nvs" 18304;
	setAttr ".tgi[0].ni[25].x" 808.5714111328125;
	setAttr ".tgi[0].ni[25].y" -1437.142822265625;
	setAttr ".tgi[0].ni[25].nvs" 18304;
	setAttr ".tgi[0].ni[26].x" -1962.857177734375;
	setAttr ".tgi[0].ni[26].y" 52.857143402099609;
	setAttr ".tgi[0].ni[26].nvs" 18304;
	setAttr ".tgi[0].ni[27].x" 4940;
	setAttr ".tgi[0].ni[27].y" 270;
	setAttr ".tgi[0].ni[27].nvs" 18304;
	setAttr ".tgi[0].ni[28].x" 4248.5712890625;
	setAttr ".tgi[0].ni[28].y" -1037.142822265625;
	setAttr ".tgi[0].ni[28].nvs" 18304;
	setAttr ".tgi[0].ni[29].x" -727.14288330078125;
	setAttr ".tgi[0].ni[29].y" 141.42857360839844;
	setAttr ".tgi[0].ni[29].nvs" 18304;
	setAttr ".tgi[0].ni[30].x" 1135.7142333984375;
	setAttr ".tgi[0].ni[30].y" -1444.2857666015625;
	setAttr ".tgi[0].ni[30].nvs" 18304;
	setAttr ".tgi[0].ni[31].x" 2712.857177734375;
	setAttr ".tgi[0].ni[31].y" -1055.7142333984375;
	setAttr ".tgi[0].ni[31].nvs" 18304;
	setAttr ".tgi[0].ni[32].x" 2398.571533203125;
	setAttr ".tgi[0].ni[32].y" -960;
	setAttr ".tgi[0].ni[32].nvs" 18304;
	setAttr ".tgi[0].ni[33].x" 4940;
	setAttr ".tgi[0].ni[33].y" -2074.28564453125;
	setAttr ".tgi[0].ni[33].nvs" 18304;
	setAttr ".tgi[0].ni[34].x" 4555.71435546875;
	setAttr ".tgi[0].ni[34].y" -2432.857177734375;
	setAttr ".tgi[0].ni[34].nvs" 18304;
	setAttr ".tgi[0].ni[35].x" -1962.857177734375;
	setAttr ".tgi[0].ni[35].y" 348.57144165039062;
	setAttr ".tgi[0].ni[35].nvs" 18304;
	setAttr ".tgi[0].ni[36].x" 808.5714111328125;
	setAttr ".tgi[0].ni[36].y" -1301.4285888671875;
	setAttr ".tgi[0].ni[36].nvs" 18304;
	setAttr ".tgi[0].ni[37].x" -1962.857177734375;
	setAttr ".tgi[0].ni[37].y" 841.4285888671875;
	setAttr ".tgi[0].ni[37].nvs" 18304;
	setAttr ".tgi[0].ni[38].x" 4555.71435546875;
	setAttr ".tgi[0].ni[38].y" 284.28570556640625;
	setAttr ".tgi[0].ni[38].nvs" 18304;
	setAttr ".tgi[0].ni[39].x" 501.42855834960938;
	setAttr ".tgi[0].ni[39].y" -944.28570556640625;
	setAttr ".tgi[0].ni[39].nvs" 18304;
	setAttr ".tgi[0].ni[40].x" 4555.71435546875;
	setAttr ".tgi[0].ni[40].y" -1162.857177734375;
	setAttr ".tgi[0].ni[40].nvs" 18304;
	setAttr ".tgi[0].ni[41].x" 194.28572082519531;
	setAttr ".tgi[0].ni[41].y" -202.85714721679688;
	setAttr ".tgi[0].ni[41].nvs" 18304;
	setAttr ".tgi[0].ni[42].x" 4555.71435546875;
	setAttr ".tgi[0].ni[42].y" -3102.857177734375;
	setAttr ".tgi[0].ni[42].nvs" 18304;
	setAttr ".tgi[0].ni[43].x" 808.5714111328125;
	setAttr ".tgi[0].ni[43].y" -818.5714111328125;
	setAttr ".tgi[0].ni[43].nvs" 18304;
	setAttr ".tgi[0].ni[44].x" 1442.857177734375;
	setAttr ".tgi[0].ni[44].y" -924.28570556640625;
	setAttr ".tgi[0].ni[44].nvs" 18304;
	setAttr ".tgi[0].ni[45].x" 2712.857177734375;
	setAttr ".tgi[0].ni[45].y" -1798.5714111328125;
	setAttr ".tgi[0].ni[45].nvs" 18304;
	setAttr ".tgi[0].ni[46].x" 194.28572082519531;
	setAttr ".tgi[0].ni[46].y" -762.85711669921875;
	setAttr ".tgi[0].ni[46].nvs" 18304;
	setAttr ".tgi[0].ni[47].x" 1750;
	setAttr ".tgi[0].ni[47].y" -1495.7142333984375;
	setAttr ".tgi[0].ni[47].nvs" 18304;
	setAttr ".tgi[0].ni[48].x" -1962.857177734375;
	setAttr ".tgi[0].ni[48].y" 250;
	setAttr ".tgi[0].ni[48].nvs" 18304;
	setAttr ".tgi[0].ni[49].x" 2398.571533203125;
	setAttr ".tgi[0].ni[49].y" -1118.5714111328125;
	setAttr ".tgi[0].ni[49].nvs" 18304;
	setAttr ".tgi[0].ni[50].x" 3634.28564453125;
	setAttr ".tgi[0].ni[50].y" -1990;
	setAttr ".tgi[0].ni[50].nvs" 18304;
	setAttr ".tgi[0].ni[51].x" -1962.857177734375;
	setAttr ".tgi[0].ni[51].y" 545.71429443359375;
	setAttr ".tgi[0].ni[51].nvs" 18304;
	setAttr ".tgi[0].ni[52].x" 3327.142822265625;
	setAttr ".tgi[0].ni[52].y" -1117.142822265625;
	setAttr ".tgi[0].ni[52].nvs" 18304;
	setAttr ".tgi[0].ni[53].x" 3020;
	setAttr ".tgi[0].ni[53].y" -2007.142822265625;
	setAttr ".tgi[0].ni[53].nvs" 18304;
	setAttr ".tgi[0].ni[54].x" 4940;
	setAttr ".tgi[0].ni[54].y" -2191.428466796875;
	setAttr ".tgi[0].ni[54].nvs" 18304;
	setAttr ".tgi[0].ni[55].x" 4555.71435546875;
	setAttr ".tgi[0].ni[55].y" 382.85714721679688;
	setAttr ".tgi[0].ni[55].nvs" 18304;
	setAttr ".tgi[0].ni[56].x" -1655.7142333984375;
	setAttr ".tgi[0].ni[56].y" 447.14285278320312;
	setAttr ".tgi[0].ni[56].nvs" 18304;
	setAttr ".tgi[0].ni[57].x" 4248.5712890625;
	setAttr ".tgi[0].ni[57].y" -3084.28564453125;
	setAttr ".tgi[0].ni[57].nvs" 18304;
	setAttr ".tgi[0].ni[58].x" 3941.428466796875;
	setAttr ".tgi[0].ni[58].y" -861.4285888671875;
	setAttr ".tgi[0].ni[58].nvs" 18304;
	setAttr ".tgi[0].ni[59].x" -1337.72021484375;
	setAttr ".tgi[0].ni[59].y" 381.06640625;
	setAttr ".tgi[0].ni[59].nvs" 18306;
	setAttr ".tgi[0].ni[60].x" -727.14288330078125;
	setAttr ".tgi[0].ni[60].y" 297.14285278320312;
	setAttr ".tgi[0].ni[60].nvs" 18304;
	setAttr ".tgi[0].ni[61].x" 1750;
	setAttr ".tgi[0].ni[61].y" -841.4285888671875;
	setAttr ".tgi[0].ni[61].nvs" 18304;
	setAttr ".tgi[0].ni[62].x" 1135.7142333984375;
	setAttr ".tgi[0].ni[62].y" -692.85711669921875;
	setAttr ".tgi[0].ni[62].nvs" 18304;
	setAttr ".tgi[0].ni[63].x" 1442.857177734375;
	setAttr ".tgi[0].ni[63].y" -1430;
	setAttr ".tgi[0].ni[63].nvs" 18304;
	setAttr ".tgi[0].ni[64].x" 2398.571533203125;
	setAttr ".tgi[0].ni[64].y" -1725.7142333984375;
	setAttr ".tgi[0].ni[64].nvs" 18304;
	setAttr ".tgi[0].ni[65].x" 3634.28564453125;
	setAttr ".tgi[0].ni[65].y" 110;
	setAttr ".tgi[0].ni[65].nvs" 18306;
	setAttr ".tgi[0].ni[66].x" 1750;
	setAttr ".tgi[0].ni[66].y" -1111.4285888671875;
	setAttr ".tgi[0].ni[66].nvs" 18304;
	setAttr ".tgi[0].ni[67].x" 4940;
	setAttr ".tgi[0].ni[67].y" -2492.857177734375;
	setAttr ".tgi[0].ni[67].nvs" 18304;
	setAttr ".tgi[0].ni[68].x" 2091.428466796875;
	setAttr ".tgi[0].ni[68].y" -1594.2857666015625;
	setAttr ".tgi[0].ni[68].nvs" 18304;
	setAttr ".tgi[0].ni[69].x" -1041.4285888671875;
	setAttr ".tgi[0].ni[69].y" 222.85714721679688;
	setAttr ".tgi[0].ni[69].nvs" 18304;
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
	setAttr -s 28 ".u";
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
select -ne :ikSystem;
connectAttr "decomposeMatrix1.ot" "out1.t";
connectAttr "decomposeMatrix1.or" "out1.r";
connectAttr "decomposeMatrix1.os" "out1.s";
connectAttr "decomposeMatrix2.ot" "out2.t";
connectAttr "decomposeMatrix2.or" "out2.r";
connectAttr "decomposeMatrix2.os" "out2.s";
connectAttr "decomposeMatrix3.ot" "out3.t";
connectAttr "decomposeMatrix3.or" "out3.r";
connectAttr "decomposeMatrix3.os" "out3.s";
connectAttr "dag.fkIk" "ik:arm_ik_anm_grp.v";
connectAttr "decomposeMatrix4.ot" "ik:arm_ik_anm_offset.t";
connectAttr "makeNurbCircle1.oc" "ik:arm_ik_swivel_anmShape.cr";
connectAttr "ik:locator1_pointConstraint1.ctx" "ik:arm_ik_swivelLineLoc_anm.tx";
connectAttr "ik:locator1_pointConstraint1.cty" "ik:arm_ik_swivelLineLoc_anm.ty";
connectAttr "ik:locator1_pointConstraint1.ctz" "ik:arm_ik_swivelLineLoc_anm.tz";
connectAttr "ik:arm_ik_swivelLineLoc_anm.pim" "ik:locator1_pointConstraint1.cpim"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anm.rp" "ik:locator1_pointConstraint1.crp";
connectAttr "ik:arm_ik_swivelLineLoc_anm.rpt" "ik:locator1_pointConstraint1.crt"
		;
connectAttr "out2.t" "ik:locator1_pointConstraint1.tg[0].tt";
connectAttr "out2.rp" "ik:locator1_pointConstraint1.tg[0].trp";
connectAttr "out2.rpt" "ik:locator1_pointConstraint1.tg[0].trt";
connectAttr "out2.pm" "ik:locator1_pointConstraint1.tg[0].tpm";
connectAttr "ik:locator1_pointConstraint1.w0" "ik:locator1_pointConstraint1.tg[0].tw"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anmShape.wm" "ik:arm_ik_swivelLineAnn_anm.dom"
		 -na;
connectAttr "decomposeGuide01LocalTm.ot" "ik:arm_ik_ikChain_rig.t";
connectAttr "decomposeGuide01LocalTm.or" "ik:arm_ik_ikChain_rig.r";
connectAttr "ik:arm_ik_01_rig.msg" "ik:arm_ik_ikHandle_rig.hsj";
connectAttr "ik:arm_ik_ikEffector_rig.hp" "ik:arm_ik_ikHandle_rig.hee";
connectAttr "ikRPsolver.msg" "ik:arm_ik_ikHandle_rig.hsv";
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.ctx" "ik:arm_ik_ikHandle_rig.tx"
		;
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.cty" "ik:arm_ik_ikHandle_rig.ty"
		;
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.ctz" "ik:arm_ik_ikHandle_rig.tz"
		;
connectAttr "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.ctx" "ik:arm_ik_ikHandle_rig.pvx"
		;
connectAttr "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.cty" "ik:arm_ik_ikHandle_rig.pvy"
		;
connectAttr "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.ctz" "ik:arm_ik_ikHandle_rig.pvz"
		;
connectAttr "ik:arm_ik_ikHandle_rig.pim" "ik:arm_ik_ikHandle_rig_softIkConstraint1.cpim"
		;
connectAttr "ik:arm_ik_ikHandle_rig.rp" "ik:arm_ik_ikHandle_rig_softIkConstraint1.crp"
		;
connectAttr "ik:arm_ik_ikHandle_rig.rpt" "ik:arm_ik_ikHandle_rig_softIkConstraint1.crt"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.t" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].tt"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.rp" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].trp"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.rpt" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].trt"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.pm" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].tpm"
		;
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.w0" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].tw"
		;
connectAttr "ik:arm_ik_ikChain_rig.t" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].tt"
		;
connectAttr "ik:arm_ik_ikChain_rig.rp" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].trp"
		;
connectAttr "ik:arm_ik_ikChain_rig.rpt" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].trt"
		;
connectAttr "ik:arm_ik_ikChain_rig.pm" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].tpm"
		;
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.w1" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].tw"
		;
connectAttr "ik:arm_ik_anm.t" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].tt"
		;
connectAttr "ik:arm_ik_anm.rp" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].trp"
		;
connectAttr "ik:arm_ik_anm.rpt" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].trt"
		;
connectAttr "ik:arm_ik_anm.pm" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].tpm"
		;
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.w2" "ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].tw"
		;
connectAttr "ik:softik:out.outRatio" "ik:arm_ik_ikHandle_rig_softIkConstraint1.w0"
		;
connectAttr "reverse1.ox" "ik:arm_ik_ikHandle_rig_softIkConstraint1.w1";
connectAttr "ik:arm_ik_ikHandle_rig.pim" "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.cpim"
		;
connectAttr "ik:arm_ik_01_rig.pm" "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.ps"
		;
connectAttr "ik:arm_ik_01_rig.t" "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.crp"
		;
connectAttr "ik:arm_ik_swivel_anm.t" "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].tt"
		;
connectAttr "ik:arm_ik_swivel_anm.rp" "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].trp"
		;
connectAttr "ik:arm_ik_swivel_anm.rpt" "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].trt"
		;
connectAttr "ik:arm_ik_swivel_anm.pm" "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].tpm"
		;
connectAttr "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.w0" "ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].tw"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.ctx" "ik:arm_ik_ikHandleTarget_rig.tx"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.cty" "ik:arm_ik_ikHandleTarget_rig.ty"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.ctz" "ik:arm_ik_ikHandleTarget_rig.tz"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.pim" "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.cpim"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.rp" "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.crp"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.rpt" "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.crt"
		;
connectAttr "ik:arm_ik_anm.t" "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].tt"
		;
connectAttr "ik:arm_ik_anm.rp" "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].trp"
		;
connectAttr "ik:arm_ik_anm.rpt" "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].trt"
		;
connectAttr "ik:arm_ik_anm.pm" "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].tpm"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.w0" "ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].tw"
		;
connectAttr "multiplyDivide13.o" "ik:arm_ik_02_rig.t";
connectAttr "multiplyDivide14.o" "ik:arm_ik_03_rig.t";
connectAttr "ik:arm_ik_03_rig_orientConstraint1.crx" "ik:arm_ik_03_rig.rx";
connectAttr "ik:arm_ik_03_rig_orientConstraint1.cry" "ik:arm_ik_03_rig.ry";
connectAttr "ik:arm_ik_03_rig_orientConstraint1.crz" "ik:arm_ik_03_rig.rz";
connectAttr "ik:arm_ik_03_rig.ro" "ik:arm_ik_03_rig_orientConstraint1.cro";
connectAttr "ik:arm_ik_03_rig.pim" "ik:arm_ik_03_rig_orientConstraint1.cpim";
connectAttr "ik:arm_ik_03_rig.jo" "ik:arm_ik_03_rig_orientConstraint1.cjo";
connectAttr "ik:arm_ik_03_rig.is" "ik:arm_ik_03_rig_orientConstraint1.is";
connectAttr "ik:arm_ik_anm.r" "ik:arm_ik_03_rig_orientConstraint1.tg[0].tr";
connectAttr "ik:arm_ik_anm.ro" "ik:arm_ik_03_rig_orientConstraint1.tg[0].tro";
connectAttr "ik:arm_ik_anm.pm" "ik:arm_ik_03_rig_orientConstraint1.tg[0].tpm";
connectAttr "ik:arm_ik_03_rig_orientConstraint1.w0" "ik:arm_ik_03_rig_orientConstraint1.tg[0].tw"
		;
connectAttr "ik:arm_ik_03_rig.tx" "ik:arm_ik_ikEffector_rig.tx";
connectAttr "ik:arm_ik_03_rig.ty" "ik:arm_ik_ikEffector_rig.ty";
connectAttr "ik:arm_ik_03_rig.tz" "ik:arm_ik_ikEffector_rig.tz";
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
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "ik:arm_ik_anm.softIkRatio" "multiplyDivide1.i1x";
connectAttr "ik:softik:out.outRatio" "reverse1.ix";
connectAttr "ik:arm_ik_ikHandleTarget_rig.wm" "ik:softik:inn.inMatrixE";
connectAttr "ik:arm_ik_ikChain_rig.wm" "ik:softik:inn.inMatrixS";
connectAttr "ik:arm_ik_anm.stretch" "ik:softik:inn.inStretch";
connectAttr "getLimbLength.o" "ik:softik:inn.inChainLength";
connectAttr "multiplyDivide1.ox" "ik:softik:inn.inRatio";
connectAttr "ik:softik:multiplyDivide3.ox" "ik:softik:multiplyDivide4.i2x";
connectAttr "ik:softik:multiplyDivide2.ox" "ik:softik:multiplyDivide3.i1x";
connectAttr "ik:softik:multiplyDivide5.ox" "ik:softik:plusMinusAverage4.i1[0]";
connectAttr "ik:softik:plusMinusAverage1.o1" "ik:softik:plusMinusAverage4.i1[1]"
		;
connectAttr "ik:softik:inn.inMatrixE" "ik:softik:distanceBetween1.im2";
connectAttr "ik:softik:inn.inMatrixS" "ik:softik:distanceBetween1.im1";
connectAttr "ik:softik:plusMinusAverage1.o1" "ik:softik:condition2.st";
connectAttr "ik:softik:multiplyDivide6.ox" "ik:softik:condition2.ctr";
connectAttr "ik:softik:distanceBetween1.d" "ik:softik:condition2.ft";
connectAttr "ik:softik:multiplyDivide1.ox" "ik:softik:clamp1.ipr";
connectAttr "ik:softik:multiplyDivide4.ox" "ik:softik:plusMinusAverage3.i1[1]";
connectAttr "ik:softik:inn.inStretch" "ik:softik:blendTwoAttr2.ab";
connectAttr "ik:softik:condition2.ocr" "ik:softik:blendTwoAttr2.i[1]";
connectAttr "ik:softik:multiplyDivide1.ox" "ik:softik:multiplyDivide5.i1x";
connectAttr "ik:softik:plusMinusAverage3.o1" "ik:softik:multiplyDivide5.i2x";
connectAttr "ik:softik:multiplyDivide7.ox" "ik:softik:out.outRatio";
connectAttr "ik:softik:blendTwoAttr2.o" "ik:softik:out.outStretch";
connectAttr "ik:softik:inn.inChainLength" "ik:softik:multiplyDivide1.i1x";
connectAttr "ik:softik:inn.inRatio" "ik:softik:multiplyDivide1.i2x";
connectAttr "ik:softik:inn.inChainLength" "ik:softik:plusMinusAverage1.i1[0]";
connectAttr "ik:softik:multiplyDivide1.ox" "ik:softik:plusMinusAverage1.i1[1]";
connectAttr "ik:softik:plusMinusAverage4.o1" "ik:softik:condition1.ctr";
connectAttr "ik:softik:distanceBetween1.d" "ik:softik:condition1.cfr";
connectAttr "ik:softik:multiplyDivide2.ox" "ik:softik:condition1.ft";
connectAttr "ik:softik:plusMinusAverage2.o1" "ik:softik:multiplyDivide2.i1x";
connectAttr "ik:softik:clamp1.opr" "ik:softik:multiplyDivide2.i2x";
connectAttr "ik:softik:blendTwoAttr1.o" "ik:softik:multiplyDivide7.i1x";
connectAttr "ik:softik:distanceBetween1.d" "ik:softik:multiplyDivide7.i2x";
connectAttr "ik:softik:distanceBetween1.d" "ik:softik:plusMinusAverage2.i1[0]";
connectAttr "ik:softik:plusMinusAverage1.o1" "ik:softik:plusMinusAverage2.i1[1]"
		;
connectAttr "ik:softik:inn.inStretch" "ik:softik:blendTwoAttr1.ab";
connectAttr "ik:softik:condition1.ocr" "ik:softik:blendTwoAttr1.i[0]";
connectAttr "ik:softik:distanceBetween1.d" "ik:softik:blendTwoAttr1.i[1]";
connectAttr "ik:softik:distanceBetween1.d" "ik:softik:multiplyDivide6.i1x";
connectAttr "ik:softik:plusMinusAverage4.o1" "ik:softik:multiplyDivide6.i2x";
connectAttr "inn1.m" "inn.Guide01_LocalTm";
connectAttr "inn2.m" "inn.Guide02_LocalTm";
connectAttr "inn3.m" "inn.Guide03_LocalTm";
connectAttr "inn.Guide01_LocalTm" "decomposeGuide01LocalTm.imat";
connectAttr "inn.Guide02_LocalTm" "decomposeGuide02LocalTm.imat";
connectAttr "inn.Guide03_LocalTm" "decomposeGuide03LocalTm.imat";
connectAttr "composeMatrix1.omat" "out.outCtrlSwivelOffsetTm";
connectAttr "getGuide03WorldTm.o" "out.outCtrlIkOffsetTm";
connectAttr "decomposeGuide02LocalTm.ot" "getLimbSegment1Length.p2";
connectAttr "decomposeGuide03LocalTm.ot" "getLimbSegment2Length.p2";
connectAttr "getLimbSegment1Length.d" "getLimbLength.i1";
connectAttr "getLimbSegment2Length.d" "getLimbLength.i2";
connectAttr "ik:softik:out.outStretch" "multiplyDivide13.i2x";
connectAttr "ik:softik:out.outStretch" "multiplyDivide13.i2y";
connectAttr "ik:softik:out.outStretch" "multiplyDivide13.i2z";
connectAttr "decomposeGuide02LocalTm.ot" "multiplyDivide13.i1";
connectAttr "ik:softik:out.outStretch" "multiplyDivide14.i2x";
connectAttr "ik:softik:out.outStretch" "multiplyDivide14.i2y";
connectAttr "decomposeGuide03LocalTm.ot" "multiplyDivide14.i1";
connectAttr "inn.Guide03_LocalTm" "getGuide03WorldTm.i[0]";
connectAttr "getGuide02WorldTm.o" "getGuide03WorldTm.i[1]";
connectAttr "out.outCtrlIkOffsetTm" "decomposeMatrix4.imat";
connectAttr "getLimbLength.o" "getSwivelDistance.i1x";
connectAttr "inn.swivelDistanceRatio" "getSwivelDistance.i2x";
connectAttr "getLimbSegment1Length.d" "getLimbRatio.i1x";
connectAttr "getLimbLength.o" "getLimbRatio.i2x";
connectAttr "decomposeGuide03WorldTm1.ot" "getLimbAim.i3[0]";
connectAttr "decomposeGuide01LocalTm.ot" "getLimbAim.i3[1]";
connectAttr "getLimbRatio.ox" "getLimbMiddleAim.i2x";
connectAttr "getLimbRatio.ox" "getLimbMiddleAim.i2y";
connectAttr "getLimbRatio.ox" "getLimbMiddleAim.i2z";
connectAttr "getLimbAim.o3" "getLimbMiddleAim.i1";
connectAttr "decomposeGuide01LocalTm.ot" "getKneePosProjectedOnLimbDir.i3[0]";
connectAttr "getLimbMiddleAim.o" "getKneePosProjectedOnLimbDir.i3[1]";
connectAttr "decomposeGuide02WorldTm.ot" "getKneeDirection.i3[0]";
connectAttr "getKneePosProjectedOnLimbDir.o3" "getKneeDirection.i3[1]";
connectAttr "inn.Guide02_LocalTm" "getGuide02WorldTm.i[0]";
connectAttr "inn.Guide01_LocalTm" "getGuide02WorldTm.i[1]";
connectAttr "getGuide02WorldTm.o" "decomposeGuide02WorldTm.imat";
connectAttr "getKneeDirection.o3" "getKneeDirectionNormalized.i1";
connectAttr "getKneeDirectionNormalized.o" "getKneeDirectionOffset.i1";
connectAttr "getSwivelDistance.ox" "getKneeDirectionOffset.i2x";
connectAttr "getSwivelDistance.ox" "getKneeDirectionOffset.i2y";
connectAttr "getSwivelDistance.ox" "getKneeDirectionOffset.i2z";
connectAttr "decomposeGuide02WorldTm.ot" "getSwivelDefaultPos.i3[0]";
connectAttr "getKneeDirectionOffset.o" "getSwivelDefaultPos.i3[1]";
connectAttr "out.outInf01LocalTm" "decomposeMatrix1.imat";
connectAttr "out.outInf02LocalTm" "decomposeMatrix2.imat";
connectAttr "out.outInf03LocalTm" "decomposeMatrix3.imat";
connectAttr "getSwivelDefaultPos.o3" "composeMatrix1.it";
connectAttr "getGuide03WorldTm.o" "decomposeGuide03WorldTm1.imat";
connectAttr "out1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "ik:softik:multiplyDivide6.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "decomposeMatrix1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "ik:arm_ik_ikChain_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn";
connectAttr "out3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn";
connectAttr "getKneeDirection.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "ik:arm_ik_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "guide_02_translateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn";
connectAttr "ik:softik:multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "guide_02_rotateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn"
		;
connectAttr "inn1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn";
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "decomposeGuide03WorldTm1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn"
		;
connectAttr "inn3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn";
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn";
connectAttr "ik:softik:blendTwoAttr1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "guide_02_rotateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn"
		;
connectAttr "decomposeMatrix3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[22].dn"
		;
connectAttr "getSwivelDefaultPos.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[23].dn"
		;
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[24].dn";
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn"
		;
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[26].dn"
		;
connectAttr "ik:arm_ik_03_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[27].dn"
		;
connectAttr "out2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[28].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[29].dn"
		;
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[30].dn"
		;
connectAttr "getKneeDirectionOffset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[31].dn"
		;
connectAttr "getKneeDirectionNormalized.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[32].dn"
		;
connectAttr "ik:arm_ik_ikHandle_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[33].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[34].dn"
		;
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[35].dn"
		;
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[36].dn"
		;
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[37].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[38].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[39].dn"
		;
connectAttr "ik:locator1_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[40].dn"
		;
connectAttr "getGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[41].dn"
		;
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[42].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[43].dn"
		;
connectAttr "getLimbMiddleAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[44].dn"
		;
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[45].dn"
		;
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[46].dn"
		;
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[47].dn"
		;
connectAttr "guide_02_scaleX.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[48].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[49].dn"
		;
connectAttr "ik:softik:blendTwoAttr2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[50].dn"
		;
connectAttr "guide_02_translateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[51].dn"
		;
connectAttr "composeMatrix1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[52].dn";
connectAttr "ik:softik:condition1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[53].dn"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[54].dn"
		;
connectAttr "decomposeMatrix4.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[55].dn"
		;
connectAttr "inn2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[56].dn";
connectAttr "reverse1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[57].dn";
connectAttr "decomposeMatrix2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[58].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[59].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[60].dn"
		;
connectAttr "getKneePosProjectedOnLimbDir.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[61].dn"
		;
connectAttr "getLimbAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[62].dn";
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[63].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[64].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[65].dn";
connectAttr "decomposeGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[66].dn"
		;
connectAttr "ik:arm_ik_02_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[67].dn"
		;
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[68].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[69].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeGuide02LocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeGuide03LocalTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getLimbSegment1Length.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLimbSegment2Length.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getLimbLength.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide13.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide14.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getGuide03WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeMatrix4.msg" ":defaultRenderUtilityList1.u" -na;
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
connectAttr "composeMatrix1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "decomposeGuide03WorldTm1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "ikRPsolver.msg" ":ikSystem.sol" -na;
// End of ik.ma
