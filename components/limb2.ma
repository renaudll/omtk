//Maya ASCII 2017ff05 scene
//Name: limb2.ma
//Last modified: Thu, Apr 19, 2018 09:00:45 PM
//Codeset: UTF-8
requires maya "2017ff05";
requires -nodeType "decomposeMatrix" "matrixNodes" "1.0";
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
fileInfo "omtk.component.uid" "9e38b6df-b42c-5f6d-b243-bbfeb645518a";
fileInfo "omtk.component.name" "IK3";
createNode transform -s -n "persp";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000917";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 21.406821015558286 6.2491289053982797 14.794906471481227 ;
	setAttr ".r" -type "double3" -9.9383527296052421 50.600000000004776 -2.5054370439965773e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000918";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 26.328657086291436;
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
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "out2" -p "out1";
	rename -uid "699D7980-0000-0F71-5AB5-BDAA00000927";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
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
	setAttr "._graphpos" -type "float2" 365.71429 308.57144 ;
createNode transform -n "anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002E8";
createNode transform -n "arm_atts_anm_offset" -p "anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F4";
createNode transform -n "arm_atts_anm" -p "arm_atts_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F3";
	addAttr -ci true -k true -sn "fkIk" -ln "fkIk" -dv 1 -min 0 -max 1 -at "double";
	setAttr -k on ".ro";
createNode nurbsCurve -n "arm_atts_anmShape" -p "arm_atts_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F2";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 25 0 no 3
		26 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25
		26
		0 0 0.65781884989194483
		0 0.46047319492436134 0.46047319492436134
		0 0.65781884989194483 0
		0 0.46047319492436134 -0.46047319492436134
		0 0 -0.65781884989194483
		0 -0.46047319492436134 -0.46047319492436134
		0 -0.65781884989194483 0
		0 -0.46047319492436134 0.46047319492436134
		0 0 0.65781884989194483
		-0.46047319492436134 0 0.46047319492436134
		-0.65781884989194483 0 0
		-0.46047319492436134 0.46047319492436134 0
		0 0.65781884989194483 0
		0.46047319492436134 0.46047319492436134 0
		0.65781884989194483 0 0
		0.46047319492436134 0 -0.46047319492436134
		0 0 -0.65781884989194483
		-0.46047319492436134 0 -0.46047319492436134
		-0.65781884989194483 0 0
		-0.46047319492436134 -0.46047319492436134 0
		0 -0.65781884989194483 0
		0.46047319492436134 -0.46047319492436134 0
		0.65781884989194483 0 0
		0.46047319492436134 0 0.46047319492436134
		0 0 0.65781884989194483
		-0.46047319492436134 0 0.46047319492436134
		;
createNode parentConstraint -n "arm_atts_anm_offset_parentConstraint1" -p "arm_atts_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F5";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "infl_03W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" -90 -135 90 ;
	setAttr ".rst" -type "double3" -5.8878467200641567e-16 8.8817841970012523e-16 -1.3322676295501878e-15 ;
	setAttr ".rsrr" -type "double3" 90 -45.000000000000014 -90 ;
	setAttr -k on ".w0";
createNode transform -n "arm_elbow01_anm_offset" -p "anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000401";
	setAttr ".t" -type "double3" -3.9252311467094368e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".r" -type "double3" 89.999999999999986 44.999999999999986 -90.000000000000057 ;
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
createNode transform -n "guides";
	rename -uid "F4C8C980-0000-752C-5AD9-37E500000AB2";
createNode joint -n "guide_01" -p "guides";
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
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "guide_02" -p "guide_01";
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
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
createNode joint -n "guide_03" -p "guide_02";
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
	setAttr "._graphpos" -type "float2" 365.71429 308.57144 ;
createNode joint -n "FK3:out1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009CE";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "FK3:out2" -p "FK3:out1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009CF";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
createNode joint -n "FK3:out3" -p "FK3:out2";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D0";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 365.71429 308.57144 ;
createNode transform -n "FK3:dag";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D1";
createNode transform -n "FK3:root" -p "FK3:dag";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D2";
createNode transform -n "FK3:ctrl1_zero" -p "FK3:root";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D3";
createNode transform -n "FK3:ctrl1" -p "FK3:ctrl1_zero";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D4";
createNode nurbsCurve -n "FK3:ctrl1Shape" -p "FK3:ctrl1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D5";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "FK3:ctrl2_zero" -p "FK3:ctrl1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D6";
createNode transform -n "FK3:arm_fk_infl_02_anm" -p "FK3:ctrl2_zero";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D7";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".rz";
createNode nurbsCurve -n "FK3:ctrl2" -p "FK3:arm_fk_infl_02_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D8";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "FK3:ctrl3_zero" -p "FK3:arm_fk_infl_02_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009D9";
createNode transform -n "FK3:ctrl3" -p "FK3:ctrl3_zero";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009DA";
createNode nurbsCurve -n "FK3:ctrl3Shape" -p "FK3:ctrl3";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009DB";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode joint -n "FK3:inn1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009DC";
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
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "FK3:inn2" -p "FK3:inn1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009DD";
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
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
createNode joint -n "FK3:inn3" -p "FK3:inn2";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009DE";
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
	setAttr "._graphpos" -type "float2" 365.71429 308.57144 ;
createNode joint -n "IK3:out1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A2A";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "IK3:out2" -p "IK3:out1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A2B";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
createNode joint -n "IK3:out3" -p "IK3:out2";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A2C";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 365.71429 308.57144 ;
createNode transform -n "IK3:anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A2D";
createNode transform -n "IK3:arm_atts_anm_offset" -p "IK3:anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A2E";
createNode transform -n "IK3:arm_atts_anm" -p "IK3:arm_atts_anm_offset";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A2F";
	addAttr -ci true -k true -sn "fkIk" -ln "fkIk" -dv 1 -min 0 -max 1 -at "double";
	setAttr -k on ".ro";
	setAttr -k on ".fkIk";
createNode nurbsCurve -n "IK3:arm_atts_anmShape" -p "IK3:arm_atts_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A30";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 25 0 no 3
		26 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25
		26
		0 0 0.65781884989194483
		0 0.46047319492436134 0.46047319492436134
		0 0.65781884989194483 0
		0 0.46047319492436134 -0.46047319492436134
		0 0 -0.65781884989194483
		0 -0.46047319492436134 -0.46047319492436134
		0 -0.65781884989194483 0
		0 -0.46047319492436134 0.46047319492436134
		0 0 0.65781884989194483
		-0.46047319492436134 0 0.46047319492436134
		-0.65781884989194483 0 0
		-0.46047319492436134 0.46047319492436134 0
		0 0.65781884989194483 0
		0.46047319492436134 0.46047319492436134 0
		0.65781884989194483 0 0
		0.46047319492436134 0 -0.46047319492436134
		0 0 -0.65781884989194483
		-0.46047319492436134 0 -0.46047319492436134
		-0.65781884989194483 0 0
		-0.46047319492436134 -0.46047319492436134 0
		0 -0.65781884989194483 0
		0.46047319492436134 -0.46047319492436134 0
		0.65781884989194483 0 0
		0.46047319492436134 0 0.46047319492436134
		0 0 0.65781884989194483
		-0.46047319492436134 0 0.46047319492436134
		;
createNode parentConstraint -n "IK3:arm_atts_anm_offset_parentConstraint1" -p "IK3:arm_atts_anm_offset";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A31";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "infl_03W0" -dv 1 -min 0 -at "double";
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
	setAttr ".lr" -type "double3" -90 -135 90 ;
	setAttr ".rst" -type "double3" -5.8878467200641567e-16 8.8817841970012523e-16 -1.3322676295501878e-15 ;
	setAttr ".rsrr" -type "double3" 90 -45.000000000000014 -90 ;
	setAttr -k on ".w0";
createNode transform -n "IK3:arm_elbow01_anm_offset" -p "IK3:anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A32";
	setAttr ".t" -type "double3" -3.9252311467094368e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".r" -type "double3" 89.999999999999986 44.999999999999986 -90.000000000000057 ;
createNode transform -n "IK3:arm_elbow01_anm" -p "IK3:arm_elbow01_anm_offset";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A33";
	setAttr -k on ".ro";
createNode nurbsCurve -n "IK3:arm_elbow01_anmShape" -p "IK3:arm_elbow01_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A34";
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
createNode transform -n "IK3:ik:arm_ik_anm_grp" -p "IK3:anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A35";
createNode transform -n "IK3:ik:arm_ik_anm_offset" -p "IK3:ik:arm_ik_anm_grp";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A36";
createNode transform -n "IK3:ik:arm_ik_anm" -p "IK3:ik:arm_ik_anm_offset";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A37";
	addAttr -ci true -k true -sn "softIkRatio" -ln "softIkRatio" -nn "SoftIK" -min 
		0 -max 50 -at "double";
	addAttr -ci true -k true -sn "stretch" -ln "stretch" -nn "Stretch" -min 0 -max 1 
		-at "double";
	setAttr ".r" -type "double3" 180 -45 -90 ;
	setAttr -k on ".ro";
	setAttr -k on ".softIkRatio";
	setAttr -k on ".stretch" 1;
createNode nurbsCurve -n "IK3:ik:arm_ik_anmShape" -p "IK3:ik:arm_ik_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A38";
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
createNode transform -n "IK3:ik:arm_ik_swivel_anm_offset" -p "IK3:ik:arm_ik_anm_grp";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A39";
createNode transform -n "IK3:ik:arm_ik_swivel_anm" -p "IK3:ik:arm_ik_swivel_anm_offset";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A3A";
	addAttr -ci true -k true -sn "space" -ln "space" -min -2 -max 0 -en "World=-2:arm=0" 
		-at "enum";
	setAttr -k on ".space" -2;
createNode nurbsCurve -n "IK3:ik:arm_ik_swivel_anmShape" -p "IK3:ik:arm_ik_swivel_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A3B";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "IK3:ik:arm_ik_swivelLineLoc_anm" -p "IK3:ik:arm_ik_swivel_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A3C";
	setAttr ".v" no;
createNode locator -n "IK3:ik:arm_ik_swivelLineLoc_anmShape" -p "IK3:ik:arm_ik_swivelLineLoc_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A3D";
	setAttr -k off ".v";
createNode pointConstraint -n "IK3:ik:locator1_pointConstraint1" -p "IK3:ik:arm_ik_swivelLineLoc_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A3E";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "infl_02W0" -dv 1 -min 0 -at "double";
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
createNode annotationShape -n "IK3:ik:arm_ik_swivelLineAnn_anm" -p "IK3:ik:arm_ik_swivel_anm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A3F";
	setAttr -k off ".v";
createNode transform -n "IK3:dag";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A40";
	addAttr -ci true -sn "globalScale" -ln "globalScale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "fkIk" -ln "fkIk" -dv 1 -min 0 -max 1 -at "double";
	setAttr ".v" no;
	setAttr -k on ".fkIk";
createNode transform -n "IK3:ik:arm_ik_data_grp" -p "IK3:dag";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A41";
	addAttr -ci true -sn "globalScale" -ln "globalScale" -dv 1 -at "double";
createNode transform -n "IK3:ik:arm_ik_ikChain_rig" -p "IK3:ik:arm_ik_data_grp";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A42";
createNode ikHandle -n "IK3:ik:arm_ik_ikHandle_rig" -p "IK3:ik:arm_ik_ikChain_rig";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A43";
	setAttr ".r" -type "double3" -45.000000000000007 90 0 ;
	setAttr ".s" -type "double3" 0.99999999999999956 1 1 ;
	setAttr ".roc" yes;
createNode pointConstraint -n "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1" -p "IK3:ik:arm_ik_ikHandle_rig";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A44";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_ik_ikHandleTarget_rigW0" -dv 
		1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "arm_ik_ikChain_rigW1" -dv 1 -min 0 
		-at "double";
	addAttr -dcb 0 -ci true -k true -sn "w2" -ln "arm_ik_anmW2" -dv 1 -min 0 -at "double";
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
createNode poleVectorConstraint -n "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1" 
		-p "IK3:ik:arm_ik_ikHandle_rig";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A45";
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
createNode transform -n "IK3:ik:arm_ik_ikHandleTarget_rig" -p "IK3:ik:arm_ik_data_grp";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A46";
createNode pointConstraint -n "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1" 
		-p "IK3:ik:arm_ik_ikHandleTarget_rig";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A47";
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
createNode joint -n "IK3:ik:arm_ik_01_rig" -p "IK3:ik:arm_ik_data_grp";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A48";
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
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "IK3:ik:arm_ik_02_rig" -p "IK3:ik:arm_ik_01_rig";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A49";
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
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
createNode joint -n "IK3:ik:arm_ik_03_rig" -p "IK3:ik:arm_ik_02_rig";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A4A";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" 365.71429 308.57144 ;
createNode orientConstraint -n "IK3:ik:arm_ik_03_rig_orientConstraint1" -p "IK3:ik:arm_ik_03_rig";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A4B";
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
	setAttr ".lr" -type "double3" 90 0 -8.9959671327898901e-15 ;
	setAttr ".o" -type "double3" -89.999999999999986 0 0 ;
	setAttr -k on ".w0";
createNode ikEffector -n "IK3:ik:arm_ik_ikEffector_rig" -p "IK3:ik:arm_ik_02_rig";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A4C";
	setAttr ".v" no;
	setAttr ".hd" yes;
createNode joint -n "IK3:inn1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A4D";
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
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "IK3:inn2" -p "IK3:inn1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A4E";
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
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
createNode joint -n "IK3:inn3" -p "IK3:inn2";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A4F";
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
	setAttr "._graphpos" -type "float2" 365.71429 308.57144 ;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "6087C980-0000-3D03-5AD9-3B380000098F";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "6087C980-0000-3D03-5AD9-3B3800000990";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "6087C980-0000-3D03-5AD9-3B3800000991";
createNode displayLayerManager -n "layerManager";
	rename -uid "6087C980-0000-3D03-5AD9-3B3800000992";
createNode displayLayer -n "defaultLayer";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000923";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "6087C980-0000-3D03-5AD9-3B3800000994";
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
		+ "            -shadows 0\n            -captureSequenceNumber -1\n            -width 609\n            -height 716\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n"
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
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 609\\n    -height 716\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 609\\n    -height 716\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "699D7980-0000-0F71-5AB5-BDD500000933";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode multiplyDivide -n "multiplyDivide1";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002FC";
	setAttr ".i2" -type "float3" 0.0099999998 1 1 ;
createNode multiplyDivide -n "multiplyDivide9";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000030F";
	setAttr ".i1" -type "float3" 7.0710678 0 0 ;
createNode multiplyDivide -n "multiplyDivide10";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000312";
	setAttr ".i2" -type "float3" 3.5355339 0 3.9252311e-16 ;
createNode multiplyDivide -n "multiplyDivide11";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000313";
	setAttr ".i2" -type "float3" 3.5355339 -6.2803697e-16 -1.9626156e-16 ;
createNode network -n "ik:softik:inn";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D5";
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
createNode network -n "ik:softik:metadata";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D6";
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
createNode multiplyDivide -n "ik:softik:multiplyDivide4";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D7";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 2.7182817 0 0 ;
createNode multiplyDivide -n "ik:softik:multiplyDivide3";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D8";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode plusMinusAverage -n "ik:softik:plusMinusAverage4";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D9";
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode distanceBetween -n "ik:softik:distanceBetween1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DA";
createNode condition -n "ik:softik:condition2";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DB";
	setAttr ".op" 2;
createNode clamp -n "ik:softik:clamp1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DC";
	setAttr ".mn" -type "float3" 9.9999997e-05 0 0 ;
	setAttr ".mx" -type "float3" 999 0 0 ;
createNode plusMinusAverage -n "ik:softik:plusMinusAverage3";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DD";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  1 inf;
createNode blendTwoAttr -n "ik:softik:blendTwoAttr2";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DE";
	setAttr -s 2 ".i[0:1]"  1 1;
createNode multiplyDivide -n "ik:softik:multiplyDivide5";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005DF";
createNode network -n "ik:softik:out";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E0";
	addAttr -ci true -sn "outStretch" -ln "outStretch" -nn "outStretch" -at "float";
	addAttr -ci true -sn "outRatio" -ln "outRatio" -nn "outRatio" -at "float";
createNode multiplyDivide -n "ik:softik:multiplyDivide1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E1";
createNode plusMinusAverage -n "ik:softik:plusMinusAverage1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E2";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode condition -n "ik:softik:condition1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E3";
	setAttr ".op" 2;
createNode multiplyDivide -n "ik:softik:multiplyDivide2";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E4";
	setAttr ".op" 2;
createNode multiplyDivide -n "ik:softik:multiplyDivide7";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E5";
	setAttr ".op" 2;
createNode plusMinusAverage -n "ik:softik:plusMinusAverage2";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E6";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode blendTwoAttr -n "ik:softik:blendTwoAttr1";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E7";
	setAttr -s 2 ".i";
	setAttr -s 2 ".i";
createNode multiplyDivide -n "ik:softik:multiplyDivide6";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005E8";
	setAttr ".op" 2;
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
	setAttr "._graphpos" -type "float2" 0 1 ;
	setAttr -k on ".swivelDistanceRatio";
createNode decomposeMatrix -n "decomposeGuide01LocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C59B0000062B";
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
createNode decomposeMatrix -n "decomposeGuide02LocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C59C0000062C";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
createNode decomposeMatrix -n "decomposeGuide03LocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C59D0000062D";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode network -n "out";
	rename -uid "9830B980-0000-24DE-5AB5-C94500000818";
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
		 -1.0000000000000002 0 1.1102230246251565e-16 0 0 5 0 1;
	setAttr ".outInf02LocalTm" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 3.535533905932736 0 3.9252311467094368e-16 1;
	setAttr ".outInf03LocalTm" -type "matrix" -2.2204460492503131e-16 1 0 0 -1 -2.2204460492503131e-16 0 0
		 0 0 1 0 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 1;
createNode decomposeMatrix -n "decomposeCtrlFk01DefaultLocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C9A400000819";
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
createNode decomposeMatrix -n "decomposeCtrlFk02DefaultLocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C9B10000081A";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
createNode decomposeMatrix -n "decomposeCtrlFk03DefaultLocalTm";
	rename -uid "9830B980-0000-24DE-5AB5-C9B60000081B";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode distanceBetween -n "getLimbSegment1Length";
	rename -uid "8CE2E980-0000-3155-5AB5-CE5000000678";
createNode distanceBetween -n "getLimbSegment2Length";
	rename -uid "8CE2E980-0000-3155-5AB5-CE5D00000679";
createNode addDoubleLinear -n "getLimbLength";
	rename -uid "8CE2E980-0000-3155-5AB5-CE8C0000067A";
createNode multiplyDivide -n "multiplyDivide13";
	rename -uid "8CE2E980-0000-3155-5AB5-D0870000091D";
createNode multiplyDivide -n "multiplyDivide14";
	rename -uid "8CE2E980-0000-3155-5AB5-D08B0000091E";
createNode multMatrix -n "getGuide03WorldTm";
	rename -uid "8C391980-0000-426F-5AD6-9C3B000005EB";
	setAttr -s 2 ".i";
createNode decomposeMatrix -n "decomposeGuide03WorldTm";
	rename -uid "8C391980-0000-426F-5AD6-9C63000005F0";
	setAttr ".ot" -type "double3" -5.8878467200641577e-16 8.8817841970012523e-16 -1.3322676295501878e-15 ;
	setAttr ".or" -type "double3" 90 -45.000000000000028 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818829;
	setAttr ".oqz" -0.27059805007309845;
	setAttr ".oqw" 0.65328148243818829;
createNode multiplyDivide -n "getSwivelDistance";
	rename -uid "8C391980-0000-426F-5AD6-9E3000000613";
createNode multiplyDivide -n "getLimbRatio";
	rename -uid "8C391980-0000-426F-5AD6-9E6100000616";
	setAttr ".op" 2;
createNode plusMinusAverage -n "getLimbAim";
	rename -uid "8C391980-0000-426F-5AD6-9F5400000623";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode multiplyDivide -n "getLimbMiddleAim";
	rename -uid "8C391980-0000-426F-5AD6-9FD600000624";
createNode plusMinusAverage -n "getKneePosProjectedOnLimbDir";
	rename -uid "8C391980-0000-426F-5AD6-9FF900000626";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode plusMinusAverage -n "getKneeDirection";
	rename -uid "8C391980-0000-426F-5AD6-A08A00000634";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode multMatrix -n "getGuide02WorldTm";
	rename -uid "8C391980-0000-426F-5AD6-A09C00000635";
	setAttr -s 2 ".i";
createNode decomposeMatrix -n "decomposeGuide02WorldTm";
	rename -uid "8C391980-0000-426F-5AD6-A0CF00000636";
	setAttr ".ot" -type "double3" -3.9252311467094378e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".or" -type "double3" 90 45 -90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.65328148243818818;
	setAttr ".oqy" -0.27059805007309845;
	setAttr ".oqz" -0.65328148243818829;
	setAttr ".oqw" 0.27059805007309851;
createNode vectorProduct -n "getKneeDirectionNormalized";
	rename -uid "8C391980-0000-426F-5AD6-A11700000639";
	setAttr ".op" 0;
	setAttr ".no" yes;
createNode multiplyDivide -n "getKneeDirectionOffset";
	rename -uid "8C391980-0000-426F-5AD6-A1370000063C";
createNode plusMinusAverage -n "getSwivelDefaultPos";
	rename -uid "8C391980-0000-426F-5AD6-A1640000063D";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode decomposeMatrix -n "decomposeMatrix1";
	rename -uid "F4C8C980-0000-752C-5AD6-B690000003FA";
	setAttr ".ot" -type "double3" 0 5 0 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
createNode decomposeMatrix -n "decomposeMatrix2";
	rename -uid "F4C8C980-0000-752C-5AD6-B694000003FB";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094368e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
createNode decomposeMatrix -n "decomposeMatrix3";
	rename -uid "F4C8C980-0000-752C-5AD6-B697000003FC";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "F4C8C980-0000-752C-5AD9-382C00000AB4";
	setAttr -s 7 ".tgi";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -3739.9723788593819 -4397.6188728734051 ;
	setAttr ".tgi[0].vh" -type "double2" 2914.9724116419275 -2595.2379921126339 ;
	setAttr -s 51 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -2608.571533203125;
	setAttr ".tgi[0].ni[0].y" -1645.7142333984375;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" -3568.920654296875;
	setAttr ".tgi[0].ni[1].y" -1715.50048828125;
	setAttr ".tgi[0].ni[1].nvs" 18306;
	setAttr ".tgi[0].ni[2].x" -3559.94384765625;
	setAttr ".tgi[0].ni[2].y" -792.08404541015625;
	setAttr ".tgi[0].ni[2].nvs" 1931;
	setAttr ".tgi[0].ni[3].x" 344.28570556640625;
	setAttr ".tgi[0].ni[3].y" -2895.71435546875;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" -2608.571533203125;
	setAttr ".tgi[0].ni[4].y" -2040;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" -934.78204345703125;
	setAttr ".tgi[0].ni[5].y" -7.1206927299499512;
	setAttr ".tgi[0].ni[5].nvs" 18314;
	setAttr ".tgi[0].ni[6].x" -1625.73779296875;
	setAttr ".tgi[0].ni[6].y" -2420.765380859375;
	setAttr ".tgi[0].ni[6].nvs" 18314;
	setAttr ".tgi[0].ni[7].x" -3557.593505859375;
	setAttr ".tgi[0].ni[7].y" -1245.670654296875;
	setAttr ".tgi[0].ni[7].nvs" 1931;
	setAttr ".tgi[0].ni[8].x" -2608.571533203125;
	setAttr ".tgi[0].ni[8].y" -1842.857177734375;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" -504.69732666015625;
	setAttr ".tgi[0].ni[9].y" 556.9248046875;
	setAttr ".tgi[0].ni[9].nvs" 1931;
	setAttr ".tgi[0].ni[10].x" -2282.696533203125;
	setAttr ".tgi[0].ni[10].y" -3022.0634765625;
	setAttr ".tgi[0].ni[10].nvs" 1923;
	setAttr ".tgi[0].ni[11].x" -1914.81103515625;
	setAttr ".tgi[0].ni[11].y" -1217.4683837890625;
	setAttr ".tgi[0].ni[11].nvs" 18314;
	setAttr ".tgi[0].ni[12].x" -504.69732666015625;
	setAttr ".tgi[0].ni[12].y" -867.29010009765625;
	setAttr ".tgi[0].ni[12].nvs" 1931;
	setAttr ".tgi[0].ni[13].x" -1684.191650390625;
	setAttr ".tgi[0].ni[13].y" -2916.984130859375;
	setAttr ".tgi[0].ni[13].nvs" 18306;
	setAttr ".tgi[0].ni[14].x" 344.28570556640625;
	setAttr ".tgi[0].ni[14].y" -1784.2857666015625;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" -2791.646240234375;
	setAttr ".tgi[0].ni[15].y" -2204.69677734375;
	setAttr ".tgi[0].ni[15].nvs" 1931;
	setAttr ".tgi[0].ni[16].x" -1045.780029296875;
	setAttr ".tgi[0].ni[16].y" -3607.777099609375;
	setAttr ".tgi[0].ni[16].nvs" 18306;
	setAttr ".tgi[0].ni[17].x" -4220.34716796875;
	setAttr ".tgi[0].ni[17].y" -1245.670654296875;
	setAttr ".tgi[0].ni[17].nvs" 18313;
	setAttr ".tgi[0].ni[18].x" -504.69732666015625;
	setAttr ".tgi[0].ni[18].y" -1513.5921630859375;
	setAttr ".tgi[0].ni[18].nvs" 1931;
	setAttr ".tgi[0].ni[19].x" -3317.874267578125;
	setAttr ".tgi[0].ni[19].y" -2000.0814208984375;
	setAttr ".tgi[0].ni[19].nvs" 18314;
	setAttr ".tgi[0].ni[20].x" -2608.571533203125;
	setAttr ".tgi[0].ni[20].y" -2138.571533203125;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" -2608.571533203125;
	setAttr ".tgi[0].ni[21].y" -1744.2857666015625;
	setAttr ".tgi[0].ni[21].nvs" 18304;
	setAttr ".tgi[0].ni[22].x" -1342.2041015625;
	setAttr ".tgi[0].ni[22].y" -3234.176025390625;
	setAttr ".tgi[0].ni[22].nvs" 18306;
	setAttr ".tgi[0].ni[23].x" -3180.7255859375;
	setAttr ".tgi[0].ni[23].y" -1443.1690673828125;
	setAttr ".tgi[0].ni[23].nvs" 18306;
	setAttr ".tgi[0].ni[24].x" -2836.08544921875;
	setAttr ".tgi[0].ni[24].y" -1189.26611328125;
	setAttr ".tgi[0].ni[24].nvs" 18314;
	setAttr ".tgi[0].ni[25].x" -3910.1220703125;
	setAttr ".tgi[0].ni[25].y" -1473.6390380859375;
	setAttr ".tgi[0].ni[25].nvs" 18314;
	setAttr ".tgi[0].ni[26].x" -84.285713195800781;
	setAttr ".tgi[0].ni[26].y" -2127.142822265625;
	setAttr ".tgi[0].ni[26].nvs" 18304;
	setAttr ".tgi[0].ni[27].x" -4222.697265625;
	setAttr ".tgi[0].ni[27].y" -1379.6314697265625;
	setAttr ".tgi[0].ni[27].nvs" 18313;
	setAttr ".tgi[0].ni[28].x" -3557.593505859375;
	setAttr ".tgi[0].ni[28].y" -1010.6516723632812;
	setAttr ".tgi[0].ni[28].nvs" 1931;
	setAttr ".tgi[0].ni[29].x" -504.69732666015625;
	setAttr ".tgi[0].ni[29].y" -162.23320007324219;
	setAttr ".tgi[0].ni[29].nvs" 18314;
	setAttr ".tgi[0].ni[30].x" -619.85455322265625;
	setAttr ".tgi[0].ni[30].y" -3527.8486328125;
	setAttr ".tgi[0].ni[30].nvs" 1923;
	setAttr ".tgi[0].ni[31].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[31].y" 284.30282592773438;
	setAttr ".tgi[0].ni[31].nvs" 18314;
	setAttr ".tgi[0].ni[32].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[32].y" -1755.6617431640625;
	setAttr ".tgi[0].ni[32].nvs" 18314;
	setAttr ".tgi[0].ni[33].x" -265.63861083984375;
	setAttr ".tgi[0].ni[33].y" -3593.725830078125;
	setAttr ".tgi[0].ni[33].nvs" 18306;
	setAttr ".tgi[0].ni[34].x" -3317.874267578125;
	setAttr ".tgi[0].ni[34].y" -1844.968994140625;
	setAttr ".tgi[0].ni[34].nvs" 18312;
	setAttr ".tgi[0].ni[35].x" -4220.34716796875;
	setAttr ".tgi[0].ni[35].y" -1645.202880859375;
	setAttr ".tgi[0].ni[35].nvs" 18313;
	setAttr ".tgi[0].ni[36].x" -3632.42724609375;
	setAttr ".tgi[0].ni[36].y" -1477.7398681640625;
	setAttr ".tgi[0].ni[36].nvs" 18306;
	setAttr ".tgi[0].ni[37].x" -2608.571533203125;
	setAttr ".tgi[0].ni[37].y" -1448.5714111328125;
	setAttr ".tgi[0].ni[37].nvs" 18304;
	setAttr ".tgi[0].ni[38].x" 344.28570556640625;
	setAttr ".tgi[0].ni[38].y" -2397.142822265625;
	setAttr ".tgi[0].ni[38].nvs" 18304;
	setAttr ".tgi[0].ni[39].x" -2608.571533203125;
	setAttr ".tgi[0].ni[39].y" -1941.4285888671875;
	setAttr ".tgi[0].ni[39].nvs" 18304;
	setAttr ".tgi[0].ni[40].x" -1602.093994140625;
	setAttr ".tgi[0].ni[40].y" -3595.533203125;
	setAttr ".tgi[0].ni[40].nvs" 18306;
	setAttr ".tgi[0].ni[41].x" -1992.3165283203125;
	setAttr ".tgi[0].ni[41].y" -2653.79296875;
	setAttr ".tgi[0].ni[41].nvs" 1923;
	setAttr ".tgi[0].ni[42].x" -934.78204345703125;
	setAttr ".tgi[0].ni[42].y" 709.6871337890625;
	setAttr ".tgi[0].ni[42].nvs" 18314;
	setAttr ".tgi[0].ni[43].x" -1372.857177734375;
	setAttr ".tgi[0].ni[43].y" -2048.571533203125;
	setAttr ".tgi[0].ni[43].nvs" 18304;
	setAttr ".tgi[0].ni[44].x" -3125.15478515625;
	setAttr ".tgi[0].ni[44].y" -2569.7314453125;
	setAttr ".tgi[0].ni[44].nvs" 18314;
	setAttr ".tgi[0].ni[45].x" -2608.571533203125;
	setAttr ".tgi[0].ni[45].y" -1350;
	setAttr ".tgi[0].ni[45].nvs" 18304;
	setAttr ".tgi[0].ni[46].x" -2948.89453125;
	setAttr ".tgi[0].ni[46].y" -1946.027099609375;
	setAttr ".tgi[0].ni[46].nvs" 18312;
	setAttr ".tgi[0].ni[47].x" -2438.543212890625;
	setAttr ".tgi[0].ni[47].y" -2591.839599609375;
	setAttr ".tgi[0].ni[47].nvs" 18306;
	setAttr ".tgi[0].ni[48].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[48].y" -510.061279296875;
	setAttr ".tgi[0].ni[48].nvs" 1931;
	setAttr ".tgi[0].ni[49].x" -2608.571533203125;
	setAttr ".tgi[0].ni[49].y" -1547.142822265625;
	setAttr ".tgi[0].ni[49].nvs" 18304;
	setAttr ".tgi[0].ni[50].x" -934.78204345703125;
	setAttr ".tgi[0].ni[50].y" -1372.580810546875;
	setAttr ".tgi[0].ni[50].nvs" 18314;
	setAttr ".tgi[1].tn" -type "string" "Untitled_2";
	setAttr ".tgi[1].vl" -type "double2" -1452.5182573004249 -682.14283003693629 ;
	setAttr ".tgi[1].vh" -type "double2" 3558.4705545697802 674.99997317791087 ;
	setAttr -s 30 ".tgi[1].ni";
	setAttr ".tgi[1].ni[0].x" 4744.28564453125;
	setAttr ".tgi[1].ni[0].y" -538.5714111328125;
	setAttr ".tgi[1].ni[0].nvs" 18304;
	setAttr ".tgi[1].ni[1].x" 1082.3115234375;
	setAttr ".tgi[1].ni[1].y" 629.90948486328125;
	setAttr ".tgi[1].ni[1].nvs" 18313;
	setAttr ".tgi[1].ni[2].x" 766.423095703125;
	setAttr ".tgi[1].ni[2].y" 94.310020446777344;
	setAttr ".tgi[1].ni[2].nvs" 18314;
	setAttr ".tgi[1].ni[3].x" 2605.094970703125;
	setAttr ".tgi[1].ni[3].y" -352.89810180664062;
	setAttr ".tgi[1].ni[3].nvs" 1931;
	setAttr ".tgi[1].ni[4].x" 5372.85693359375;
	setAttr ".tgi[1].ni[4].y" -560;
	setAttr ".tgi[1].ni[4].nvs" 18304;
	setAttr ".tgi[1].ni[5].x" 440.24679565429688;
	setAttr ".tgi[1].ni[5].y" 493.32656860351562;
	setAttr ".tgi[1].ni[5].nvs" 18313;
	setAttr ".tgi[1].ni[6].x" 5372.85693359375;
	setAttr ".tgi[1].ni[6].y" -1131.4285888671875;
	setAttr ".tgi[1].ni[6].nvs" 18304;
	setAttr ".tgi[1].ni[7].x" 1445.1500244140625;
	setAttr ".tgi[1].ni[7].y" -404.11505126953125;
	setAttr ".tgi[1].ni[7].nvs" 1931;
	setAttr ".tgi[1].ni[8].x" 1171.720703125;
	setAttr ".tgi[1].ni[8].y" -329.415283203125;
	setAttr ".tgi[1].ni[8].nvs" 1931;
	setAttr ".tgi[1].ni[9].x" 1794.710205078125;
	setAttr ".tgi[1].ni[9].y" 692.2615966796875;
	setAttr ".tgi[1].ni[9].nvs" 18306;
	setAttr ".tgi[1].ni[10].x" 5801.4287109375;
	setAttr ".tgi[1].ni[10].y" -565.71429443359375;
	setAttr ".tgi[1].ni[10].nvs" 18304;
	setAttr ".tgi[1].ni[11].x" 5801.4287109375;
	setAttr ".tgi[1].ni[11].y" -838.5714111328125;
	setAttr ".tgi[1].ni[11].nvs" 18304;
	setAttr ".tgi[1].ni[12].x" 5058.5712890625;
	setAttr ".tgi[1].ni[12].y" -765.71429443359375;
	setAttr ".tgi[1].ni[12].nvs" 18304;
	setAttr ".tgi[1].ni[13].x" 775.30780029296875;
	setAttr ".tgi[1].ni[13].y" 602.08502197265625;
	setAttr ".tgi[1].ni[13].nvs" 18314;
	setAttr ".tgi[1].ni[14].x" 5801.4287109375;
	setAttr ".tgi[1].ni[14].y" -664.28570556640625;
	setAttr ".tgi[1].ni[14].nvs" 18304;
	setAttr ".tgi[1].ni[15].x" 777.67034912109375;
	setAttr ".tgi[1].ni[15].y" 346.83428955078125;
	setAttr ".tgi[1].ni[15].nvs" 18314;
	setAttr ".tgi[1].ni[16].x" 1087.7464599609375;
	setAttr ".tgi[1].ni[16].y" 382.31390380859375;
	setAttr ".tgi[1].ni[16].nvs" 18313;
	setAttr ".tgi[1].ni[17].x" 128.57142639160156;
	setAttr ".tgi[1].ni[17].y" 494.28570556640625;
	setAttr ".tgi[1].ni[17].nvs" 18312;
	setAttr ".tgi[1].ni[18].x" 128.57142639160156;
	setAttr ".tgi[1].ni[18].y" 691.4285888671875;
	setAttr ".tgi[1].ni[18].nvs" 18312;
	setAttr ".tgi[1].ni[19].x" 1231.4013671875;
	setAttr ".tgi[1].ni[19].y" 1002.9470825195312;
	setAttr ".tgi[1].ni[19].nvs" 18306;
	setAttr ".tgi[1].ni[20].x" 1775.695556640625;
	setAttr ".tgi[1].ni[20].y" 414.17254638671875;
	setAttr ".tgi[1].ni[20].nvs" 18306;
	setAttr ".tgi[1].ni[21].x" 2615.598876953125;
	setAttr ".tgi[1].ni[21].y" -604.36865234375;
	setAttr ".tgi[1].ni[21].nvs" 1931;
	setAttr ".tgi[1].ni[22].x" 1171.720703125;
	setAttr ".tgi[1].ni[22].y" -470.35821533203125;
	setAttr ".tgi[1].ni[22].nvs" 1931;
	setAttr ".tgi[1].ni[23].x" 2377.003662109375;
	setAttr ".tgi[1].ni[23].y" -456.60031127929688;
	setAttr ".tgi[1].ni[23].nvs" 18314;
	setAttr ".tgi[1].ni[24].x" 5372.85693359375;
	setAttr ".tgi[1].ni[24].y" -900;
	setAttr ".tgi[1].ni[24].nvs" 18304;
	setAttr ".tgi[1].ni[25].x" 2612.2412109375;
	setAttr ".tgi[1].ni[25].y" -847.4547119140625;
	setAttr ".tgi[1].ni[25].nvs" 1931;
	setAttr ".tgi[1].ni[26].x" 1092.040771484375;
	setAttr ".tgi[1].ni[26].y" 1.5936880111694336;
	setAttr ".tgi[1].ni[26].nvs" 18313;
	setAttr ".tgi[1].ni[27].x" 128.57142639160156;
	setAttr ".tgi[1].ni[27].y" 592.85711669921875;
	setAttr ".tgi[1].ni[27].nvs" 18312;
	setAttr ".tgi[1].ni[28].x" 5801.4287109375;
	setAttr ".tgi[1].ni[28].y" -1208.5714111328125;
	setAttr ".tgi[1].ni[28].nvs" 18304;
	setAttr ".tgi[1].ni[29].x" 1062.303466796875;
	setAttr ".tgi[1].ni[29].y" 502.62240600585938;
	setAttr ".tgi[1].ni[29].nvs" 18312;
	setAttr ".tgi[2].tn" -type "string" "Untitled_3";
	setAttr ".tgi[2].vl" -type "double2" -8842.49049112184 814.28568192890828 ;
	setAttr ".tgi[2].vh" -type "double2" -5119.4137159866959 1822.6189751946765 ;
	setAttr -s 20 ".tgi[2].ni";
	setAttr ".tgi[2].ni[0].x" -6055.71435546875;
	setAttr ".tgi[2].ni[0].y" 1120;
	setAttr ".tgi[2].ni[0].nvs" 18304;
	setAttr ".tgi[2].ni[1].x" -6670;
	setAttr ".tgi[2].ni[1].y" 1308.5714111328125;
	setAttr ".tgi[2].ni[1].nvs" 18304;
	setAttr ".tgi[2].ni[2].x" -6362.85693359375;
	setAttr ".tgi[2].ni[2].y" 1158.5714111328125;
	setAttr ".tgi[2].ni[2].nvs" 18304;
	setAttr ".tgi[2].ni[3].x" -6362.85693359375;
	setAttr ".tgi[2].ni[3].y" 1022.8571166992188;
	setAttr ".tgi[2].ni[3].nvs" 18304;
	setAttr ".tgi[2].ni[4].x" -5441.4287109375;
	setAttr ".tgi[2].ni[4].y" 1251.4285888671875;
	setAttr ".tgi[2].ni[4].nvs" 18304;
	setAttr ".tgi[2].ni[5].x" -3905.71435546875;
	setAttr ".tgi[2].ni[5].y" 1582.185302734375;
	setAttr ".tgi[2].ni[5].nvs" 18305;
	setAttr ".tgi[2].ni[6].x" -4212.85693359375;
	setAttr ".tgi[2].ni[6].y" 1634.1630859375;
	setAttr ".tgi[2].ni[6].nvs" 18305;
	setAttr ".tgi[2].ni[7].x" -6647.90478515625;
	setAttr ".tgi[2].ni[7].y" 1642.2860107421875;
	setAttr ".tgi[2].ni[7].nvs" 18305;
	setAttr ".tgi[2].ni[8].x" -7046.1904296875;
	setAttr ".tgi[2].ni[8].y" 1695.8096923828125;
	setAttr ".tgi[2].ni[8].nvs" 18305;
	setAttr ".tgi[2].ni[9].x" -3598.571533203125;
	setAttr ".tgi[2].ni[9].y" 1354.2857666015625;
	setAttr ".tgi[2].ni[9].nvs" 18305;
	setAttr ".tgi[2].ni[10].x" -4831.2265625;
	setAttr ".tgi[2].ni[10].y" 1315.84912109375;
	setAttr ".tgi[2].ni[10].nvs" 18305;
	setAttr ".tgi[2].ni[11].x" -3905.71435546875;
	setAttr ".tgi[2].ni[11].y" 1311.4285888671875;
	setAttr ".tgi[2].ni[11].nvs" 18304;
	setAttr ".tgi[2].ni[12].x" -3581.855712890625;
	setAttr ".tgi[2].ni[12].y" 1680.837158203125;
	setAttr ".tgi[2].ni[12].nvs" 18305;
	setAttr ".tgi[2].ni[13].x" -5748.5712890625;
	setAttr ".tgi[2].ni[13].y" 1238.5714111328125;
	setAttr ".tgi[2].ni[13].nvs" 18304;
	setAttr ".tgi[2].ni[14].x" -3291.428466796875;
	setAttr ".tgi[2].ni[14].y" 1488.5714111328125;
	setAttr ".tgi[2].ni[14].nvs" 18306;
	setAttr ".tgi[2].ni[15].x" -4212.85693359375;
	setAttr ".tgi[2].ni[15].y" 1237.142822265625;
	setAttr ".tgi[2].ni[15].nvs" 18304;
	setAttr ".tgi[2].ni[16].x" -2984.28564453125;
	setAttr ".tgi[2].ni[16].y" 1490;
	setAttr ".tgi[2].ni[16].nvs" 18304;
	setAttr ".tgi[2].ni[17].x" -5134.28564453125;
	setAttr ".tgi[2].ni[17].y" 1267.142822265625;
	setAttr ".tgi[2].ni[17].nvs" 18304;
	setAttr ".tgi[2].ni[18].x" -7416.857421875;
	setAttr ".tgi[2].ni[18].y" 1527.61865234375;
	setAttr ".tgi[2].ni[18].nvs" 18305;
	setAttr ".tgi[2].ni[19].x" -4490.2841796875;
	setAttr ".tgi[2].ni[19].y" 1141.6575927734375;
	setAttr ".tgi[2].ni[19].nvs" 18305;
	setAttr ".tgi[3].tn" -type "string" "Untitled_4";
	setAttr ".tgi[3].vl" -type "double2" -5797.7561798742599 -773.8094930610971 ;
	setAttr ".tgi[3].vh" -type "double2" -1701.0530459593201 335.71427237419903 ;
	setAttr -s 33 ".tgi[3].ni";
	setAttr ".tgi[3].ni[0].x" -4630;
	setAttr ".tgi[3].ni[0].y" -265.71429443359375;
	setAttr ".tgi[3].ni[0].nvs" 18304;
	setAttr ".tgi[3].ni[1].x" -17.39495849609375;
	setAttr ".tgi[3].ni[1].y" -97.058822631835938;
	setAttr ".tgi[3].ni[1].nvs" 18305;
	setAttr ".tgi[3].ni[2].x" -5244.28564453125;
	setAttr ".tgi[3].ni[2].y" -167.14285278320312;
	setAttr ".tgi[3].ni[2].nvs" 18304;
	setAttr ".tgi[3].ni[3].x" -4630;
	setAttr ".tgi[3].ni[3].y" -364.28570556640625;
	setAttr ".tgi[3].ni[3].nvs" 18304;
	setAttr ".tgi[3].ni[4].x" -3394.28564453125;
	setAttr ".tgi[3].ni[4].y" -157.14285278320312;
	setAttr ".tgi[3].ni[4].nvs" 18304;
	setAttr ".tgi[3].ni[5].x" -5244.28564453125;
	setAttr ".tgi[3].ni[5].y" -364.28570556640625;
	setAttr ".tgi[3].ni[5].nvs" 18304;
	setAttr ".tgi[3].ni[6].x" -4937.14306640625;
	setAttr ".tgi[3].ni[6].y" -265.71429443359375;
	setAttr ".tgi[3].ni[6].nvs" 18304;
	setAttr ".tgi[3].ni[7].x" -4315.71435546875;
	setAttr ".tgi[3].ni[7].y" -30;
	setAttr ".tgi[3].ni[7].nvs" 18304;
	setAttr ".tgi[3].ni[8].x" -1858.5714111328125;
	setAttr ".tgi[3].ni[8].y" -192.85714721679688;
	setAttr ".tgi[3].ni[8].nvs" 18304;
	setAttr ".tgi[3].ni[9].x" -4630;
	setAttr ".tgi[3].ni[9].y" -167.14285278320312;
	setAttr ".tgi[3].ni[9].nvs" 18304;
	setAttr ".tgi[3].ni[10].x" -2165.71435546875;
	setAttr ".tgi[3].ni[10].y" -192.85714721679688;
	setAttr ".tgi[3].ni[10].nvs" 18304;
	setAttr ".tgi[3].ni[11].x" -4011.748291015625;
	setAttr ".tgi[3].ni[11].y" -168.62957763671875;
	setAttr ".tgi[3].ni[11].nvs" 18304;
	setAttr ".tgi[3].ni[12].x" 291.42855834960938;
	setAttr ".tgi[3].ni[12].y" 47.142856597900391;
	setAttr ".tgi[3].ni[12].nvs" 18304;
	setAttr ".tgi[3].ni[13].x" -4315.71435546875;
	setAttr ".tgi[3].ni[13].y" -331.42855834960938;
	setAttr ".tgi[3].ni[13].nvs" 18304;
	setAttr ".tgi[3].ni[14].x" -3111.67724609375;
	setAttr ".tgi[3].ni[14].y" 233.31568908691406;
	setAttr ".tgi[3].ni[14].nvs" 18305;
	setAttr ".tgi[3].ni[15].x" -2780;
	setAttr ".tgi[3].ni[15].y" -330;
	setAttr ".tgi[3].ni[15].nvs" 18304;
	setAttr ".tgi[3].ni[16].x" -1244.2857666015625;
	setAttr ".tgi[3].ni[16].y" -131.42857360839844;
	setAttr ".tgi[3].ni[16].nvs" 18304;
	setAttr ".tgi[3].ni[17].x" -4008.571533203125;
	setAttr ".tgi[3].ni[17].y" -58.571430206298828;
	setAttr ".tgi[3].ni[17].nvs" 18304;
	setAttr ".tgi[3].ni[18].x" -2780;
	setAttr ".tgi[3].ni[18].y" -194.28572082519531;
	setAttr ".tgi[3].ni[18].nvs" 18304;
	setAttr ".tgi[3].ni[19].x" -3087.142822265625;
	setAttr ".tgi[3].ni[19].y" -130;
	setAttr ".tgi[3].ni[19].nvs" 18304;
	setAttr ".tgi[3].ni[20].x" -322.85714721679688;
	setAttr ".tgi[3].ni[20].y" -57.142856597900391;
	setAttr ".tgi[3].ni[20].nvs" 18304;
	setAttr ".tgi[3].ni[21].x" 1290;
	setAttr ".tgi[3].ni[21].y" 47.142856597900391;
	setAttr ".tgi[3].ni[21].nvs" 18304;
	setAttr ".tgi[3].ni[22].x" -2472.857177734375;
	setAttr ".tgi[3].ni[22].y" -261.42855834960938;
	setAttr ".tgi[3].ni[22].nvs" 18304;
	setAttr ".tgi[3].ni[23].x" -630;
	setAttr ".tgi[3].ni[23].y" -68.571426391601562;
	setAttr ".tgi[3].ni[23].nvs" 18304;
	setAttr ".tgi[3].ni[24].x" -4315.71435546875;
	setAttr ".tgi[3].ni[24].y" -232.85714721679688;
	setAttr ".tgi[3].ni[24].nvs" 18304;
	setAttr ".tgi[3].ni[25].x" 598.5714111328125;
	setAttr ".tgi[3].ni[25].y" 18.571428298950195;
	setAttr ".tgi[3].ni[25].nvs" 18304;
	setAttr ".tgi[3].ni[26].x" 905.71429443359375;
	setAttr ".tgi[3].ni[26].y" 47.142856597900391;
	setAttr ".tgi[3].ni[26].nvs" 18304;
	setAttr ".tgi[3].ni[27].x" -4019.244384765625;
	setAttr ".tgi[3].ni[27].y" 120.07266235351562;
	setAttr ".tgi[3].ni[27].nvs" 18304;
	setAttr ".tgi[3].ni[28].x" -1551.4285888671875;
	setAttr ".tgi[3].ni[28].y" -184.28572082519531;
	setAttr ".tgi[3].ni[28].nvs" 18304;
	setAttr ".tgi[3].ni[29].x" -5244.28564453125;
	setAttr ".tgi[3].ni[29].y" -265.71429443359375;
	setAttr ".tgi[3].ni[29].nvs" 18304;
	setAttr ".tgi[3].ni[30].x" -3676.175048828125;
	setAttr ".tgi[3].ni[30].y" 24.352910995483398;
	setAttr ".tgi[3].ni[30].nvs" 18305;
	setAttr ".tgi[3].ni[31].x" -4008.571533203125;
	setAttr ".tgi[3].ni[31].y" -274.28570556640625;
	setAttr ".tgi[3].ni[31].nvs" 18304;
	setAttr ".tgi[3].ni[32].x" -937.14288330078125;
	setAttr ".tgi[3].ni[32].y" -82.857139587402344;
	setAttr ".tgi[3].ni[32].nvs" 18304;
	setAttr ".tgi[4].tn" -type "string" "Untitled_5";
	setAttr ".tgi[4].vl" -type "double2" -10739.560012808668 -1855.9523072034626 ;
	setAttr ".tgi[4].vh" -type "double2" -6717.5821506496868 -766.6666362020718 ;
	setAttr -s 60 ".tgi[4].ni";
	setAttr ".tgi[4].ni[0].x" -9848.5712890625;
	setAttr ".tgi[4].ni[0].y" -912.85711669921875;
	setAttr ".tgi[4].ni[0].nvs" 18304;
	setAttr ".tgi[4].ni[1].x" -1692.857177734375;
	setAttr ".tgi[4].ni[1].y" -861.4285888671875;
	setAttr ".tgi[4].ni[1].nvs" 18304;
	setAttr ".tgi[4].ni[2].x" -957.14288330078125;
	setAttr ".tgi[4].ni[2].y" -700;
	setAttr ".tgi[4].ni[2].nvs" 18304;
	setAttr ".tgi[4].ni[3].x" -6155.71435546875;
	setAttr ".tgi[4].ni[3].y" -1094.2857666015625;
	setAttr ".tgi[4].ni[3].nvs" 18304;
	setAttr ".tgi[4].ni[4].x" -6462.85693359375;
	setAttr ".tgi[4].ni[4].y" -1108.5714111328125;
	setAttr ".tgi[4].ni[4].nvs" 18304;
	setAttr ".tgi[4].ni[5].x" -3698.571533203125;
	setAttr ".tgi[4].ni[5].y" -998.5714111328125;
	setAttr ".tgi[4].ni[5].nvs" 18304;
	setAttr ".tgi[4].ni[6].x" -10155.7138671875;
	setAttr ".tgi[4].ni[6].y" -814.28570556640625;
	setAttr ".tgi[4].ni[6].nvs" 18304;
	setAttr ".tgi[4].ni[7].x" -5234.28564453125;
	setAttr ".tgi[4].ni[7].y" -840;
	setAttr ".tgi[4].ni[7].nvs" 18304;
	setAttr ".tgi[4].ni[8].x" -10155.7138671875;
	setAttr ".tgi[4].ni[8].y" -912.85711669921875;
	setAttr ".tgi[4].ni[8].nvs" 18304;
	setAttr ".tgi[4].ni[9].x" -8920;
	setAttr ".tgi[4].ni[9].y" -1061.4285888671875;
	setAttr ".tgi[4].ni[9].nvs" 18304;
	setAttr ".tgi[4].ni[10].x" -7384.28564453125;
	setAttr ".tgi[4].ni[10].y" -1048.5714111328125;
	setAttr ".tgi[4].ni[10].nvs" 18304;
	setAttr ".tgi[4].ni[11].x" -4620;
	setAttr ".tgi[4].ni[11].y" -1047.142822265625;
	setAttr ".tgi[4].ni[11].nvs" 18304;
	setAttr ".tgi[4].ni[12].x" -8920;
	setAttr ".tgi[4].ni[12].y" -845.71429443359375;
	setAttr ".tgi[4].ni[12].nvs" 18304;
	setAttr ".tgi[4].ni[13].x" -957.14288330078125;
	setAttr ".tgi[4].ni[13].y" -1230;
	setAttr ".tgi[4].ni[13].nvs" 18304;
	setAttr ".tgi[4].ni[14].x" -4005.71435546875;
	setAttr ".tgi[4].ni[14].y" -1008.5714111328125;
	setAttr ".tgi[4].ni[14].nvs" 18304;
	setAttr ".tgi[4].ni[15].x" -2367.142822265625;
	setAttr ".tgi[4].ni[15].y" -1208.5714111328125;
	setAttr ".tgi[4].ni[15].nvs" 18304;
	setAttr ".tgi[4].ni[16].x" -10155.7138671875;
	setAttr ".tgi[4].ni[16].y" -715.71429443359375;
	setAttr ".tgi[4].ni[16].nvs" 18304;
	setAttr ".tgi[4].ni[17].x" -957.14288330078125;
	setAttr ".tgi[4].ni[17].y" -465.71429443359375;
	setAttr ".tgi[4].ni[17].nvs" 18304;
	setAttr ".tgi[4].ni[18].x" -4312.85693359375;
	setAttr ".tgi[4].ni[18].y" -945.71429443359375;
	setAttr ".tgi[4].ni[18].nvs" 18304;
	setAttr ".tgi[4].ni[19].x" -5234.28564453125;
	setAttr ".tgi[4].ni[19].y" -1090;
	setAttr ".tgi[4].ni[19].nvs" 18304;
	setAttr ".tgi[4].ni[20].x" -10155.7138671875;
	setAttr ".tgi[4].ni[20].y" -617.14288330078125;
	setAttr ".tgi[4].ni[20].nvs" 18304;
	setAttr ".tgi[4].ni[21].x" -957.14288330078125;
	setAttr ".tgi[4].ni[21].y" -798.5714111328125;
	setAttr ".tgi[4].ni[21].nvs" 18304;
	setAttr ".tgi[4].ni[22].x" -9234.2861328125;
	setAttr ".tgi[4].ni[22].y" -912.85711669921875;
	setAttr ".tgi[4].ni[22].nvs" 18304;
	setAttr ".tgi[4].ni[23].x" -9234.2861328125;
	setAttr ".tgi[4].ni[23].y" -1110;
	setAttr ".tgi[4].ni[23].nvs" 18304;
	setAttr ".tgi[4].ni[24].x" -7691.4287109375;
	setAttr ".tgi[4].ni[24].y" -855.71429443359375;
	setAttr ".tgi[4].ni[24].nvs" 18304;
	setAttr ".tgi[4].ni[25].x" -8612.857421875;
	setAttr ".tgi[4].ni[25].y" -1087.142822265625;
	setAttr ".tgi[4].ni[25].nvs" 18304;
	setAttr ".tgi[4].ni[26].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[26].y" -908.5714111328125;
	setAttr ".tgi[4].ni[26].nvs" 18304;
	setAttr ".tgi[4].ni[27].x" -957.14288330078125;
	setAttr ".tgi[4].ni[27].y" -1032.857177734375;
	setAttr ".tgi[4].ni[27].nvs" 18304;
	setAttr ".tgi[4].ni[28].x" -10155.7138671875;
	setAttr ".tgi[4].ni[28].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[28].nvs" 18304;
	setAttr ".tgi[4].ni[29].x" -8611.7607421875;
	setAttr ".tgi[4].ni[29].y" -752.093505859375;
	setAttr ".tgi[4].ni[29].nvs" 18304;
	setAttr ".tgi[4].ni[30].x" -7077.14306640625;
	setAttr ".tgi[4].ni[30].y" -972.85711669921875;
	setAttr ".tgi[4].ni[30].nvs" 18304;
	setAttr ".tgi[4].ni[31].x" -9848.5712890625;
	setAttr ".tgi[4].ni[31].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[31].nvs" 18304;
	setAttr ".tgi[4].ni[32].x" -9542.23828125;
	setAttr ".tgi[4].ni[32].y" -1033.5311279296875;
	setAttr ".tgi[4].ni[32].nvs" 18306;
	setAttr ".tgi[4].ni[33].x" -7384.28564453125;
	setAttr ".tgi[4].ni[33].y" -912.85711669921875;
	setAttr ".tgi[4].ni[33].nvs" 18304;
	setAttr ".tgi[4].ni[34].x" -9234.2861328125;
	setAttr ".tgi[4].ni[34].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[34].nvs" 18304;
	setAttr ".tgi[4].ni[35].x" -4927.14306640625;
	setAttr ".tgi[4].ni[35].y" -838.5714111328125;
	setAttr ".tgi[4].ni[35].nvs" 18304;
	setAttr ".tgi[4].ni[36].x" -957.14288330078125;
	setAttr ".tgi[4].ni[36].y" -915.71429443359375;
	setAttr ".tgi[4].ni[36].nvs" 18304;
	setAttr ".tgi[4].ni[37].x" -1692.857177734375;
	setAttr ".tgi[4].ni[37].y" -1017.1428833007812;
	setAttr ".tgi[4].ni[37].nvs" 18304;
	setAttr ".tgi[4].ni[38].x" -1692.857177734375;
	setAttr ".tgi[4].ni[38].y" -762.85711669921875;
	setAttr ".tgi[4].ni[38].nvs" 18304;
	setAttr ".tgi[4].ni[39].x" -6770;
	setAttr ".tgi[4].ni[39].y" -1124.2857666015625;
	setAttr ".tgi[4].ni[39].nvs" 18304;
	setAttr ".tgi[4].ni[40].x" -7998.5712890625;
	setAttr ".tgi[4].ni[40].y" -874.28570556640625;
	setAttr ".tgi[4].ni[40].nvs" 18304;
	setAttr ".tgi[4].ni[41].x" -5848.5712890625;
	setAttr ".tgi[4].ni[41].y" -1038.5714111328125;
	setAttr ".tgi[4].ni[41].nvs" 18304;
	setAttr ".tgi[4].ni[42].x" -9848.5712890625;
	setAttr ".tgi[4].ni[42].y" -1110;
	setAttr ".tgi[4].ni[42].nvs" 18304;
	setAttr ".tgi[4].ni[43].x" -8920;
	setAttr ".tgi[4].ni[43].y" -962.85711669921875;
	setAttr ".tgi[4].ni[43].nvs" 18304;
	setAttr ".tgi[4].ni[44].x" -10155.7138671875;
	setAttr ".tgi[4].ni[44].y" -1405.7142333984375;
	setAttr ".tgi[4].ni[44].nvs" 18304;
	setAttr ".tgi[4].ni[45].x" -8945.8779296875;
	setAttr ".tgi[4].ni[45].y" -1389.3060302734375;
	setAttr ".tgi[4].ni[45].nvs" 18306;
	setAttr ".tgi[4].ni[46].x" -10155.7138671875;
	setAttr ".tgi[4].ni[46].y" -1208.5714111328125;
	setAttr ".tgi[4].ni[46].nvs" 18304;
	setAttr ".tgi[4].ni[47].x" -4620;
	setAttr ".tgi[4].ni[47].y" -911.4285888671875;
	setAttr ".tgi[4].ni[47].nvs" 18304;
	setAttr ".tgi[4].ni[48].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[48].y" -1025.7142333984375;
	setAttr ".tgi[4].ni[48].nvs" 18304;
	setAttr ".tgi[4].ni[49].x" -8293.830078125;
	setAttr ".tgi[4].ni[49].y" -867.90045166015625;
	setAttr ".tgi[4].ni[49].nvs" 18306;
	setAttr ".tgi[4].ni[50].x" -2717.142822265625;
	setAttr ".tgi[4].ni[50].y" -1185.7142333984375;
	setAttr ".tgi[4].ni[50].nvs" 18304;
	setAttr ".tgi[4].ni[51].x" -10155.7138671875;
	setAttr ".tgi[4].ni[51].y" -1307.142822265625;
	setAttr ".tgi[4].ni[51].nvs" 18304;
	setAttr ".tgi[4].ni[52].x" -8614.15234375;
	setAttr ".tgi[4].ni[52].y" -1219.30224609375;
	setAttr ".tgi[4].ni[52].nvs" 18306;
	setAttr ".tgi[4].ni[53].x" -7691.4287109375;
	setAttr ".tgi[4].ni[53].y" -991.4285888671875;
	setAttr ".tgi[4].ni[53].nvs" 18304;
	setAttr ".tgi[4].ni[54].x" -957.14288330078125;
	setAttr ".tgi[4].ni[54].y" -564.28570556640625;
	setAttr ".tgi[4].ni[54].nvs" 18304;
	setAttr ".tgi[4].ni[55].x" -10155.7138671875;
	setAttr ".tgi[4].ni[55].y" -1110;
	setAttr ".tgi[4].ni[55].nvs" 18304;
	setAttr ".tgi[4].ni[56].x" -4927.14306640625;
	setAttr ".tgi[4].ni[56].y" -1081.4285888671875;
	setAttr ".tgi[4].ni[56].nvs" 18304;
	setAttr ".tgi[4].ni[57].x" -8612.857421875;
	setAttr ".tgi[4].ni[57].y" -871.4285888671875;
	setAttr ".tgi[4].ni[57].nvs" 18304;
	setAttr ".tgi[4].ni[58].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[58].y" -788.5714111328125;
	setAttr ".tgi[4].ni[58].nvs" 18304;
	setAttr ".tgi[4].ni[59].x" -5541.4287109375;
	setAttr ".tgi[4].ni[59].y" -987.14288330078125;
	setAttr ".tgi[4].ni[59].nvs" 18304;
	setAttr ".tgi[5].tn" -type "string" "Untitled_6";
	setAttr ".tgi[5].vl" -type "double2" -3649.2214667145759 -3032.1427366563157 ;
	setAttr ".tgi[5].vh" -type "double2" 2755.1738831932234 -1297.618996056287 ;
	setAttr -s 39 ".tgi[5].ni";
	setAttr ".tgi[5].ni[0].x" -717.14288330078125;
	setAttr ".tgi[5].ni[0].y" -1441.4285888671875;
	setAttr ".tgi[5].ni[0].nvs" 18304;
	setAttr ".tgi[5].ni[1].x" -2649.8759765625;
	setAttr ".tgi[5].ni[1].y" -767.46453857421875;
	setAttr ".tgi[5].ni[1].nvs" 18306;
	setAttr ".tgi[5].ni[2].x" -3545.71435546875;
	setAttr ".tgi[5].ni[2].y" -605.71429443359375;
	setAttr ".tgi[5].ni[2].nvs" 18304;
	setAttr ".tgi[5].ni[3].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[3].y" -941.4285888671875;
	setAttr ".tgi[5].ni[3].nvs" 18304;
	setAttr ".tgi[5].ni[4].x" -3545.71435546875;
	setAttr ".tgi[5].ni[4].y" -704.28570556640625;
	setAttr ".tgi[5].ni[4].nvs" 18304;
	setAttr ".tgi[5].ni[5].x" -2660.843017578125;
	setAttr ".tgi[5].ni[5].y" -1198.5745849609375;
	setAttr ".tgi[5].ni[5].nvs" 18306;
	setAttr ".tgi[5].ni[6].x" -2280.754150390625;
	setAttr ".tgi[5].ni[6].y" -1337.3529052734375;
	setAttr ".tgi[5].ni[6].nvs" 18306;
	setAttr ".tgi[5].ni[7].x" -717.14288330078125;
	setAttr ".tgi[5].ni[7].y" -1225.7142333984375;
	setAttr ".tgi[5].ni[7].nvs" 18304;
	setAttr ".tgi[5].ni[8].x" -3238.571533203125;
	setAttr ".tgi[5].ni[8].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[8].nvs" 18304;
	setAttr ".tgi[5].ni[9].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[9].y" -1388.5714111328125;
	setAttr ".tgi[5].ni[9].nvs" 18304;
	setAttr ".tgi[5].ni[10].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[10].y" -1040;
	setAttr ".tgi[5].ni[10].nvs" 18304;
	setAttr ".tgi[5].ni[11].x" -2268.605224609375;
	setAttr ".tgi[5].ni[11].y" -1083.2686767578125;
	setAttr ".tgi[5].ni[11].nvs" 18306;
	setAttr ".tgi[5].ni[12].x" -3545.71435546875;
	setAttr ".tgi[5].ni[12].y" -1295.7142333984375;
	setAttr ".tgi[5].ni[12].nvs" 18304;
	setAttr ".tgi[5].ni[13].x" -3545.71435546875;
	setAttr ".tgi[5].ni[13].y" -901.4285888671875;
	setAttr ".tgi[5].ni[13].nvs" 18304;
	setAttr ".tgi[5].ni[14].x" -1388.5714111328125;
	setAttr ".tgi[5].ni[14].y" -1298.5714111328125;
	setAttr ".tgi[5].ni[14].nvs" 18304;
	setAttr ".tgi[5].ni[15].x" -3238.571533203125;
	setAttr ".tgi[5].ni[15].y" -1000;
	setAttr ".tgi[5].ni[15].nvs" 18304;
	setAttr ".tgi[5].ni[16].x" -717.14288330078125;
	setAttr ".tgi[5].ni[16].y" -1872.857177734375;
	setAttr ".tgi[5].ni[16].nvs" 18304;
	setAttr ".tgi[5].ni[17].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[17].y" -1715.7142333984375;
	setAttr ".tgi[5].ni[17].nvs" 18304;
	setAttr ".tgi[5].ni[18].x" -3238.571533203125;
	setAttr ".tgi[5].ni[18].y" -1197.142822265625;
	setAttr ".tgi[5].ni[18].nvs" 18304;
	setAttr ".tgi[5].ni[19].x" -2624.28564453125;
	setAttr ".tgi[5].ni[19].y" -1058.5714111328125;
	setAttr ".tgi[5].ni[19].nvs" 18304;
	setAttr ".tgi[5].ni[20].x" -1096.7374267578125;
	setAttr ".tgi[5].ni[20].y" -2203.770263671875;
	setAttr ".tgi[5].ni[20].nvs" 18306;
	setAttr ".tgi[5].ni[21].x" -1388.5714111328125;
	setAttr ".tgi[5].ni[21].y" -1200;
	setAttr ".tgi[5].ni[21].nvs" 18304;
	setAttr ".tgi[5].ni[22].x" -717.14288330078125;
	setAttr ".tgi[5].ni[22].y" -658.5714111328125;
	setAttr ".tgi[5].ni[22].nvs" 18304;
	setAttr ".tgi[5].ni[23].x" -3545.71435546875;
	setAttr ".tgi[5].ni[23].y" -1000;
	setAttr ".tgi[5].ni[23].nvs" 18304;
	setAttr ".tgi[5].ni[24].x" -1695.7142333984375;
	setAttr ".tgi[5].ni[24].y" -1118.5714111328125;
	setAttr ".tgi[5].ni[24].nvs" 18304;
	setAttr ".tgi[5].ni[25].x" -3545.71435546875;
	setAttr ".tgi[5].ni[25].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[25].nvs" 18304;
	setAttr ".tgi[5].ni[26].x" -717.14288330078125;
	setAttr ".tgi[5].ni[26].y" -1127.142822265625;
	setAttr ".tgi[5].ni[26].nvs" 18304;
	setAttr ".tgi[5].ni[27].x" -3545.71435546875;
	setAttr ".tgi[5].ni[27].y" -802.85711669921875;
	setAttr ".tgi[5].ni[27].nvs" 18304;
	setAttr ".tgi[5].ni[28].x" -671.21630859375;
	setAttr ".tgi[5].ni[28].y" -2372.208984375;
	setAttr ".tgi[5].ni[28].nvs" 18305;
	setAttr ".tgi[5].ni[29].x" -717.14288330078125;
	setAttr ".tgi[5].ni[29].y" -794.28570556640625;
	setAttr ".tgi[5].ni[29].nvs" 18304;
	setAttr ".tgi[5].ni[30].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[30].y" -1814.2857666015625;
	setAttr ".tgi[5].ni[30].nvs" 1923;
	setAttr ".tgi[5].ni[31].x" -3545.71435546875;
	setAttr ".tgi[5].ni[31].y" -1394.2857666015625;
	setAttr ".tgi[5].ni[31].nvs" 18304;
	setAttr ".tgi[5].ni[32].x" -1982.1771240234375;
	setAttr ".tgi[5].ni[32].y" -1443.332763671875;
	setAttr ".tgi[5].ni[32].nvs" 18306;
	setAttr ".tgi[5].ni[33].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[33].y" -1252.857177734375;
	setAttr ".tgi[5].ni[33].nvs" 18304;
	setAttr ".tgi[5].ni[34].x" -717.14288330078125;
	setAttr ".tgi[5].ni[34].y" -1971.4285888671875;
	setAttr ".tgi[5].ni[34].nvs" 18304;
	setAttr ".tgi[5].ni[35].x" -717.14288330078125;
	setAttr ".tgi[5].ni[35].y" -1324.2857666015625;
	setAttr ".tgi[5].ni[35].nvs" 18304;
	setAttr ".tgi[5].ni[36].x" -3545.71435546875;
	setAttr ".tgi[5].ni[36].y" -1197.142822265625;
	setAttr ".tgi[5].ni[36].nvs" 18304;
	setAttr ".tgi[5].ni[37].x" -717.14288330078125;
	setAttr ".tgi[5].ni[37].y" -892.85711669921875;
	setAttr ".tgi[5].ni[37].nvs" 18304;
	setAttr ".tgi[5].ni[38].x" -2931.428466796875;
	setAttr ".tgi[5].ni[38].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[38].nvs" 18304;
	setAttr ".tgi[6].tn" -type "string" "Untitled_7";
	setAttr ".tgi[6].vl" -type "double2" 1088.4190862902346 -1426.5179969412816 ;
	setAttr ".tgi[6].vh" -type "double2" 1996.8224221547453 -858.45078598438158 ;
	setAttr -s 66 ".tgi[6].ni";
	setAttr ".tgi[6].ni[0].x" 1750;
	setAttr ".tgi[6].ni[0].y" -960;
	setAttr ".tgi[6].ni[0].nvs" 18304;
	setAttr ".tgi[6].ni[1].x" 6068.5712890625;
	setAttr ".tgi[6].ni[1].y" -1405.7142333984375;
	setAttr ".tgi[6].ni[1].nvs" 18304;
	setAttr ".tgi[6].ni[2].x" 7338.5712890625;
	setAttr ".tgi[6].ni[2].y" -1534.2857666015625;
	setAttr ".tgi[6].ni[2].nvs" 18304;
	setAttr ".tgi[6].ni[3].x" 7031.4287109375;
	setAttr ".tgi[6].ni[3].y" -1620;
	setAttr ".tgi[6].ni[3].nvs" 18304;
	setAttr ".tgi[6].ni[4].x" 6068.5712890625;
	setAttr ".tgi[6].ni[4].y" -827.14288330078125;
	setAttr ".tgi[6].ni[4].nvs" 18304;
	setAttr ".tgi[6].ni[5].x" 4521.4287109375;
	setAttr ".tgi[6].ni[5].y" -1291.4285888671875;
	setAttr ".tgi[6].ni[5].nvs" 18304;
	setAttr ".tgi[6].ni[6].x" 7031.4287109375;
	setAttr ".tgi[6].ni[6].y" -864.28570556640625;
	setAttr ".tgi[6].ni[6].nvs" 18304;
	setAttr ".tgi[6].ni[7].x" 7768.5712890625;
	setAttr ".tgi[6].ni[7].y" -632.85711669921875;
	setAttr ".tgi[6].ni[7].nvs" 18304;
	setAttr ".tgi[6].ni[8].x" 1400.84033203125;
	setAttr ".tgi[6].ni[8].y" -1032.43701171875;
	setAttr ".tgi[6].ni[8].nvs" 18306;
	setAttr ".tgi[6].ni[9].x" 2985.71435546875;
	setAttr ".tgi[6].ni[9].y" -1191.4285888671875;
	setAttr ".tgi[6].ni[9].nvs" 18304;
	setAttr ".tgi[6].ni[10].x" 7338.5712890625;
	setAttr ".tgi[6].ni[10].y" -1632.857177734375;
	setAttr ".tgi[6].ni[10].nvs" 18304;
	setAttr ".tgi[6].ni[11].x" 7768.5712890625;
	setAttr ".tgi[6].ni[11].y" -731.4285888671875;
	setAttr ".tgi[6].ni[11].nvs" 18304;
	setAttr ".tgi[6].ni[12].x" 828.5714111328125;
	setAttr ".tgi[6].ni[12].y" -1308.5714111328125;
	setAttr ".tgi[6].ni[12].nvs" 18304;
	setAttr ".tgi[6].ni[13].x" 5454.28564453125;
	setAttr ".tgi[6].ni[13].y" -904.28570556640625;
	setAttr ".tgi[6].ni[13].nvs" 18304;
	setAttr ".tgi[6].ni[14].x" 2064.28564453125;
	setAttr ".tgi[6].ni[14].y" -834.28570556640625;
	setAttr ".tgi[6].ni[14].nvs" 18304;
	setAttr ".tgi[6].ni[15].x" 7338.5712890625;
	setAttr ".tgi[6].ni[15].y" -842.85711669921875;
	setAttr ".tgi[6].ni[15].nvs" 18304;
	setAttr ".tgi[6].ni[16].x" 6068.5712890625;
	setAttr ".tgi[6].ni[16].y" -1255.7142333984375;
	setAttr ".tgi[6].ni[16].nvs" 18304;
	setAttr ".tgi[6].ni[17].x" 7768.5712890625;
	setAttr ".tgi[6].ni[17].y" -848.5714111328125;
	setAttr ".tgi[6].ni[17].nvs" 18304;
	setAttr ".tgi[6].ni[18].x" 6717.14306640625;
	setAttr ".tgi[6].ni[18].y" -1267.142822265625;
	setAttr ".tgi[6].ni[18].nvs" 18304;
	setAttr ".tgi[6].ni[19].x" 828.5714111328125;
	setAttr ".tgi[6].ni[19].y" -1012.8571166992188;
	setAttr ".tgi[6].ni[19].nvs" 18304;
	setAttr ".tgi[6].ni[20].x" 6068.5712890625;
	setAttr ".tgi[6].ni[20].y" -728.5714111328125;
	setAttr ".tgi[6].ni[20].nvs" 18304;
	setAttr ".tgi[6].ni[21].x" 3292.857177734375;
	setAttr ".tgi[6].ni[21].y" -1322.857177734375;
	setAttr ".tgi[6].ni[21].nvs" 18304;
	setAttr ".tgi[6].ni[22].x" 828.5714111328125;
	setAttr ".tgi[6].ni[22].y" -914.28570556640625;
	setAttr ".tgi[6].ni[22].nvs" 18304;
	setAttr ".tgi[6].ni[23].x" 4214.28564453125;
	setAttr ".tgi[6].ni[23].y" -1284.2857666015625;
	setAttr ".tgi[6].ni[23].nvs" 18304;
	setAttr ".tgi[6].ni[24].x" 828.5714111328125;
	setAttr ".tgi[6].ni[24].y" -815.71429443359375;
	setAttr ".tgi[6].ni[24].nvs" 18304;
	setAttr ".tgi[6].ni[25].x" 6410;
	setAttr ".tgi[6].ni[25].y" -805.71429443359375;
	setAttr ".tgi[6].ni[25].nvs" 18304;
	setAttr ".tgi[6].ni[26].x" 7338.5712890625;
	setAttr ".tgi[6].ni[26].y" -1027.142822265625;
	setAttr ".tgi[6].ni[26].nvs" 18304;
	setAttr ".tgi[6].ni[27].x" 2064.28564453125;
	setAttr ".tgi[6].ni[27].y" -932.85711669921875;
	setAttr ".tgi[6].ni[27].nvs" 18304;
	setAttr ".tgi[6].ni[28].x" 7768.5712890625;
	setAttr ".tgi[6].ni[28].y" -965.71429443359375;
	setAttr ".tgi[6].ni[28].nvs" 18304;
	setAttr ".tgi[6].ni[29].x" 7338.5712890625;
	setAttr ".tgi[6].ni[29].y" -1182.857177734375;
	setAttr ".tgi[6].ni[29].nvs" 19682;
	setAttr ".tgi[6].ni[30].x" 7768.5712890625;
	setAttr ".tgi[6].ni[30].y" -1064.2857666015625;
	setAttr ".tgi[6].ni[30].nvs" 18304;
	setAttr ".tgi[6].ni[31].x" 1135.7142333984375;
	setAttr ".tgi[6].ni[31].y" -1111.4285888671875;
	setAttr ".tgi[6].ni[31].nvs" 18304;
	setAttr ".tgi[6].ni[32].x" 5135.71435546875;
	setAttr ".tgi[6].ni[32].y" -1074.2857666015625;
	setAttr ".tgi[6].ni[32].nvs" 18304;
	setAttr ".tgi[6].ni[33].x" 4521.4287109375;
	setAttr ".tgi[6].ni[33].y" -644.28570556640625;
	setAttr ".tgi[6].ni[33].nvs" 18304;
	setAttr ".tgi[6].ni[34].x" 828.5714111328125;
	setAttr ".tgi[6].ni[34].y" -1505.7142333984375;
	setAttr ".tgi[6].ni[34].nvs" 18304;
	setAttr ".tgi[6].ni[35].x" 1750;
	setAttr ".tgi[6].ni[35].y" -1172.857177734375;
	setAttr ".tgi[6].ni[35].nvs" 18304;
	setAttr ".tgi[6].ni[36].x" 5761.4287109375;
	setAttr ".tgi[6].ni[36].y" -1438.5714111328125;
	setAttr ".tgi[6].ni[36].nvs" 18304;
	setAttr ".tgi[6].ni[37].x" 1135.7142333984375;
	setAttr ".tgi[6].ni[37].y" -1210;
	setAttr ".tgi[6].ni[37].nvs" 18304;
	setAttr ".tgi[6].ni[38].x" 5454.28564453125;
	setAttr ".tgi[6].ni[38].y" -805.71429443359375;
	setAttr ".tgi[6].ni[38].nvs" 18304;
	setAttr ".tgi[6].ni[39].x" 7768.5712890625;
	setAttr ".tgi[6].ni[39].y" -1181.4285888671875;
	setAttr ".tgi[6].ni[39].nvs" 18304;
	setAttr ".tgi[6].ni[40].x" 4828.5712890625;
	setAttr ".tgi[6].ni[40].y" -1302.857177734375;
	setAttr ".tgi[6].ni[40].nvs" 18304;
	setAttr ".tgi[6].ni[41].x" 7768.5712890625;
	setAttr ".tgi[6].ni[41].y" -1280;
	setAttr ".tgi[6].ni[41].nvs" 18304;
	setAttr ".tgi[6].ni[42].x" 6410;
	setAttr ".tgi[6].ni[42].y" -1374.2857666015625;
	setAttr ".tgi[6].ni[42].nvs" 18304;
	setAttr ".tgi[6].ni[43].x" 6717.14306640625;
	setAttr ".tgi[6].ni[43].y" -927.14288330078125;
	setAttr ".tgi[6].ni[43].nvs" 18304;
	setAttr ".tgi[6].ni[44].x" 828.5714111328125;
	setAttr ".tgi[6].ni[44].y" -1604.2857666015625;
	setAttr ".tgi[6].ni[44].nvs" 18304;
	setAttr ".tgi[6].ni[45].x" 3907.142822265625;
	setAttr ".tgi[6].ni[45].y" -1404.2857666015625;
	setAttr ".tgi[6].ni[45].nvs" 18304;
	setAttr ".tgi[6].ni[46].x" 6717.14306640625;
	setAttr ".tgi[6].ni[46].y" -828.5714111328125;
	setAttr ".tgi[6].ni[46].nvs" 18304;
	setAttr ".tgi[6].ni[47].x" 5135.71435546875;
	setAttr ".tgi[6].ni[47].y" -1344.2857666015625;
	setAttr ".tgi[6].ni[47].nvs" 18304;
	setAttr ".tgi[6].ni[48].x" 7768.5712890625;
	setAttr ".tgi[6].ni[48].y" -1378.5714111328125;
	setAttr ".tgi[6].ni[48].nvs" 18304;
	setAttr ".tgi[6].ni[49].x" 5454.28564453125;
	setAttr ".tgi[6].ni[49].y" -1368.5714111328125;
	setAttr ".tgi[6].ni[49].nvs" 18304;
	setAttr ".tgi[6].ni[50].x" 6410;
	setAttr ".tgi[6].ni[50].y" -1238.5714111328125;
	setAttr ".tgi[6].ni[50].nvs" 18304;
	setAttr ".tgi[6].ni[51].x" 2371.428466796875;
	setAttr ".tgi[6].ni[51].y" -928.5714111328125;
	setAttr ".tgi[6].ni[51].nvs" 18304;
	setAttr ".tgi[6].ni[52].x" 5135.71435546875;
	setAttr ".tgi[6].ni[52].y" -720;
	setAttr ".tgi[6].ni[52].nvs" 18304;
	setAttr ".tgi[6].ni[53].x" 7768.5712890625;
	setAttr ".tgi[6].ni[53].y" -1495.7142333984375;
	setAttr ".tgi[6].ni[53].nvs" 18304;
	setAttr ".tgi[6].ni[54].x" 1135.7142333984375;
	setAttr ".tgi[6].ni[54].y" -1012.8571166992188;
	setAttr ".tgi[6].ni[54].nvs" 18304;
	setAttr ".tgi[6].ni[55].x" 3600;
	setAttr ".tgi[6].ni[55].y" -1307.142822265625;
	setAttr ".tgi[6].ni[55].nvs" 18304;
	setAttr ".tgi[6].ni[56].x" 5761.4287109375;
	setAttr ".tgi[6].ni[56].y" -842.85711669921875;
	setAttr ".tgi[6].ni[56].nvs" 18304;
	setAttr ".tgi[6].ni[57].x" 3600;
	setAttr ".tgi[6].ni[57].y" -1442.857177734375;
	setAttr ".tgi[6].ni[57].nvs" 18304;
	setAttr ".tgi[6].ni[58].x" 2678.571533203125;
	setAttr ".tgi[6].ni[58].y" -1191.4285888671875;
	setAttr ".tgi[6].ni[58].nvs" 18304;
	setAttr ".tgi[6].ni[59].x" 5761.4287109375;
	setAttr ".tgi[6].ni[59].y" -1302.857177734375;
	setAttr ".tgi[6].ni[59].nvs" 18304;
	setAttr ".tgi[6].ni[60].x" 4828.5712890625;
	setAttr ".tgi[6].ni[60].y" -707.14288330078125;
	setAttr ".tgi[6].ni[60].nvs" 18304;
	setAttr ".tgi[6].ni[61].x" 828.5714111328125;
	setAttr ".tgi[6].ni[61].y" -1210;
	setAttr ".tgi[6].ni[61].nvs" 18304;
	setAttr ".tgi[6].ni[62].x" 7031.4287109375;
	setAttr ".tgi[6].ni[62].y" -1521.4285888671875;
	setAttr ".tgi[6].ni[62].nvs" 18304;
	setAttr ".tgi[6].ni[63].x" 7768.5712890625;
	setAttr ".tgi[6].ni[63].y" -1741.4285888671875;
	setAttr ".tgi[6].ni[63].nvs" 18304;
	setAttr ".tgi[6].ni[64].x" 828.5714111328125;
	setAttr ".tgi[6].ni[64].y" -1407.142822265625;
	setAttr ".tgi[6].ni[64].nvs" 18304;
	setAttr ".tgi[6].ni[65].x" 828.5714111328125;
	setAttr ".tgi[6].ni[65].y" -1111.4285888671875;
	setAttr ".tgi[6].ni[65].nvs" 18304;
createNode renderLayerManager -n "FK3:renderLayerManager";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009E3";
createNode renderLayer -n "FK3:defaultRenderLayer";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009E4";
	setAttr ".g" yes;
createNode multiplyDivide -n "FK3:multiplyDivide1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009E7";
	setAttr ".i2" -type "float3" 0.0099999998 1 1 ;
createNode multiplyDivide -n "FK3:multiplyDivide9";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009E8";
	setAttr ".i1" -type "float3" 7.0710678 0 0 ;
createNode multiplyDivide -n "FK3:multiplyDivide10";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009E9";
	setAttr ".i2" -type "float3" 3.5355339 0 3.9252311e-16 ;
createNode multiplyDivide -n "FK3:multiplyDivide11";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009EA";
	setAttr ".i2" -type "float3" 3.5355339 -6.2803697e-16 -1.9626156e-16 ;
createNode makeNurbCircle -n "FK3:makeNurbCircle2";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009EB";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 1.1477089008538313;
createNode makeNurbCircle -n "FK3:makeNurbCircle3";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009EC";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 0.72360073488113941;
createNode makeNurbCircle -n "FK3:makeNurbCircle4";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009ED";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 0.72360073488113941;
createNode network -n "FK3:ik:softik:inn";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009EE";
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
createNode network -n "FK3:ik:softik:metadata";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009EF";
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
createNode multiplyDivide -n "FK3:ik:softik:multiplyDivide4";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F0";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 2.7182817 0 0 ;
createNode multiplyDivide -n "FK3:ik:softik:multiplyDivide3";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F1";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode plusMinusAverage -n "FK3:ik:softik:plusMinusAverage4";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F2";
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode distanceBetween -n "FK3:ik:softik:distanceBetween1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F3";
createNode condition -n "FK3:ik:softik:condition2";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F4";
	setAttr ".op" 2;
createNode clamp -n "FK3:ik:softik:clamp1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F5";
	setAttr ".mn" -type "float3" 9.9999997e-05 0 0 ;
	setAttr ".mx" -type "float3" 999 0 0 ;
createNode plusMinusAverage -n "FK3:ik:softik:plusMinusAverage3";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F6";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  1 inf;
createNode blendTwoAttr -n "FK3:ik:softik:blendTwoAttr2";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F7";
	setAttr -s 2 ".i[0:1]"  1 1;
createNode multiplyDivide -n "FK3:ik:softik:multiplyDivide5";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F8";
createNode network -n "FK3:ik:softik:out";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009F9";
	addAttr -ci true -sn "outStretch" -ln "outStretch" -nn "outStretch" -at "float";
	addAttr -ci true -sn "outRatio" -ln "outRatio" -nn "outRatio" -at "float";
createNode multiplyDivide -n "FK3:ik:softik:multiplyDivide1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009FA";
createNode plusMinusAverage -n "FK3:ik:softik:plusMinusAverage1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009FB";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode condition -n "FK3:ik:softik:condition1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009FC";
	setAttr ".op" 2;
createNode multiplyDivide -n "FK3:ik:softik:multiplyDivide2";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009FD";
	setAttr ".op" 2;
createNode multiplyDivide -n "FK3:ik:softik:multiplyDivide7";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009FE";
	setAttr ".op" 2;
createNode plusMinusAverage -n "FK3:ik:softik:plusMinusAverage2";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D000009FF";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode blendTwoAttr -n "FK3:ik:softik:blendTwoAttr1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A00";
	setAttr -s 2 ".i";
	setAttr -s 2 ".i";
createNode multiplyDivide -n "FK3:ik:softik:multiplyDivide6";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A01";
	setAttr ".op" 2;
createNode network -n "FK3:inn";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A02";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	addAttr -ci true -sn "Guide01_LocalTm" -ln "Guide01_LocalTm" -dt "matrix";
	addAttr -ci true -sn "Guide02_LocalTm" -ln "Guide02_LocalTm" -dt "matrix";
	addAttr -ci true -sn "Guide03_LocalTm" -ln "Guide03_LocalTm" -dt "matrix";
	addAttr -ci true -sn "swivelDistanceRatio" -ln "swivelDistanceRatio" -dv 0.5 -min 
		0 -max 1 -at "double";
	setAttr "._graphpos" -type "float2" 0 1 ;
	setAttr -k on ".swivelDistanceRatio";
createNode decomposeMatrix -n "FK3:decomposeGuide01LocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A03";
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
createNode decomposeMatrix -n "FK3:decomposeGuide02LocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A04";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
createNode decomposeMatrix -n "FK3:decomposeGuide03LocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A05";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode network -n "FK3:out";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A06";
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
createNode decomposeMatrix -n "FK3:decomposeCtrlFk01DefaultLocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A07";
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
createNode decomposeMatrix -n "FK3:decomposeCtrlFk02DefaultLocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A08";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
createNode decomposeMatrix -n "FK3:decomposeCtrlFk03DefaultLocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A09";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode distanceBetween -n "FK3:getLimbSegment1Length";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A0A";
createNode distanceBetween -n "FK3:getLimbSegment2Length";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A0B";
createNode addDoubleLinear -n "FK3:getLimbLength";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A0C";
createNode multiplyDivide -n "FK3:multiplyDivide13";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A0D";
createNode multiplyDivide -n "FK3:multiplyDivide14";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A0E";
createNode animCurveTL -n "FK3:guide_02_translateX";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A0F";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.535533905932736 10 6.3911650194459524;
createNode animCurveTL -n "FK3:guide_02_translateY";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A10";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 1.8998827256160656e-16;
createNode animCurveTL -n "FK3:guide_02_translateZ";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A11";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.9252311467094363e-16 10 7.5484373465108625e-17;
createNode animCurveTU -n "FK3:guide_02_visibility";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A12";
	setAttr ".tan" 9;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
createNode animCurveTA -n "FK3:guide_02_rotateX";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A13";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTA -n "FK3:guide_02_rotateY";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A14";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTA -n "FK3:guide_02_rotateZ";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A15";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTU -n "FK3:guide_02_scaleX";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A16";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode animCurveTU -n "FK3:guide_02_scaleY";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A17";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode animCurveTU -n "FK3:guide_02_scaleZ";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A18";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode multMatrix -n "FK3:getGuide03WorldTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A19";
	setAttr -s 2 ".i";
createNode decomposeMatrix -n "FK3:decomposeGuide03WorldTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A1A";
	setAttr ".ot" -type "double3" -5.8878467200641577e-16 8.8817841970012523e-16 -1.3322676295501878e-15 ;
	setAttr ".or" -type "double3" 90 -45.000000000000028 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818829;
	setAttr ".oqz" -0.27059805007309845;
	setAttr ".oqw" 0.65328148243818829;
createNode multiplyDivide -n "FK3:getSwivelDistance";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A1B";
createNode multiplyDivide -n "FK3:getLimbRatio";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A1C";
	setAttr ".op" 2;
createNode plusMinusAverage -n "FK3:getLimbAim";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A1D";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode multiplyDivide -n "FK3:getLimbMiddleAim";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A1E";
createNode plusMinusAverage -n "FK3:getKneePosProjectedOnLimbDir";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A1F";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode plusMinusAverage -n "FK3:getKneeDirection";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A20";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode multMatrix -n "FK3:getGuide02WorldTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A21";
	setAttr -s 2 ".i";
createNode decomposeMatrix -n "FK3:decomposeGuide02WorldTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A22";
	setAttr ".ot" -type "double3" -3.9252311467094378e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".or" -type "double3" 90 45 -90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.65328148243818818;
	setAttr ".oqy" -0.27059805007309845;
	setAttr ".oqz" -0.65328148243818829;
	setAttr ".oqw" 0.27059805007309851;
createNode vectorProduct -n "FK3:getKneeDirectionNormalized";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A23";
	setAttr ".op" 0;
	setAttr ".no" yes;
createNode multiplyDivide -n "FK3:getKneeDirectionOffset";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A24";
createNode plusMinusAverage -n "FK3:getSwivelDefaultPos";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A25";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode decomposeMatrix -n "FK3:decomposeMatrix1";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A26";
	setAttr ".ot" -type "double3" 4.9303806576313249e-32 5 -5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
createNode decomposeMatrix -n "FK3:decomposeMatrix2";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A27";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
createNode decomposeMatrix -n "FK3:decomposeMatrix3";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A28";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
createNode nodeGraphEditorInfo -n "FK3:MayaNodeEditorSavedTabsInfo";
	rename -uid "6087C980-0000-3D03-5AD9-3B3D00000A29";
	setAttr ".def" no;
	setAttr -s 7 ".tgi";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -3738.3698148204944 -4396.4283967302044 ;
	setAttr ".tgi[0].vh" -type "double2" 2912.1793714598757 -2595.2379921126035 ;
	setAttr -s 63 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[0].y" 284.30282592773438;
	setAttr ".tgi[0].ni[0].nvs" 18314;
	setAttr ".tgi[0].ni[1].x" -934.78204345703125;
	setAttr ".tgi[0].ni[1].y" -7.1206927299499512;
	setAttr ".tgi[0].ni[1].nvs" 18314;
	setAttr ".tgi[0].ni[2].x" -3125.15478515625;
	setAttr ".tgi[0].ni[2].y" -2569.7314453125;
	setAttr ".tgi[0].ni[2].nvs" 18314;
	setAttr ".tgi[0].ni[3].x" -2791.646240234375;
	setAttr ".tgi[0].ni[3].y" -2204.69677734375;
	setAttr ".tgi[0].ni[3].nvs" 1931;
	setAttr ".tgi[0].ni[4].x" -2608.571533203125;
	setAttr ".tgi[0].ni[4].y" -2040;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" -2836.08544921875;
	setAttr ".tgi[0].ni[5].y" -1189.26611328125;
	setAttr ".tgi[0].ni[5].nvs" 18314;
	setAttr ".tgi[0].ni[6].x" -84.285713195800781;
	setAttr ".tgi[0].ni[6].y" -2127.142822265625;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" -2608.571533203125;
	setAttr ".tgi[0].ni[7].y" -1350;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" -2282.696533203125;
	setAttr ".tgi[0].ni[8].y" -3022.0634765625;
	setAttr ".tgi[0].ni[8].nvs" 1923;
	setAttr ".tgi[0].ni[9].x" -3180.7255859375;
	setAttr ".tgi[0].ni[9].y" -1443.1690673828125;
	setAttr ".tgi[0].ni[9].nvs" 18306;
	setAttr ".tgi[0].ni[10].x" -2608.571533203125;
	setAttr ".tgi[0].ni[10].y" -1448.5714111328125;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" -1914.81103515625;
	setAttr ".tgi[0].ni[11].y" -1854.3697509765625;
	setAttr ".tgi[0].ni[11].nvs" 18314;
	setAttr ".tgi[0].ni[12].x" -4220.34716796875;
	setAttr ".tgi[0].ni[12].y" -1645.202880859375;
	setAttr ".tgi[0].ni[12].nvs" 18313;
	setAttr ".tgi[0].ni[13].x" -934.78204345703125;
	setAttr ".tgi[0].ni[13].y" -1372.580810546875;
	setAttr ".tgi[0].ni[13].nvs" 18314;
	setAttr ".tgi[0].ni[14].x" -4220.34716796875;
	setAttr ".tgi[0].ni[14].y" -1245.670654296875;
	setAttr ".tgi[0].ni[14].nvs" 18313;
	setAttr ".tgi[0].ni[15].x" -3910.1220703125;
	setAttr ".tgi[0].ni[15].y" -1473.6390380859375;
	setAttr ".tgi[0].ni[15].nvs" 18314;
	setAttr ".tgi[0].ni[16].x" -1684.191650390625;
	setAttr ".tgi[0].ni[16].y" -2916.984130859375;
	setAttr ".tgi[0].ni[16].nvs" 18306;
	setAttr ".tgi[0].ni[17].x" -3317.874267578125;
	setAttr ".tgi[0].ni[17].y" -2000.0814208984375;
	setAttr ".tgi[0].ni[17].nvs" 18314;
	setAttr ".tgi[0].ni[18].x" 344.28570556640625;
	setAttr ".tgi[0].ni[18].y" -1784.2857666015625;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" -1609.2864990234375;
	setAttr ".tgi[0].ni[19].y" -770.93231201171875;
	setAttr ".tgi[0].ni[19].nvs" 18314;
	setAttr ".tgi[0].ni[20].x" -1372.857177734375;
	setAttr ".tgi[0].ni[20].y" -2048.571533203125;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" -1992.3165283203125;
	setAttr ".tgi[0].ni[21].y" -2653.79296875;
	setAttr ".tgi[0].ni[21].nvs" 1923;
	setAttr ".tgi[0].ni[22].x" -2608.571533203125;
	setAttr ".tgi[0].ni[22].y" -2138.571533203125;
	setAttr ".tgi[0].ni[22].nvs" 18304;
	setAttr ".tgi[0].ni[23].x" -504.69732666015625;
	setAttr ".tgi[0].ni[23].y" 1276.0828857421875;
	setAttr ".tgi[0].ni[23].nvs" 18314;
	setAttr ".tgi[0].ni[24].x" -3317.874267578125;
	setAttr ".tgi[0].ni[24].y" -1844.968994140625;
	setAttr ".tgi[0].ni[24].nvs" 18312;
	setAttr ".tgi[0].ni[25].x" 714.28570556640625;
	setAttr ".tgi[0].ni[25].y" -1784.2857666015625;
	setAttr ".tgi[0].ni[25].nvs" 18304;
	setAttr ".tgi[0].ni[26].x" -3568.920654296875;
	setAttr ".tgi[0].ni[26].y" -1715.50048828125;
	setAttr ".tgi[0].ni[26].nvs" 18306;
	setAttr ".tgi[0].ni[27].x" -504.69732666015625;
	setAttr ".tgi[0].ni[27].y" -867.29010009765625;
	setAttr ".tgi[0].ni[27].nvs" 1931;
	setAttr ".tgi[0].ni[28].x" -1625.73779296875;
	setAttr ".tgi[0].ni[28].y" -2420.765380859375;
	setAttr ".tgi[0].ni[28].nvs" 18314;
	setAttr ".tgi[0].ni[29].x" -3557.593505859375;
	setAttr ".tgi[0].ni[29].y" -1010.6516723632812;
	setAttr ".tgi[0].ni[29].nvs" 1931;
	setAttr ".tgi[0].ni[30].x" 714.28570556640625;
	setAttr ".tgi[0].ni[30].y" -2797.142822265625;
	setAttr ".tgi[0].ni[30].nvs" 18304;
	setAttr ".tgi[0].ni[31].x" -4222.697265625;
	setAttr ".tgi[0].ni[31].y" -1379.6314697265625;
	setAttr ".tgi[0].ni[31].nvs" 18313;
	setAttr ".tgi[0].ni[32].x" -1342.2041015625;
	setAttr ".tgi[0].ni[32].y" -3234.176025390625;
	setAttr ".tgi[0].ni[32].nvs" 18306;
	setAttr ".tgi[0].ni[33].x" -2948.89453125;
	setAttr ".tgi[0].ni[33].y" -1946.027099609375;
	setAttr ".tgi[0].ni[33].nvs" 18312;
	setAttr ".tgi[0].ni[34].x" -2608.571533203125;
	setAttr ".tgi[0].ni[34].y" -1744.2857666015625;
	setAttr ".tgi[0].ni[34].nvs" 18304;
	setAttr ".tgi[0].ni[35].x" -504.69732666015625;
	setAttr ".tgi[0].ni[35].y" -162.23320007324219;
	setAttr ".tgi[0].ni[35].nvs" 18314;
	setAttr ".tgi[0].ni[36].x" 344.28570556640625;
	setAttr ".tgi[0].ni[36].y" -2397.142822265625;
	setAttr ".tgi[0].ni[36].nvs" 18304;
	setAttr ".tgi[0].ni[37].x" 344.28570556640625;
	setAttr ".tgi[0].ni[37].y" -2895.71435546875;
	setAttr ".tgi[0].ni[37].nvs" 18304;
	setAttr ".tgi[0].ni[38].x" -3632.42724609375;
	setAttr ".tgi[0].ni[38].y" -1477.7398681640625;
	setAttr ".tgi[0].ni[38].nvs" 18306;
	setAttr ".tgi[0].ni[39].x" -934.78204345703125;
	setAttr ".tgi[0].ni[39].y" 709.6871337890625;
	setAttr ".tgi[0].ni[39].nvs" 18314;
	setAttr ".tgi[0].ni[40].x" 714.28570556640625;
	setAttr ".tgi[0].ni[40].y" -2895.71435546875;
	setAttr ".tgi[0].ni[40].nvs" 18304;
	setAttr ".tgi[0].ni[41].x" -2572.8642578125;
	setAttr ".tgi[0].ni[41].y" -745.0802001953125;
	setAttr ".tgi[0].ni[41].nvs" 18314;
	setAttr ".tgi[0].ni[42].x" -3559.94384765625;
	setAttr ".tgi[0].ni[42].y" -792.08404541015625;
	setAttr ".tgi[0].ni[42].nvs" 1931;
	setAttr ".tgi[0].ni[43].x" -2970.046142578125;
	setAttr ".tgi[0].ni[43].y" -425.45443725585938;
	setAttr ".tgi[0].ni[43].nvs" 18314;
	setAttr ".tgi[0].ni[44].x" -2608.571533203125;
	setAttr ".tgi[0].ni[44].y" -1941.4285888671875;
	setAttr ".tgi[0].ni[44].nvs" 18304;
	setAttr ".tgi[0].ni[45].x" -504.69732666015625;
	setAttr ".tgi[0].ni[45].y" -1513.5921630859375;
	setAttr ".tgi[0].ni[45].nvs" 1931;
	setAttr ".tgi[0].ni[46].x" -2608.571533203125;
	setAttr ".tgi[0].ni[46].y" -1645.7142333984375;
	setAttr ".tgi[0].ni[46].nvs" 18304;
	setAttr ".tgi[0].ni[47].x" -1045.780029296875;
	setAttr ".tgi[0].ni[47].y" -3607.777099609375;
	setAttr ".tgi[0].ni[47].nvs" 18306;
	setAttr ".tgi[0].ni[48].x" -3557.593505859375;
	setAttr ".tgi[0].ni[48].y" -1245.670654296875;
	setAttr ".tgi[0].ni[48].nvs" 1931;
	setAttr ".tgi[0].ni[49].x" -2438.543212890625;
	setAttr ".tgi[0].ni[49].y" -2591.839599609375;
	setAttr ".tgi[0].ni[49].nvs" 18306;
	setAttr ".tgi[0].ni[50].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[50].y" -1755.6617431640625;
	setAttr ".tgi[0].ni[50].nvs" 18314;
	setAttr ".tgi[0].ni[51].x" -934.78204345703125;
	setAttr ".tgi[0].ni[51].y" 1435.895751953125;
	setAttr ".tgi[0].ni[51].nvs" 18314;
	setAttr ".tgi[0].ni[52].x" -1914.81103515625;
	setAttr ".tgi[0].ni[52].y" -1217.4683837890625;
	setAttr ".tgi[0].ni[52].nvs" 18314;
	setAttr ".tgi[0].ni[53].x" -619.85455322265625;
	setAttr ".tgi[0].ni[53].y" -3527.8486328125;
	setAttr ".tgi[0].ni[53].nvs" 1923;
	setAttr ".tgi[0].ni[54].x" -2608.571533203125;
	setAttr ".tgi[0].ni[54].y" -1842.857177734375;
	setAttr ".tgi[0].ni[54].nvs" 18304;
	setAttr ".tgi[0].ni[55].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[55].y" -510.061279296875;
	setAttr ".tgi[0].ni[55].nvs" 1931;
	setAttr ".tgi[0].ni[56].x" -504.69732666015625;
	setAttr ".tgi[0].ni[56].y" 556.9248046875;
	setAttr ".tgi[0].ni[56].nvs" 1931;
	setAttr ".tgi[0].ni[57].x" -265.63861083984375;
	setAttr ".tgi[0].ni[57].y" -3593.725830078125;
	setAttr ".tgi[0].ni[57].nvs" 18306;
	setAttr ".tgi[0].ni[58].x" -2264.9892578125;
	setAttr ".tgi[0].ni[58].y" -1344.3785400390625;
	setAttr ".tgi[0].ni[58].nvs" 18314;
	setAttr ".tgi[0].ni[59].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[59].y" -1057.6553955078125;
	setAttr ".tgi[0].ni[59].nvs" 18314;
	setAttr ".tgi[0].ni[60].x" -1602.093994140625;
	setAttr ".tgi[0].ni[60].y" -3595.533203125;
	setAttr ".tgi[0].ni[60].nvs" 18306;
	setAttr ".tgi[0].ni[61].x" -934.78204345703125;
	setAttr ".tgi[0].ni[61].y" -667.52398681640625;
	setAttr ".tgi[0].ni[61].nvs" 18314;
	setAttr ".tgi[0].ni[62].x" -2608.571533203125;
	setAttr ".tgi[0].ni[62].y" -1547.142822265625;
	setAttr ".tgi[0].ni[62].nvs" 18304;
	setAttr ".tgi[1].tn" -type "string" "Untitled_2";
	setAttr ".tgi[1].vl" -type "double2" -1450.9156932615472 -680.95235389376558 ;
	setAttr ".tgi[1].vh" -type "double2" 3555.6775143877203 674.99997317791099 ;
	setAttr -s 42 ".tgi[1].ni";
	setAttr ".tgi[1].ni[0].x" 1092.040771484375;
	setAttr ".tgi[1].ni[0].y" 1.5936880111694336;
	setAttr ".tgi[1].ni[0].nvs" 18313;
	setAttr ".tgi[1].ni[1].x" 1775.695556640625;
	setAttr ".tgi[1].ni[1].y" 414.17254638671875;
	setAttr ".tgi[1].ni[1].nvs" 18306;
	setAttr ".tgi[1].ni[2].x" 5058.5712890625;
	setAttr ".tgi[1].ni[2].y" -765.71429443359375;
	setAttr ".tgi[1].ni[2].nvs" 18304;
	setAttr ".tgi[1].ni[3].x" 2902.684326171875;
	setAttr ".tgi[1].ni[3].y" -622.25701904296875;
	setAttr ".tgi[1].ni[3].nvs" 1931;
	setAttr ".tgi[1].ni[4].x" 1231.4013671875;
	setAttr ".tgi[1].ni[4].y" 1002.9470825195312;
	setAttr ".tgi[1].ni[4].nvs" 18306;
	setAttr ".tgi[1].ni[5].x" 5372.85693359375;
	setAttr ".tgi[1].ni[5].y" -900;
	setAttr ".tgi[1].ni[5].nvs" 18304;
	setAttr ".tgi[1].ni[6].x" 128.57142639160156;
	setAttr ".tgi[1].ni[6].y" 494.28570556640625;
	setAttr ".tgi[1].ni[6].nvs" 18312;
	setAttr ".tgi[1].ni[7].x" 777.67034912109375;
	setAttr ".tgi[1].ni[7].y" 346.83428955078125;
	setAttr ".tgi[1].ni[7].nvs" 18314;
	setAttr ".tgi[1].ni[8].x" 5801.4287109375;
	setAttr ".tgi[1].ni[8].y" -664.28570556640625;
	setAttr ".tgi[1].ni[8].nvs" 18304;
	setAttr ".tgi[1].ni[9].x" 440.24679565429688;
	setAttr ".tgi[1].ni[9].y" 493.32656860351562;
	setAttr ".tgi[1].ni[9].nvs" 18313;
	setAttr ".tgi[1].ni[10].x" 2377.003662109375;
	setAttr ".tgi[1].ni[10].y" -456.60031127929688;
	setAttr ".tgi[1].ni[10].nvs" 18314;
	setAttr ".tgi[1].ni[11].x" 4130;
	setAttr ".tgi[1].ni[11].y" -297.14285278320312;
	setAttr ".tgi[1].ni[11].nvs" 18304;
	setAttr ".tgi[1].ni[12].x" 5372.85693359375;
	setAttr ".tgi[1].ni[12].y" -1131.4285888671875;
	setAttr ".tgi[1].ni[12].nvs" 18304;
	setAttr ".tgi[1].ni[13].x" 128.57142639160156;
	setAttr ".tgi[1].ni[13].y" 592.85711669921875;
	setAttr ".tgi[1].ni[13].nvs" 18312;
	setAttr ".tgi[1].ni[14].x" 1171.720703125;
	setAttr ".tgi[1].ni[14].y" -329.415283203125;
	setAttr ".tgi[1].ni[14].nvs" 1931;
	setAttr ".tgi[1].ni[15].x" 1171.720703125;
	setAttr ".tgi[1].ni[15].y" -470.35821533203125;
	setAttr ".tgi[1].ni[15].nvs" 1931;
	setAttr ".tgi[1].ni[16].x" 2906.5791015625;
	setAttr ".tgi[1].ni[16].y" -384.2847900390625;
	setAttr ".tgi[1].ni[16].nvs" 1931;
	setAttr ".tgi[1].ni[17].x" 1794.710205078125;
	setAttr ".tgi[1].ni[17].y" 692.2615966796875;
	setAttr ".tgi[1].ni[17].nvs" 18306;
	setAttr ".tgi[1].ni[18].x" 5372.85693359375;
	setAttr ".tgi[1].ni[18].y" -1305.7142333984375;
	setAttr ".tgi[1].ni[18].nvs" 18304;
	setAttr ".tgi[1].ni[19].x" 1495.360595703125;
	setAttr ".tgi[1].ni[19].y" 215.49528503417969;
	setAttr ".tgi[1].ni[19].nvs" 18312;
	setAttr ".tgi[1].ni[20].x" 2605.094970703125;
	setAttr ".tgi[1].ni[20].y" -352.89810180664062;
	setAttr ".tgi[1].ni[20].nvs" 1931;
	setAttr ".tgi[1].ni[21].x" 128.57142639160156;
	setAttr ".tgi[1].ni[21].y" 691.4285888671875;
	setAttr ".tgi[1].ni[21].nvs" 18312;
	setAttr ".tgi[1].ni[22].x" 1445.1500244140625;
	setAttr ".tgi[1].ni[22].y" -404.11505126953125;
	setAttr ".tgi[1].ni[22].nvs" 1931;
	setAttr ".tgi[1].ni[23].x" 5372.85693359375;
	setAttr ".tgi[1].ni[23].y" -560;
	setAttr ".tgi[1].ni[23].nvs" 18304;
	setAttr ".tgi[1].ni[24].x" 2948.19287109375;
	setAttr ".tgi[1].ni[24].y" -885.89019775390625;
	setAttr ".tgi[1].ni[24].nvs" 1931;
	setAttr ".tgi[1].ni[25].x" 5801.4287109375;
	setAttr ".tgi[1].ni[25].y" -838.5714111328125;
	setAttr ".tgi[1].ni[25].nvs" 18304;
	setAttr ".tgi[1].ni[26].x" 2612.2412109375;
	setAttr ".tgi[1].ni[26].y" -847.4547119140625;
	setAttr ".tgi[1].ni[26].nvs" 1931;
	setAttr ".tgi[1].ni[27].x" 2615.598876953125;
	setAttr ".tgi[1].ni[27].y" -604.36865234375;
	setAttr ".tgi[1].ni[27].nvs" 1931;
	setAttr ".tgi[1].ni[28].x" 2027.486572265625;
	setAttr ".tgi[1].ni[28].y" 71.034370422363281;
	setAttr ".tgi[1].ni[28].nvs" 18312;
	setAttr ".tgi[1].ni[29].x" 775.30780029296875;
	setAttr ".tgi[1].ni[29].y" 602.08502197265625;
	setAttr ".tgi[1].ni[29].nvs" 18314;
	setAttr ".tgi[1].ni[30].x" 1484.4676513671875;
	setAttr ".tgi[1].ni[30].y" 57.473037719726562;
	setAttr ".tgi[1].ni[30].nvs" 18312;
	setAttr ".tgi[1].ni[31].x" 5801.4287109375;
	setAttr ".tgi[1].ni[31].y" -1208.5714111328125;
	setAttr ".tgi[1].ni[31].nvs" 18304;
	setAttr ".tgi[1].ni[32].x" 766.423095703125;
	setAttr ".tgi[1].ni[32].y" 94.310020446777344;
	setAttr ".tgi[1].ni[32].nvs" 18314;
	setAttr ".tgi[1].ni[33].x" 4744.28564453125;
	setAttr ".tgi[1].ni[33].y" -538.5714111328125;
	setAttr ".tgi[1].ni[33].nvs" 18304;
	setAttr ".tgi[1].ni[34].x" 5801.4287109375;
	setAttr ".tgi[1].ni[34].y" -1325.7142333984375;
	setAttr ".tgi[1].ni[34].nvs" 18304;
	setAttr ".tgi[1].ni[35].x" 1087.7464599609375;
	setAttr ".tgi[1].ni[35].y" 382.31390380859375;
	setAttr ".tgi[1].ni[35].nvs" 18313;
	setAttr ".tgi[1].ni[36].x" 1062.303466796875;
	setAttr ".tgi[1].ni[36].y" 502.62240600585938;
	setAttr ".tgi[1].ni[36].nvs" 18312;
	setAttr ".tgi[1].ni[37].x" 1082.3115234375;
	setAttr ".tgi[1].ni[37].y" 629.90948486328125;
	setAttr ".tgi[1].ni[37].nvs" 18313;
	setAttr ".tgi[1].ni[38].x" 5801.4287109375;
	setAttr ".tgi[1].ni[38].y" -565.71429443359375;
	setAttr ".tgi[1].ni[38].nvs" 18304;
	setAttr ".tgi[1].ni[39].x" 2432.826904296875;
	setAttr ".tgi[1].ni[39].y" 108.26145935058594;
	setAttr ".tgi[1].ni[39].nvs" 18312;
	setAttr ".tgi[1].ni[40].x" 2011.998046875;
	setAttr ".tgi[1].ni[40].y" 200.9871826171875;
	setAttr ".tgi[1].ni[40].nvs" 18312;
	setAttr ".tgi[1].ni[41].x" 2439.32275390625;
	setAttr ".tgi[1].ni[41].y" 287.60781860351562;
	setAttr ".tgi[1].ni[41].nvs" 18312;
	setAttr ".tgi[2].tn" -type "string" "Untitled_3";
	setAttr ".tgi[2].vl" -type "double2" -8840.8879270829548 815.47615807207944 ;
	setAttr ".tgi[2].vh" -type "double2" -5122.2067561687491 1822.6189751946765 ;
	setAttr -s 20 ".tgi[2].ni";
	setAttr ".tgi[2].ni[0].x" -2984.28564453125;
	setAttr ".tgi[2].ni[0].y" 1490;
	setAttr ".tgi[2].ni[0].nvs" 18304;
	setAttr ".tgi[2].ni[1].x" -7046.1904296875;
	setAttr ".tgi[2].ni[1].y" 1695.8096923828125;
	setAttr ".tgi[2].ni[1].nvs" 18305;
	setAttr ".tgi[2].ni[2].x" -3581.855712890625;
	setAttr ".tgi[2].ni[2].y" 1680.837158203125;
	setAttr ".tgi[2].ni[2].nvs" 18305;
	setAttr ".tgi[2].ni[3].x" -6670;
	setAttr ".tgi[2].ni[3].y" 1308.5714111328125;
	setAttr ".tgi[2].ni[3].nvs" 18304;
	setAttr ".tgi[2].ni[4].x" -6362.85693359375;
	setAttr ".tgi[2].ni[4].y" 1158.5714111328125;
	setAttr ".tgi[2].ni[4].nvs" 18304;
	setAttr ".tgi[2].ni[5].x" -5748.5712890625;
	setAttr ".tgi[2].ni[5].y" 1238.5714111328125;
	setAttr ".tgi[2].ni[5].nvs" 18304;
	setAttr ".tgi[2].ni[6].x" -6647.90478515625;
	setAttr ".tgi[2].ni[6].y" 1642.2860107421875;
	setAttr ".tgi[2].ni[6].nvs" 18305;
	setAttr ".tgi[2].ni[7].x" -6055.71435546875;
	setAttr ".tgi[2].ni[7].y" 1120;
	setAttr ".tgi[2].ni[7].nvs" 18304;
	setAttr ".tgi[2].ni[8].x" -5441.4287109375;
	setAttr ".tgi[2].ni[8].y" 1251.4285888671875;
	setAttr ".tgi[2].ni[8].nvs" 18304;
	setAttr ".tgi[2].ni[9].x" -3291.428466796875;
	setAttr ".tgi[2].ni[9].y" 1488.5714111328125;
	setAttr ".tgi[2].ni[9].nvs" 18306;
	setAttr ".tgi[2].ni[10].x" -3598.571533203125;
	setAttr ".tgi[2].ni[10].y" 1354.2857666015625;
	setAttr ".tgi[2].ni[10].nvs" 18305;
	setAttr ".tgi[2].ni[11].x" -4490.2841796875;
	setAttr ".tgi[2].ni[11].y" 1141.6575927734375;
	setAttr ".tgi[2].ni[11].nvs" 18305;
	setAttr ".tgi[2].ni[12].x" -3905.71435546875;
	setAttr ".tgi[2].ni[12].y" 1311.4285888671875;
	setAttr ".tgi[2].ni[12].nvs" 18304;
	setAttr ".tgi[2].ni[13].x" -4212.85693359375;
	setAttr ".tgi[2].ni[13].y" 1237.142822265625;
	setAttr ".tgi[2].ni[13].nvs" 18304;
	setAttr ".tgi[2].ni[14].x" -5134.28564453125;
	setAttr ".tgi[2].ni[14].y" 1267.142822265625;
	setAttr ".tgi[2].ni[14].nvs" 18304;
	setAttr ".tgi[2].ni[15].x" -3905.71435546875;
	setAttr ".tgi[2].ni[15].y" 1582.185302734375;
	setAttr ".tgi[2].ni[15].nvs" 18305;
	setAttr ".tgi[2].ni[16].x" -4212.85693359375;
	setAttr ".tgi[2].ni[16].y" 1634.1630859375;
	setAttr ".tgi[2].ni[16].nvs" 18305;
	setAttr ".tgi[2].ni[17].x" -4831.2265625;
	setAttr ".tgi[2].ni[17].y" 1315.84912109375;
	setAttr ".tgi[2].ni[17].nvs" 18305;
	setAttr ".tgi[2].ni[18].x" -6362.85693359375;
	setAttr ".tgi[2].ni[18].y" 1022.8571166992188;
	setAttr ".tgi[2].ni[18].nvs" 18304;
	setAttr ".tgi[2].ni[19].x" -7416.857421875;
	setAttr ".tgi[2].ni[19].y" 1527.61865234375;
	setAttr ".tgi[2].ni[19].nvs" 18305;
	setAttr ".tgi[3].tn" -type "string" "Untitled_4";
	setAttr ".tgi[3].vl" -type "double2" -5796.1536158353956 -772.61901691792741 ;
	setAttr ".tgi[3].vh" -type "double2" -1703.8460861413939 335.71427237419795 ;
	setAttr -s 33 ".tgi[3].ni";
	setAttr ".tgi[3].ni[0].x" -2780;
	setAttr ".tgi[3].ni[0].y" -194.28572082519531;
	setAttr ".tgi[3].ni[0].nvs" 18304;
	setAttr ".tgi[3].ni[1].x" 905.71429443359375;
	setAttr ".tgi[3].ni[1].y" 47.142856597900391;
	setAttr ".tgi[3].ni[1].nvs" 18304;
	setAttr ".tgi[3].ni[2].x" -4008.571533203125;
	setAttr ".tgi[3].ni[2].y" -58.571430206298828;
	setAttr ".tgi[3].ni[2].nvs" 18304;
	setAttr ".tgi[3].ni[3].x" -3394.28564453125;
	setAttr ".tgi[3].ni[3].y" -157.14285278320312;
	setAttr ".tgi[3].ni[3].nvs" 18304;
	setAttr ".tgi[3].ni[4].x" 291.42855834960938;
	setAttr ".tgi[3].ni[4].y" 47.142856597900391;
	setAttr ".tgi[3].ni[4].nvs" 18304;
	setAttr ".tgi[3].ni[5].x" -17.39495849609375;
	setAttr ".tgi[3].ni[5].y" -97.058822631835938;
	setAttr ".tgi[3].ni[5].nvs" 18305;
	setAttr ".tgi[3].ni[6].x" -4630;
	setAttr ".tgi[3].ni[6].y" -364.28570556640625;
	setAttr ".tgi[3].ni[6].nvs" 18304;
	setAttr ".tgi[3].ni[7].x" -4315.71435546875;
	setAttr ".tgi[3].ni[7].y" -30;
	setAttr ".tgi[3].ni[7].nvs" 18304;
	setAttr ".tgi[3].ni[8].x" -2165.71435546875;
	setAttr ".tgi[3].ni[8].y" -192.85714721679688;
	setAttr ".tgi[3].ni[8].nvs" 18304;
	setAttr ".tgi[3].ni[9].x" -4630;
	setAttr ".tgi[3].ni[9].y" -167.14285278320312;
	setAttr ".tgi[3].ni[9].nvs" 18304;
	setAttr ".tgi[3].ni[10].x" -4315.71435546875;
	setAttr ".tgi[3].ni[10].y" -232.85714721679688;
	setAttr ".tgi[3].ni[10].nvs" 18304;
	setAttr ".tgi[3].ni[11].x" -4008.571533203125;
	setAttr ".tgi[3].ni[11].y" -274.28570556640625;
	setAttr ".tgi[3].ni[11].nvs" 18304;
	setAttr ".tgi[3].ni[12].x" -5244.28564453125;
	setAttr ".tgi[3].ni[12].y" -364.28570556640625;
	setAttr ".tgi[3].ni[12].nvs" 18304;
	setAttr ".tgi[3].ni[13].x" -2472.857177734375;
	setAttr ".tgi[3].ni[13].y" -261.42855834960938;
	setAttr ".tgi[3].ni[13].nvs" 18304;
	setAttr ".tgi[3].ni[14].x" -1858.5714111328125;
	setAttr ".tgi[3].ni[14].y" -192.85714721679688;
	setAttr ".tgi[3].ni[14].nvs" 18304;
	setAttr ".tgi[3].ni[15].x" 1290;
	setAttr ".tgi[3].ni[15].y" 47.142856597900391;
	setAttr ".tgi[3].ni[15].nvs" 18304;
	setAttr ".tgi[3].ni[16].x" -3087.142822265625;
	setAttr ".tgi[3].ni[16].y" -130;
	setAttr ".tgi[3].ni[16].nvs" 18304;
	setAttr ".tgi[3].ni[17].x" -4937.14306640625;
	setAttr ".tgi[3].ni[17].y" -265.71429443359375;
	setAttr ".tgi[3].ni[17].nvs" 18304;
	setAttr ".tgi[3].ni[18].x" -3111.67724609375;
	setAttr ".tgi[3].ni[18].y" 233.31568908691406;
	setAttr ".tgi[3].ni[18].nvs" 18305;
	setAttr ".tgi[3].ni[19].x" -4019.244384765625;
	setAttr ".tgi[3].ni[19].y" 120.07266235351562;
	setAttr ".tgi[3].ni[19].nvs" 18304;
	setAttr ".tgi[3].ni[20].x" 598.5714111328125;
	setAttr ".tgi[3].ni[20].y" 18.571428298950195;
	setAttr ".tgi[3].ni[20].nvs" 18304;
	setAttr ".tgi[3].ni[21].x" -4315.71435546875;
	setAttr ".tgi[3].ni[21].y" -331.42855834960938;
	setAttr ".tgi[3].ni[21].nvs" 18304;
	setAttr ".tgi[3].ni[22].x" -5244.28564453125;
	setAttr ".tgi[3].ni[22].y" -265.71429443359375;
	setAttr ".tgi[3].ni[22].nvs" 18304;
	setAttr ".tgi[3].ni[23].x" -937.14288330078125;
	setAttr ".tgi[3].ni[23].y" -82.857139587402344;
	setAttr ".tgi[3].ni[23].nvs" 18304;
	setAttr ".tgi[3].ni[24].x" -4011.748291015625;
	setAttr ".tgi[3].ni[24].y" -168.62957763671875;
	setAttr ".tgi[3].ni[24].nvs" 18304;
	setAttr ".tgi[3].ni[25].x" -322.85714721679688;
	setAttr ".tgi[3].ni[25].y" -57.142856597900391;
	setAttr ".tgi[3].ni[25].nvs" 18304;
	setAttr ".tgi[3].ni[26].x" -630;
	setAttr ".tgi[3].ni[26].y" -68.571426391601562;
	setAttr ".tgi[3].ni[26].nvs" 18304;
	setAttr ".tgi[3].ni[27].x" -1551.4285888671875;
	setAttr ".tgi[3].ni[27].y" -184.28572082519531;
	setAttr ".tgi[3].ni[27].nvs" 18304;
	setAttr ".tgi[3].ni[28].x" -4630;
	setAttr ".tgi[3].ni[28].y" -265.71429443359375;
	setAttr ".tgi[3].ni[28].nvs" 18304;
	setAttr ".tgi[3].ni[29].x" -5244.28564453125;
	setAttr ".tgi[3].ni[29].y" -167.14285278320312;
	setAttr ".tgi[3].ni[29].nvs" 18304;
	setAttr ".tgi[3].ni[30].x" -2780;
	setAttr ".tgi[3].ni[30].y" -330;
	setAttr ".tgi[3].ni[30].nvs" 18304;
	setAttr ".tgi[3].ni[31].x" -1244.2857666015625;
	setAttr ".tgi[3].ni[31].y" -131.42857360839844;
	setAttr ".tgi[3].ni[31].nvs" 18304;
	setAttr ".tgi[3].ni[32].x" -3676.175048828125;
	setAttr ".tgi[3].ni[32].y" 24.352910995483398;
	setAttr ".tgi[3].ni[32].nvs" 18305;
	setAttr ".tgi[4].tn" -type "string" "Untitled_5";
	setAttr ".tgi[4].vl" -type "double2" -10737.957448769785 -1854.7618310602825 ;
	setAttr ".tgi[4].vh" -type "double2" -6720.3751908317427 -766.66663620206236 ;
	setAttr -s 69 ".tgi[4].ni";
	setAttr ".tgi[4].ni[0].x" -2367.142822265625;
	setAttr ".tgi[4].ni[0].y" -1208.5714111328125;
	setAttr ".tgi[4].ni[0].nvs" 18304;
	setAttr ".tgi[4].ni[1].x" -3391.428466796875;
	setAttr ".tgi[4].ni[1].y" -985.71429443359375;
	setAttr ".tgi[4].ni[1].nvs" 18304;
	setAttr ".tgi[4].ni[2].x" -957.14288330078125;
	setAttr ".tgi[4].ni[2].y" -1032.857177734375;
	setAttr ".tgi[4].ni[2].nvs" 18304;
	setAttr ".tgi[4].ni[3].x" -8614.15234375;
	setAttr ".tgi[4].ni[3].y" -1219.30224609375;
	setAttr ".tgi[4].ni[3].nvs" 18306;
	setAttr ".tgi[4].ni[4].x" -1692.857177734375;
	setAttr ".tgi[4].ni[4].y" -762.85711669921875;
	setAttr ".tgi[4].ni[4].nvs" 18304;
	setAttr ".tgi[4].ni[5].x" -8920;
	setAttr ".tgi[4].ni[5].y" -1061.4285888671875;
	setAttr ".tgi[4].ni[5].nvs" 18304;
	setAttr ".tgi[4].ni[6].x" -8920;
	setAttr ".tgi[4].ni[6].y" -845.71429443359375;
	setAttr ".tgi[4].ni[6].nvs" 18304;
	setAttr ".tgi[4].ni[7].x" -10155.7138671875;
	setAttr ".tgi[4].ni[7].y" -1110;
	setAttr ".tgi[4].ni[7].nvs" 18304;
	setAttr ".tgi[4].ni[8].x" -9542.23828125;
	setAttr ".tgi[4].ni[8].y" -1033.5311279296875;
	setAttr ".tgi[4].ni[8].nvs" 18306;
	setAttr ".tgi[4].ni[9].x" -7691.4287109375;
	setAttr ".tgi[4].ni[9].y" -855.71429443359375;
	setAttr ".tgi[4].ni[9].nvs" 18304;
	setAttr ".tgi[4].ni[10].x" -5848.5712890625;
	setAttr ".tgi[4].ni[10].y" -1038.5714111328125;
	setAttr ".tgi[4].ni[10].nvs" 18304;
	setAttr ".tgi[4].ni[11].x" -2367.142822265625;
	setAttr ".tgi[4].ni[11].y" -764.28570556640625;
	setAttr ".tgi[4].ni[11].nvs" 18304;
	setAttr ".tgi[4].ni[12].x" -10155.7138671875;
	setAttr ".tgi[4].ni[12].y" -1208.5714111328125;
	setAttr ".tgi[4].ni[12].nvs" 18304;
	setAttr ".tgi[4].ni[13].x" -10155.7138671875;
	setAttr ".tgi[4].ni[13].y" -1307.142822265625;
	setAttr ".tgi[4].ni[13].nvs" 18304;
	setAttr ".tgi[4].ni[14].x" -10155.7138671875;
	setAttr ".tgi[4].ni[14].y" -617.14288330078125;
	setAttr ".tgi[4].ni[14].nvs" 18304;
	setAttr ".tgi[4].ni[15].x" -7691.4287109375;
	setAttr ".tgi[4].ni[15].y" -991.4285888671875;
	setAttr ".tgi[4].ni[15].nvs" 18304;
	setAttr ".tgi[4].ni[16].x" -957.14288330078125;
	setAttr ".tgi[4].ni[16].y" -465.71429443359375;
	setAttr ".tgi[4].ni[16].nvs" 18304;
	setAttr ".tgi[4].ni[17].x" -8945.8779296875;
	setAttr ".tgi[4].ni[17].y" -1389.3060302734375;
	setAttr ".tgi[4].ni[17].nvs" 18306;
	setAttr ".tgi[4].ni[18].x" -5234.28564453125;
	setAttr ".tgi[4].ni[18].y" -1090;
	setAttr ".tgi[4].ni[18].nvs" 18304;
	setAttr ".tgi[4].ni[19].x" -9848.5712890625;
	setAttr ".tgi[4].ni[19].y" -1110;
	setAttr ".tgi[4].ni[19].nvs" 18304;
	setAttr ".tgi[4].ni[20].x" -4312.85693359375;
	setAttr ".tgi[4].ni[20].y" -945.71429443359375;
	setAttr ".tgi[4].ni[20].nvs" 18304;
	setAttr ".tgi[4].ni[21].x" -6155.71435546875;
	setAttr ".tgi[4].ni[21].y" -1094.2857666015625;
	setAttr ".tgi[4].ni[21].nvs" 18304;
	setAttr ".tgi[4].ni[22].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[22].y" -1124.2857666015625;
	setAttr ".tgi[4].ni[22].nvs" 18304;
	setAttr ".tgi[4].ni[23].x" -2717.142822265625;
	setAttr ".tgi[4].ni[23].y" -1185.7142333984375;
	setAttr ".tgi[4].ni[23].nvs" 18304;
	setAttr ".tgi[4].ni[24].x" -1692.857177734375;
	setAttr ".tgi[4].ni[24].y" -1217.142822265625;
	setAttr ".tgi[4].ni[24].nvs" 18304;
	setAttr ".tgi[4].ni[25].x" -8611.7607421875;
	setAttr ".tgi[4].ni[25].y" -752.093505859375;
	setAttr ".tgi[4].ni[25].nvs" 18304;
	setAttr ".tgi[4].ni[26].x" -4005.71435546875;
	setAttr ".tgi[4].ni[26].y" -1008.5714111328125;
	setAttr ".tgi[4].ni[26].nvs" 18304;
	setAttr ".tgi[4].ni[27].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[27].y" -788.5714111328125;
	setAttr ".tgi[4].ni[27].nvs" 18304;
	setAttr ".tgi[4].ni[28].x" -10155.7138671875;
	setAttr ".tgi[4].ni[28].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[28].nvs" 18304;
	setAttr ".tgi[4].ni[29].x" -957.14288330078125;
	setAttr ".tgi[4].ni[29].y" -564.28570556640625;
	setAttr ".tgi[4].ni[29].nvs" 18304;
	setAttr ".tgi[4].ni[30].x" -5234.28564453125;
	setAttr ".tgi[4].ni[30].y" -840;
	setAttr ".tgi[4].ni[30].nvs" 18304;
	setAttr ".tgi[4].ni[31].x" -957.14288330078125;
	setAttr ".tgi[4].ni[31].y" -1131.4285888671875;
	setAttr ".tgi[4].ni[31].nvs" 18304;
	setAttr ".tgi[4].ni[32].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[32].y" -1222.857177734375;
	setAttr ".tgi[4].ni[32].nvs" 18304;
	setAttr ".tgi[4].ni[33].x" -2717.142822265625;
	setAttr ".tgi[4].ni[33].y" -764.28570556640625;
	setAttr ".tgi[4].ni[33].nvs" 18304;
	setAttr ".tgi[4].ni[34].x" -7384.28564453125;
	setAttr ".tgi[4].ni[34].y" -912.85711669921875;
	setAttr ".tgi[4].ni[34].nvs" 18304;
	setAttr ".tgi[4].ni[35].x" -9848.5712890625;
	setAttr ".tgi[4].ni[35].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[35].nvs" 18304;
	setAttr ".tgi[4].ni[36].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[36].y" -1025.7142333984375;
	setAttr ".tgi[4].ni[36].nvs" 18304;
	setAttr ".tgi[4].ni[37].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[37].y" -908.5714111328125;
	setAttr ".tgi[4].ni[37].nvs" 18304;
	setAttr ".tgi[4].ni[38].x" -4927.14306640625;
	setAttr ".tgi[4].ni[38].y" -838.5714111328125;
	setAttr ".tgi[4].ni[38].nvs" 18304;
	setAttr ".tgi[4].ni[39].x" -1692.857177734375;
	setAttr ".tgi[4].ni[39].y" -1017.1428833007812;
	setAttr ".tgi[4].ni[39].nvs" 18304;
	setAttr ".tgi[4].ni[40].x" -10155.7138671875;
	setAttr ".tgi[4].ni[40].y" -1405.7142333984375;
	setAttr ".tgi[4].ni[40].nvs" 18304;
	setAttr ".tgi[4].ni[41].x" -6462.85693359375;
	setAttr ".tgi[4].ni[41].y" -1108.5714111328125;
	setAttr ".tgi[4].ni[41].nvs" 18304;
	setAttr ".tgi[4].ni[42].x" -7077.14306640625;
	setAttr ".tgi[4].ni[42].y" -972.85711669921875;
	setAttr ".tgi[4].ni[42].nvs" 18304;
	setAttr ".tgi[4].ni[43].x" -10155.7138671875;
	setAttr ".tgi[4].ni[43].y" -912.85711669921875;
	setAttr ".tgi[4].ni[43].nvs" 18304;
	setAttr ".tgi[4].ni[44].x" -9848.5712890625;
	setAttr ".tgi[4].ni[44].y" -912.85711669921875;
	setAttr ".tgi[4].ni[44].nvs" 18304;
	setAttr ".tgi[4].ni[45].x" -957.14288330078125;
	setAttr ".tgi[4].ni[45].y" -1230;
	setAttr ".tgi[4].ni[45].nvs" 18304;
	setAttr ".tgi[4].ni[46].x" -7384.28564453125;
	setAttr ".tgi[4].ni[46].y" -1048.5714111328125;
	setAttr ".tgi[4].ni[46].nvs" 18304;
	setAttr ".tgi[4].ni[47].x" -5541.4287109375;
	setAttr ".tgi[4].ni[47].y" -987.14288330078125;
	setAttr ".tgi[4].ni[47].nvs" 18304;
	setAttr ".tgi[4].ni[48].x" -10155.7138671875;
	setAttr ".tgi[4].ni[48].y" -814.28570556640625;
	setAttr ".tgi[4].ni[48].nvs" 18304;
	setAttr ".tgi[4].ni[49].x" -9234.2861328125;
	setAttr ".tgi[4].ni[49].y" -912.85711669921875;
	setAttr ".tgi[4].ni[49].nvs" 18304;
	setAttr ".tgi[4].ni[50].x" -4620;
	setAttr ".tgi[4].ni[50].y" -1047.142822265625;
	setAttr ".tgi[4].ni[50].nvs" 18304;
	setAttr ".tgi[4].ni[51].x" -8612.857421875;
	setAttr ".tgi[4].ni[51].y" -1087.142822265625;
	setAttr ".tgi[4].ni[51].nvs" 18304;
	setAttr ".tgi[4].ni[52].x" -7998.5712890625;
	setAttr ".tgi[4].ni[52].y" -874.28570556640625;
	setAttr ".tgi[4].ni[52].nvs" 18304;
	setAttr ".tgi[4].ni[53].x" -3024.28564453125;
	setAttr ".tgi[4].ni[53].y" -972.85711669921875;
	setAttr ".tgi[4].ni[53].nvs" 18304;
	setAttr ".tgi[4].ni[54].x" -2060;
	setAttr ".tgi[4].ni[54].y" -1212.857177734375;
	setAttr ".tgi[4].ni[54].nvs" 18304;
	setAttr ".tgi[4].ni[55].x" -957.14288330078125;
	setAttr ".tgi[4].ni[55].y" -700;
	setAttr ".tgi[4].ni[55].nvs" 18304;
	setAttr ".tgi[4].ni[56].x" -9234.2861328125;
	setAttr ".tgi[4].ni[56].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[56].nvs" 18304;
	setAttr ".tgi[4].ni[57].x" -957.14288330078125;
	setAttr ".tgi[4].ni[57].y" -915.71429443359375;
	setAttr ".tgi[4].ni[57].nvs" 18304;
	setAttr ".tgi[4].ni[58].x" -10155.7138671875;
	setAttr ".tgi[4].ni[58].y" -715.71429443359375;
	setAttr ".tgi[4].ni[58].nvs" 18304;
	setAttr ".tgi[4].ni[59].x" -957.14288330078125;
	setAttr ".tgi[4].ni[59].y" -798.5714111328125;
	setAttr ".tgi[4].ni[59].nvs" 18304;
	setAttr ".tgi[4].ni[60].x" -8293.830078125;
	setAttr ".tgi[4].ni[60].y" -867.90045166015625;
	setAttr ".tgi[4].ni[60].nvs" 18306;
	setAttr ".tgi[4].ni[61].x" -8920;
	setAttr ".tgi[4].ni[61].y" -962.85711669921875;
	setAttr ".tgi[4].ni[61].nvs" 18304;
	setAttr ".tgi[4].ni[62].x" -1692.857177734375;
	setAttr ".tgi[4].ni[62].y" -861.4285888671875;
	setAttr ".tgi[4].ni[62].nvs" 18304;
	setAttr ".tgi[4].ni[63].x" -9234.2861328125;
	setAttr ".tgi[4].ni[63].y" -1110;
	setAttr ".tgi[4].ni[63].nvs" 18304;
	setAttr ".tgi[4].ni[64].x" -4927.14306640625;
	setAttr ".tgi[4].ni[64].y" -1081.4285888671875;
	setAttr ".tgi[4].ni[64].nvs" 18304;
	setAttr ".tgi[4].ni[65].x" -8612.857421875;
	setAttr ".tgi[4].ni[65].y" -871.4285888671875;
	setAttr ".tgi[4].ni[65].nvs" 18304;
	setAttr ".tgi[4].ni[66].x" -4620;
	setAttr ".tgi[4].ni[66].y" -911.4285888671875;
	setAttr ".tgi[4].ni[66].nvs" 18304;
	setAttr ".tgi[4].ni[67].x" -3698.571533203125;
	setAttr ".tgi[4].ni[67].y" -998.5714111328125;
	setAttr ".tgi[4].ni[67].nvs" 18304;
	setAttr ".tgi[4].ni[68].x" -6770;
	setAttr ".tgi[4].ni[68].y" -1124.2857666015625;
	setAttr ".tgi[4].ni[68].nvs" 18304;
	setAttr ".tgi[5].tn" -type "string" "Untitled_6";
	setAttr ".tgi[5].vl" -type "double2" -3647.6189026756924 -3030.9522605131447 ;
	setAttr ".tgi[5].vh" -type "double2" 2752.3808430111685 -1297.618996056287 ;
	setAttr -s 42 ".tgi[5].ni";
	setAttr ".tgi[5].ni[0].x" -717.14288330078125;
	setAttr ".tgi[5].ni[0].y" -1225.7142333984375;
	setAttr ".tgi[5].ni[0].nvs" 18304;
	setAttr ".tgi[5].ni[1].x" -2268.605224609375;
	setAttr ".tgi[5].ni[1].y" -1083.2686767578125;
	setAttr ".tgi[5].ni[1].nvs" 18306;
	setAttr ".tgi[5].ni[2].x" -3545.71435546875;
	setAttr ".tgi[5].ni[2].y" -1394.2857666015625;
	setAttr ".tgi[5].ni[2].nvs" 18304;
	setAttr ".tgi[5].ni[3].x" -3238.571533203125;
	setAttr ".tgi[5].ni[3].y" -1197.142822265625;
	setAttr ".tgi[5].ni[3].nvs" 18304;
	setAttr ".tgi[5].ni[4].x" -2931.428466796875;
	setAttr ".tgi[5].ni[4].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[4].nvs" 18304;
	setAttr ".tgi[5].ni[5].x" -3545.71435546875;
	setAttr ".tgi[5].ni[5].y" -1295.7142333984375;
	setAttr ".tgi[5].ni[5].nvs" 18304;
	setAttr ".tgi[5].ni[6].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[6].y" -1040;
	setAttr ".tgi[5].ni[6].nvs" 18304;
	setAttr ".tgi[5].ni[7].x" -2649.8759765625;
	setAttr ".tgi[5].ni[7].y" -767.46453857421875;
	setAttr ".tgi[5].ni[7].nvs" 18306;
	setAttr ".tgi[5].ni[8].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[8].y" -1715.7142333984375;
	setAttr ".tgi[5].ni[8].nvs" 18304;
	setAttr ".tgi[5].ni[9].x" -717.14288330078125;
	setAttr ".tgi[5].ni[9].y" -658.5714111328125;
	setAttr ".tgi[5].ni[9].nvs" 18304;
	setAttr ".tgi[5].ni[10].x" -2280.754150390625;
	setAttr ".tgi[5].ni[10].y" -1337.3529052734375;
	setAttr ".tgi[5].ni[10].nvs" 18306;
	setAttr ".tgi[5].ni[11].x" -717.14288330078125;
	setAttr ".tgi[5].ni[11].y" -1028.5714111328125;
	setAttr ".tgi[5].ni[11].nvs" 18304;
	setAttr ".tgi[5].ni[12].x" -1388.5714111328125;
	setAttr ".tgi[5].ni[12].y" -1200;
	setAttr ".tgi[5].ni[12].nvs" 18304;
	setAttr ".tgi[5].ni[13].x" -717.14288330078125;
	setAttr ".tgi[5].ni[13].y" -1577.142822265625;
	setAttr ".tgi[5].ni[13].nvs" 18304;
	setAttr ".tgi[5].ni[14].x" -717.14288330078125;
	setAttr ".tgi[5].ni[14].y" -1441.4285888671875;
	setAttr ".tgi[5].ni[14].nvs" 18304;
	setAttr ".tgi[5].ni[15].x" -3238.571533203125;
	setAttr ".tgi[5].ni[15].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[15].nvs" 18304;
	setAttr ".tgi[5].ni[16].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[16].y" -1814.2857666015625;
	setAttr ".tgi[5].ni[16].nvs" 1923;
	setAttr ".tgi[5].ni[17].x" -717.14288330078125;
	setAttr ".tgi[5].ni[17].y" -1127.142822265625;
	setAttr ".tgi[5].ni[17].nvs" 18304;
	setAttr ".tgi[5].ni[18].x" -717.14288330078125;
	setAttr ".tgi[5].ni[18].y" -794.28570556640625;
	setAttr ".tgi[5].ni[18].nvs" 18304;
	setAttr ".tgi[5].ni[19].x" -3545.71435546875;
	setAttr ".tgi[5].ni[19].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[19].nvs" 18304;
	setAttr ".tgi[5].ni[20].x" -3545.71435546875;
	setAttr ".tgi[5].ni[20].y" -802.85711669921875;
	setAttr ".tgi[5].ni[20].nvs" 18304;
	setAttr ".tgi[5].ni[21].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[21].y" -1388.5714111328125;
	setAttr ".tgi[5].ni[21].nvs" 18304;
	setAttr ".tgi[5].ni[22].x" -3238.571533203125;
	setAttr ".tgi[5].ni[22].y" -1000;
	setAttr ".tgi[5].ni[22].nvs" 18304;
	setAttr ".tgi[5].ni[23].x" -1982.1771240234375;
	setAttr ".tgi[5].ni[23].y" -1443.332763671875;
	setAttr ".tgi[5].ni[23].nvs" 18306;
	setAttr ".tgi[5].ni[24].x" -1388.5714111328125;
	setAttr ".tgi[5].ni[24].y" -1298.5714111328125;
	setAttr ".tgi[5].ni[24].nvs" 18304;
	setAttr ".tgi[5].ni[25].x" -717.14288330078125;
	setAttr ".tgi[5].ni[25].y" -1774.2857666015625;
	setAttr ".tgi[5].ni[25].nvs" 18304;
	setAttr ".tgi[5].ni[26].x" -3545.71435546875;
	setAttr ".tgi[5].ni[26].y" -704.28570556640625;
	setAttr ".tgi[5].ni[26].nvs" 18304;
	setAttr ".tgi[5].ni[27].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[27].y" -941.4285888671875;
	setAttr ".tgi[5].ni[27].nvs" 18304;
	setAttr ".tgi[5].ni[28].x" -2624.28564453125;
	setAttr ".tgi[5].ni[28].y" -1058.5714111328125;
	setAttr ".tgi[5].ni[28].nvs" 18304;
	setAttr ".tgi[5].ni[29].x" -717.14288330078125;
	setAttr ".tgi[5].ni[29].y" -1872.857177734375;
	setAttr ".tgi[5].ni[29].nvs" 18304;
	setAttr ".tgi[5].ni[30].x" -3545.71435546875;
	setAttr ".tgi[5].ni[30].y" -1000;
	setAttr ".tgi[5].ni[30].nvs" 18304;
	setAttr ".tgi[5].ni[31].x" -3545.71435546875;
	setAttr ".tgi[5].ni[31].y" -605.71429443359375;
	setAttr ".tgi[5].ni[31].nvs" 18304;
	setAttr ".tgi[5].ni[32].x" -717.14288330078125;
	setAttr ".tgi[5].ni[32].y" -892.85711669921875;
	setAttr ".tgi[5].ni[32].nvs" 18304;
	setAttr ".tgi[5].ni[33].x" -2660.843017578125;
	setAttr ".tgi[5].ni[33].y" -1198.5745849609375;
	setAttr ".tgi[5].ni[33].nvs" 18306;
	setAttr ".tgi[5].ni[34].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[34].y" -1252.857177734375;
	setAttr ".tgi[5].ni[34].nvs" 18304;
	setAttr ".tgi[5].ni[35].x" -717.14288330078125;
	setAttr ".tgi[5].ni[35].y" -1971.4285888671875;
	setAttr ".tgi[5].ni[35].nvs" 18304;
	setAttr ".tgi[5].ni[36].x" -3545.71435546875;
	setAttr ".tgi[5].ni[36].y" -901.4285888671875;
	setAttr ".tgi[5].ni[36].nvs" 18304;
	setAttr ".tgi[5].ni[37].x" -717.14288330078125;
	setAttr ".tgi[5].ni[37].y" -1324.2857666015625;
	setAttr ".tgi[5].ni[37].nvs" 18304;
	setAttr ".tgi[5].ni[38].x" -671.21630859375;
	setAttr ".tgi[5].ni[38].y" -2372.208984375;
	setAttr ".tgi[5].ni[38].nvs" 18305;
	setAttr ".tgi[5].ni[39].x" -1096.7374267578125;
	setAttr ".tgi[5].ni[39].y" -2203.770263671875;
	setAttr ".tgi[5].ni[39].nvs" 18306;
	setAttr ".tgi[5].ni[40].x" -3545.71435546875;
	setAttr ".tgi[5].ni[40].y" -1197.142822265625;
	setAttr ".tgi[5].ni[40].nvs" 18304;
	setAttr ".tgi[5].ni[41].x" -1695.7142333984375;
	setAttr ".tgi[5].ni[41].y" -1118.5714111328125;
	setAttr ".tgi[5].ni[41].nvs" 18304;
	setAttr ".tgi[6].tn" -type "string" "Untitled_7";
	setAttr ".tgi[6].vl" -type "double2" 3336.4854255075497 -2048.5182914920128 ;
	setAttr ".tgi[6].vh" -type "double2" 5965.8938318773999 -404.22589305906371 ;
	setAttr -s 70 ".tgi[6].ni";
	setAttr ".tgi[6].ni[0].x" 5540.099609375;
	setAttr ".tgi[6].ni[0].y" -361.22265625;
	setAttr ".tgi[6].ni[0].nvs" 18304;
	setAttr ".tgi[6].ni[1].x" -857.14288330078125;
	setAttr ".tgi[6].ni[1].y" 10;
	setAttr ".tgi[6].ni[1].nvs" 18304;
	setAttr ".tgi[6].ni[2].x" -3621.428466796875;
	setAttr ".tgi[6].ni[2].y" -268.57144165039062;
	setAttr ".tgi[6].ni[2].nvs" 18304;
	setAttr ".tgi[6].ni[3].x" 985.71429443359375;
	setAttr ".tgi[6].ni[3].y" 325.71429443359375;
	setAttr ".tgi[6].ni[3].nvs" 18304;
	setAttr ".tgi[6].ni[4].x" -5164.28564453125;
	setAttr ".tgi[6].ni[4].y" 77.142860412597656;
	setAttr ".tgi[6].ni[4].nvs" 18304;
	setAttr ".tgi[6].ni[5].x" -1471.4285888671875;
	setAttr ".tgi[6].ni[5].y" 17.142856597900391;
	setAttr ".tgi[6].ni[5].nvs" 18304;
	setAttr ".tgi[6].ni[6].x" -2085.71435546875;
	setAttr ".tgi[6].ni[6].y" -38.571430206298828;
	setAttr ".tgi[6].ni[6].nvs" 18304;
	setAttr ".tgi[6].ni[7].x" -5164.28564453125;
	setAttr ".tgi[6].ni[7].y" -120;
	setAttr ".tgi[6].ni[7].nvs" 18304;
	setAttr ".tgi[6].ni[8].x" -2392.857177734375;
	setAttr ".tgi[6].ni[8].y" 21.428571701049805;
	setAttr ".tgi[6].ni[8].nvs" 18304;
	setAttr ".tgi[6].ni[9].x" -550;
	setAttr ".tgi[6].ni[9].y" -10;
	setAttr ".tgi[6].ni[9].nvs" 18304;
	setAttr ".tgi[6].ni[10].x" -3928.571533203125;
	setAttr ".tgi[6].ni[10].y" -268.57144165039062;
	setAttr ".tgi[6].ni[10].nvs" 18304;
	setAttr ".tgi[6].ni[11].x" 985.71429443359375;
	setAttr ".tgi[6].ni[11].y" 208.57142639160156;
	setAttr ".tgi[6].ni[11].nvs" 18304;
	setAttr ".tgi[6].ni[12].x" -5164.28564453125;
	setAttr ".tgi[6].ni[12].y" -415.71429443359375;
	setAttr ".tgi[6].ni[12].nvs" 18304;
	setAttr ".tgi[6].ni[13].x" -4550;
	setAttr ".tgi[6].ni[13].y" -170;
	setAttr ".tgi[6].ni[13].nvs" 18304;
	setAttr ".tgi[6].ni[14].x" 4326.14453125;
	setAttr ".tgi[6].ni[14].y" -587.30316162109375;
	setAttr ".tgi[6].ni[14].nvs" 18306;
	setAttr ".tgi[6].ni[15].x" 1660;
	setAttr ".tgi[6].ni[15].y" 194.28572082519531;
	setAttr ".tgi[6].ni[15].nvs" 18304;
	setAttr ".tgi[6].ni[16].x" 2027.142822265625;
	setAttr ".tgi[6].ni[16].y" 135.71427917480469;
	setAttr ".tgi[6].ni[16].nvs" 18304;
	setAttr ".tgi[6].ni[17].x" 985.71429443359375;
	setAttr ".tgi[6].ni[17].y" 424.28570556640625;
	setAttr ".tgi[6].ni[17].nvs" 18304;
	setAttr ".tgi[6].ni[18].x" -2700;
	setAttr ".tgi[6].ni[18].y" 2.8571429252624512;
	setAttr ".tgi[6].ni[18].nvs" 18304;
	setAttr ".tgi[6].ni[19].x" -4242.85693359375;
	setAttr ".tgi[6].ni[19].y" -218.57142639160156;
	setAttr ".tgi[6].ni[19].nvs" 18304;
	setAttr ".tgi[6].ni[20].x" -5164.28564453125;
	setAttr ".tgi[6].ni[20].y" -317.14285278320312;
	setAttr ".tgi[6].ni[20].nvs" 18304;
	setAttr ".tgi[6].ni[21].x" 4788.099609375;
	setAttr ".tgi[6].ni[21].y" -4.6341962814331055;
	setAttr ".tgi[6].ni[21].nvs" 18304;
	setAttr ".tgi[6].ni[22].x" -3314.28564453125;
	setAttr ".tgi[6].ni[22].y" -64.285713195800781;
	setAttr ".tgi[6].ni[22].nvs" 18304;
	setAttr ".tgi[6].ni[23].x" -3928.571533203125;
	setAttr ".tgi[6].ni[23].y" -170;
	setAttr ".tgi[6].ni[23].nvs" 18304;
	setAttr ".tgi[6].ni[24].x" 3965.71435546875;
	setAttr ".tgi[6].ni[24].y" 100;
	setAttr ".tgi[6].ni[24].nvs" 18304;
	setAttr ".tgi[6].ni[25].x" 64.285713195800781;
	setAttr ".tgi[6].ni[25].y" -21.428571701049805;
	setAttr ".tgi[6].ni[25].nvs" 18304;
	setAttr ".tgi[6].ni[26].x" -3621.428466796875;
	setAttr ".tgi[6].ni[26].y" -151.42857360839844;
	setAttr ".tgi[6].ni[26].nvs" 18304;
	setAttr ".tgi[6].ni[27].x" 1292.857177734375;
	setAttr ".tgi[6].ni[27].y" 34.285713195800781;
	setAttr ".tgi[6].ni[27].nvs" 18304;
	setAttr ".tgi[6].ni[28].x" -4857.14306640625;
	setAttr ".tgi[6].ni[28].y" -120;
	setAttr ".tgi[6].ni[28].nvs" 18304;
	setAttr ".tgi[6].ni[29].x" 678.5714111328125;
	setAttr ".tgi[6].ni[29].y" 22.857143402099609;
	setAttr ".tgi[6].ni[29].nvs" 18304;
	setAttr ".tgi[6].ni[30].x" -1164.2857666015625;
	setAttr ".tgi[6].ni[30].y" 27.142856597900391;
	setAttr ".tgi[6].ni[30].nvs" 18304;
	setAttr ".tgi[6].ni[31].x" 1660;
	setAttr ".tgi[6].ni[31].y" 95.714286804199219;
	setAttr ".tgi[6].ni[31].nvs" 18304;
	setAttr ".tgi[6].ni[32].x" -3621.428466796875;
	setAttr ".tgi[6].ni[32].y" -34.285713195800781;
	setAttr ".tgi[6].ni[32].nvs" 18304;
	setAttr ".tgi[6].ni[33].x" -3928.571533203125;
	setAttr ".tgi[6].ni[33].y" -52.857143402099609;
	setAttr ".tgi[6].ni[33].nvs" 18304;
	setAttr ".tgi[6].ni[34].x" 1660;
	setAttr ".tgi[6].ni[34].y" 301.42855834960938;
	setAttr ".tgi[6].ni[34].nvs" 18304;
	setAttr ".tgi[6].ni[35].x" 1292.857177734375;
	setAttr ".tgi[6].ni[35].y" 345.71429443359375;
	setAttr ".tgi[6].ni[35].nvs" 18304;
	setAttr ".tgi[6].ni[36].x" -1778.5714111328125;
	setAttr ".tgi[6].ni[36].y" -12.857142448425293;
	setAttr ".tgi[6].ni[36].nvs" 18304;
	setAttr ".tgi[6].ni[37].x" 985.71429443359375;
	setAttr ".tgi[6].ni[37].y" 38.571430206298828;
	setAttr ".tgi[6].ni[37].nvs" 18304;
	setAttr ".tgi[6].ni[38].x" 4539.75732421875;
	setAttr ".tgi[6].ni[38].y" -289.2232666015625;
	setAttr ".tgi[6].ni[38].nvs" 18304;
	setAttr ".tgi[6].ni[39].x" -5164.28564453125;
	setAttr ".tgi[6].ni[39].y" -218.57142639160156;
	setAttr ".tgi[6].ni[39].nvs" 18304;
	setAttr ".tgi[6].ni[40].x" 678.5714111328125;
	setAttr ".tgi[6].ni[40].y" 267.14285278320312;
	setAttr ".tgi[6].ni[40].nvs" 18304;
	setAttr ".tgi[6].ni[41].x" -5164.28564453125;
	setAttr ".tgi[6].ni[41].y" -612.85711669921875;
	setAttr ".tgi[6].ni[41].nvs" 18304;
	setAttr ".tgi[6].ni[42].x" -4242.85693359375;
	setAttr ".tgi[6].ni[42].y" -120;
	setAttr ".tgi[6].ni[42].nvs" 18304;
	setAttr ".tgi[6].ni[43].x" 371.42855834960938;
	setAttr ".tgi[6].ni[43].y" 24.285715103149414;
	setAttr ".tgi[6].ni[43].nvs" 18304;
	setAttr ".tgi[6].ni[44].x" 1292.857177734375;
	setAttr ".tgi[6].ni[44].y" 132.85714721679688;
	setAttr ".tgi[6].ni[44].nvs" 18304;
	setAttr ".tgi[6].ni[45].x" -3621.428466796875;
	setAttr ".tgi[6].ni[45].y" 121.42857360839844;
	setAttr ".tgi[6].ni[45].nvs" 18304;
	setAttr ".tgi[6].ni[46].x" -3007.142822265625;
	setAttr ".tgi[6].ni[46].y" -81.428573608398438;
	setAttr ".tgi[6].ni[46].nvs" 18304;
	setAttr ".tgi[6].ni[47].x" 2027.142822265625;
	setAttr ".tgi[6].ni[47].y" -20;
	setAttr ".tgi[6].ni[47].nvs" 18304;
	setAttr ".tgi[6].ni[48].x" 371.42855834960938;
	setAttr ".tgi[6].ni[48].y" 267.14285278320312;
	setAttr ".tgi[6].ni[48].nvs" 18304;
	setAttr ".tgi[6].ni[49].x" 3587.983154296875;
	setAttr ".tgi[6].ni[49].y" -421.51260375976562;
	setAttr ".tgi[6].ni[49].nvs" 18304;
	setAttr ".tgi[6].ni[50].x" 2615.93798828125;
	setAttr ".tgi[6].ni[50].y" -562.11175537109375;
	setAttr ".tgi[6].ni[50].nvs" 18306;
	setAttr ".tgi[6].ni[51].x" -5164.28564453125;
	setAttr ".tgi[6].ni[51].y" -514.28570556640625;
	setAttr ".tgi[6].ni[51].nvs" 18304;
	setAttr ".tgi[6].ni[52].x" -5164.28564453125;
	setAttr ".tgi[6].ni[52].y" -21.428571701049805;
	setAttr ".tgi[6].ni[52].nvs" 18304;
	setAttr ".tgi[6].ni[53].x" -5164.28564453125;
	setAttr ".tgi[6].ni[53].y" 175.71427917480469;
	setAttr ".tgi[6].ni[53].nvs" 18304;
	setAttr ".tgi[6].ni[54].x" -2700;
	setAttr ".tgi[6].ni[54].y" -247.14285278320312;
	setAttr ".tgi[6].ni[54].nvs" 18304;
	setAttr ".tgi[6].ni[55].x" -242.85714721679688;
	setAttr ".tgi[6].ni[55].y" 32.857143402099609;
	setAttr ".tgi[6].ni[55].nvs" 18304;
	setAttr ".tgi[6].ni[56].x" 1935.4622802734375;
	setAttr ".tgi[6].ni[56].y" -815.96636962890625;
	setAttr ".tgi[6].ni[56].nvs" 18304;
	setAttr ".tgi[6].ni[57].x" 2387.142822265625;
	setAttr ".tgi[6].ni[57].y" 68.571426391601562;
	setAttr ".tgi[6].ni[57].nvs" 18304;
	setAttr ".tgi[6].ni[58].x" -2392.857177734375;
	setAttr ".tgi[6].ni[58].y" -114.28571319580078;
	setAttr ".tgi[6].ni[58].nvs" 18304;
	setAttr ".tgi[6].ni[59].x" 4446.748046875;
	setAttr ".tgi[6].ni[59].y" -1068.4276123046875;
	setAttr ".tgi[6].ni[59].nvs" 18306;
	setAttr ".tgi[6].ni[60].x" -4857.14306640625;
	setAttr ".tgi[6].ni[60].y" -218.57142639160156;
	setAttr ".tgi[6].ni[60].nvs" 18304;
	setAttr ".tgi[6].ni[61].x" 5094.3408203125;
	setAttr ".tgi[6].ni[61].y" -186.97982788085938;
	setAttr ".tgi[6].ni[61].nvs" 18304;
	setAttr ".tgi[6].ni[62].x" 2247.64697265625;
	setAttr ".tgi[6].ni[62].y" -284.95797729492188;
	setAttr ".tgi[6].ni[62].nvs" 18306;
	setAttr ".tgi[6].ni[63].x" 4781.08544921875;
	setAttr ".tgi[6].ni[63].y" -1426.770751953125;
	setAttr ".tgi[6].ni[63].nvs" 18306;
	setAttr ".tgi[6].ni[64].x" 3965.71435546875;
	setAttr ".tgi[6].ni[64].y" -461.42855834960938;
	setAttr ".tgi[6].ni[64].nvs" 18304;
	setAttr ".tgi[6].ni[65].x" 3606.6142578125;
	setAttr ".tgi[6].ni[65].y" -860.692138671875;
	setAttr ".tgi[6].ni[65].nvs" 19682;
	setAttr ".tgi[6].ni[66].x" 4035.063720703125;
	setAttr ".tgi[6].ni[66].y" -1191.70751953125;
	setAttr ".tgi[6].ni[66].nvs" 1939;
	setAttr ".tgi[6].ni[67].x" 4040.2236328125;
	setAttr ".tgi[6].ni[67].y" -1501.2996826171875;
	setAttr ".tgi[6].ni[67].nvs" 1923;
	setAttr ".tgi[6].ni[68].x" 4021.30419921875;
	setAttr ".tgi[6].ni[68].y" -969.83319091796875;
	setAttr ".tgi[6].ni[68].nvs" 1923;
	setAttr ".tgi[6].ni[69].x" 2952.49755859375;
	setAttr ".tgi[6].ni[69].y" -628.49761962890625;
	setAttr ".tgi[6].ni[69].nvs" 18306;
createNode renderLayerManager -n "IK3:renderLayerManager";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A54";
createNode renderLayer -n "IK3:defaultRenderLayer";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A55";
	setAttr ".g" yes;
createNode ikRPsolver -n "IK3:ikRPsolver";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A58";
createNode multiplyDivide -n "IK3:multiplyDivide1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A59";
	setAttr ".i2" -type "float3" 0.0099999998 1 1 ;
createNode multiplyDivide -n "IK3:multiplyDivide9";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A5A";
	setAttr ".i1" -type "float3" 7.0710678 0 0 ;
createNode reverse -n "IK3:reverse1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A5B";
createNode multiplyDivide -n "IK3:multiplyDivide10";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A5C";
	setAttr ".i2" -type "float3" 3.5355339 0 3.9252311e-16 ;
createNode multiplyDivide -n "IK3:multiplyDivide11";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A5D";
	setAttr ".i2" -type "float3" 3.5355339 -6.2803697e-16 -1.9626156e-16 ;
createNode makeNurbCircle -n "IK3:makeNurbCircle1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A5E";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".d" 1;
	setAttr ".s" 4;
createNode network -n "IK3:ik:softik:inn";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A5F";
	addAttr -ci true -sn "inMatrixE" -ln "inMatrixE" -nn "inMatrixE" -dt "matrix";
	addAttr -ci true -sn "inMatrixS" -ln "inMatrixS" -nn "inMatrixS" -dt "matrix";
	addAttr -ci true -sn "inStretch" -ln "inStretch" -nn "inStretch" -at "float";
	addAttr -ci true -sn "inChainLength" -ln "inChainLength" -nn "inChainLength" -at "float";
	addAttr -ci true -sn "inRatio" -ln "inRatio" -nn "inRatio" -at "float";
createNode network -n "IK3:ik:softik:metadata";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A60";
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
createNode multiplyDivide -n "IK3:ik:softik:multiplyDivide4";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A61";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 2.7182817 0 0 ;
createNode multiplyDivide -n "IK3:ik:softik:multiplyDivide3";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A62";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode plusMinusAverage -n "IK3:ik:softik:plusMinusAverage4";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A63";
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode distanceBetween -n "IK3:ik:softik:distanceBetween1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A64";
createNode condition -n "IK3:ik:softik:condition2";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A65";
	setAttr ".op" 2;
createNode clamp -n "IK3:ik:softik:clamp1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A66";
	setAttr ".mn" -type "float3" 9.9999997e-05 0 0 ;
	setAttr ".mx" -type "float3" 999 0 0 ;
createNode plusMinusAverage -n "IK3:ik:softik:plusMinusAverage3";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A67";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  1 inf;
createNode blendTwoAttr -n "IK3:ik:softik:blendTwoAttr2";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A68";
	setAttr -s 2 ".i[0:1]"  1 1;
createNode multiplyDivide -n "IK3:ik:softik:multiplyDivide5";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A69";
createNode network -n "IK3:ik:softik:out";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A6A";
	addAttr -ci true -sn "outStretch" -ln "outStretch" -nn "outStretch" -at "float";
	addAttr -ci true -sn "outRatio" -ln "outRatio" -nn "outRatio" -at "float";
createNode multiplyDivide -n "IK3:ik:softik:multiplyDivide1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A6B";
createNode plusMinusAverage -n "IK3:ik:softik:plusMinusAverage1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A6C";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode condition -n "IK3:ik:softik:condition1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A6D";
	setAttr ".op" 2;
createNode multiplyDivide -n "IK3:ik:softik:multiplyDivide2";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A6E";
	setAttr ".op" 2;
createNode multiplyDivide -n "IK3:ik:softik:multiplyDivide7";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A6F";
	setAttr ".op" 2;
createNode plusMinusAverage -n "IK3:ik:softik:plusMinusAverage2";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A70";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode blendTwoAttr -n "IK3:ik:softik:blendTwoAttr1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A71";
	setAttr -s 2 ".i";
	setAttr -s 2 ".i";
createNode multiplyDivide -n "IK3:ik:softik:multiplyDivide6";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A72";
	setAttr ".op" 2;
createNode network -n "IK3:inn";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A73";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	addAttr -ci true -sn "Guide01_LocalTm" -ln "Guide01_LocalTm" -dt "matrix";
	addAttr -ci true -sn "Guide02_LocalTm" -ln "Guide02_LocalTm" -dt "matrix";
	addAttr -ci true -sn "Guide03_LocalTm" -ln "Guide03_LocalTm" -dt "matrix";
	addAttr -ci true -sn "swivelDistanceRatio" -ln "swivelDistanceRatio" -dv 0.5 -min 
		0 -max 1 -at "double";
	setAttr "._graphpos" -type "float2" 0 1 ;
	setAttr -k on ".swivelDistanceRatio";
createNode decomposeMatrix -n "IK3:decomposeGuide01LocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A74";
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
createNode decomposeMatrix -n "IK3:decomposeGuide02LocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A75";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
createNode decomposeMatrix -n "IK3:decomposeGuide03LocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A76";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode network -n "IK3:out";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A77";
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
		 -1.0000000000000002 0 1.1102230246251565e-16 0 0 5 0 1;
	setAttr ".outInf02LocalTm" -type "matrix" 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0 0
		 0 0 1 0 3.535533905932736 0 3.9252311467094368e-16 1;
	setAttr ".outInf03LocalTm" -type "matrix" -2.2204460492503131e-16 1 0 0 -1 -2.2204460492503131e-16 0 0
		 0 0 1 0 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 1;
createNode decomposeMatrix -n "IK3:decomposeCtrlFk01DefaultLocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A78";
	setAttr ".ot" -type "double3" -4.9303806576313249e-32 5 5.4738221262688167e-48 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818818;
	setAttr ".oqz" -0.27059805007309851;
	setAttr ".oqw" 0.65328148243818829;
createNode decomposeMatrix -n "IK3:decomposeCtrlFk02DefaultLocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A79";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" -0.70710678118654746;
	setAttr ".oqw" 0.70710678118654757;
createNode decomposeMatrix -n "IK3:decomposeCtrlFk03DefaultLocalTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A7A";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
	setAttr ".oqz" 0.70710678118654757;
	setAttr ".oqw" 0.70710678118654746;
createNode distanceBetween -n "IK3:getLimbSegment1Length";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A7B";
createNode distanceBetween -n "IK3:getLimbSegment2Length";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A7C";
createNode addDoubleLinear -n "IK3:getLimbLength";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A7D";
createNode multiplyDivide -n "IK3:multiplyDivide13";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A7E";
createNode multiplyDivide -n "IK3:multiplyDivide14";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A7F";
createNode animCurveTL -n "IK3:guide_02_translateX";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A80";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.535533905932736 10 6.3911650194459524;
createNode animCurveTL -n "IK3:guide_02_translateY";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A81";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 1.8998827256160656e-16;
createNode animCurveTL -n "IK3:guide_02_translateZ";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A82";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.9252311467094363e-16 10 7.5484373465108625e-17;
createNode animCurveTU -n "IK3:guide_02_visibility";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A83";
	setAttr ".tan" 9;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
createNode animCurveTA -n "IK3:guide_02_rotateX";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A84";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTA -n "IK3:guide_02_rotateY";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A85";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTA -n "IK3:guide_02_rotateZ";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A86";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTU -n "IK3:guide_02_scaleX";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A87";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode animCurveTU -n "IK3:guide_02_scaleY";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A88";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode animCurveTU -n "IK3:guide_02_scaleZ";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A89";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode multMatrix -n "IK3:getGuide03WorldTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A8A";
	setAttr -s 2 ".i";
createNode decomposeMatrix -n "IK3:decomposeGuide03WorldTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A8B";
	setAttr ".ot" -type "double3" -5.8878467200641577e-16 8.8817841970012523e-16 -1.3322676295501878e-15 ;
	setAttr ".or" -type "double3" 90 -45.000000000000028 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.27059805007309845;
	setAttr ".oqy" -0.65328148243818829;
	setAttr ".oqz" -0.27059805007309845;
	setAttr ".oqw" 0.65328148243818829;
createNode multiplyDivide -n "IK3:getSwivelDistance";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A8C";
createNode multiplyDivide -n "IK3:getLimbRatio";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A8D";
	setAttr ".op" 2;
createNode plusMinusAverage -n "IK3:getLimbAim";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A8E";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode multiplyDivide -n "IK3:getLimbMiddleAim";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A8F";
createNode plusMinusAverage -n "IK3:getKneePosProjectedOnLimbDir";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A90";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode plusMinusAverage -n "IK3:getKneeDirection";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A91";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode multMatrix -n "IK3:getGuide02WorldTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A92";
	setAttr -s 2 ".i";
createNode decomposeMatrix -n "IK3:decomposeGuide02WorldTm";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A93";
	setAttr ".ot" -type "double3" -3.9252311467094378e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".or" -type "double3" 90 45 -90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
	setAttr ".oqx" 0.65328148243818818;
	setAttr ".oqy" -0.27059805007309845;
	setAttr ".oqz" -0.65328148243818829;
	setAttr ".oqw" 0.27059805007309851;
createNode vectorProduct -n "IK3:getKneeDirectionNormalized";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A94";
	setAttr ".op" 0;
	setAttr ".no" yes;
createNode multiplyDivide -n "IK3:getKneeDirectionOffset";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A95";
createNode plusMinusAverage -n "IK3:getSwivelDefaultPos";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A96";
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode decomposeMatrix -n "IK3:decomposeMatrix1";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A97";
	setAttr ".ot" -type "double3" 0 5 0 ;
	setAttr ".or" -type "double3" 90 -45 -90 ;
	setAttr ".os" -type "double3" 1 1 1.0000000000000002 ;
createNode decomposeMatrix -n "IK3:decomposeMatrix2";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A98";
	setAttr ".ot" -type "double3" 3.535533905932736 0 3.9252311467094368e-16 ;
	setAttr ".or" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".os" -type "double3" 1 1 1 ;
createNode decomposeMatrix -n "IK3:decomposeMatrix3";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A99";
	setAttr ".ot" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".or" -type "double3" 0 0 90.000000000000014 ;
	setAttr ".os" -type "double3" 1 1 1 ;
createNode nodeGraphEditorInfo -n "IK3:MayaNodeEditorSavedTabsInfo";
	rename -uid "6087C980-0000-3D03-5AD9-3B4300000A9A";
	setAttr ".def" no;
	setAttr -s 7 ".tgi";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -3739.9723788593819 -4397.6188728734051 ;
	setAttr ".tgi[0].vh" -type "double2" 2914.9724116419275 -2595.2379921126339 ;
	setAttr -s 51 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -2608.571533203125;
	setAttr ".tgi[0].ni[0].y" -1645.7142333984375;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" -3568.920654296875;
	setAttr ".tgi[0].ni[1].y" -1715.50048828125;
	setAttr ".tgi[0].ni[1].nvs" 18306;
	setAttr ".tgi[0].ni[2].x" -3559.94384765625;
	setAttr ".tgi[0].ni[2].y" -792.08404541015625;
	setAttr ".tgi[0].ni[2].nvs" 1931;
	setAttr ".tgi[0].ni[3].x" 344.28570556640625;
	setAttr ".tgi[0].ni[3].y" -2895.71435546875;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" -2608.571533203125;
	setAttr ".tgi[0].ni[4].y" -2040;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" -934.78204345703125;
	setAttr ".tgi[0].ni[5].y" -7.1206927299499512;
	setAttr ".tgi[0].ni[5].nvs" 18314;
	setAttr ".tgi[0].ni[6].x" -1625.73779296875;
	setAttr ".tgi[0].ni[6].y" -2420.765380859375;
	setAttr ".tgi[0].ni[6].nvs" 18314;
	setAttr ".tgi[0].ni[7].x" -3557.593505859375;
	setAttr ".tgi[0].ni[7].y" -1245.670654296875;
	setAttr ".tgi[0].ni[7].nvs" 1931;
	setAttr ".tgi[0].ni[8].x" -2608.571533203125;
	setAttr ".tgi[0].ni[8].y" -1842.857177734375;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" -504.69732666015625;
	setAttr ".tgi[0].ni[9].y" 556.9248046875;
	setAttr ".tgi[0].ni[9].nvs" 1931;
	setAttr ".tgi[0].ni[10].x" -2282.696533203125;
	setAttr ".tgi[0].ni[10].y" -3022.0634765625;
	setAttr ".tgi[0].ni[10].nvs" 1923;
	setAttr ".tgi[0].ni[11].x" -1914.81103515625;
	setAttr ".tgi[0].ni[11].y" -1217.4683837890625;
	setAttr ".tgi[0].ni[11].nvs" 18314;
	setAttr ".tgi[0].ni[12].x" -504.69732666015625;
	setAttr ".tgi[0].ni[12].y" -867.29010009765625;
	setAttr ".tgi[0].ni[12].nvs" 1931;
	setAttr ".tgi[0].ni[13].x" -1684.191650390625;
	setAttr ".tgi[0].ni[13].y" -2916.984130859375;
	setAttr ".tgi[0].ni[13].nvs" 18306;
	setAttr ".tgi[0].ni[14].x" 344.28570556640625;
	setAttr ".tgi[0].ni[14].y" -1784.2857666015625;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" -2791.646240234375;
	setAttr ".tgi[0].ni[15].y" -2204.69677734375;
	setAttr ".tgi[0].ni[15].nvs" 1931;
	setAttr ".tgi[0].ni[16].x" -1045.780029296875;
	setAttr ".tgi[0].ni[16].y" -3607.777099609375;
	setAttr ".tgi[0].ni[16].nvs" 18306;
	setAttr ".tgi[0].ni[17].x" -4220.34716796875;
	setAttr ".tgi[0].ni[17].y" -1245.670654296875;
	setAttr ".tgi[0].ni[17].nvs" 18313;
	setAttr ".tgi[0].ni[18].x" -504.69732666015625;
	setAttr ".tgi[0].ni[18].y" -1513.5921630859375;
	setAttr ".tgi[0].ni[18].nvs" 1931;
	setAttr ".tgi[0].ni[19].x" -3317.874267578125;
	setAttr ".tgi[0].ni[19].y" -2000.0814208984375;
	setAttr ".tgi[0].ni[19].nvs" 18314;
	setAttr ".tgi[0].ni[20].x" -2608.571533203125;
	setAttr ".tgi[0].ni[20].y" -2138.571533203125;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" -2608.571533203125;
	setAttr ".tgi[0].ni[21].y" -1744.2857666015625;
	setAttr ".tgi[0].ni[21].nvs" 18304;
	setAttr ".tgi[0].ni[22].x" -1342.2041015625;
	setAttr ".tgi[0].ni[22].y" -3234.176025390625;
	setAttr ".tgi[0].ni[22].nvs" 18306;
	setAttr ".tgi[0].ni[23].x" -3180.7255859375;
	setAttr ".tgi[0].ni[23].y" -1443.1690673828125;
	setAttr ".tgi[0].ni[23].nvs" 18306;
	setAttr ".tgi[0].ni[24].x" -2836.08544921875;
	setAttr ".tgi[0].ni[24].y" -1189.26611328125;
	setAttr ".tgi[0].ni[24].nvs" 18314;
	setAttr ".tgi[0].ni[25].x" -3910.1220703125;
	setAttr ".tgi[0].ni[25].y" -1473.6390380859375;
	setAttr ".tgi[0].ni[25].nvs" 18314;
	setAttr ".tgi[0].ni[26].x" -84.285713195800781;
	setAttr ".tgi[0].ni[26].y" -2127.142822265625;
	setAttr ".tgi[0].ni[26].nvs" 18304;
	setAttr ".tgi[0].ni[27].x" -4222.697265625;
	setAttr ".tgi[0].ni[27].y" -1379.6314697265625;
	setAttr ".tgi[0].ni[27].nvs" 18313;
	setAttr ".tgi[0].ni[28].x" -3557.593505859375;
	setAttr ".tgi[0].ni[28].y" -1010.6516723632812;
	setAttr ".tgi[0].ni[28].nvs" 1931;
	setAttr ".tgi[0].ni[29].x" -504.69732666015625;
	setAttr ".tgi[0].ni[29].y" -162.23320007324219;
	setAttr ".tgi[0].ni[29].nvs" 18314;
	setAttr ".tgi[0].ni[30].x" -619.85455322265625;
	setAttr ".tgi[0].ni[30].y" -3527.8486328125;
	setAttr ".tgi[0].ni[30].nvs" 1923;
	setAttr ".tgi[0].ni[31].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[31].y" 284.30282592773438;
	setAttr ".tgi[0].ni[31].nvs" 18314;
	setAttr ".tgi[0].ni[32].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[32].y" -1755.6617431640625;
	setAttr ".tgi[0].ni[32].nvs" 18314;
	setAttr ".tgi[0].ni[33].x" -265.63861083984375;
	setAttr ".tgi[0].ni[33].y" -3593.725830078125;
	setAttr ".tgi[0].ni[33].nvs" 18306;
	setAttr ".tgi[0].ni[34].x" -3317.874267578125;
	setAttr ".tgi[0].ni[34].y" -1844.968994140625;
	setAttr ".tgi[0].ni[34].nvs" 18312;
	setAttr ".tgi[0].ni[35].x" -4220.34716796875;
	setAttr ".tgi[0].ni[35].y" -1645.202880859375;
	setAttr ".tgi[0].ni[35].nvs" 18313;
	setAttr ".tgi[0].ni[36].x" -3632.42724609375;
	setAttr ".tgi[0].ni[36].y" -1477.7398681640625;
	setAttr ".tgi[0].ni[36].nvs" 18306;
	setAttr ".tgi[0].ni[37].x" -2608.571533203125;
	setAttr ".tgi[0].ni[37].y" -1448.5714111328125;
	setAttr ".tgi[0].ni[37].nvs" 18304;
	setAttr ".tgi[0].ni[38].x" 344.28570556640625;
	setAttr ".tgi[0].ni[38].y" -2397.142822265625;
	setAttr ".tgi[0].ni[38].nvs" 18304;
	setAttr ".tgi[0].ni[39].x" -2608.571533203125;
	setAttr ".tgi[0].ni[39].y" -1941.4285888671875;
	setAttr ".tgi[0].ni[39].nvs" 18304;
	setAttr ".tgi[0].ni[40].x" -1602.093994140625;
	setAttr ".tgi[0].ni[40].y" -3595.533203125;
	setAttr ".tgi[0].ni[40].nvs" 18306;
	setAttr ".tgi[0].ni[41].x" -1992.3165283203125;
	setAttr ".tgi[0].ni[41].y" -2653.79296875;
	setAttr ".tgi[0].ni[41].nvs" 1923;
	setAttr ".tgi[0].ni[42].x" -934.78204345703125;
	setAttr ".tgi[0].ni[42].y" 709.6871337890625;
	setAttr ".tgi[0].ni[42].nvs" 18314;
	setAttr ".tgi[0].ni[43].x" -1372.857177734375;
	setAttr ".tgi[0].ni[43].y" -2048.571533203125;
	setAttr ".tgi[0].ni[43].nvs" 18304;
	setAttr ".tgi[0].ni[44].x" -3125.15478515625;
	setAttr ".tgi[0].ni[44].y" -2569.7314453125;
	setAttr ".tgi[0].ni[44].nvs" 18314;
	setAttr ".tgi[0].ni[45].x" -2608.571533203125;
	setAttr ".tgi[0].ni[45].y" -1350;
	setAttr ".tgi[0].ni[45].nvs" 18304;
	setAttr ".tgi[0].ni[46].x" -2948.89453125;
	setAttr ".tgi[0].ni[46].y" -1946.027099609375;
	setAttr ".tgi[0].ni[46].nvs" 18312;
	setAttr ".tgi[0].ni[47].x" -2438.543212890625;
	setAttr ".tgi[0].ni[47].y" -2591.839599609375;
	setAttr ".tgi[0].ni[47].nvs" 18306;
	setAttr ".tgi[0].ni[48].x" -1242.6568603515625;
	setAttr ".tgi[0].ni[48].y" -510.061279296875;
	setAttr ".tgi[0].ni[48].nvs" 1931;
	setAttr ".tgi[0].ni[49].x" -2608.571533203125;
	setAttr ".tgi[0].ni[49].y" -1547.142822265625;
	setAttr ".tgi[0].ni[49].nvs" 18304;
	setAttr ".tgi[0].ni[50].x" -934.78204345703125;
	setAttr ".tgi[0].ni[50].y" -1372.580810546875;
	setAttr ".tgi[0].ni[50].nvs" 18314;
	setAttr ".tgi[1].tn" -type "string" "Untitled_2";
	setAttr ".tgi[1].vl" -type "double2" -1452.5182573004249 -682.14283003693629 ;
	setAttr ".tgi[1].vh" -type "double2" 3558.4705545697802 674.99997317791087 ;
	setAttr -s 30 ".tgi[1].ni";
	setAttr ".tgi[1].ni[0].x" 4744.28564453125;
	setAttr ".tgi[1].ni[0].y" -538.5714111328125;
	setAttr ".tgi[1].ni[0].nvs" 18304;
	setAttr ".tgi[1].ni[1].x" 1082.3115234375;
	setAttr ".tgi[1].ni[1].y" 629.90948486328125;
	setAttr ".tgi[1].ni[1].nvs" 18313;
	setAttr ".tgi[1].ni[2].x" 766.423095703125;
	setAttr ".tgi[1].ni[2].y" 94.310020446777344;
	setAttr ".tgi[1].ni[2].nvs" 18314;
	setAttr ".tgi[1].ni[3].x" 2605.094970703125;
	setAttr ".tgi[1].ni[3].y" -352.89810180664062;
	setAttr ".tgi[1].ni[3].nvs" 1931;
	setAttr ".tgi[1].ni[4].x" 5372.85693359375;
	setAttr ".tgi[1].ni[4].y" -560;
	setAttr ".tgi[1].ni[4].nvs" 18304;
	setAttr ".tgi[1].ni[5].x" 440.24679565429688;
	setAttr ".tgi[1].ni[5].y" 493.32656860351562;
	setAttr ".tgi[1].ni[5].nvs" 18313;
	setAttr ".tgi[1].ni[6].x" 5372.85693359375;
	setAttr ".tgi[1].ni[6].y" -1131.4285888671875;
	setAttr ".tgi[1].ni[6].nvs" 18304;
	setAttr ".tgi[1].ni[7].x" 1445.1500244140625;
	setAttr ".tgi[1].ni[7].y" -404.11505126953125;
	setAttr ".tgi[1].ni[7].nvs" 1931;
	setAttr ".tgi[1].ni[8].x" 1171.720703125;
	setAttr ".tgi[1].ni[8].y" -329.415283203125;
	setAttr ".tgi[1].ni[8].nvs" 1931;
	setAttr ".tgi[1].ni[9].x" 1794.710205078125;
	setAttr ".tgi[1].ni[9].y" 692.2615966796875;
	setAttr ".tgi[1].ni[9].nvs" 18306;
	setAttr ".tgi[1].ni[10].x" 5801.4287109375;
	setAttr ".tgi[1].ni[10].y" -565.71429443359375;
	setAttr ".tgi[1].ni[10].nvs" 18304;
	setAttr ".tgi[1].ni[11].x" 5801.4287109375;
	setAttr ".tgi[1].ni[11].y" -838.5714111328125;
	setAttr ".tgi[1].ni[11].nvs" 18304;
	setAttr ".tgi[1].ni[12].x" 5058.5712890625;
	setAttr ".tgi[1].ni[12].y" -765.71429443359375;
	setAttr ".tgi[1].ni[12].nvs" 18304;
	setAttr ".tgi[1].ni[13].x" 775.30780029296875;
	setAttr ".tgi[1].ni[13].y" 602.08502197265625;
	setAttr ".tgi[1].ni[13].nvs" 18314;
	setAttr ".tgi[1].ni[14].x" 5801.4287109375;
	setAttr ".tgi[1].ni[14].y" -664.28570556640625;
	setAttr ".tgi[1].ni[14].nvs" 18304;
	setAttr ".tgi[1].ni[15].x" 777.67034912109375;
	setAttr ".tgi[1].ni[15].y" 346.83428955078125;
	setAttr ".tgi[1].ni[15].nvs" 18314;
	setAttr ".tgi[1].ni[16].x" 1087.7464599609375;
	setAttr ".tgi[1].ni[16].y" 382.31390380859375;
	setAttr ".tgi[1].ni[16].nvs" 18313;
	setAttr ".tgi[1].ni[17].x" 128.57142639160156;
	setAttr ".tgi[1].ni[17].y" 494.28570556640625;
	setAttr ".tgi[1].ni[17].nvs" 18312;
	setAttr ".tgi[1].ni[18].x" 128.57142639160156;
	setAttr ".tgi[1].ni[18].y" 691.4285888671875;
	setAttr ".tgi[1].ni[18].nvs" 18312;
	setAttr ".tgi[1].ni[19].x" 1231.4013671875;
	setAttr ".tgi[1].ni[19].y" 1002.9470825195312;
	setAttr ".tgi[1].ni[19].nvs" 18306;
	setAttr ".tgi[1].ni[20].x" 1775.695556640625;
	setAttr ".tgi[1].ni[20].y" 414.17254638671875;
	setAttr ".tgi[1].ni[20].nvs" 18306;
	setAttr ".tgi[1].ni[21].x" 2615.598876953125;
	setAttr ".tgi[1].ni[21].y" -604.36865234375;
	setAttr ".tgi[1].ni[21].nvs" 1931;
	setAttr ".tgi[1].ni[22].x" 1171.720703125;
	setAttr ".tgi[1].ni[22].y" -470.35821533203125;
	setAttr ".tgi[1].ni[22].nvs" 1931;
	setAttr ".tgi[1].ni[23].x" 2377.003662109375;
	setAttr ".tgi[1].ni[23].y" -456.60031127929688;
	setAttr ".tgi[1].ni[23].nvs" 18314;
	setAttr ".tgi[1].ni[24].x" 5372.85693359375;
	setAttr ".tgi[1].ni[24].y" -900;
	setAttr ".tgi[1].ni[24].nvs" 18304;
	setAttr ".tgi[1].ni[25].x" 2612.2412109375;
	setAttr ".tgi[1].ni[25].y" -847.4547119140625;
	setAttr ".tgi[1].ni[25].nvs" 1931;
	setAttr ".tgi[1].ni[26].x" 1092.040771484375;
	setAttr ".tgi[1].ni[26].y" 1.5936880111694336;
	setAttr ".tgi[1].ni[26].nvs" 18313;
	setAttr ".tgi[1].ni[27].x" 128.57142639160156;
	setAttr ".tgi[1].ni[27].y" 592.85711669921875;
	setAttr ".tgi[1].ni[27].nvs" 18312;
	setAttr ".tgi[1].ni[28].x" 5801.4287109375;
	setAttr ".tgi[1].ni[28].y" -1208.5714111328125;
	setAttr ".tgi[1].ni[28].nvs" 18304;
	setAttr ".tgi[1].ni[29].x" 1062.303466796875;
	setAttr ".tgi[1].ni[29].y" 502.62240600585938;
	setAttr ".tgi[1].ni[29].nvs" 18312;
	setAttr ".tgi[2].tn" -type "string" "Untitled_3";
	setAttr ".tgi[2].vl" -type "double2" -8842.49049112184 814.28568192890828 ;
	setAttr ".tgi[2].vh" -type "double2" -5119.4137159866959 1822.6189751946765 ;
	setAttr -s 20 ".tgi[2].ni";
	setAttr ".tgi[2].ni[0].x" -6055.71435546875;
	setAttr ".tgi[2].ni[0].y" 1120;
	setAttr ".tgi[2].ni[0].nvs" 18304;
	setAttr ".tgi[2].ni[1].x" -6670;
	setAttr ".tgi[2].ni[1].y" 1308.5714111328125;
	setAttr ".tgi[2].ni[1].nvs" 18304;
	setAttr ".tgi[2].ni[2].x" -6362.85693359375;
	setAttr ".tgi[2].ni[2].y" 1158.5714111328125;
	setAttr ".tgi[2].ni[2].nvs" 18304;
	setAttr ".tgi[2].ni[3].x" -6362.85693359375;
	setAttr ".tgi[2].ni[3].y" 1022.8571166992188;
	setAttr ".tgi[2].ni[3].nvs" 18304;
	setAttr ".tgi[2].ni[4].x" -5441.4287109375;
	setAttr ".tgi[2].ni[4].y" 1251.4285888671875;
	setAttr ".tgi[2].ni[4].nvs" 18304;
	setAttr ".tgi[2].ni[5].x" -3905.71435546875;
	setAttr ".tgi[2].ni[5].y" 1582.185302734375;
	setAttr ".tgi[2].ni[5].nvs" 18305;
	setAttr ".tgi[2].ni[6].x" -4212.85693359375;
	setAttr ".tgi[2].ni[6].y" 1634.1630859375;
	setAttr ".tgi[2].ni[6].nvs" 18305;
	setAttr ".tgi[2].ni[7].x" -6647.90478515625;
	setAttr ".tgi[2].ni[7].y" 1642.2860107421875;
	setAttr ".tgi[2].ni[7].nvs" 18305;
	setAttr ".tgi[2].ni[8].x" -7046.1904296875;
	setAttr ".tgi[2].ni[8].y" 1695.8096923828125;
	setAttr ".tgi[2].ni[8].nvs" 18305;
	setAttr ".tgi[2].ni[9].x" -3598.571533203125;
	setAttr ".tgi[2].ni[9].y" 1354.2857666015625;
	setAttr ".tgi[2].ni[9].nvs" 18305;
	setAttr ".tgi[2].ni[10].x" -4831.2265625;
	setAttr ".tgi[2].ni[10].y" 1315.84912109375;
	setAttr ".tgi[2].ni[10].nvs" 18305;
	setAttr ".tgi[2].ni[11].x" -3905.71435546875;
	setAttr ".tgi[2].ni[11].y" 1311.4285888671875;
	setAttr ".tgi[2].ni[11].nvs" 18304;
	setAttr ".tgi[2].ni[12].x" -3581.855712890625;
	setAttr ".tgi[2].ni[12].y" 1680.837158203125;
	setAttr ".tgi[2].ni[12].nvs" 18305;
	setAttr ".tgi[2].ni[13].x" -5748.5712890625;
	setAttr ".tgi[2].ni[13].y" 1238.5714111328125;
	setAttr ".tgi[2].ni[13].nvs" 18304;
	setAttr ".tgi[2].ni[14].x" -3291.428466796875;
	setAttr ".tgi[2].ni[14].y" 1488.5714111328125;
	setAttr ".tgi[2].ni[14].nvs" 18306;
	setAttr ".tgi[2].ni[15].x" -4212.85693359375;
	setAttr ".tgi[2].ni[15].y" 1237.142822265625;
	setAttr ".tgi[2].ni[15].nvs" 18304;
	setAttr ".tgi[2].ni[16].x" -2984.28564453125;
	setAttr ".tgi[2].ni[16].y" 1490;
	setAttr ".tgi[2].ni[16].nvs" 18304;
	setAttr ".tgi[2].ni[17].x" -5134.28564453125;
	setAttr ".tgi[2].ni[17].y" 1267.142822265625;
	setAttr ".tgi[2].ni[17].nvs" 18304;
	setAttr ".tgi[2].ni[18].x" -7416.857421875;
	setAttr ".tgi[2].ni[18].y" 1527.61865234375;
	setAttr ".tgi[2].ni[18].nvs" 18305;
	setAttr ".tgi[2].ni[19].x" -4490.2841796875;
	setAttr ".tgi[2].ni[19].y" 1141.6575927734375;
	setAttr ".tgi[2].ni[19].nvs" 18305;
	setAttr ".tgi[3].tn" -type "string" "Untitled_4";
	setAttr ".tgi[3].vl" -type "double2" -5797.7561798742599 -773.8094930610971 ;
	setAttr ".tgi[3].vh" -type "double2" -1701.0530459593201 335.71427237419903 ;
	setAttr -s 33 ".tgi[3].ni";
	setAttr ".tgi[3].ni[0].x" -4630;
	setAttr ".tgi[3].ni[0].y" -265.71429443359375;
	setAttr ".tgi[3].ni[0].nvs" 18304;
	setAttr ".tgi[3].ni[1].x" -17.39495849609375;
	setAttr ".tgi[3].ni[1].y" -97.058822631835938;
	setAttr ".tgi[3].ni[1].nvs" 18305;
	setAttr ".tgi[3].ni[2].x" -5244.28564453125;
	setAttr ".tgi[3].ni[2].y" -167.14285278320312;
	setAttr ".tgi[3].ni[2].nvs" 18304;
	setAttr ".tgi[3].ni[3].x" -4630;
	setAttr ".tgi[3].ni[3].y" -364.28570556640625;
	setAttr ".tgi[3].ni[3].nvs" 18304;
	setAttr ".tgi[3].ni[4].x" -3394.28564453125;
	setAttr ".tgi[3].ni[4].y" -157.14285278320312;
	setAttr ".tgi[3].ni[4].nvs" 18304;
	setAttr ".tgi[3].ni[5].x" -5244.28564453125;
	setAttr ".tgi[3].ni[5].y" -364.28570556640625;
	setAttr ".tgi[3].ni[5].nvs" 18304;
	setAttr ".tgi[3].ni[6].x" -4937.14306640625;
	setAttr ".tgi[3].ni[6].y" -265.71429443359375;
	setAttr ".tgi[3].ni[6].nvs" 18304;
	setAttr ".tgi[3].ni[7].x" -4315.71435546875;
	setAttr ".tgi[3].ni[7].y" -30;
	setAttr ".tgi[3].ni[7].nvs" 18304;
	setAttr ".tgi[3].ni[8].x" -1858.5714111328125;
	setAttr ".tgi[3].ni[8].y" -192.85714721679688;
	setAttr ".tgi[3].ni[8].nvs" 18304;
	setAttr ".tgi[3].ni[9].x" -4630;
	setAttr ".tgi[3].ni[9].y" -167.14285278320312;
	setAttr ".tgi[3].ni[9].nvs" 18304;
	setAttr ".tgi[3].ni[10].x" -2165.71435546875;
	setAttr ".tgi[3].ni[10].y" -192.85714721679688;
	setAttr ".tgi[3].ni[10].nvs" 18304;
	setAttr ".tgi[3].ni[11].x" -4011.748291015625;
	setAttr ".tgi[3].ni[11].y" -168.62957763671875;
	setAttr ".tgi[3].ni[11].nvs" 18304;
	setAttr ".tgi[3].ni[12].x" 291.42855834960938;
	setAttr ".tgi[3].ni[12].y" 47.142856597900391;
	setAttr ".tgi[3].ni[12].nvs" 18304;
	setAttr ".tgi[3].ni[13].x" -4315.71435546875;
	setAttr ".tgi[3].ni[13].y" -331.42855834960938;
	setAttr ".tgi[3].ni[13].nvs" 18304;
	setAttr ".tgi[3].ni[14].x" -3111.67724609375;
	setAttr ".tgi[3].ni[14].y" 233.31568908691406;
	setAttr ".tgi[3].ni[14].nvs" 18305;
	setAttr ".tgi[3].ni[15].x" -2780;
	setAttr ".tgi[3].ni[15].y" -330;
	setAttr ".tgi[3].ni[15].nvs" 18304;
	setAttr ".tgi[3].ni[16].x" -1244.2857666015625;
	setAttr ".tgi[3].ni[16].y" -131.42857360839844;
	setAttr ".tgi[3].ni[16].nvs" 18304;
	setAttr ".tgi[3].ni[17].x" -4008.571533203125;
	setAttr ".tgi[3].ni[17].y" -58.571430206298828;
	setAttr ".tgi[3].ni[17].nvs" 18304;
	setAttr ".tgi[3].ni[18].x" -2780;
	setAttr ".tgi[3].ni[18].y" -194.28572082519531;
	setAttr ".tgi[3].ni[18].nvs" 18304;
	setAttr ".tgi[3].ni[19].x" -3087.142822265625;
	setAttr ".tgi[3].ni[19].y" -130;
	setAttr ".tgi[3].ni[19].nvs" 18304;
	setAttr ".tgi[3].ni[20].x" -322.85714721679688;
	setAttr ".tgi[3].ni[20].y" -57.142856597900391;
	setAttr ".tgi[3].ni[20].nvs" 18304;
	setAttr ".tgi[3].ni[21].x" 1290;
	setAttr ".tgi[3].ni[21].y" 47.142856597900391;
	setAttr ".tgi[3].ni[21].nvs" 18304;
	setAttr ".tgi[3].ni[22].x" -2472.857177734375;
	setAttr ".tgi[3].ni[22].y" -261.42855834960938;
	setAttr ".tgi[3].ni[22].nvs" 18304;
	setAttr ".tgi[3].ni[23].x" -630;
	setAttr ".tgi[3].ni[23].y" -68.571426391601562;
	setAttr ".tgi[3].ni[23].nvs" 18304;
	setAttr ".tgi[3].ni[24].x" -4315.71435546875;
	setAttr ".tgi[3].ni[24].y" -232.85714721679688;
	setAttr ".tgi[3].ni[24].nvs" 18304;
	setAttr ".tgi[3].ni[25].x" 598.5714111328125;
	setAttr ".tgi[3].ni[25].y" 18.571428298950195;
	setAttr ".tgi[3].ni[25].nvs" 18304;
	setAttr ".tgi[3].ni[26].x" 905.71429443359375;
	setAttr ".tgi[3].ni[26].y" 47.142856597900391;
	setAttr ".tgi[3].ni[26].nvs" 18304;
	setAttr ".tgi[3].ni[27].x" -4019.244384765625;
	setAttr ".tgi[3].ni[27].y" 120.07266235351562;
	setAttr ".tgi[3].ni[27].nvs" 18304;
	setAttr ".tgi[3].ni[28].x" -1551.4285888671875;
	setAttr ".tgi[3].ni[28].y" -184.28572082519531;
	setAttr ".tgi[3].ni[28].nvs" 18304;
	setAttr ".tgi[3].ni[29].x" -5244.28564453125;
	setAttr ".tgi[3].ni[29].y" -265.71429443359375;
	setAttr ".tgi[3].ni[29].nvs" 18304;
	setAttr ".tgi[3].ni[30].x" -3676.175048828125;
	setAttr ".tgi[3].ni[30].y" 24.352910995483398;
	setAttr ".tgi[3].ni[30].nvs" 18305;
	setAttr ".tgi[3].ni[31].x" -4008.571533203125;
	setAttr ".tgi[3].ni[31].y" -274.28570556640625;
	setAttr ".tgi[3].ni[31].nvs" 18304;
	setAttr ".tgi[3].ni[32].x" -937.14288330078125;
	setAttr ".tgi[3].ni[32].y" -82.857139587402344;
	setAttr ".tgi[3].ni[32].nvs" 18304;
	setAttr ".tgi[4].tn" -type "string" "Untitled_5";
	setAttr ".tgi[4].vl" -type "double2" -10739.560012808668 -1855.9523072034626 ;
	setAttr ".tgi[4].vh" -type "double2" -6717.5821506496868 -766.6666362020718 ;
	setAttr -s 60 ".tgi[4].ni";
	setAttr ".tgi[4].ni[0].x" -9848.5712890625;
	setAttr ".tgi[4].ni[0].y" -912.85711669921875;
	setAttr ".tgi[4].ni[0].nvs" 18304;
	setAttr ".tgi[4].ni[1].x" -1692.857177734375;
	setAttr ".tgi[4].ni[1].y" -861.4285888671875;
	setAttr ".tgi[4].ni[1].nvs" 18304;
	setAttr ".tgi[4].ni[2].x" -957.14288330078125;
	setAttr ".tgi[4].ni[2].y" -700;
	setAttr ".tgi[4].ni[2].nvs" 18304;
	setAttr ".tgi[4].ni[3].x" -6155.71435546875;
	setAttr ".tgi[4].ni[3].y" -1094.2857666015625;
	setAttr ".tgi[4].ni[3].nvs" 18304;
	setAttr ".tgi[4].ni[4].x" -6462.85693359375;
	setAttr ".tgi[4].ni[4].y" -1108.5714111328125;
	setAttr ".tgi[4].ni[4].nvs" 18304;
	setAttr ".tgi[4].ni[5].x" -3698.571533203125;
	setAttr ".tgi[4].ni[5].y" -998.5714111328125;
	setAttr ".tgi[4].ni[5].nvs" 18304;
	setAttr ".tgi[4].ni[6].x" -10155.7138671875;
	setAttr ".tgi[4].ni[6].y" -814.28570556640625;
	setAttr ".tgi[4].ni[6].nvs" 18304;
	setAttr ".tgi[4].ni[7].x" -5234.28564453125;
	setAttr ".tgi[4].ni[7].y" -840;
	setAttr ".tgi[4].ni[7].nvs" 18304;
	setAttr ".tgi[4].ni[8].x" -10155.7138671875;
	setAttr ".tgi[4].ni[8].y" -912.85711669921875;
	setAttr ".tgi[4].ni[8].nvs" 18304;
	setAttr ".tgi[4].ni[9].x" -8920;
	setAttr ".tgi[4].ni[9].y" -1061.4285888671875;
	setAttr ".tgi[4].ni[9].nvs" 18304;
	setAttr ".tgi[4].ni[10].x" -7384.28564453125;
	setAttr ".tgi[4].ni[10].y" -1048.5714111328125;
	setAttr ".tgi[4].ni[10].nvs" 18304;
	setAttr ".tgi[4].ni[11].x" -4620;
	setAttr ".tgi[4].ni[11].y" -1047.142822265625;
	setAttr ".tgi[4].ni[11].nvs" 18304;
	setAttr ".tgi[4].ni[12].x" -8920;
	setAttr ".tgi[4].ni[12].y" -845.71429443359375;
	setAttr ".tgi[4].ni[12].nvs" 18304;
	setAttr ".tgi[4].ni[13].x" -957.14288330078125;
	setAttr ".tgi[4].ni[13].y" -1230;
	setAttr ".tgi[4].ni[13].nvs" 18304;
	setAttr ".tgi[4].ni[14].x" -4005.71435546875;
	setAttr ".tgi[4].ni[14].y" -1008.5714111328125;
	setAttr ".tgi[4].ni[14].nvs" 18304;
	setAttr ".tgi[4].ni[15].x" -2367.142822265625;
	setAttr ".tgi[4].ni[15].y" -1208.5714111328125;
	setAttr ".tgi[4].ni[15].nvs" 18304;
	setAttr ".tgi[4].ni[16].x" -10155.7138671875;
	setAttr ".tgi[4].ni[16].y" -715.71429443359375;
	setAttr ".tgi[4].ni[16].nvs" 18304;
	setAttr ".tgi[4].ni[17].x" -957.14288330078125;
	setAttr ".tgi[4].ni[17].y" -465.71429443359375;
	setAttr ".tgi[4].ni[17].nvs" 18304;
	setAttr ".tgi[4].ni[18].x" -4312.85693359375;
	setAttr ".tgi[4].ni[18].y" -945.71429443359375;
	setAttr ".tgi[4].ni[18].nvs" 18304;
	setAttr ".tgi[4].ni[19].x" -5234.28564453125;
	setAttr ".tgi[4].ni[19].y" -1090;
	setAttr ".tgi[4].ni[19].nvs" 18304;
	setAttr ".tgi[4].ni[20].x" -10155.7138671875;
	setAttr ".tgi[4].ni[20].y" -617.14288330078125;
	setAttr ".tgi[4].ni[20].nvs" 18304;
	setAttr ".tgi[4].ni[21].x" -957.14288330078125;
	setAttr ".tgi[4].ni[21].y" -798.5714111328125;
	setAttr ".tgi[4].ni[21].nvs" 18304;
	setAttr ".tgi[4].ni[22].x" -9234.2861328125;
	setAttr ".tgi[4].ni[22].y" -912.85711669921875;
	setAttr ".tgi[4].ni[22].nvs" 18304;
	setAttr ".tgi[4].ni[23].x" -9234.2861328125;
	setAttr ".tgi[4].ni[23].y" -1110;
	setAttr ".tgi[4].ni[23].nvs" 18304;
	setAttr ".tgi[4].ni[24].x" -7691.4287109375;
	setAttr ".tgi[4].ni[24].y" -855.71429443359375;
	setAttr ".tgi[4].ni[24].nvs" 18304;
	setAttr ".tgi[4].ni[25].x" -8612.857421875;
	setAttr ".tgi[4].ni[25].y" -1087.142822265625;
	setAttr ".tgi[4].ni[25].nvs" 18304;
	setAttr ".tgi[4].ni[26].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[26].y" -908.5714111328125;
	setAttr ".tgi[4].ni[26].nvs" 18304;
	setAttr ".tgi[4].ni[27].x" -957.14288330078125;
	setAttr ".tgi[4].ni[27].y" -1032.857177734375;
	setAttr ".tgi[4].ni[27].nvs" 18304;
	setAttr ".tgi[4].ni[28].x" -10155.7138671875;
	setAttr ".tgi[4].ni[28].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[28].nvs" 18304;
	setAttr ".tgi[4].ni[29].x" -8611.7607421875;
	setAttr ".tgi[4].ni[29].y" -752.093505859375;
	setAttr ".tgi[4].ni[29].nvs" 18304;
	setAttr ".tgi[4].ni[30].x" -7077.14306640625;
	setAttr ".tgi[4].ni[30].y" -972.85711669921875;
	setAttr ".tgi[4].ni[30].nvs" 18304;
	setAttr ".tgi[4].ni[31].x" -9848.5712890625;
	setAttr ".tgi[4].ni[31].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[31].nvs" 18304;
	setAttr ".tgi[4].ni[32].x" -9542.23828125;
	setAttr ".tgi[4].ni[32].y" -1033.5311279296875;
	setAttr ".tgi[4].ni[32].nvs" 18306;
	setAttr ".tgi[4].ni[33].x" -7384.28564453125;
	setAttr ".tgi[4].ni[33].y" -912.85711669921875;
	setAttr ".tgi[4].ni[33].nvs" 18304;
	setAttr ".tgi[4].ni[34].x" -9234.2861328125;
	setAttr ".tgi[4].ni[34].y" -1011.4285888671875;
	setAttr ".tgi[4].ni[34].nvs" 18304;
	setAttr ".tgi[4].ni[35].x" -4927.14306640625;
	setAttr ".tgi[4].ni[35].y" -838.5714111328125;
	setAttr ".tgi[4].ni[35].nvs" 18304;
	setAttr ".tgi[4].ni[36].x" -957.14288330078125;
	setAttr ".tgi[4].ni[36].y" -915.71429443359375;
	setAttr ".tgi[4].ni[36].nvs" 18304;
	setAttr ".tgi[4].ni[37].x" -1692.857177734375;
	setAttr ".tgi[4].ni[37].y" -1017.1428833007812;
	setAttr ".tgi[4].ni[37].nvs" 18304;
	setAttr ".tgi[4].ni[38].x" -1692.857177734375;
	setAttr ".tgi[4].ni[38].y" -762.85711669921875;
	setAttr ".tgi[4].ni[38].nvs" 18304;
	setAttr ".tgi[4].ni[39].x" -6770;
	setAttr ".tgi[4].ni[39].y" -1124.2857666015625;
	setAttr ".tgi[4].ni[39].nvs" 18304;
	setAttr ".tgi[4].ni[40].x" -7998.5712890625;
	setAttr ".tgi[4].ni[40].y" -874.28570556640625;
	setAttr ".tgi[4].ni[40].nvs" 18304;
	setAttr ".tgi[4].ni[41].x" -5848.5712890625;
	setAttr ".tgi[4].ni[41].y" -1038.5714111328125;
	setAttr ".tgi[4].ni[41].nvs" 18304;
	setAttr ".tgi[4].ni[42].x" -9848.5712890625;
	setAttr ".tgi[4].ni[42].y" -1110;
	setAttr ".tgi[4].ni[42].nvs" 18304;
	setAttr ".tgi[4].ni[43].x" -8920;
	setAttr ".tgi[4].ni[43].y" -962.85711669921875;
	setAttr ".tgi[4].ni[43].nvs" 18304;
	setAttr ".tgi[4].ni[44].x" -10155.7138671875;
	setAttr ".tgi[4].ni[44].y" -1405.7142333984375;
	setAttr ".tgi[4].ni[44].nvs" 18304;
	setAttr ".tgi[4].ni[45].x" -8945.8779296875;
	setAttr ".tgi[4].ni[45].y" -1389.3060302734375;
	setAttr ".tgi[4].ni[45].nvs" 18306;
	setAttr ".tgi[4].ni[46].x" -10155.7138671875;
	setAttr ".tgi[4].ni[46].y" -1208.5714111328125;
	setAttr ".tgi[4].ni[46].nvs" 18304;
	setAttr ".tgi[4].ni[47].x" -4620;
	setAttr ".tgi[4].ni[47].y" -911.4285888671875;
	setAttr ".tgi[4].ni[47].nvs" 18304;
	setAttr ".tgi[4].ni[48].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[48].y" -1025.7142333984375;
	setAttr ".tgi[4].ni[48].nvs" 18304;
	setAttr ".tgi[4].ni[49].x" -8293.830078125;
	setAttr ".tgi[4].ni[49].y" -867.90045166015625;
	setAttr ".tgi[4].ni[49].nvs" 18306;
	setAttr ".tgi[4].ni[50].x" -2717.142822265625;
	setAttr ".tgi[4].ni[50].y" -1185.7142333984375;
	setAttr ".tgi[4].ni[50].nvs" 18304;
	setAttr ".tgi[4].ni[51].x" -10155.7138671875;
	setAttr ".tgi[4].ni[51].y" -1307.142822265625;
	setAttr ".tgi[4].ni[51].nvs" 18304;
	setAttr ".tgi[4].ni[52].x" -8614.15234375;
	setAttr ".tgi[4].ni[52].y" -1219.30224609375;
	setAttr ".tgi[4].ni[52].nvs" 18306;
	setAttr ".tgi[4].ni[53].x" -7691.4287109375;
	setAttr ".tgi[4].ni[53].y" -991.4285888671875;
	setAttr ".tgi[4].ni[53].nvs" 18304;
	setAttr ".tgi[4].ni[54].x" -957.14288330078125;
	setAttr ".tgi[4].ni[54].y" -564.28570556640625;
	setAttr ".tgi[4].ni[54].nvs" 18304;
	setAttr ".tgi[4].ni[55].x" -10155.7138671875;
	setAttr ".tgi[4].ni[55].y" -1110;
	setAttr ".tgi[4].ni[55].nvs" 18304;
	setAttr ".tgi[4].ni[56].x" -4927.14306640625;
	setAttr ".tgi[4].ni[56].y" -1081.4285888671875;
	setAttr ".tgi[4].ni[56].nvs" 18304;
	setAttr ".tgi[4].ni[57].x" -8612.857421875;
	setAttr ".tgi[4].ni[57].y" -871.4285888671875;
	setAttr ".tgi[4].ni[57].nvs" 18304;
	setAttr ".tgi[4].ni[58].x" -1385.7142333984375;
	setAttr ".tgi[4].ni[58].y" -788.5714111328125;
	setAttr ".tgi[4].ni[58].nvs" 18304;
	setAttr ".tgi[4].ni[59].x" -5541.4287109375;
	setAttr ".tgi[4].ni[59].y" -987.14288330078125;
	setAttr ".tgi[4].ni[59].nvs" 18304;
	setAttr ".tgi[5].tn" -type "string" "Untitled_6";
	setAttr ".tgi[5].vl" -type "double2" -3649.2214667145759 -3032.1427366563157 ;
	setAttr ".tgi[5].vh" -type "double2" 2755.1738831932234 -1297.618996056287 ;
	setAttr -s 39 ".tgi[5].ni";
	setAttr ".tgi[5].ni[0].x" -717.14288330078125;
	setAttr ".tgi[5].ni[0].y" -1441.4285888671875;
	setAttr ".tgi[5].ni[0].nvs" 18304;
	setAttr ".tgi[5].ni[1].x" -2649.8759765625;
	setAttr ".tgi[5].ni[1].y" -767.46453857421875;
	setAttr ".tgi[5].ni[1].nvs" 18306;
	setAttr ".tgi[5].ni[2].x" -3545.71435546875;
	setAttr ".tgi[5].ni[2].y" -605.71429443359375;
	setAttr ".tgi[5].ni[2].nvs" 18304;
	setAttr ".tgi[5].ni[3].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[3].y" -941.4285888671875;
	setAttr ".tgi[5].ni[3].nvs" 18304;
	setAttr ".tgi[5].ni[4].x" -3545.71435546875;
	setAttr ".tgi[5].ni[4].y" -704.28570556640625;
	setAttr ".tgi[5].ni[4].nvs" 18304;
	setAttr ".tgi[5].ni[5].x" -2660.843017578125;
	setAttr ".tgi[5].ni[5].y" -1198.5745849609375;
	setAttr ".tgi[5].ni[5].nvs" 18306;
	setAttr ".tgi[5].ni[6].x" -2280.754150390625;
	setAttr ".tgi[5].ni[6].y" -1337.3529052734375;
	setAttr ".tgi[5].ni[6].nvs" 18306;
	setAttr ".tgi[5].ni[7].x" -717.14288330078125;
	setAttr ".tgi[5].ni[7].y" -1225.7142333984375;
	setAttr ".tgi[5].ni[7].nvs" 18304;
	setAttr ".tgi[5].ni[8].x" -3238.571533203125;
	setAttr ".tgi[5].ni[8].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[8].nvs" 18304;
	setAttr ".tgi[5].ni[9].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[9].y" -1388.5714111328125;
	setAttr ".tgi[5].ni[9].nvs" 18304;
	setAttr ".tgi[5].ni[10].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[10].y" -1040;
	setAttr ".tgi[5].ni[10].nvs" 18304;
	setAttr ".tgi[5].ni[11].x" -2268.605224609375;
	setAttr ".tgi[5].ni[11].y" -1083.2686767578125;
	setAttr ".tgi[5].ni[11].nvs" 18306;
	setAttr ".tgi[5].ni[12].x" -3545.71435546875;
	setAttr ".tgi[5].ni[12].y" -1295.7142333984375;
	setAttr ".tgi[5].ni[12].nvs" 18304;
	setAttr ".tgi[5].ni[13].x" -3545.71435546875;
	setAttr ".tgi[5].ni[13].y" -901.4285888671875;
	setAttr ".tgi[5].ni[13].nvs" 18304;
	setAttr ".tgi[5].ni[14].x" -1388.5714111328125;
	setAttr ".tgi[5].ni[14].y" -1298.5714111328125;
	setAttr ".tgi[5].ni[14].nvs" 18304;
	setAttr ".tgi[5].ni[15].x" -3238.571533203125;
	setAttr ".tgi[5].ni[15].y" -1000;
	setAttr ".tgi[5].ni[15].nvs" 18304;
	setAttr ".tgi[5].ni[16].x" -717.14288330078125;
	setAttr ".tgi[5].ni[16].y" -1872.857177734375;
	setAttr ".tgi[5].ni[16].nvs" 18304;
	setAttr ".tgi[5].ni[17].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[17].y" -1715.7142333984375;
	setAttr ".tgi[5].ni[17].nvs" 18304;
	setAttr ".tgi[5].ni[18].x" -3238.571533203125;
	setAttr ".tgi[5].ni[18].y" -1197.142822265625;
	setAttr ".tgi[5].ni[18].nvs" 18304;
	setAttr ".tgi[5].ni[19].x" -2624.28564453125;
	setAttr ".tgi[5].ni[19].y" -1058.5714111328125;
	setAttr ".tgi[5].ni[19].nvs" 18304;
	setAttr ".tgi[5].ni[20].x" -1096.7374267578125;
	setAttr ".tgi[5].ni[20].y" -2203.770263671875;
	setAttr ".tgi[5].ni[20].nvs" 18306;
	setAttr ".tgi[5].ni[21].x" -1388.5714111328125;
	setAttr ".tgi[5].ni[21].y" -1200;
	setAttr ".tgi[5].ni[21].nvs" 18304;
	setAttr ".tgi[5].ni[22].x" -717.14288330078125;
	setAttr ".tgi[5].ni[22].y" -658.5714111328125;
	setAttr ".tgi[5].ni[22].nvs" 18304;
	setAttr ".tgi[5].ni[23].x" -3545.71435546875;
	setAttr ".tgi[5].ni[23].y" -1000;
	setAttr ".tgi[5].ni[23].nvs" 18304;
	setAttr ".tgi[5].ni[24].x" -1695.7142333984375;
	setAttr ".tgi[5].ni[24].y" -1118.5714111328125;
	setAttr ".tgi[5].ni[24].nvs" 18304;
	setAttr ".tgi[5].ni[25].x" -3545.71435546875;
	setAttr ".tgi[5].ni[25].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[25].nvs" 18304;
	setAttr ".tgi[5].ni[26].x" -717.14288330078125;
	setAttr ".tgi[5].ni[26].y" -1127.142822265625;
	setAttr ".tgi[5].ni[26].nvs" 18304;
	setAttr ".tgi[5].ni[27].x" -3545.71435546875;
	setAttr ".tgi[5].ni[27].y" -802.85711669921875;
	setAttr ".tgi[5].ni[27].nvs" 18304;
	setAttr ".tgi[5].ni[28].x" -671.21630859375;
	setAttr ".tgi[5].ni[28].y" -2372.208984375;
	setAttr ".tgi[5].ni[28].nvs" 18305;
	setAttr ".tgi[5].ni[29].x" -717.14288330078125;
	setAttr ".tgi[5].ni[29].y" -794.28570556640625;
	setAttr ".tgi[5].ni[29].nvs" 18304;
	setAttr ".tgi[5].ni[30].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[30].y" -1814.2857666015625;
	setAttr ".tgi[5].ni[30].nvs" 1923;
	setAttr ".tgi[5].ni[31].x" -3545.71435546875;
	setAttr ".tgi[5].ni[31].y" -1394.2857666015625;
	setAttr ".tgi[5].ni[31].nvs" 18304;
	setAttr ".tgi[5].ni[32].x" -1982.1771240234375;
	setAttr ".tgi[5].ni[32].y" -1443.332763671875;
	setAttr ".tgi[5].ni[32].nvs" 18306;
	setAttr ".tgi[5].ni[33].x" -1081.4285888671875;
	setAttr ".tgi[5].ni[33].y" -1252.857177734375;
	setAttr ".tgi[5].ni[33].nvs" 18304;
	setAttr ".tgi[5].ni[34].x" -717.14288330078125;
	setAttr ".tgi[5].ni[34].y" -1971.4285888671875;
	setAttr ".tgi[5].ni[34].nvs" 18304;
	setAttr ".tgi[5].ni[35].x" -717.14288330078125;
	setAttr ".tgi[5].ni[35].y" -1324.2857666015625;
	setAttr ".tgi[5].ni[35].nvs" 18304;
	setAttr ".tgi[5].ni[36].x" -3545.71435546875;
	setAttr ".tgi[5].ni[36].y" -1197.142822265625;
	setAttr ".tgi[5].ni[36].nvs" 18304;
	setAttr ".tgi[5].ni[37].x" -717.14288330078125;
	setAttr ".tgi[5].ni[37].y" -892.85711669921875;
	setAttr ".tgi[5].ni[37].nvs" 18304;
	setAttr ".tgi[5].ni[38].x" -2931.428466796875;
	setAttr ".tgi[5].ni[38].y" -1098.5714111328125;
	setAttr ".tgi[5].ni[38].nvs" 18304;
	setAttr ".tgi[6].tn" -type "string" "Untitled_7";
	setAttr ".tgi[6].vl" -type "double2" 1088.4190862902346 -1426.5179969412816 ;
	setAttr ".tgi[6].vh" -type "double2" 1996.8224221547453 -858.45078598438158 ;
	setAttr -s 66 ".tgi[6].ni";
	setAttr ".tgi[6].ni[0].x" 1750;
	setAttr ".tgi[6].ni[0].y" -960;
	setAttr ".tgi[6].ni[0].nvs" 18304;
	setAttr ".tgi[6].ni[1].x" 6068.5712890625;
	setAttr ".tgi[6].ni[1].y" -1405.7142333984375;
	setAttr ".tgi[6].ni[1].nvs" 18304;
	setAttr ".tgi[6].ni[2].x" 7338.5712890625;
	setAttr ".tgi[6].ni[2].y" -1534.2857666015625;
	setAttr ".tgi[6].ni[2].nvs" 18304;
	setAttr ".tgi[6].ni[3].x" 7031.4287109375;
	setAttr ".tgi[6].ni[3].y" -1620;
	setAttr ".tgi[6].ni[3].nvs" 18304;
	setAttr ".tgi[6].ni[4].x" 6068.5712890625;
	setAttr ".tgi[6].ni[4].y" -827.14288330078125;
	setAttr ".tgi[6].ni[4].nvs" 18304;
	setAttr ".tgi[6].ni[5].x" 4521.4287109375;
	setAttr ".tgi[6].ni[5].y" -1291.4285888671875;
	setAttr ".tgi[6].ni[5].nvs" 18304;
	setAttr ".tgi[6].ni[6].x" 7031.4287109375;
	setAttr ".tgi[6].ni[6].y" -864.28570556640625;
	setAttr ".tgi[6].ni[6].nvs" 18304;
	setAttr ".tgi[6].ni[7].x" 7768.5712890625;
	setAttr ".tgi[6].ni[7].y" -632.85711669921875;
	setAttr ".tgi[6].ni[7].nvs" 18304;
	setAttr ".tgi[6].ni[8].x" 1400.84033203125;
	setAttr ".tgi[6].ni[8].y" -1032.43701171875;
	setAttr ".tgi[6].ni[8].nvs" 18306;
	setAttr ".tgi[6].ni[9].x" 2985.71435546875;
	setAttr ".tgi[6].ni[9].y" -1191.4285888671875;
	setAttr ".tgi[6].ni[9].nvs" 18304;
	setAttr ".tgi[6].ni[10].x" 7338.5712890625;
	setAttr ".tgi[6].ni[10].y" -1632.857177734375;
	setAttr ".tgi[6].ni[10].nvs" 18304;
	setAttr ".tgi[6].ni[11].x" 7768.5712890625;
	setAttr ".tgi[6].ni[11].y" -731.4285888671875;
	setAttr ".tgi[6].ni[11].nvs" 18304;
	setAttr ".tgi[6].ni[12].x" 828.5714111328125;
	setAttr ".tgi[6].ni[12].y" -1308.5714111328125;
	setAttr ".tgi[6].ni[12].nvs" 18304;
	setAttr ".tgi[6].ni[13].x" 5454.28564453125;
	setAttr ".tgi[6].ni[13].y" -904.28570556640625;
	setAttr ".tgi[6].ni[13].nvs" 18304;
	setAttr ".tgi[6].ni[14].x" 2064.28564453125;
	setAttr ".tgi[6].ni[14].y" -834.28570556640625;
	setAttr ".tgi[6].ni[14].nvs" 18304;
	setAttr ".tgi[6].ni[15].x" 7338.5712890625;
	setAttr ".tgi[6].ni[15].y" -842.85711669921875;
	setAttr ".tgi[6].ni[15].nvs" 18304;
	setAttr ".tgi[6].ni[16].x" 6068.5712890625;
	setAttr ".tgi[6].ni[16].y" -1255.7142333984375;
	setAttr ".tgi[6].ni[16].nvs" 18304;
	setAttr ".tgi[6].ni[17].x" 7768.5712890625;
	setAttr ".tgi[6].ni[17].y" -848.5714111328125;
	setAttr ".tgi[6].ni[17].nvs" 18304;
	setAttr ".tgi[6].ni[18].x" 6717.14306640625;
	setAttr ".tgi[6].ni[18].y" -1267.142822265625;
	setAttr ".tgi[6].ni[18].nvs" 18304;
	setAttr ".tgi[6].ni[19].x" 828.5714111328125;
	setAttr ".tgi[6].ni[19].y" -1012.8571166992188;
	setAttr ".tgi[6].ni[19].nvs" 18304;
	setAttr ".tgi[6].ni[20].x" 6068.5712890625;
	setAttr ".tgi[6].ni[20].y" -728.5714111328125;
	setAttr ".tgi[6].ni[20].nvs" 18304;
	setAttr ".tgi[6].ni[21].x" 3292.857177734375;
	setAttr ".tgi[6].ni[21].y" -1322.857177734375;
	setAttr ".tgi[6].ni[21].nvs" 18304;
	setAttr ".tgi[6].ni[22].x" 828.5714111328125;
	setAttr ".tgi[6].ni[22].y" -914.28570556640625;
	setAttr ".tgi[6].ni[22].nvs" 18304;
	setAttr ".tgi[6].ni[23].x" 4214.28564453125;
	setAttr ".tgi[6].ni[23].y" -1284.2857666015625;
	setAttr ".tgi[6].ni[23].nvs" 18304;
	setAttr ".tgi[6].ni[24].x" 828.5714111328125;
	setAttr ".tgi[6].ni[24].y" -815.71429443359375;
	setAttr ".tgi[6].ni[24].nvs" 18304;
	setAttr ".tgi[6].ni[25].x" 6410;
	setAttr ".tgi[6].ni[25].y" -805.71429443359375;
	setAttr ".tgi[6].ni[25].nvs" 18304;
	setAttr ".tgi[6].ni[26].x" 7338.5712890625;
	setAttr ".tgi[6].ni[26].y" -1027.142822265625;
	setAttr ".tgi[6].ni[26].nvs" 18304;
	setAttr ".tgi[6].ni[27].x" 2064.28564453125;
	setAttr ".tgi[6].ni[27].y" -932.85711669921875;
	setAttr ".tgi[6].ni[27].nvs" 18304;
	setAttr ".tgi[6].ni[28].x" 7768.5712890625;
	setAttr ".tgi[6].ni[28].y" -965.71429443359375;
	setAttr ".tgi[6].ni[28].nvs" 18304;
	setAttr ".tgi[6].ni[29].x" 7338.5712890625;
	setAttr ".tgi[6].ni[29].y" -1182.857177734375;
	setAttr ".tgi[6].ni[29].nvs" 19682;
	setAttr ".tgi[6].ni[30].x" 7768.5712890625;
	setAttr ".tgi[6].ni[30].y" -1064.2857666015625;
	setAttr ".tgi[6].ni[30].nvs" 18304;
	setAttr ".tgi[6].ni[31].x" 1135.7142333984375;
	setAttr ".tgi[6].ni[31].y" -1111.4285888671875;
	setAttr ".tgi[6].ni[31].nvs" 18304;
	setAttr ".tgi[6].ni[32].x" 5135.71435546875;
	setAttr ".tgi[6].ni[32].y" -1074.2857666015625;
	setAttr ".tgi[6].ni[32].nvs" 18304;
	setAttr ".tgi[6].ni[33].x" 4521.4287109375;
	setAttr ".tgi[6].ni[33].y" -644.28570556640625;
	setAttr ".tgi[6].ni[33].nvs" 18304;
	setAttr ".tgi[6].ni[34].x" 828.5714111328125;
	setAttr ".tgi[6].ni[34].y" -1505.7142333984375;
	setAttr ".tgi[6].ni[34].nvs" 18304;
	setAttr ".tgi[6].ni[35].x" 1750;
	setAttr ".tgi[6].ni[35].y" -1172.857177734375;
	setAttr ".tgi[6].ni[35].nvs" 18304;
	setAttr ".tgi[6].ni[36].x" 5761.4287109375;
	setAttr ".tgi[6].ni[36].y" -1438.5714111328125;
	setAttr ".tgi[6].ni[36].nvs" 18304;
	setAttr ".tgi[6].ni[37].x" 1135.7142333984375;
	setAttr ".tgi[6].ni[37].y" -1210;
	setAttr ".tgi[6].ni[37].nvs" 18304;
	setAttr ".tgi[6].ni[38].x" 5454.28564453125;
	setAttr ".tgi[6].ni[38].y" -805.71429443359375;
	setAttr ".tgi[6].ni[38].nvs" 18304;
	setAttr ".tgi[6].ni[39].x" 7768.5712890625;
	setAttr ".tgi[6].ni[39].y" -1181.4285888671875;
	setAttr ".tgi[6].ni[39].nvs" 18304;
	setAttr ".tgi[6].ni[40].x" 4828.5712890625;
	setAttr ".tgi[6].ni[40].y" -1302.857177734375;
	setAttr ".tgi[6].ni[40].nvs" 18304;
	setAttr ".tgi[6].ni[41].x" 7768.5712890625;
	setAttr ".tgi[6].ni[41].y" -1280;
	setAttr ".tgi[6].ni[41].nvs" 18304;
	setAttr ".tgi[6].ni[42].x" 6410;
	setAttr ".tgi[6].ni[42].y" -1374.2857666015625;
	setAttr ".tgi[6].ni[42].nvs" 18304;
	setAttr ".tgi[6].ni[43].x" 6717.14306640625;
	setAttr ".tgi[6].ni[43].y" -927.14288330078125;
	setAttr ".tgi[6].ni[43].nvs" 18304;
	setAttr ".tgi[6].ni[44].x" 828.5714111328125;
	setAttr ".tgi[6].ni[44].y" -1604.2857666015625;
	setAttr ".tgi[6].ni[44].nvs" 18304;
	setAttr ".tgi[6].ni[45].x" 3907.142822265625;
	setAttr ".tgi[6].ni[45].y" -1404.2857666015625;
	setAttr ".tgi[6].ni[45].nvs" 18304;
	setAttr ".tgi[6].ni[46].x" 6717.14306640625;
	setAttr ".tgi[6].ni[46].y" -828.5714111328125;
	setAttr ".tgi[6].ni[46].nvs" 18304;
	setAttr ".tgi[6].ni[47].x" 5135.71435546875;
	setAttr ".tgi[6].ni[47].y" -1344.2857666015625;
	setAttr ".tgi[6].ni[47].nvs" 18304;
	setAttr ".tgi[6].ni[48].x" 7768.5712890625;
	setAttr ".tgi[6].ni[48].y" -1378.5714111328125;
	setAttr ".tgi[6].ni[48].nvs" 18304;
	setAttr ".tgi[6].ni[49].x" 5454.28564453125;
	setAttr ".tgi[6].ni[49].y" -1368.5714111328125;
	setAttr ".tgi[6].ni[49].nvs" 18304;
	setAttr ".tgi[6].ni[50].x" 6410;
	setAttr ".tgi[6].ni[50].y" -1238.5714111328125;
	setAttr ".tgi[6].ni[50].nvs" 18304;
	setAttr ".tgi[6].ni[51].x" 2371.428466796875;
	setAttr ".tgi[6].ni[51].y" -928.5714111328125;
	setAttr ".tgi[6].ni[51].nvs" 18304;
	setAttr ".tgi[6].ni[52].x" 5135.71435546875;
	setAttr ".tgi[6].ni[52].y" -720;
	setAttr ".tgi[6].ni[52].nvs" 18304;
	setAttr ".tgi[6].ni[53].x" 7768.5712890625;
	setAttr ".tgi[6].ni[53].y" -1495.7142333984375;
	setAttr ".tgi[6].ni[53].nvs" 18304;
	setAttr ".tgi[6].ni[54].x" 1135.7142333984375;
	setAttr ".tgi[6].ni[54].y" -1012.8571166992188;
	setAttr ".tgi[6].ni[54].nvs" 18304;
	setAttr ".tgi[6].ni[55].x" 3600;
	setAttr ".tgi[6].ni[55].y" -1307.142822265625;
	setAttr ".tgi[6].ni[55].nvs" 18304;
	setAttr ".tgi[6].ni[56].x" 5761.4287109375;
	setAttr ".tgi[6].ni[56].y" -842.85711669921875;
	setAttr ".tgi[6].ni[56].nvs" 18304;
	setAttr ".tgi[6].ni[57].x" 3600;
	setAttr ".tgi[6].ni[57].y" -1442.857177734375;
	setAttr ".tgi[6].ni[57].nvs" 18304;
	setAttr ".tgi[6].ni[58].x" 2678.571533203125;
	setAttr ".tgi[6].ni[58].y" -1191.4285888671875;
	setAttr ".tgi[6].ni[58].nvs" 18304;
	setAttr ".tgi[6].ni[59].x" 5761.4287109375;
	setAttr ".tgi[6].ni[59].y" -1302.857177734375;
	setAttr ".tgi[6].ni[59].nvs" 18304;
	setAttr ".tgi[6].ni[60].x" 4828.5712890625;
	setAttr ".tgi[6].ni[60].y" -707.14288330078125;
	setAttr ".tgi[6].ni[60].nvs" 18304;
	setAttr ".tgi[6].ni[61].x" 828.5714111328125;
	setAttr ".tgi[6].ni[61].y" -1210;
	setAttr ".tgi[6].ni[61].nvs" 18304;
	setAttr ".tgi[6].ni[62].x" 7031.4287109375;
	setAttr ".tgi[6].ni[62].y" -1521.4285888671875;
	setAttr ".tgi[6].ni[62].nvs" 18304;
	setAttr ".tgi[6].ni[63].x" 7768.5712890625;
	setAttr ".tgi[6].ni[63].y" -1741.4285888671875;
	setAttr ".tgi[6].ni[63].nvs" 18304;
	setAttr ".tgi[6].ni[64].x" 828.5714111328125;
	setAttr ".tgi[6].ni[64].y" -1407.142822265625;
	setAttr ".tgi[6].ni[64].nvs" 18304;
	setAttr ".tgi[6].ni[65].x" 828.5714111328125;
	setAttr ".tgi[6].ni[65].y" -1111.4285888671875;
	setAttr ".tgi[6].ni[65].nvs" 18304;
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
	setAttr -s 81 ".u";
select -ne :defaultRenderingList1;
	setAttr -s 3 ".r";
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
connectAttr "out1.s" "out2.is";
connectAttr "decomposeMatrix2.ot" "out2.t";
connectAttr "decomposeMatrix2.or" "out2.r";
connectAttr "decomposeMatrix2.os" "out2.s";
connectAttr "out2.s" "out3.is";
connectAttr "decomposeMatrix3.ot" "out3.t";
connectAttr "decomposeMatrix3.or" "out3.r";
connectAttr "decomposeMatrix3.os" "out3.s";
connectAttr "arm_atts_anm_offset_parentConstraint1.ctx" "arm_atts_anm_offset.tx"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.cty" "arm_atts_anm_offset.ty"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.ctz" "arm_atts_anm_offset.tz"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.crx" "arm_atts_anm_offset.rx"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.cry" "arm_atts_anm_offset.ry"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.crz" "arm_atts_anm_offset.rz"
		;
connectAttr "arm_atts_anm_offset.ro" "arm_atts_anm_offset_parentConstraint1.cro"
		;
connectAttr "arm_atts_anm_offset.pim" "arm_atts_anm_offset_parentConstraint1.cpim"
		;
connectAttr "arm_atts_anm_offset.rp" "arm_atts_anm_offset_parentConstraint1.crp"
		;
connectAttr "arm_atts_anm_offset.rpt" "arm_atts_anm_offset_parentConstraint1.crt"
		;
connectAttr "out3.t" "arm_atts_anm_offset_parentConstraint1.tg[0].tt";
connectAttr "out3.rp" "arm_atts_anm_offset_parentConstraint1.tg[0].trp";
connectAttr "out3.rpt" "arm_atts_anm_offset_parentConstraint1.tg[0].trt";
connectAttr "out3.r" "arm_atts_anm_offset_parentConstraint1.tg[0].tr";
connectAttr "out3.ro" "arm_atts_anm_offset_parentConstraint1.tg[0].tro";
connectAttr "out3.s" "arm_atts_anm_offset_parentConstraint1.tg[0].ts";
connectAttr "out3.pm" "arm_atts_anm_offset_parentConstraint1.tg[0].tpm";
connectAttr "out3.jo" "arm_atts_anm_offset_parentConstraint1.tg[0].tjo";
connectAttr "out3.ssc" "arm_atts_anm_offset_parentConstraint1.tg[0].tsc";
connectAttr "out3.is" "arm_atts_anm_offset_parentConstraint1.tg[0].tis";
connectAttr "arm_atts_anm_offset_parentConstraint1.w0" "arm_atts_anm_offset_parentConstraint1.tg[0].tw"
		;
connectAttr "FK3:decomposeMatrix1.ot" "FK3:out1.t";
connectAttr "FK3:decomposeMatrix1.or" "FK3:out1.r";
connectAttr "FK3:decomposeMatrix1.os" "FK3:out1.s";
connectAttr "FK3:out1.s" "FK3:out2.is";
connectAttr "FK3:decomposeMatrix2.ot" "FK3:out2.t";
connectAttr "FK3:decomposeMatrix2.or" "FK3:out2.r";
connectAttr "FK3:decomposeMatrix2.os" "FK3:out2.s";
connectAttr "FK3:out2.s" "FK3:out3.is";
connectAttr "FK3:decomposeMatrix3.ot" "FK3:out3.t";
connectAttr "FK3:decomposeMatrix3.or" "FK3:out3.r";
connectAttr "FK3:decomposeMatrix3.os" "FK3:out3.s";
connectAttr "FK3:decomposeCtrlFk01DefaultLocalTm.ot" "FK3:ctrl1_zero.t";
connectAttr "FK3:decomposeCtrlFk01DefaultLocalTm.or" "FK3:ctrl1_zero.r";
connectAttr "FK3:decomposeCtrlFk01DefaultLocalTm.os" "FK3:ctrl1_zero.s";
connectAttr "FK3:makeNurbCircle2.oc" "FK3:ctrl1Shape.cr";
connectAttr "FK3:decomposeCtrlFk02DefaultLocalTm.ot" "FK3:ctrl2_zero.t";
connectAttr "FK3:decomposeCtrlFk02DefaultLocalTm.or" "FK3:ctrl2_zero.r";
connectAttr "FK3:decomposeCtrlFk02DefaultLocalTm.os" "FK3:ctrl2_zero.s";
connectAttr "FK3:makeNurbCircle3.oc" "FK3:ctrl2.cr";
connectAttr "FK3:decomposeCtrlFk03DefaultLocalTm.ot" "FK3:ctrl3_zero.t";
connectAttr "FK3:decomposeCtrlFk03DefaultLocalTm.or" "FK3:ctrl3_zero.r";
connectAttr "FK3:decomposeCtrlFk03DefaultLocalTm.os" "FK3:ctrl3_zero.s";
connectAttr "FK3:makeNurbCircle4.oc" "FK3:ctrl3Shape.cr";
connectAttr "FK3:guide_02_translateX.o" "FK3:inn2.tx";
connectAttr "FK3:guide_02_translateY.o" "FK3:inn2.ty";
connectAttr "FK3:guide_02_translateZ.o" "FK3:inn2.tz";
connectAttr "FK3:guide_02_visibility.o" "FK3:inn2.v";
connectAttr "FK3:guide_02_rotateX.o" "FK3:inn2.rx";
connectAttr "FK3:guide_02_rotateY.o" "FK3:inn2.ry";
connectAttr "FK3:guide_02_rotateZ.o" "FK3:inn2.rz";
connectAttr "FK3:guide_02_scaleX.o" "FK3:inn2.sx";
connectAttr "FK3:guide_02_scaleY.o" "FK3:inn2.sy";
connectAttr "FK3:guide_02_scaleZ.o" "FK3:inn2.sz";
connectAttr "IK3:decomposeMatrix1.ot" "IK3:out1.t";
connectAttr "IK3:decomposeMatrix1.or" "IK3:out1.r";
connectAttr "IK3:decomposeMatrix1.os" "IK3:out1.s";
connectAttr "IK3:out1.s" "IK3:out2.is";
connectAttr "IK3:decomposeMatrix2.ot" "IK3:out2.t";
connectAttr "IK3:decomposeMatrix2.or" "IK3:out2.r";
connectAttr "IK3:decomposeMatrix2.os" "IK3:out2.s";
connectAttr "IK3:out2.s" "IK3:out3.is";
connectAttr "IK3:decomposeMatrix3.ot" "IK3:out3.t";
connectAttr "IK3:decomposeMatrix3.or" "IK3:out3.r";
connectAttr "IK3:decomposeMatrix3.os" "IK3:out3.s";
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.ctx" "IK3:arm_atts_anm_offset.tx"
		;
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.cty" "IK3:arm_atts_anm_offset.ty"
		;
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.ctz" "IK3:arm_atts_anm_offset.tz"
		;
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.crx" "IK3:arm_atts_anm_offset.rx"
		;
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.cry" "IK3:arm_atts_anm_offset.ry"
		;
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.crz" "IK3:arm_atts_anm_offset.rz"
		;
connectAttr "IK3:arm_atts_anm_offset.ro" "IK3:arm_atts_anm_offset_parentConstraint1.cro"
		;
connectAttr "IK3:arm_atts_anm_offset.pim" "IK3:arm_atts_anm_offset_parentConstraint1.cpim"
		;
connectAttr "IK3:arm_atts_anm_offset.rp" "IK3:arm_atts_anm_offset_parentConstraint1.crp"
		;
connectAttr "IK3:arm_atts_anm_offset.rpt" "IK3:arm_atts_anm_offset_parentConstraint1.crt"
		;
connectAttr "IK3:out3.t" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].tt";
connectAttr "IK3:out3.rp" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].trp";
connectAttr "IK3:out3.rpt" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].trt"
		;
connectAttr "IK3:out3.r" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].tr";
connectAttr "IK3:out3.ro" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].tro";
connectAttr "IK3:out3.s" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].ts";
connectAttr "IK3:out3.pm" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].tpm";
connectAttr "IK3:out3.jo" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].tjo";
connectAttr "IK3:out3.ssc" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].tsc"
		;
connectAttr "IK3:out3.is" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].tis";
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.w0" "IK3:arm_atts_anm_offset_parentConstraint1.tg[0].tw"
		;
connectAttr "IK3:dag.fkIk" "IK3:ik:arm_ik_anm_grp.v";
connectAttr "IK3:decomposeGuide03WorldTm.ot" "IK3:ik:arm_ik_anm_offset.t";
connectAttr "IK3:getSwivelDefaultPos.o3" "IK3:ik:arm_ik_swivel_anm_offset.t";
connectAttr "IK3:makeNurbCircle1.oc" "IK3:ik:arm_ik_swivel_anmShape.cr";
connectAttr "IK3:ik:locator1_pointConstraint1.ctx" "IK3:ik:arm_ik_swivelLineLoc_anm.tx"
		;
connectAttr "IK3:ik:locator1_pointConstraint1.cty" "IK3:ik:arm_ik_swivelLineLoc_anm.ty"
		;
connectAttr "IK3:ik:locator1_pointConstraint1.ctz" "IK3:ik:arm_ik_swivelLineLoc_anm.tz"
		;
connectAttr "IK3:ik:arm_ik_swivelLineLoc_anm.pim" "IK3:ik:locator1_pointConstraint1.cpim"
		;
connectAttr "IK3:ik:arm_ik_swivelLineLoc_anm.rp" "IK3:ik:locator1_pointConstraint1.crp"
		;
connectAttr "IK3:ik:arm_ik_swivelLineLoc_anm.rpt" "IK3:ik:locator1_pointConstraint1.crt"
		;
connectAttr "IK3:out2.t" "IK3:ik:locator1_pointConstraint1.tg[0].tt";
connectAttr "IK3:out2.rp" "IK3:ik:locator1_pointConstraint1.tg[0].trp";
connectAttr "IK3:out2.rpt" "IK3:ik:locator1_pointConstraint1.tg[0].trt";
connectAttr "IK3:out2.pm" "IK3:ik:locator1_pointConstraint1.tg[0].tpm";
connectAttr "IK3:ik:locator1_pointConstraint1.w0" "IK3:ik:locator1_pointConstraint1.tg[0].tw"
		;
connectAttr "IK3:ik:arm_ik_swivelLineLoc_anmShape.wm" "IK3:ik:arm_ik_swivelLineAnn_anm.dom"
		 -na;
connectAttr "IK3:arm_atts_anm.fkIk" "IK3:dag.fkIk";
connectAttr "IK3:decomposeGuide01LocalTm.ot" "IK3:ik:arm_ik_ikChain_rig.t";
connectAttr "IK3:decomposeGuide01LocalTm.or" "IK3:ik:arm_ik_ikChain_rig.r";
connectAttr "IK3:ik:arm_ik_01_rig.msg" "IK3:ik:arm_ik_ikHandle_rig.hsj";
connectAttr "IK3:ik:arm_ik_ikEffector_rig.hp" "IK3:ik:arm_ik_ikHandle_rig.hee";
connectAttr "IK3:ikRPsolver.msg" "IK3:ik:arm_ik_ikHandle_rig.hsv";
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.ctx" "IK3:ik:arm_ik_ikHandle_rig.tx"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.cty" "IK3:ik:arm_ik_ikHandle_rig.ty"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.ctz" "IK3:ik:arm_ik_ikHandle_rig.tz"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.ctx" "IK3:ik:arm_ik_ikHandle_rig.pvx"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.cty" "IK3:ik:arm_ik_ikHandle_rig.pvy"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.ctz" "IK3:ik:arm_ik_ikHandle_rig.pvz"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig.pim" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.cpim"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig.rp" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.crp"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig.rpt" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.crt"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.t" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].tt"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.rp" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].trp"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.rpt" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].trt"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.pm" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].tpm"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.w0" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[0].tw"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.t" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].tt"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.rp" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].trp"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.rpt" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].trt"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.pm" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].tpm"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.w1" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[1].tw"
		;
connectAttr "IK3:ik:arm_ik_anm.t" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].tt"
		;
connectAttr "IK3:ik:arm_ik_anm.rp" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].trp"
		;
connectAttr "IK3:ik:arm_ik_anm.rpt" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].trt"
		;
connectAttr "IK3:ik:arm_ik_anm.pm" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].tpm"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.w2" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.tg[2].tw"
		;
connectAttr "IK3:ik:softik:out.outRatio" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.w0"
		;
connectAttr "IK3:reverse1.ox" "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.w1";
connectAttr "IK3:ik:arm_ik_ikHandle_rig.pim" "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.cpim"
		;
connectAttr "IK3:ik:arm_ik_01_rig.pm" "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.ps"
		;
connectAttr "IK3:ik:arm_ik_01_rig.t" "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.crp"
		;
connectAttr "IK3:ik:arm_ik_swivel_anm.t" "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].tt"
		;
connectAttr "IK3:ik:arm_ik_swivel_anm.rp" "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].trp"
		;
connectAttr "IK3:ik:arm_ik_swivel_anm.rpt" "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].trt"
		;
connectAttr "IK3:ik:arm_ik_swivel_anm.pm" "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].tpm"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.w0" "IK3:ik:arm_ik_ikHandle_rig_poleVectorConstraint1.tg[0].tw"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.ctx" "IK3:ik:arm_ik_ikHandleTarget_rig.tx"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.cty" "IK3:ik:arm_ik_ikHandleTarget_rig.ty"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.ctz" "IK3:ik:arm_ik_ikHandleTarget_rig.tz"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.pim" "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.cpim"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.rp" "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.crp"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.rpt" "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.crt"
		;
connectAttr "IK3:ik:arm_ik_anm.t" "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].tt"
		;
connectAttr "IK3:ik:arm_ik_anm.rp" "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].trp"
		;
connectAttr "IK3:ik:arm_ik_anm.rpt" "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].trt"
		;
connectAttr "IK3:ik:arm_ik_anm.pm" "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].tpm"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.w0" "IK3:ik:arm_ik_ikHandleTarget_rig_pointConstraint1.tg[0].tw"
		;
connectAttr "IK3:multiplyDivide13.o" "IK3:ik:arm_ik_02_rig.t";
connectAttr "IK3:multiplyDivide14.o" "IK3:ik:arm_ik_03_rig.t";
connectAttr "IK3:ik:arm_ik_03_rig_orientConstraint1.crx" "IK3:ik:arm_ik_03_rig.rx"
		;
connectAttr "IK3:ik:arm_ik_03_rig_orientConstraint1.cry" "IK3:ik:arm_ik_03_rig.ry"
		;
connectAttr "IK3:ik:arm_ik_03_rig_orientConstraint1.crz" "IK3:ik:arm_ik_03_rig.rz"
		;
connectAttr "IK3:ik:arm_ik_03_rig.ro" "IK3:ik:arm_ik_03_rig_orientConstraint1.cro"
		;
connectAttr "IK3:ik:arm_ik_03_rig.pim" "IK3:ik:arm_ik_03_rig_orientConstraint1.cpim"
		;
connectAttr "IK3:ik:arm_ik_03_rig.jo" "IK3:ik:arm_ik_03_rig_orientConstraint1.cjo"
		;
connectAttr "IK3:ik:arm_ik_03_rig.is" "IK3:ik:arm_ik_03_rig_orientConstraint1.is"
		;
connectAttr "IK3:ik:arm_ik_anm.r" "IK3:ik:arm_ik_03_rig_orientConstraint1.tg[0].tr"
		;
connectAttr "IK3:ik:arm_ik_anm.ro" "IK3:ik:arm_ik_03_rig_orientConstraint1.tg[0].tro"
		;
connectAttr "IK3:ik:arm_ik_anm.pm" "IK3:ik:arm_ik_03_rig_orientConstraint1.tg[0].tpm"
		;
connectAttr "IK3:ik:arm_ik_03_rig_orientConstraint1.w0" "IK3:ik:arm_ik_03_rig_orientConstraint1.tg[0].tw"
		;
connectAttr "IK3:ik:arm_ik_03_rig.tx" "IK3:ik:arm_ik_ikEffector_rig.tx";
connectAttr "IK3:ik:arm_ik_03_rig.ty" "IK3:ik:arm_ik_ikEffector_rig.ty";
connectAttr "IK3:ik:arm_ik_03_rig.tz" "IK3:ik:arm_ik_ikEffector_rig.tz";
connectAttr "IK3:guide_02_translateX.o" "IK3:inn2.tx";
connectAttr "IK3:guide_02_translateY.o" "IK3:inn2.ty";
connectAttr "IK3:guide_02_translateZ.o" "IK3:inn2.tz";
connectAttr "IK3:guide_02_visibility.o" "IK3:inn2.v";
connectAttr "IK3:guide_02_rotateX.o" "IK3:inn2.rx";
connectAttr "IK3:guide_02_rotateY.o" "IK3:inn2.ry";
connectAttr "IK3:guide_02_rotateZ.o" "IK3:inn2.rz";
connectAttr "IK3:guide_02_scaleX.o" "IK3:inn2.sx";
connectAttr "IK3:guide_02_scaleY.o" "IK3:inn2.sy";
connectAttr "IK3:guide_02_scaleZ.o" "IK3:inn2.sz";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "ik:softik:out.outStretch" "multiplyDivide10.i1x";
connectAttr "ik:softik:out.outStretch" "multiplyDivide10.i1y";
connectAttr "ik:softik:out.outStretch" "multiplyDivide10.i1z";
connectAttr "ik:softik:out.outStretch" "multiplyDivide11.i1x";
connectAttr "ik:softik:out.outStretch" "multiplyDivide11.i1y";
connectAttr "ik:softik:out.outStretch" "multiplyDivide11.i1z";
connectAttr "getLimbLength.o" "ik:softik:inn.inChainLength";
connectAttr "multiplyDivide1.ox" "ik:softik:inn.inRatio";
connectAttr "ik:softik:inn.msg" "ik:softik:metadata.grp_inn";
connectAttr "ik:softik:out.msg" "ik:softik:metadata.grp_out";
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
connectAttr "ik:softik:blendTwoAttr2.o" "ik:softik:out.outStretch";
connectAttr "ik:softik:multiplyDivide7.ox" "ik:softik:out.outRatio";
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
connectAttr "guide_01.m" "inn.Guide01_LocalTm";
connectAttr "guide_02.m" "inn.Guide02_LocalTm";
connectAttr "guide_03.m" "inn.Guide03_LocalTm";
connectAttr "inn.Guide01_LocalTm" "decomposeGuide01LocalTm.imat";
connectAttr "inn.Guide02_LocalTm" "decomposeGuide02LocalTm.imat";
connectAttr "inn.Guide03_LocalTm" "decomposeGuide03LocalTm.imat";
connectAttr "inn.Guide01_LocalTm" "out.CtrlFk01_BaseLocalTm";
connectAttr "inn.Guide02_LocalTm" "out.CtrlFk02_BaseLocalTm";
connectAttr "inn.Guide03_LocalTm" "out.CtrlFk03_BaseLocalTm";
connectAttr "out.CtrlFk01_BaseLocalTm" "decomposeCtrlFk01DefaultLocalTm.imat";
connectAttr "out.CtrlFk02_BaseLocalTm" "decomposeCtrlFk02DefaultLocalTm.imat";
connectAttr "out.CtrlFk03_BaseLocalTm" "decomposeCtrlFk03DefaultLocalTm.imat";
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
connectAttr "getGuide03WorldTm.o" "decomposeGuide03WorldTm.imat";
connectAttr "getLimbLength.o" "getSwivelDistance.i1x";
connectAttr "inn.swivelDistanceRatio" "getSwivelDistance.i2x";
connectAttr "getLimbSegment1Length.d" "getLimbRatio.i1x";
connectAttr "getLimbLength.o" "getLimbRatio.i2x";
connectAttr "decomposeGuide03WorldTm.ot" "getLimbAim.i3[0]";
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
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "arm_atts_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "decomposeGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "arm_elbow01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn"
		;
connectAttr "getKneeDirection.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn"
		;
connectAttr "getLimbAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn";
connectAttr "getKneeDirectionOffset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn"
		;
connectAttr "getKneeDirectionNormalized.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[22].dn"
		;
connectAttr "decomposeGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[23].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn";
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[26].dn";
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[27].dn";
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[28].dn"
		;
connectAttr "getSwivelDefaultPos.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[30].dn"
		;
connectAttr "out3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[31].dn";
connectAttr "out2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[32].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[34].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[35].dn";
connectAttr "getGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[36].dn"
		;
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[38].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[40].dn"
		;
connectAttr "getKneePosProjectedOnLimbDir.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[41].dn"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[42].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[43].dn"
		;
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[44].dn";
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[46].dn";
connectAttr "getLimbMiddleAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[47].dn"
		;
connectAttr "out2.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[0].dn";
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[2].dn"
		;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[3].dn"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[4].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[5].dn";
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[7].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[8].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[9].dn"
		;
connectAttr "arm_atts_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[10].dn"
		;
connectAttr "out3.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[12].dn";
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[13].dn"
		;
connectAttr "arm_elbow01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[14].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[15].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[17].dn";
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[18].dn";
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[19].dn";
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[20].dn"
		;
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[21].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[22].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[23].dn";
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[25].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[27].dn";
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[0].dn"
		;
connectAttr "ik:softik:distanceBetween1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[1].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[2].dn"
		;
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[3].dn"
		;
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[4].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[5].dn"
		;
connectAttr "ik:softik:multiplyDivide6.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[6].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[7].dn"
		;
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[8].dn"
		;
connectAttr "ik:softik:multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[9].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[10].dn"
		;
connectAttr "ik:softik:blendTwoAttr1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[11].dn"
		;
connectAttr "ik:softik:blendTwoAttr2.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[12].dn"
		;
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[13].dn"
		;
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[14].dn";
connectAttr "ik:softik:condition1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[15].dn"
		;
connectAttr "ik:softik:metadata.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[16].dn"
		;
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[17].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[18].dn";
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[19].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[0].dn"
		;
connectAttr "ik:softik:multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[1].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[2].dn";
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[3].dn"
		;
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[4].dn"
		;
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[5].dn";
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[6].dn";
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[8].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[9].dn"
		;
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[10].dn"
		;
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[12].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[13].dn"
		;
connectAttr "ik:softik:distanceBetween1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[14].dn"
		;
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[15].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[16].dn"
		;
connectAttr "multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[17].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[18].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[19].dn"
		;
connectAttr "ik:softik:blendTwoAttr1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[20].dn"
		;
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[22].dn"
		;
connectAttr "ik:softik:condition1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[23].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[24].dn"
		;
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[28].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[29].dn";
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[30].dn";
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[31].dn";
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[32].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[0].dn";
connectAttr "multiplyDivide11.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[2].dn"
		;
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[3].dn"
		;
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[4].dn"
		;
connectAttr "ik:softik:condition1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[7].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[9].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[10].dn"
		;
connectAttr "ik:softik:blendTwoAttr2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[11].dn"
		;
connectAttr "arm_elbow01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[13].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[14].dn"
		;
connectAttr "multiplyDivide10.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[17].dn"
		;
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[18].dn";
connectAttr "ik:softik:multiplyDivide6.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[19].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[22].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[23].dn"
		;
connectAttr "ik:softik:distanceBetween1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[24].dn"
		;
connectAttr "multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[25].dn"
		;
connectAttr "arm_atts_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[27].dn"
		;
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[30].dn"
		;
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[31].dn";
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[32].dn";
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[33].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[34].dn"
		;
connectAttr "ik:softik:blendTwoAttr1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[35].dn"
		;
connectAttr "out3.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[37].dn";
connectAttr "out2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[38].dn";
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[39].dn"
		;
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[40].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[41].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[42].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[43].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[45].dn"
		;
connectAttr "ik:softik:multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[47].dn"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[48].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[49].dn";
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[50].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[52].dn";
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[53].dn"
		;
connectAttr "ik:softik:metadata.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[54].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[56].dn"
		;
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[59].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[0].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[1].dn"
		;
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[3].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[5].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[6].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[7].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[8].dn";
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[9].dn"
		;
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[10].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[11].dn"
		;
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[14].dn"
		;
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[15].dn";
connectAttr ":defaultRenderUtilityList1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[16].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[17].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[18].dn";
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[19].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[20].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[21].dn";
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[22].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[24].dn";
connectAttr "decomposeGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[26].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[28].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[29].dn"
		;
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[30].dn";
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[32].dn";
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[33].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[34].dn"
		;
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[37].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[38].dn";
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[0].dn"
		;
connectAttr "ik:softik:blendTwoAttr1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[1].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[2].dn"
		;
connectAttr "getKneePosProjectedOnLimbDir.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[4].dn"
		;
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[5].dn"
		;
connectAttr "getKneeDirectionOffset.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[6].dn"
		;
connectAttr "multiplyDivide10.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[7].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[8].dn";
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[9].dn"
		;
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[13].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[14].dn"
		;
connectAttr "getSwivelDefaultPos.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[15].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[16].dn"
		;
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[18].dn";
connectAttr "decomposeGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[20].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[21].dn"
		;
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[23].dn"
		;
connectAttr "getKneeDirection.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[25].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[26].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[27].dn"
		;
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[28].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[29].dn";
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[31].dn";
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[32].dn"
		;
connectAttr "getGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[33].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[35].dn"
		;
connectAttr "ik:softik:condition1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[36].dn"
		;
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[37].dn";
connectAttr "getLimbAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[38].dn";
connectAttr "multiplyDivide11.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[39].dn"
		;
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[40].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[41].dn"
		;
connectAttr "ik:softik:multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[42].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[43].dn"
		;
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[45].dn"
		;
connectAttr "getKneeDirectionNormalized.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[46].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[47].dn"
		;
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[49].dn"
		;
connectAttr "ik:softik:blendTwoAttr2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[50].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[51].dn";
connectAttr "decomposeGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[52].dn"
		;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[53].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[54].dn";
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[55].dn"
		;
connectAttr "getLimbMiddleAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[56].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[57].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[58].dn";
connectAttr "ik:softik:multiplyDivide6.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[59].dn"
		;
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[60].dn"
		;
connectAttr "FK3:renderLayerManager.rlmi[0]" "FK3:defaultRenderLayer.rlid";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide10.i1x";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide10.i1y";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide10.i1z";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide11.i1x";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide11.i1y";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide11.i1z";
connectAttr "FK3:getLimbLength.o" "FK3:ik:softik:inn.inChainLength";
connectAttr "FK3:multiplyDivide1.ox" "FK3:ik:softik:inn.inRatio";
connectAttr "FK3:ik:softik:inn.msg" "FK3:ik:softik:metadata.grp_inn";
connectAttr "FK3:ik:softik:out.msg" "FK3:ik:softik:metadata.grp_out";
connectAttr "FK3:ik:softik:multiplyDivide3.ox" "FK3:ik:softik:multiplyDivide4.i2x"
		;
connectAttr "FK3:ik:softik:multiplyDivide2.ox" "FK3:ik:softik:multiplyDivide3.i1x"
		;
connectAttr "FK3:ik:softik:multiplyDivide5.ox" "FK3:ik:softik:plusMinusAverage4.i1[0]"
		;
connectAttr "FK3:ik:softik:plusMinusAverage1.o1" "FK3:ik:softik:plusMinusAverage4.i1[1]"
		;
connectAttr "FK3:ik:softik:inn.inMatrixE" "FK3:ik:softik:distanceBetween1.im2";
connectAttr "FK3:ik:softik:inn.inMatrixS" "FK3:ik:softik:distanceBetween1.im1";
connectAttr "FK3:ik:softik:plusMinusAverage1.o1" "FK3:ik:softik:condition2.st";
connectAttr "FK3:ik:softik:multiplyDivide6.ox" "FK3:ik:softik:condition2.ctr";
connectAttr "FK3:ik:softik:distanceBetween1.d" "FK3:ik:softik:condition2.ft";
connectAttr "FK3:ik:softik:multiplyDivide1.ox" "FK3:ik:softik:clamp1.ipr";
connectAttr "FK3:ik:softik:multiplyDivide4.ox" "FK3:ik:softik:plusMinusAverage3.i1[1]"
		;
connectAttr "FK3:ik:softik:inn.inStretch" "FK3:ik:softik:blendTwoAttr2.ab";
connectAttr "FK3:ik:softik:condition2.ocr" "FK3:ik:softik:blendTwoAttr2.i[1]";
connectAttr "FK3:ik:softik:multiplyDivide1.ox" "FK3:ik:softik:multiplyDivide5.i1x"
		;
connectAttr "FK3:ik:softik:plusMinusAverage3.o1" "FK3:ik:softik:multiplyDivide5.i2x"
		;
connectAttr "FK3:ik:softik:blendTwoAttr2.o" "FK3:ik:softik:out.outStretch";
connectAttr "FK3:ik:softik:multiplyDivide7.ox" "FK3:ik:softik:out.outRatio";
connectAttr "FK3:ik:softik:inn.inChainLength" "FK3:ik:softik:multiplyDivide1.i1x"
		;
connectAttr "FK3:ik:softik:inn.inRatio" "FK3:ik:softik:multiplyDivide1.i2x";
connectAttr "FK3:ik:softik:inn.inChainLength" "FK3:ik:softik:plusMinusAverage1.i1[0]"
		;
connectAttr "FK3:ik:softik:multiplyDivide1.ox" "FK3:ik:softik:plusMinusAverage1.i1[1]"
		;
connectAttr "FK3:ik:softik:plusMinusAverage4.o1" "FK3:ik:softik:condition1.ctr";
connectAttr "FK3:ik:softik:distanceBetween1.d" "FK3:ik:softik:condition1.cfr";
connectAttr "FK3:ik:softik:multiplyDivide2.ox" "FK3:ik:softik:condition1.ft";
connectAttr "FK3:ik:softik:plusMinusAverage2.o1" "FK3:ik:softik:multiplyDivide2.i1x"
		;
connectAttr "FK3:ik:softik:clamp1.opr" "FK3:ik:softik:multiplyDivide2.i2x";
connectAttr "FK3:ik:softik:blendTwoAttr1.o" "FK3:ik:softik:multiplyDivide7.i1x";
connectAttr "FK3:ik:softik:distanceBetween1.d" "FK3:ik:softik:multiplyDivide7.i2x"
		;
connectAttr "FK3:ik:softik:distanceBetween1.d" "FK3:ik:softik:plusMinusAverage2.i1[0]"
		;
connectAttr "FK3:ik:softik:plusMinusAverage1.o1" "FK3:ik:softik:plusMinusAverage2.i1[1]"
		;
connectAttr "FK3:ik:softik:inn.inStretch" "FK3:ik:softik:blendTwoAttr1.ab";
connectAttr "FK3:ik:softik:condition1.ocr" "FK3:ik:softik:blendTwoAttr1.i[0]";
connectAttr "FK3:ik:softik:distanceBetween1.d" "FK3:ik:softik:blendTwoAttr1.i[1]"
		;
connectAttr "FK3:ik:softik:distanceBetween1.d" "FK3:ik:softik:multiplyDivide6.i1x"
		;
connectAttr "FK3:ik:softik:plusMinusAverage4.o1" "FK3:ik:softik:multiplyDivide6.i2x"
		;
connectAttr "FK3:inn1.m" "FK3:inn.Guide01_LocalTm";
connectAttr "FK3:inn2.m" "FK3:inn.Guide02_LocalTm";
connectAttr "FK3:inn3.m" "FK3:inn.Guide03_LocalTm";
connectAttr "FK3:inn.Guide01_LocalTm" "FK3:decomposeGuide01LocalTm.imat";
connectAttr "FK3:inn.Guide02_LocalTm" "FK3:decomposeGuide02LocalTm.imat";
connectAttr "FK3:inn.Guide03_LocalTm" "FK3:decomposeGuide03LocalTm.imat";
connectAttr "FK3:inn.Guide01_LocalTm" "FK3:out.CtrlFk01_BaseLocalTm";
connectAttr "FK3:inn.Guide02_LocalTm" "FK3:out.CtrlFk02_BaseLocalTm";
connectAttr "FK3:inn.Guide03_LocalTm" "FK3:out.CtrlFk03_BaseLocalTm";
connectAttr "FK3:out.CtrlFk01_BaseLocalTm" "FK3:decomposeCtrlFk01DefaultLocalTm.imat"
		;
connectAttr "FK3:out.CtrlFk02_BaseLocalTm" "FK3:decomposeCtrlFk02DefaultLocalTm.imat"
		;
connectAttr "FK3:out.CtrlFk03_BaseLocalTm" "FK3:decomposeCtrlFk03DefaultLocalTm.imat"
		;
connectAttr "FK3:decomposeGuide02LocalTm.ot" "FK3:getLimbSegment1Length.p2";
connectAttr "FK3:decomposeGuide03LocalTm.ot" "FK3:getLimbSegment2Length.p2";
connectAttr "FK3:getLimbSegment1Length.d" "FK3:getLimbLength.i1";
connectAttr "FK3:getLimbSegment2Length.d" "FK3:getLimbLength.i2";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide13.i2x";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide13.i2y";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide13.i2z";
connectAttr "FK3:decomposeGuide02LocalTm.ot" "FK3:multiplyDivide13.i1";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide14.i2x";
connectAttr "FK3:ik:softik:out.outStretch" "FK3:multiplyDivide14.i2y";
connectAttr "FK3:decomposeGuide03LocalTm.ot" "FK3:multiplyDivide14.i1";
connectAttr "FK3:inn.Guide03_LocalTm" "FK3:getGuide03WorldTm.i[0]";
connectAttr "FK3:getGuide02WorldTm.o" "FK3:getGuide03WorldTm.i[1]";
connectAttr "FK3:getGuide03WorldTm.o" "FK3:decomposeGuide03WorldTm.imat";
connectAttr "FK3:getLimbLength.o" "FK3:getSwivelDistance.i1x";
connectAttr "FK3:inn.swivelDistanceRatio" "FK3:getSwivelDistance.i2x";
connectAttr "FK3:getLimbSegment1Length.d" "FK3:getLimbRatio.i1x";
connectAttr "FK3:getLimbLength.o" "FK3:getLimbRatio.i2x";
connectAttr "FK3:decomposeGuide03WorldTm.ot" "FK3:getLimbAim.i3[0]";
connectAttr "FK3:decomposeGuide01LocalTm.ot" "FK3:getLimbAim.i3[1]";
connectAttr "FK3:getLimbRatio.ox" "FK3:getLimbMiddleAim.i2x";
connectAttr "FK3:getLimbRatio.ox" "FK3:getLimbMiddleAim.i2y";
connectAttr "FK3:getLimbRatio.ox" "FK3:getLimbMiddleAim.i2z";
connectAttr "FK3:getLimbAim.o3" "FK3:getLimbMiddleAim.i1";
connectAttr "FK3:decomposeGuide01LocalTm.ot" "FK3:getKneePosProjectedOnLimbDir.i3[0]"
		;
connectAttr "FK3:getLimbMiddleAim.o" "FK3:getKneePosProjectedOnLimbDir.i3[1]";
connectAttr "FK3:decomposeGuide02WorldTm.ot" "FK3:getKneeDirection.i3[0]";
connectAttr "FK3:getKneePosProjectedOnLimbDir.o3" "FK3:getKneeDirection.i3[1]";
connectAttr "FK3:inn.Guide02_LocalTm" "FK3:getGuide02WorldTm.i[0]";
connectAttr "FK3:inn.Guide01_LocalTm" "FK3:getGuide02WorldTm.i[1]";
connectAttr "FK3:getGuide02WorldTm.o" "FK3:decomposeGuide02WorldTm.imat";
connectAttr "FK3:getKneeDirection.o3" "FK3:getKneeDirectionNormalized.i1";
connectAttr "FK3:getKneeDirectionNormalized.o" "FK3:getKneeDirectionOffset.i1";
connectAttr "FK3:getSwivelDistance.ox" "FK3:getKneeDirectionOffset.i2x";
connectAttr "FK3:getSwivelDistance.ox" "FK3:getKneeDirectionOffset.i2y";
connectAttr "FK3:getSwivelDistance.ox" "FK3:getKneeDirectionOffset.i2z";
connectAttr "FK3:decomposeGuide02WorldTm.ot" "FK3:getSwivelDefaultPos.i3[0]";
connectAttr "FK3:getKneeDirectionOffset.o" "FK3:getSwivelDefaultPos.i3[1]";
connectAttr "FK3:out.outInf01LocalTm" "FK3:decomposeMatrix1.imat";
connectAttr "FK3:out.outInf02LocalTm" "FK3:decomposeMatrix2.imat";
connectAttr "FK3:out.outInf03LocalTm" "FK3:decomposeMatrix3.imat";
connectAttr "FK3:out3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "FK3:getLimbRatio.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "FK3:getLimbAim.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "FK3:guide_02_translateY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "FK3:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn";
connectAttr "FK3:guide_02_translateZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "FK3:decomposeGuide02WorldTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "FK3:decomposeGuide03WorldTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "FK3:guide_02_scaleZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "FK3:inn3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn";
connectAttr "FK3:inn1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn";
connectAttr "FK3:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn";
connectAttr "FK3:getKneeDirection.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "FK3:getLimbSegment1Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn"
		;
connectAttr "FK3:decomposeCtrlFk01DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn"
		;
connectAttr "FK3:multiplyDivide13.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "FK3:getKneePosProjectedOnLimbDir.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn"
		;
connectAttr "FK3:guide_02_rotateY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[22].dn"
		;
connectAttr "FK3:getLimbSegment2Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[24].dn"
		;
connectAttr "FK3:ctrl1_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn"
		;
connectAttr "FK3:getGuide03WorldTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[26].dn"
		;
connectAttr "FK3:multiplyDivide14.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[28].dn"
		;
connectAttr "FK3:decomposeGuide02LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[29].dn"
		;
connectAttr "FK3:ctrl2_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[30].dn"
		;
connectAttr "FK3:inn2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[31].dn";
connectAttr "FK3:getKneeDirectionNormalized.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[32].dn"
		;
connectAttr "FK3:getLimbLength.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[33].dn"
		;
connectAttr "FK3:guide_02_scaleY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[34].dn"
		;
connectAttr "FK3:decomposeCtrlFk02DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[36].dn"
		;
connectAttr "FK3:decomposeCtrlFk03DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[37].dn"
		;
connectAttr "FK3:getGuide02WorldTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[38].dn"
		;
connectAttr "FK3:ctrl3_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[40].dn"
		;
connectAttr "FK3:decomposeGuide01LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[42].dn"
		;
connectAttr "FK3:guide_02_scaleX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[44].dn"
		;
connectAttr "FK3:guide_02_translateX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[46].dn"
		;
connectAttr "FK3:getKneeDirectionOffset.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[47].dn"
		;
connectAttr "FK3:decomposeGuide03LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[48].dn"
		;
connectAttr "FK3:getLimbMiddleAim.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[49].dn"
		;
connectAttr "FK3:out2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[50].dn";
connectAttr "FK3:getSwivelDefaultPos.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[53].dn"
		;
connectAttr "FK3:guide_02_rotateZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[54].dn"
		;
connectAttr "FK3:getSwivelDistance.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[60].dn"
		;
connectAttr "FK3:guide_02_rotateX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[62].dn"
		;
connectAttr "FK3:multiplyDivide14.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[1].dn"
		;
connectAttr "FK3:out3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[2].dn";
connectAttr "FK3:ctrl2_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[3].dn"
		;
connectAttr "FK3:ik:softik:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[4].dn"
		;
connectAttr "FK3:inn1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[6].dn";
connectAttr "FK3:decomposeGuide02LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[7].dn"
		;
connectAttr "FK3:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[9].dn";
connectAttr "FK3:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[10].dn";
connectAttr "FK3:inn3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[13].dn";
connectAttr "FK3:getLimbSegment1Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[14].dn"
		;
connectAttr "FK3:getLimbSegment2Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[15].dn"
		;
connectAttr "FK3:ctrl1_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[16].dn"
		;
connectAttr "FK3:multiplyDivide13.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[17].dn"
		;
connectAttr "FK3:decomposeCtrlFk01DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[20].dn"
		;
connectAttr "FK3:inn2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[21].dn";
connectAttr "FK3:getLimbLength.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[22].dn"
		;
connectAttr "FK3:ctrl3_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[24].dn"
		;
connectAttr "FK3:decomposeCtrlFk03DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[26].dn"
		;
connectAttr "FK3:decomposeCtrlFk02DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[27].dn"
		;
connectAttr "FK3:decomposeGuide01LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[29].dn"
		;
connectAttr "FK3:decomposeGuide03LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[32].dn"
		;
connectAttr "FK3:out2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[33].dn";
connectAttr "FK3:ik:softik:metadata.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[0].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[1].dn"
		;
connectAttr "FK3:ik:softik:blendTwoAttr2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[2].dn"
		;
connectAttr "FK3:ik:softik:distanceBetween1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[3].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[4].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[5].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[6].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[7].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[8].dn"
		;
connectAttr "FK3:ik:softik:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[9].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide7.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[10].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[11].dn"
		;
connectAttr "FK3:ik:softik:blendTwoAttr1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[12].dn"
		;
connectAttr "FK3:ik:softik:condition1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[13].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[14].dn"
		;
connectAttr "FK3:ik:softik:condition2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[15].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide6.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[16].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide5.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[17].dn"
		;
connectAttr "FK3:ik:softik:clamp1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[18].dn"
		;
connectAttr "FK3:ik:softik:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[19].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[0].dn"
		;
connectAttr "FK3:multiplyDivide1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[2].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[3].dn"
		;
connectAttr "FK3:ik:softik:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[4].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide7.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[5].dn"
		;
connectAttr "FK3:decomposeGuide01LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[6].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[8].dn"
		;
connectAttr "FK3:decomposeGuide03LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[9].dn"
		;
connectAttr "FK3:getLimbSegment2Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[10].dn"
		;
connectAttr "FK3:getLimbLength.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[11].dn"
		;
connectAttr "FK3:inn2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[12].dn";
connectAttr "FK3:ik:softik:multiplyDivide2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[13].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[14].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[16].dn"
		;
connectAttr "FK3:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[17].dn";
connectAttr "FK3:ik:softik:distanceBetween1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[18].dn"
		;
connectAttr "FK3:getLimbSegment1Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[21].dn"
		;
connectAttr "FK3:inn3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[22].dn";
connectAttr "FK3:ik:softik:plusMinusAverage4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[23].dn"
		;
connectAttr "FK3:ik:softik:blendTwoAttr1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[25].dn"
		;
connectAttr "FK3:ik:softik:condition1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[26].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[27].dn"
		;
connectAttr "FK3:decomposeGuide02LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[28].dn"
		;
connectAttr "FK3:inn1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[29].dn";
connectAttr "FK3:ik:softik:clamp1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[30].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide5.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[31].dn"
		;
connectAttr "FK3:ik:softik:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[32].dn"
		;
connectAttr "FK3:getLimbLength.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[3].dn"
		;
connectAttr "FK3:out2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[4].dn";
connectAttr "FK3:getLimbSegment1Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[5].dn"
		;
connectAttr "FK3:guide_02_rotateX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[7].dn"
		;
connectAttr "FK3:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[8].dn";
connectAttr "FK3:ik:softik:distanceBetween1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[9].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide5.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[10].dn"
		;
connectAttr "FK3:guide_02_scaleX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[12].dn"
		;
connectAttr "FK3:guide_02_translateZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[13].dn"
		;
connectAttr "FK3:guide_02_rotateY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[14].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[15].dn"
		;
connectAttr "FK3:multiplyDivide10.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[16].dn"
		;
connectAttr "FK3:getSwivelDistance.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[17].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide6.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[18].dn"
		;
connectAttr "FK3:inn3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[19].dn";
connectAttr "FK3:ik:softik:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[20].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[21].dn"
		;
connectAttr "FK3:multiplyDivide13.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[23].dn"
		;
connectAttr "FK3:multiplyDivide14.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[26].dn"
		;
connectAttr "FK3:guide_02_scaleY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[28].dn"
		;
connectAttr "FK3:ik:softik:metadata.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[29].dn"
		;
connectAttr "FK3:ik:softik:condition1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[30].dn"
		;
connectAttr "FK3:ik:softik:clamp1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[34].dn"
		;
connectAttr "FK3:inn2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[35].dn";
connectAttr "FK3:ik:softik:blendTwoAttr1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[38].dn"
		;
connectAttr "FK3:out3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[39].dn";
connectAttr "FK3:guide_02_scaleZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[40].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[41].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[42].dn"
		;
connectAttr "FK3:guide_02_rotateZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[43].dn"
		;
connectAttr "FK3:inn1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[44].dn";
connectAttr "FK3:ik:softik:plusMinusAverage2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[46].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[47].dn"
		;
connectAttr "FK3:guide_02_translateY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[48].dn"
		;
connectAttr "FK3:decomposeGuide03LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[49].dn"
		;
connectAttr "FK3:ik:softik:blendTwoAttr2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[50].dn"
		;
connectAttr "FK3:multiplyDivide1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[51].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[52].dn"
		;
connectAttr "FK3:multiplyDivide11.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[55].dn"
		;
connectAttr "FK3:decomposeGuide02LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[56].dn"
		;
connectAttr "FK3:guide_02_translateX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[58].dn"
		;
connectAttr "FK3:ik:softik:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[60].dn"
		;
connectAttr "FK3:getLimbSegment2Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[61].dn"
		;
connectAttr "FK3:decomposeGuide01LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[63].dn"
		;
connectAttr "FK3:ik:softik:condition2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[64].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide7.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[66].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[68].dn"
		;
connectAttr "FK3:multiplyDivide14.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[0].dn"
		;
connectAttr "FK3:getLimbSegment1Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[1].dn"
		;
connectAttr "FK3:guide_02_translateZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[2].dn"
		;
connectAttr "FK3:inn1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[3].dn";
connectAttr "FK3:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[4].dn";
connectAttr "FK3:guide_02_scaleZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[5].dn"
		;
connectAttr "FK3:getGuide03WorldTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[6].dn"
		;
connectAttr "FK3:decomposeGuide02LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[7].dn"
		;
connectAttr "FK3:decomposeCtrlFk03DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[8].dn"
		;
connectAttr "FK3:ik:softik:clamp1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[9].dn"
		;
connectAttr "FK3:getLimbSegment2Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[10].dn"
		;
connectAttr "FK3:ctrl2_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[11].dn"
		;
connectAttr "FK3:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[12].dn";
connectAttr "FK3:ctrl1_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[13].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[14].dn"
		;
connectAttr "FK3:inn3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[15].dn";
connectAttr "FK3:getLimbRatio.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[16].dn"
		;
connectAttr "FK3:decomposeGuide03WorldTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[17].dn"
		;
connectAttr "FK3:multiplyDivide13.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[18].dn"
		;
connectAttr "FK3:guide_02_translateY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[19].dn"
		;
connectAttr "FK3:guide_02_rotateY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[20].dn"
		;
connectAttr "FK3:decomposeCtrlFk01DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[21].dn"
		;
connectAttr "FK3:inn2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[22].dn";
connectAttr "FK3:getLimbLength.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[23].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[24].dn"
		;
connectAttr "FK3:ctrl3_zero.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[25].dn"
		;
connectAttr "FK3:guide_02_scaleY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[26].dn"
		;
connectAttr "FK3:decomposeCtrlFk02DefaultLocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[27].dn"
		;
connectAttr "FK3:decomposeGuide01LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[28].dn"
		;
connectAttr ":defaultRenderUtilityList1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[29].dn"
		;
connectAttr "FK3:guide_02_scaleX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[30].dn"
		;
connectAttr "FK3:guide_02_translateX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[31].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[32].dn"
		;
connectAttr "FK3:decomposeGuide03LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[33].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[34].dn"
		;
connectAttr "FK3:ik:softik:condition2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[35].dn"
		;
connectAttr "FK3:guide_02_rotateZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[36].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide5.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[38].dn"
		;
connectAttr "FK3:getSwivelDistance.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[39].dn"
		;
connectAttr "FK3:guide_02_rotateX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[40].dn"
		;
connectAttr "FK3:ik:softik:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[41].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide5.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[1].dn"
		;
connectAttr "FK3:getLimbLength.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[2].dn"
		;
connectAttr "FK3:guide_02_scaleZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[4].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[5].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[6].dn"
		;
connectAttr "FK3:guide_02_rotateZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[7].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[8].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage4.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[9].dn"
		;
connectAttr "FK3:getLimbSegment1Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[10].dn"
		;
connectAttr "FK3:guide_02_rotateX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[12].dn"
		;
connectAttr "FK3:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[13].dn";
connectAttr "FK3:out1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[14].dn";
connectAttr "FK3:ctrl1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[17].dn";
connectAttr "FK3:ik:softik:distanceBetween1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[18].dn"
		;
connectAttr "FK3:decomposeGuide02LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[19].dn"
		;
connectAttr "FK3:guide_02_translateX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[20].dn"
		;
connectAttr "FK3:ik:softik:inn.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[22].dn"
		;
connectAttr "FK3:getLimbSegment2Length.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[23].dn"
		;
connectAttr "FK3:ik:softik:condition2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[25].dn"
		;
connectAttr "FK3:inn3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[28].dn";
connectAttr "FK3:ik:softik:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[29].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[30].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[36].dn"
		;
connectAttr "FK3:multiplyDivide14.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[37].dn"
		;
connectAttr "FK3:guide_02_scaleY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[39].dn"
		;
connectAttr "FK3:guide_02_translateY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[41].dn"
		;
connectAttr "FK3:decomposeGuide03LocalTm.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[42].dn"
		;
connectAttr "FK3:ik:softik:blendTwoAttr2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[43].dn"
		;
connectAttr "FK3:ctrl3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[44].dn";
connectAttr "FK3:multiplyDivide1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[45].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[46].dn"
		;
connectAttr "FK3:guide_02_scaleX.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[51].dn"
		;
connectAttr "FK3:guide_02_translateZ.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[52].dn"
		;
connectAttr "FK3:guide_02_rotateY.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[53].dn"
		;
connectAttr "FK3:ik:softik:plusMinusAverage1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[54].dn"
		;
connectAttr "FK3:ik:softik:multiplyDivide6.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[55].dn"
		;
connectAttr "FK3:ik:softik:clamp1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[58].dn"
		;
connectAttr "FK3:out2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[59].dn";
connectAttr "FK3:inn2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[60].dn";
connectAttr "FK3:out3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[63].dn";
connectAttr "FK3:out.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[65].dn";
connectAttr "FK3:decomposeMatrix2.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[66].dn"
		;
connectAttr "FK3:decomposeMatrix3.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[67].dn"
		;
connectAttr "FK3:decomposeMatrix1.msg" "FK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[68].dn"
		;
connectAttr "IK3:renderLayerManager.rlmi[0]" "IK3:defaultRenderLayer.rlid";
connectAttr "IK3:ik:arm_ik_anm.softIkRatio" "IK3:multiplyDivide1.i1x";
connectAttr "IK3:ik:softik:out.outRatio" "IK3:reverse1.ix";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide10.i1x";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide10.i1y";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide10.i1z";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide11.i1x";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide11.i1y";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide11.i1z";
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.wm" "IK3:ik:softik:inn.inMatrixE";
connectAttr "IK3:ik:arm_ik_ikChain_rig.wm" "IK3:ik:softik:inn.inMatrixS";
connectAttr "IK3:ik:arm_ik_anm.stretch" "IK3:ik:softik:inn.inStretch";
connectAttr "IK3:getLimbLength.o" "IK3:ik:softik:inn.inChainLength";
connectAttr "IK3:multiplyDivide1.ox" "IK3:ik:softik:inn.inRatio";
connectAttr "IK3:ik:softik:inn.msg" "IK3:ik:softik:metadata.grp_inn";
connectAttr "IK3:ik:softik:out.msg" "IK3:ik:softik:metadata.grp_out";
connectAttr "IK3:ik:softik:multiplyDivide3.ox" "IK3:ik:softik:multiplyDivide4.i2x"
		;
connectAttr "IK3:ik:softik:multiplyDivide2.ox" "IK3:ik:softik:multiplyDivide3.i1x"
		;
connectAttr "IK3:ik:softik:multiplyDivide5.ox" "IK3:ik:softik:plusMinusAverage4.i1[0]"
		;
connectAttr "IK3:ik:softik:plusMinusAverage1.o1" "IK3:ik:softik:plusMinusAverage4.i1[1]"
		;
connectAttr "IK3:ik:softik:inn.inMatrixE" "IK3:ik:softik:distanceBetween1.im2";
connectAttr "IK3:ik:softik:inn.inMatrixS" "IK3:ik:softik:distanceBetween1.im1";
connectAttr "IK3:ik:softik:plusMinusAverage1.o1" "IK3:ik:softik:condition2.st";
connectAttr "IK3:ik:softik:multiplyDivide6.ox" "IK3:ik:softik:condition2.ctr";
connectAttr "IK3:ik:softik:distanceBetween1.d" "IK3:ik:softik:condition2.ft";
connectAttr "IK3:ik:softik:multiplyDivide1.ox" "IK3:ik:softik:clamp1.ipr";
connectAttr "IK3:ik:softik:multiplyDivide4.ox" "IK3:ik:softik:plusMinusAverage3.i1[1]"
		;
connectAttr "IK3:ik:softik:inn.inStretch" "IK3:ik:softik:blendTwoAttr2.ab";
connectAttr "IK3:ik:softik:condition2.ocr" "IK3:ik:softik:blendTwoAttr2.i[1]";
connectAttr "IK3:ik:softik:multiplyDivide1.ox" "IK3:ik:softik:multiplyDivide5.i1x"
		;
connectAttr "IK3:ik:softik:plusMinusAverage3.o1" "IK3:ik:softik:multiplyDivide5.i2x"
		;
connectAttr "IK3:ik:softik:multiplyDivide7.ox" "IK3:ik:softik:out.outRatio";
connectAttr "IK3:ik:softik:blendTwoAttr2.o" "IK3:ik:softik:out.outStretch";
connectAttr "IK3:ik:softik:inn.inChainLength" "IK3:ik:softik:multiplyDivide1.i1x"
		;
connectAttr "IK3:ik:softik:inn.inRatio" "IK3:ik:softik:multiplyDivide1.i2x";
connectAttr "IK3:ik:softik:inn.inChainLength" "IK3:ik:softik:plusMinusAverage1.i1[0]"
		;
connectAttr "IK3:ik:softik:multiplyDivide1.ox" "IK3:ik:softik:plusMinusAverage1.i1[1]"
		;
connectAttr "IK3:ik:softik:plusMinusAverage4.o1" "IK3:ik:softik:condition1.ctr";
connectAttr "IK3:ik:softik:distanceBetween1.d" "IK3:ik:softik:condition1.cfr";
connectAttr "IK3:ik:softik:multiplyDivide2.ox" "IK3:ik:softik:condition1.ft";
connectAttr "IK3:ik:softik:plusMinusAverage2.o1" "IK3:ik:softik:multiplyDivide2.i1x"
		;
connectAttr "IK3:ik:softik:clamp1.opr" "IK3:ik:softik:multiplyDivide2.i2x";
connectAttr "IK3:ik:softik:blendTwoAttr1.o" "IK3:ik:softik:multiplyDivide7.i1x";
connectAttr "IK3:ik:softik:distanceBetween1.d" "IK3:ik:softik:multiplyDivide7.i2x"
		;
connectAttr "IK3:ik:softik:distanceBetween1.d" "IK3:ik:softik:plusMinusAverage2.i1[0]"
		;
connectAttr "IK3:ik:softik:plusMinusAverage1.o1" "IK3:ik:softik:plusMinusAverage2.i1[1]"
		;
connectAttr "IK3:ik:softik:inn.inStretch" "IK3:ik:softik:blendTwoAttr1.ab";
connectAttr "IK3:ik:softik:condition1.ocr" "IK3:ik:softik:blendTwoAttr1.i[0]";
connectAttr "IK3:ik:softik:distanceBetween1.d" "IK3:ik:softik:blendTwoAttr1.i[1]"
		;
connectAttr "IK3:ik:softik:distanceBetween1.d" "IK3:ik:softik:multiplyDivide6.i1x"
		;
connectAttr "IK3:ik:softik:plusMinusAverage4.o1" "IK3:ik:softik:multiplyDivide6.i2x"
		;
connectAttr "IK3:inn1.m" "IK3:inn.Guide01_LocalTm";
connectAttr "IK3:inn2.m" "IK3:inn.Guide02_LocalTm";
connectAttr "IK3:inn3.m" "IK3:inn.Guide03_LocalTm";
connectAttr "IK3:inn.Guide01_LocalTm" "IK3:decomposeGuide01LocalTm.imat";
connectAttr "IK3:inn.Guide02_LocalTm" "IK3:decomposeGuide02LocalTm.imat";
connectAttr "IK3:inn.Guide03_LocalTm" "IK3:decomposeGuide03LocalTm.imat";
connectAttr "IK3:inn.Guide01_LocalTm" "IK3:out.CtrlFk01_BaseLocalTm";
connectAttr "IK3:inn.Guide02_LocalTm" "IK3:out.CtrlFk02_BaseLocalTm";
connectAttr "IK3:inn.Guide03_LocalTm" "IK3:out.CtrlFk03_BaseLocalTm";
connectAttr "IK3:out.CtrlFk01_BaseLocalTm" "IK3:decomposeCtrlFk01DefaultLocalTm.imat"
		;
connectAttr "IK3:out.CtrlFk02_BaseLocalTm" "IK3:decomposeCtrlFk02DefaultLocalTm.imat"
		;
connectAttr "IK3:out.CtrlFk03_BaseLocalTm" "IK3:decomposeCtrlFk03DefaultLocalTm.imat"
		;
connectAttr "IK3:decomposeGuide02LocalTm.ot" "IK3:getLimbSegment1Length.p2";
connectAttr "IK3:decomposeGuide03LocalTm.ot" "IK3:getLimbSegment2Length.p2";
connectAttr "IK3:getLimbSegment1Length.d" "IK3:getLimbLength.i1";
connectAttr "IK3:getLimbSegment2Length.d" "IK3:getLimbLength.i2";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide13.i2x";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide13.i2y";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide13.i2z";
connectAttr "IK3:decomposeGuide02LocalTm.ot" "IK3:multiplyDivide13.i1";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide14.i2x";
connectAttr "IK3:ik:softik:out.outStretch" "IK3:multiplyDivide14.i2y";
connectAttr "IK3:decomposeGuide03LocalTm.ot" "IK3:multiplyDivide14.i1";
connectAttr "IK3:inn.Guide03_LocalTm" "IK3:getGuide03WorldTm.i[0]";
connectAttr "IK3:getGuide02WorldTm.o" "IK3:getGuide03WorldTm.i[1]";
connectAttr "IK3:getGuide03WorldTm.o" "IK3:decomposeGuide03WorldTm.imat";
connectAttr "IK3:getLimbLength.o" "IK3:getSwivelDistance.i1x";
connectAttr "IK3:inn.swivelDistanceRatio" "IK3:getSwivelDistance.i2x";
connectAttr "IK3:getLimbSegment1Length.d" "IK3:getLimbRatio.i1x";
connectAttr "IK3:getLimbLength.o" "IK3:getLimbRatio.i2x";
connectAttr "IK3:decomposeGuide03WorldTm.ot" "IK3:getLimbAim.i3[0]";
connectAttr "IK3:decomposeGuide01LocalTm.ot" "IK3:getLimbAim.i3[1]";
connectAttr "IK3:getLimbRatio.ox" "IK3:getLimbMiddleAim.i2x";
connectAttr "IK3:getLimbRatio.ox" "IK3:getLimbMiddleAim.i2y";
connectAttr "IK3:getLimbRatio.ox" "IK3:getLimbMiddleAim.i2z";
connectAttr "IK3:getLimbAim.o3" "IK3:getLimbMiddleAim.i1";
connectAttr "IK3:decomposeGuide01LocalTm.ot" "IK3:getKneePosProjectedOnLimbDir.i3[0]"
		;
connectAttr "IK3:getLimbMiddleAim.o" "IK3:getKneePosProjectedOnLimbDir.i3[1]";
connectAttr "IK3:decomposeGuide02WorldTm.ot" "IK3:getKneeDirection.i3[0]";
connectAttr "IK3:getKneePosProjectedOnLimbDir.o3" "IK3:getKneeDirection.i3[1]";
connectAttr "IK3:inn.Guide02_LocalTm" "IK3:getGuide02WorldTm.i[0]";
connectAttr "IK3:inn.Guide01_LocalTm" "IK3:getGuide02WorldTm.i[1]";
connectAttr "IK3:getGuide02WorldTm.o" "IK3:decomposeGuide02WorldTm.imat";
connectAttr "IK3:getKneeDirection.o3" "IK3:getKneeDirectionNormalized.i1";
connectAttr "IK3:getKneeDirectionNormalized.o" "IK3:getKneeDirectionOffset.i1";
connectAttr "IK3:getSwivelDistance.ox" "IK3:getKneeDirectionOffset.i2x";
connectAttr "IK3:getSwivelDistance.ox" "IK3:getKneeDirectionOffset.i2y";
connectAttr "IK3:getSwivelDistance.ox" "IK3:getKneeDirectionOffset.i2z";
connectAttr "IK3:decomposeGuide02WorldTm.ot" "IK3:getSwivelDefaultPos.i3[0]";
connectAttr "IK3:getKneeDirectionOffset.o" "IK3:getSwivelDefaultPos.i3[1]";
connectAttr "IK3:out.outInf01LocalTm" "IK3:decomposeMatrix1.imat";
connectAttr "IK3:out.outInf02LocalTm" "IK3:decomposeMatrix2.imat";
connectAttr "IK3:out.outInf03LocalTm" "IK3:decomposeMatrix3.imat";
connectAttr "IK3:guide_02_translateX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "IK3:getGuide03WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "IK3:decomposeGuide01LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "IK3:decomposeCtrlFk03DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "IK3:guide_02_translateY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "IK3:multiplyDivide14.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "IK3:decomposeGuide03LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "IK3:guide_02_rotateZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "IK3:arm_atts_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "IK3:decomposeGuide02WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "IK3:ik:arm_ik_02_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "IK3:arm_elbow01_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn"
		;
connectAttr "IK3:getKneeDirection.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "IK3:decomposeCtrlFk01DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn"
		;
connectAttr "IK3:getLimbAim.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn"
		;
connectAttr "IK3:getKneeDirectionOffset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "IK3:inn1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn";
connectAttr "IK3:ik:arm_ik_swivelLineLoc_anm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn"
		;
connectAttr "IK3:getLimbSegment1Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn"
		;
connectAttr "IK3:guide_02_rotateY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "IK3:guide_02_scaleY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn"
		;
connectAttr "IK3:getKneeDirectionNormalized.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[22].dn"
		;
connectAttr "IK3:decomposeGuide03WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[23].dn"
		;
connectAttr "IK3:ik:arm_ik_03_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[24].dn"
		;
connectAttr "IK3:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn";
connectAttr "IK3:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[26].dn";
connectAttr "IK3:inn2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[27].dn";
connectAttr "IK3:decomposeGuide02LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[28].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[29].dn"
		;
connectAttr "IK3:getSwivelDefaultPos.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[30].dn"
		;
connectAttr "IK3:out3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[31].dn";
connectAttr "IK3:out2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[32].dn";
connectAttr "IK3:ik:arm_ik_swivel_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[33].dn"
		;
connectAttr "IK3:getLimbSegment2Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[34].dn"
		;
connectAttr "IK3:inn3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[35].dn";
connectAttr "IK3:getGuide02WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[36].dn"
		;
connectAttr "IK3:guide_02_scaleZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[37].dn"
		;
connectAttr "IK3:decomposeCtrlFk02DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[38].dn"
		;
connectAttr "IK3:guide_02_scaleX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[39].dn"
		;
connectAttr "IK3:getSwivelDistance.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[40].dn"
		;
connectAttr "IK3:getKneePosProjectedOnLimbDir.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[41].dn"
		;
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[42].dn"
		;
connectAttr "IK3:multiplyDivide13.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[43].dn"
		;
connectAttr "IK3:getLimbRatio.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[44].dn"
		;
connectAttr "IK3:guide_02_translateZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[45].dn"
		;
connectAttr "IK3:getLimbLength.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[46].dn"
		;
connectAttr "IK3:getLimbMiddleAim.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[47].dn"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[48].dn"
		;
connectAttr "IK3:guide_02_rotateX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[49].dn"
		;
connectAttr "IK3:ik:locator1_pointConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[0].ni[50].dn"
		;
connectAttr "IK3:out2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[0].dn";
connectAttr "IK3:ik:arm_ik_ikChain_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[1].dn"
		;
connectAttr "IK3:decomposeGuide03LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[2].dn"
		;
connectAttr "IK3:decomposeCtrlFk01DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[3].dn"
		;
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[4].dn"
		;
connectAttr "IK3:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[5].dn";
connectAttr "IK3:ik:locator1_pointConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[6].dn"
		;
connectAttr "IK3:getLimbLength.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[7].dn"
		;
connectAttr "IK3:getLimbSegment1Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[8].dn"
		;
connectAttr "IK3:multiplyDivide13.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[9].dn"
		;
connectAttr "IK3:arm_atts_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[10].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[11].dn"
		;
connectAttr "IK3:out3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[12].dn";
connectAttr "IK3:decomposeGuide01LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[13].dn"
		;
connectAttr "IK3:arm_elbow01_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[14].dn"
		;
connectAttr "IK3:decomposeGuide02LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[15].dn"
		;
connectAttr "IK3:ik:arm_ik_02_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[16].dn"
		;
connectAttr "IK3:inn1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[17].dn";
connectAttr "IK3:inn2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[18].dn";
connectAttr "IK3:ik:softik:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[19].dn"
		;
connectAttr "IK3:multiplyDivide14.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[20].dn"
		;
connectAttr "IK3:decomposeCtrlFk02DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[21].dn"
		;
connectAttr "IK3:getLimbSegment2Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[22].dn"
		;
connectAttr "IK3:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[23].dn";
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[24].dn"
		;
connectAttr "IK3:decomposeCtrlFk03DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[25].dn"
		;
connectAttr "IK3:ik:arm_ik_03_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[26].dn"
		;
connectAttr "IK3:inn3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[27].dn";
connectAttr "IK3:ik:arm_ik_swivelLineLoc_anm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[28].dn"
		;
connectAttr "IK3:ik:arm_ik_01_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[1].ni[29].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[0].dn"
		;
connectAttr "IK3:ik:softik:distanceBetween1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[1].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[2].dn"
		;
connectAttr "IK3:ik:softik:clamp1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[3].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[4].dn"
		;
connectAttr "IK3:ik:softik:condition2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[5].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide6.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[6].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[7].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[8].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide7.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[9].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide5.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[10].dn"
		;
connectAttr "IK3:ik:softik:blendTwoAttr1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[11].dn"
		;
connectAttr "IK3:ik:softik:blendTwoAttr2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[12].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[13].dn"
		;
connectAttr "IK3:ik:softik:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[14].dn"
		;
connectAttr "IK3:ik:softik:condition1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[15].dn"
		;
connectAttr "IK3:ik:softik:metadata.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[16].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[17].dn"
		;
connectAttr "IK3:ik:softik:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[18].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[2].ni[19].dn"
		;
connectAttr "IK3:decomposeGuide02LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[0].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide7.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[1].dn"
		;
connectAttr "IK3:inn1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[2].dn";
connectAttr "IK3:decomposeGuide01LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[3].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[4].dn"
		;
connectAttr "IK3:inn2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[5].dn";
connectAttr "IK3:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[6].dn";
connectAttr "IK3:ik:arm_ik_anm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[7].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[8].dn"
		;
connectAttr "IK3:decomposeGuide03LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[9].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[10].dn"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[11].dn"
		;
connectAttr "IK3:ik:softik:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[12].dn"
		;
connectAttr "IK3:getLimbSegment1Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[13].dn"
		;
connectAttr "IK3:ik:softik:distanceBetween1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[14].dn"
		;
connectAttr "IK3:ik:softik:clamp1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[15].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide5.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[16].dn"
		;
connectAttr "IK3:multiplyDivide1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[17].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[18].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[19].dn"
		;
connectAttr "IK3:ik:softik:blendTwoAttr1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[20].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[21].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[22].dn"
		;
connectAttr "IK3:ik:softik:condition1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[23].dn"
		;
connectAttr "IK3:getLimbSegment2Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[24].dn"
		;
connectAttr "IK3:reverse1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[25].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[26].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[27].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[28].dn"
		;
connectAttr "IK3:inn3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[29].dn";
connectAttr "IK3:ik:softik:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[30].dn"
		;
connectAttr "IK3:getLimbLength.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[31].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[3].ni[32].dn"
		;
connectAttr "IK3:inn1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[0].dn";
connectAttr "IK3:reverse1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[1].dn"
		;
connectAttr "IK3:multiplyDivide11.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[2].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[3].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[4].dn"
		;
connectAttr "IK3:ik:arm_ik_03_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[5].dn"
		;
connectAttr "IK3:guide_02_translateY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[6].dn"
		;
connectAttr "IK3:ik:softik:condition1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[7].dn"
		;
connectAttr "IK3:guide_02_rotateZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[8].dn"
		;
connectAttr "IK3:getLimbSegment1Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[9].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[10].dn"
		;
connectAttr "IK3:ik:softik:blendTwoAttr2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[11].dn"
		;
connectAttr "IK3:ik:arm_ik_anm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[12].dn"
		;
connectAttr "IK3:arm_elbow01_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[13].dn"
		;
connectAttr "IK3:multiplyDivide14.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[14].dn"
		;
connectAttr "IK3:ik:arm_ik_02_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[15].dn"
		;
connectAttr "IK3:guide_02_translateX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[16].dn"
		;
connectAttr "IK3:multiplyDivide10.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[17].dn"
		;
connectAttr "IK3:ik:softik:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[18].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide6.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[19].dn"
		;
connectAttr "IK3:guide_02_rotateY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[20].dn"
		;
connectAttr "IK3:ik:arm_ik_swivelLineLoc_anm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[21].dn"
		;
connectAttr "IK3:decomposeGuide03LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[22].dn"
		;
connectAttr "IK3:decomposeGuide01LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[23].dn"
		;
connectAttr "IK3:ik:softik:distanceBetween1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[24].dn"
		;
connectAttr "IK3:multiplyDivide1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[25].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[26].dn"
		;
connectAttr "IK3:arm_atts_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[27].dn"
		;
connectAttr "IK3:guide_02_scaleY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[28].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandleTarget_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[29].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[30].dn"
		;
connectAttr "IK3:inn2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[31].dn";
connectAttr "IK3:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[32].dn";
connectAttr "IK3:ik:softik:clamp1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[33].dn"
		;
connectAttr "IK3:decomposeGuide02LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[34].dn"
		;
connectAttr "IK3:ik:softik:blendTwoAttr1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[35].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[36].dn"
		;
connectAttr "IK3:out3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[37].dn";
connectAttr "IK3:out2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[38].dn";
connectAttr "IK3:ik:softik:multiplyDivide3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[39].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[40].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide5.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[41].dn"
		;
connectAttr "IK3:inn3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[42].dn";
connectAttr "IK3:getLimbSegment2Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[43].dn"
		;
connectAttr "IK3:guide_02_scaleZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[44].dn"
		;
connectAttr "IK3:getSwivelDistance.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[45].dn"
		;
connectAttr "IK3:guide_02_scaleX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[46].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide7.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[47].dn"
		;
connectAttr "IK3:arm_atts_anm_offset_parentConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[48].dn"
		;
connectAttr "IK3:ik:softik:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[49].dn"
		;
connectAttr "IK3:multiplyDivide13.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[50].dn"
		;
connectAttr "IK3:guide_02_translateZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[51].dn"
		;
connectAttr "IK3:getLimbLength.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[52].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[53].dn"
		;
connectAttr "IK3:ik:softik:metadata.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[54].dn"
		;
connectAttr "IK3:guide_02_rotateX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[55].dn"
		;
connectAttr "IK3:ik:softik:condition2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[56].dn"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[57].dn"
		;
connectAttr "IK3:ik:locator1_pointConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[58].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[4].ni[59].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[0].dn"
		;
connectAttr "IK3:decomposeGuide02LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[1].dn"
		;
connectAttr "IK3:guide_02_translateX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[2].dn"
		;
connectAttr "IK3:decomposeCtrlFk02DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[3].dn"
		;
connectAttr "IK3:guide_02_scaleY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[4].dn"
		;
connectAttr "IK3:decomposeGuide03LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[5].dn"
		;
connectAttr "IK3:getLimbSegment2Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[6].dn"
		;
connectAttr "IK3:multiplyDivide14.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[7].dn"
		;
connectAttr "IK3:inn3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[8].dn";
connectAttr "IK3:decomposeCtrlFk01DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[9].dn"
		;
connectAttr "IK3:getGuide03WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[10].dn"
		;
connectAttr "IK3:getLimbSegment1Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[11].dn"
		;
connectAttr "IK3:guide_02_scaleZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[12].dn"
		;
connectAttr "IK3:guide_02_rotateZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[13].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[14].dn"
		;
connectAttr "IK3:inn2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[15].dn";
connectAttr ":defaultRenderUtilityList1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[16].dn"
		;
connectAttr "IK3:decomposeCtrlFk03DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[17].dn"
		;
connectAttr "IK3:inn1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[18].dn";
connectAttr "IK3:decomposeGuide01LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[19].dn"
		;
connectAttr "IK3:getSwivelDistance.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[20].dn"
		;
connectAttr "IK3:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[21].dn";
connectAttr "IK3:ik:softik:clamp1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[22].dn"
		;
connectAttr "IK3:guide_02_scaleX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[23].dn"
		;
connectAttr "IK3:ik:softik:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[24].dn"
		;
connectAttr "IK3:guide_02_translateY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[25].dn"
		;
connectAttr "IK3:decomposeGuide03WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[26].dn"
		;
connectAttr "IK3:guide_02_rotateY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[27].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide5.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[28].dn"
		;
connectAttr "IK3:multiplyDivide13.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[29].dn"
		;
connectAttr "IK3:getLimbRatio.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[30].dn"
		;
connectAttr "IK3:guide_02_translateZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[31].dn"
		;
connectAttr "IK3:getLimbLength.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[32].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[33].dn"
		;
connectAttr "IK3:ik:softik:condition2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[34].dn"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[35].dn"
		;
connectAttr "IK3:guide_02_rotateX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[36].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[37].dn"
		;
connectAttr "IK3:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[5].ni[38].dn";
connectAttr "IK3:decomposeGuide02LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[0].dn"
		;
connectAttr "IK3:ik:softik:blendTwoAttr1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[1].dn"
		;
connectAttr "IK3:multiplyDivide14.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[2].dn"
		;
connectAttr "IK3:ik:arm_ik_ikChain_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[3].dn"
		;
connectAttr "IK3:getKneePosProjectedOnLimbDir.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[4].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[5].dn"
		;
connectAttr "IK3:getKneeDirectionOffset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[6].dn"
		;
connectAttr "IK3:multiplyDivide10.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[7].dn"
		;
connectAttr "IK3:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[8].dn";
connectAttr "IK3:ik:softik:multiplyDivide1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[9].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[10].dn"
		;
connectAttr "IK3:ik:arm_ik_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[11].dn"
		;
connectAttr "IK3:guide_02_scaleY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[12].dn"
		;
connectAttr "IK3:getLimbRatio.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[13].dn"
		;
connectAttr "IK3:getLimbSegment1Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[14].dn"
		;
connectAttr "IK3:getSwivelDefaultPos.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[15].dn"
		;
connectAttr "IK3:ik:softik:condition2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[16].dn"
		;
connectAttr "IK3:ik:arm_ik_swivel_anm_offset.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[17].dn"
		;
connectAttr "IK3:ik:softik:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[18].dn"
		;
connectAttr "IK3:guide_02_translateZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[19].dn"
		;
connectAttr "IK3:decomposeGuide02WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[20].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[21].dn"
		;
connectAttr "IK3:guide_02_translateX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[22].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[23].dn"
		;
connectAttr "IK3:guide_02_translateY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[24].dn"
		;
connectAttr "IK3:getKneeDirection.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[25].dn"
		;
connectAttr "IK3:multiplyDivide13.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[26].dn"
		;
connectAttr "IK3:getLimbSegment2Length.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[27].dn"
		;
connectAttr "IK3:decomposeCtrlFk02DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[28].dn"
		;
connectAttr "IK3:out.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[29].dn";
connectAttr "IK3:ik:arm_ik_02_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[30].dn"
		;
connectAttr "IK3:inn1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[31].dn";
connectAttr "IK3:decomposeGuide01LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[32].dn"
		;
connectAttr "IK3:getGuide02WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[33].dn"
		;
connectAttr "IK3:guide_02_rotateY.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[34].dn"
		;
connectAttr "IK3:decomposeGuide03LocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[35].dn"
		;
connectAttr "IK3:ik:softik:condition1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[36].dn"
		;
connectAttr "IK3:inn2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[37].dn";
connectAttr "IK3:getLimbAim.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[38].dn"
		;
connectAttr "IK3:multiplyDivide11.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[39].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[40].dn"
		;
connectAttr "IK3:decomposeCtrlFk03DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[41].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide7.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[42].dn"
		;
connectAttr "IK3:getSwivelDistance.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[43].dn"
		;
connectAttr "IK3:guide_02_rotateZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[44].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[45].dn"
		;
connectAttr "IK3:getKneeDirectionNormalized.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[46].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide5.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[47].dn"
		;
connectAttr "IK3:ik:arm_ik_03_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[48].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage4.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[49].dn"
		;
connectAttr "IK3:ik:softik:blendTwoAttr2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[50].dn"
		;
connectAttr "IK3:getLimbLength.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[51].dn"
		;
connectAttr "IK3:decomposeGuide03WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[52].dn"
		;
connectAttr "IK3:decomposeCtrlFk01DefaultLocalTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[53].dn"
		;
connectAttr "IK3:inn3.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[54].dn";
connectAttr "IK3:ik:softik:clamp1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[55].dn"
		;
connectAttr "IK3:getLimbMiddleAim.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[56].dn"
		;
connectAttr "IK3:ik:softik:plusMinusAverage2.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[57].dn"
		;
connectAttr "IK3:ik:softik:inn.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[58].dn"
		;
connectAttr "IK3:ik:softik:multiplyDivide6.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[59].dn"
		;
connectAttr "IK3:getGuide03WorldTm.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[60].dn"
		;
connectAttr "IK3:guide_02_scaleZ.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[61].dn"
		;
connectAttr "IK3:reverse1.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[62].dn"
		;
connectAttr "IK3:ik:arm_ik_ikHandle_rig.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[63].dn"
		;
connectAttr "IK3:guide_02_rotateX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[64].dn"
		;
connectAttr "IK3:guide_02_scaleX.msg" "IK3:MayaNodeEditorSavedTabsInfo.tgi[6].ni[65].dn"
		;
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
connectAttr "FK3:decomposeGuide01LocalTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "FK3:decomposeGuide02LocalTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "FK3:decomposeGuide03LocalTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "FK3:decomposeCtrlFk01DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "FK3:decomposeCtrlFk02DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "FK3:decomposeCtrlFk03DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "FK3:getLimbSegment1Length.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getLimbSegment2Length.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getLimbLength.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:multiplyDivide13.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:multiplyDivide14.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getGuide03WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:decomposeGuide03WorldTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "FK3:getSwivelDistance.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getLimbRatio.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getLimbAim.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getLimbMiddleAim.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getKneePosProjectedOnLimbDir.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "FK3:getKneeDirection.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getGuide02WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:decomposeGuide02WorldTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "FK3:getKneeDirectionNormalized.msg" ":defaultRenderUtilityList1.u" 
		-na;
connectAttr "FK3:getKneeDirectionOffset.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:getSwivelDefaultPos.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:decomposeMatrix1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:decomposeMatrix2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "FK3:decomposeMatrix3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:decomposeGuide01LocalTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "IK3:decomposeGuide02LocalTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "IK3:decomposeGuide03LocalTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "IK3:decomposeCtrlFk01DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "IK3:decomposeCtrlFk02DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "IK3:decomposeCtrlFk03DefaultLocalTm.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "IK3:getLimbSegment1Length.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getLimbSegment2Length.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getLimbLength.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:multiplyDivide13.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:multiplyDivide14.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getGuide03WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:decomposeGuide03WorldTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "IK3:getSwivelDistance.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getLimbRatio.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getLimbAim.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getLimbMiddleAim.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getKneePosProjectedOnLimbDir.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "IK3:getKneeDirection.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getGuide02WorldTm.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:decomposeGuide02WorldTm.msg" ":defaultRenderUtilityList1.u" -na
		;
connectAttr "IK3:getKneeDirectionNormalized.msg" ":defaultRenderUtilityList1.u" 
		-na;
connectAttr "IK3:getKneeDirectionOffset.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:getSwivelDefaultPos.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:decomposeMatrix1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:decomposeMatrix2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "IK3:decomposeMatrix3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "FK3:defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "IK3:defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "IK3:ikRPsolver.msg" ":ikSystem.sol" -na;
// End of limb2.ma
