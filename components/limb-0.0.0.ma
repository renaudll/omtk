//Maya ASCII 2017ff05 scene
//Name: limb-0.0.2.ma
//Last modified: Tue, Apr 17, 2018 11:09:53 PM
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
fileInfo "omtk.component.uid" "9e38b6df-b42f-5f6d-b243-bbfeb645518a";
fileInfo "omtk.component.name" "Limb";
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
createNode joint -n "infl_01";
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
createNode joint -n "infl_02" -p "infl_01";
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
createNode joint -n "infl_03" -p "infl_02";
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
createNode transform -n "arm_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002E8";
createNode transform -n "arm_atts_anm_offset" -p "arm_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F4";
createNode transform -n "arm_atts_anm" -p "arm_atts_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F3";
	addAttr -ci true -k true -sn "fkIk" -ln "fkIk" -dv 1 -min 0 -max 1 -at "double";
	setAttr -k on ".ro";
	setAttr -k on ".fkIk";
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
createNode transform -n "arm_elbow01_anm_offset" -p "arm_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000401";
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
createNode parentConstraint -n "arm_elbow01_anm_offset_parentConstraint1" -p "arm_elbow01_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000402";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "infl_02_blend_rigW0" -dv 1 -min 0 
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
	setAttr ".lr" -type "double3" 89.999999999999986 44.999999999999986 -90.000000000000043 ;
	setAttr ".rst" -type "double3" -3.9252311467094368e-16 2.5000000000000009 2.4999999999999991 ;
	setAttr ".rsrr" -type "double3" 89.999999999999986 44.999999999999986 -90.000000000000057 ;
	setAttr -k on ".w0";
createNode transform -n "ik:arm_ik_anm_grp" -p "arm_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EB";
createNode transform -n "ik:arm_ik_anm_offset" -p "ik:arm_ik_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F9";
createNode transform -n "ik:arm_ik_anm" -p "ik:arm_ik_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F8";
	addAttr -ci true -k true -sn "softIkRatio" -ln "softIkRatio" -nn "SoftIK" -min 
		0 -max 50 -at "double";
	addAttr -ci true -k true -sn "stretch" -ln "stretch" -nn "Stretch" -min 0 -max 1 
		-at "double";
	setAttr ".r" -type "double3" 180 -45 -90 ;
	setAttr -k on ".ro";
	setAttr -k on ".softIkRatio";
	setAttr -k on ".stretch" 1;
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
createNode transform -n "ik:arm_ik_swivel_anm" -p "ik:arm_ik_swivel_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000316";
	addAttr -ci true -k true -sn "space" -ln "space" -min -2 -max 0 -en "World=-2:arm=0" 
		-at "enum";
	setAttr -k on ".space" -2;
createNode nurbsCurve -n "ik:arm_ik_swivel_anmShape" -p "ik:arm_ik_swivel_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000315";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "ik:arm_ik_swivelLineLoc_anm" -p "ik:arm_ik_swivel_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000318";
	setAttr ".v" no;
createNode locator -n "ik:arm_ik_swivelLineLoc_anmShape" -p "ik:arm_ik_swivelLineLoc_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000319";
	setAttr -k off ".v";
createNode pointConstraint -n "ik:locator1_pointConstraint1" -p "ik:arm_ik_swivelLineLoc_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000031A";
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
createNode annotationShape -n "ik:arm_ik_swivelLineAnn_anm" -p "ik:arm_ik_swivel_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000031B";
	setAttr -k off ".v";
createNode transform -n "arm_fk_anm_grp" -p "arm_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000322";
createNode transform -n "arm_fk_infl_01_anm_offset" -p "arm_fk_anm_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000326";
createNode transform -n "arm_fk_infl_01_anm" -p "arm_fk_infl_01_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000325";
createNode nurbsCurve -n "arm_fk_infl_01_anmShape" -p "arm_fk_infl_01_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000324";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "arm_fk_infl_02_anm_offset" -p "arm_fk_infl_01_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000032A";
createNode transform -n "arm_fk_infl_02_anm" -p "arm_fk_infl_02_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000329";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".rz";
createNode nurbsCurve -n "arm_fk_infl_02_anmShape" -p "arm_fk_infl_02_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000328";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "arm_fk_infl_03_anm_offset" -p "arm_fk_infl_02_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000032E";
createNode transform -n "arm_fk_infl_03_anm" -p "arm_fk_infl_03_anm_offset";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000032D";
createNode nurbsCurve -n "arm_fk_infl_03_anmShape" -p "arm_fk_infl_03_anm";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000032C";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "arm_data_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002E9";
	addAttr -ci true -sn "globalScale" -ln "globalScale" -dv 1 -at "double";
	addAttr -ci true -k true -sn "fkIk" -ln "fkIk" -dv 1 -min 0 -max 1 -at "double";
	setAttr -k on ".fkIk";
createNode joint -n "infl_01_blend_rig" -p "arm_data_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F6";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 90 -45.000000000000007 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "infl_02_blend_rig" -p "infl_01_blend_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F7";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
createNode joint -n "infl_03_blend_rig" -p "infl_02_blend_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F8";
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
createNode parentConstraint -n "infl_03_blend_rig_parentConstraint1" -p "infl_03_blend_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003FB";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_ik_03_rigW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "arm_fk_infl_03_anmW1" -dv 1 -min 0 
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
	setAttr -s 2 ".tg";
	setAttr ".tg[0].tot" -type "double3" 9.0343999324441246e-10 -9.0344187735536351e-10 5.0150845973294299e-26 ;
	setAttr ".tg[1].tot" -type "double3" -1.9721522630525295e-31 -6.2803698347351036e-16 0 ;
	setAttr ".tg[1].tor" -type "double3" 0 0 2.5444437451708134e-14 ;
	setAttr ".rst" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr ".rsrr" -type "double3" 0 0 -1.2722218725854067e-14 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode parentConstraint -n "infl_02_blend_rig_parentConstraint1" -p "infl_02_blend_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003FA";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_ik_02_rigW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "arm_fk_infl_02_anmW1" -dv 1 -min 0 
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
	setAttr -s 2 ".tg";
	setAttr ".tg[0].tot" -type "double3" 4.4408920985006262e-16 9.0343976767208529e-10 1.0030188916181492e-25 ;
	setAttr ".tg[1].tot" -type "double3" 4.4408920985006262e-16 -4.9960036108132005e-16 -9.8607613152626476e-32 ;
	setAttr ".rst" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode parentConstraint -n "infl_01_blend_rig_parentConstraint1" -p "infl_01_blend_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F9";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_ik_01_rigW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "arm_fk_infl_01_anmW1" -dv 1 -min 0 
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
	setAttr -s 2 ".tg";
	setAttr ".tg[0].tot" -type "double3" 4.4408920985006262e-16 -4.4408920985006262e-16 -4.9303806576313238e-32 ;
	setAttr ".tg[0].tor" -type "double3" 7.0622500768802538e-31 0 0 ;
	setAttr ".tg[1].tot" -type "double3" 0 0 4.9303806576313238e-32 ;
	setAttr ".tg[1].tor" -type "double3" 7.0622500768802538e-31 0 0 ;
	setAttr ".rst" -type "double3" -5.4738221262688167e-48 5 6.0771633572862712e-64 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode joint -n "infl_01_elbow_rig" -p "arm_data_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003FC";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 90 -45.000000000000007 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "infl_02_elbow_rig" -p "infl_01_elbow_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003FD";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
createNode joint -n "infl_03_elbow_rig" -p "infl_02_elbow_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003FE";
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
createNode parentConstraint -n "infl_03_elbow_rig_parentConstraint1" -p "infl_03_elbow_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000407";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "infl_03_blend_rigW0" -dv 1 -min 0 
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
	setAttr ".rst" -type "double3" 3.5355339059327382 -6.8191403898365008e-16 -1.9626155733547189e-16 ;
	setAttr -k on ".w0";
createNode aimConstraint -n "infl_02_elbow_rig_aimConstraint1" -p "infl_02_elbow_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000405";
	addAttr -dcb 0 -ci true -sn "w0" -ln "infl_03_blend_rigW0" -dv 1 -at "double";
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
	setAttr ".wut" 2;
	setAttr ".rsrr" -type "double3" -3.180554681463516e-15 3.1805546814635152e-15 -2.5444437451708134e-14 ;
	setAttr -k on ".w0";
createNode pointConstraint -n "infl_02_elbow_rig_pointConstraint1" -p "infl_02_elbow_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000406";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "arm_elbow01_anmW0" -dv 1 -min 0 -at "double";
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
	setAttr ".rst" -type "double3" 3.535533905932736 0 3.9252311467094363e-16 ;
	setAttr -k on ".w0";
createNode pointConstraint -n "infl_01_elbow_rig_pointConstraint1" -p "infl_01_elbow_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000403";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "infl_01_blend_rigW0" -dv 1 -min 0 
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
	setAttr ".rst" -type "double3" 4.9303806576313249e-32 5 -5.4738221262688167e-48 ;
	setAttr -k on ".w0";
createNode aimConstraint -n "infl_01_elbow_rig_aimConstraint1" -p "infl_01_elbow_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A00000404";
	addAttr -dcb 0 -ci true -sn "w0" -ln "arm_elbow01_anmW0" -dv 1 -at "double";
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
	setAttr ".wut" 2;
	setAttr ".rsrr" -type "double3" -1.2722218725854064e-14 -1.4312496066585827e-14 -6.3611093629270304e-15 ;
	setAttr -k on ".w0";
createNode transform -n "ik:arm_ik_data_grp" -p "arm_data_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EC";
	addAttr -ci true -sn "globalScale" -ln "globalScale" -dv 1 -at "double";
createNode transform -n "ik:arm_ik_ikChain_rig" -p "ik:arm_ik_data_grp";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EA";
createNode joint -n "ik:arm_ik_01_rig" -p "ik:arm_ik_ikChain_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002ED";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".t" -type "double3" -4.4408920985006262e-16 4.4408920985006262e-16 0 ;
	setAttr ".r" -type "double3" 6.0370913486286657e-07 -6.0370913486286657e-07 -3.1805546479509594e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 6.3611093629270312e-15 8.9959671327898822e-15 6.3611093629270335e-15 ;
	setAttr ".ssc" no;
	setAttr ".radi" 1.0433717280489374;
	setAttr "._graphpos" -type "float2" -862.85712 217.14285 ;
createNode joint -n "ik:arm_ik_02_rig" -p "ik:arm_ik_01_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002EE";
	addAttr -ci true -sn "_graphpos" -ln "_graphpos" -at "float2" -nc 2;
	addAttr -ci true -sn "_graphposX" -ln "_graphposX" -at "float" -p "_graphpos";
	addAttr -ci true -sn "_graphposY" -ln "_graphposY" -at "float" -p "_graphpos";
	setAttr ".r" -type "double3" 2.5532766199013497e-24 1.0647823692817705e-21 4.5995742535843644e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".ssc" no;
	setAttr ".radi" 0.65781884989194483;
	setAttr "._graphpos" -type "float2" -248.57143 560 ;
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
	setAttr "._graphpos" -type "float2" 365.71429 308.57144 ;
createNode orientConstraint -n "ik:arm_ik_03_rig_orientConstraint1" -p "ik:arm_ik_03_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000321";
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
createNode ikEffector -n "ik:arm_ik_ikEffector_rig" -p "ik:arm_ik_02_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F0";
	setAttr ".v" no;
	setAttr ".hd" yes;
createNode ikHandle -n "ik:arm_ik_ikHandle_rig" -p "ik:arm_ik_ikChain_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF79000002F5";
	setAttr ".r" -type "double3" -45.000000000000007 90 0 ;
	setAttr ".s" -type "double3" 0.99999999999999956 1 1 ;
	setAttr ".roc" yes;
createNode pointConstraint -n "ik:arm_ik_ikHandle_rig_softIkConstraint1" -p "ik:arm_ik_ikHandle_rig";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000311";
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
createNode pointConstraint -n "ik:arm_ik_ikHandleTarget_rig_pointConstraint1" -p
		 "ik:arm_ik_ikHandleTarget_rig";
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
createNode joint -n "guide_01";
	rename -uid "9830B980-0000-24DE-5AB5-C4D6000005FE";
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
createNode lightLinker -s -n "lightLinker1";
	rename -uid "F4C8C980-0000-752C-5AD6-B586000003AD";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "F4C8C980-0000-752C-5AD6-B586000003AE";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "F4C8C980-0000-752C-5AD6-B586000003AF";
createNode displayLayerManager -n "layerManager";
	rename -uid "F4C8C980-0000-752C-5AD6-B586000003B0";
createNode displayLayer -n "defaultLayer";
	rename -uid "699D7980-0000-0F71-5AB5-BDA900000923";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "F4C8C980-0000-752C-5AD6-B586000003B2";
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
		+ "            -shadows 0\n            -captureSequenceNumber -1\n            -width 1249\n            -height 696\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n"
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
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1249\\n    -height 696\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1249\\n    -height 696\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
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
	setAttr ".i2" -type "float3" 0.0099999998 1 1 ;
createNode multiplyDivide -n "multiplyDivide9";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000030F";
	setAttr ".i1" -type "float3" 7.0710678 0 0 ;
createNode reverse -n "reverse1";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000310";
createNode multiplyDivide -n "multiplyDivide10";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000312";
	setAttr ".i2" -type "float3" 3.5355339 0 3.9252311e-16 ;
createNode multiplyDivide -n "multiplyDivide11";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000313";
	setAttr ".i2" -type "float3" 3.5355339 -6.2803697e-16 -1.9626156e-16 ;
createNode makeNurbCircle -n "makeNurbCircle1";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000314";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".d" 1;
	setAttr ".s" 4;
createNode makeNurbCircle -n "makeNurbCircle2";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000323";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 1.1477089008538313;
createNode makeNurbCircle -n "makeNurbCircle3";
	rename -uid "94C18980-0000-20C4-5AB5-BF7900000327";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 0.72360073488113941;
createNode makeNurbCircle -n "makeNurbCircle4";
	rename -uid "94C18980-0000-20C4-5AB5-BF790000032B";
	setAttr ".nr" -type "double3" 1 0 0 ;
	setAttr ".r" 0.72360073488113941;
createNode reverse -n "reverse2";
	rename -uid "94C18980-0000-20C4-5AB5-BF7A000003F1";
createNode network -n "ik:softik:inn";
	rename -uid "9830B980-0000-24DE-5AB5-C38D000005D5";
	addAttr -ci true -sn "inMatrixE" -ln "inMatrixE" -nn "inMatrixE" -dt "matrix";
	addAttr -ci true -sn "inMatrixS" -ln "inMatrixS" -nn "inMatrixS" -dt "matrix";
	addAttr -ci true -sn "inStretch" -ln "inStretch" -nn "inStretch" -at "float";
	addAttr -ci true -sn "inChainLength" -ln "inChainLength" -nn "inChainLength" -at "float";
	addAttr -ci true -sn "inRatio" -ln "inRatio" -nn "inRatio" -at "float";
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
createNode animCurveTL -n "guide_02_translateX";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C3";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.535533905932736 10 6.3911650194459524;
createNode animCurveTL -n "guide_02_translateY";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C4";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 1.8998827256160656e-16;
createNode animCurveTL -n "guide_02_translateZ";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C5";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 3.9252311467094363e-16 10 7.5484373465108625e-17;
createNode animCurveTU -n "guide_02_visibility";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C6";
	setAttr ".tan" 9;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
createNode animCurveTA -n "guide_02_rotateX";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C7";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTA -n "guide_02_rotateY";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C8";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTA -n "guide_02_rotateZ";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005C9";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
createNode animCurveTU -n "guide_02_scaleX";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005CA";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode animCurveTU -n "guide_02_scaleY";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005CB";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
createNode animCurveTU -n "guide_02_scaleZ";
	rename -uid "8C391980-0000-426F-5AD6-9BB4000005CC";
	setAttr ".tan" 18;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
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
	rename -uid "F4C8C980-0000-752C-5AD6-B6C6000003FD";
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
connectAttr "decomposeMatrix1.ot" "infl_01.t";
connectAttr "decomposeMatrix1.or" "infl_01.r";
connectAttr "decomposeMatrix1.os" "infl_01.s";
connectAttr "infl_01.s" "infl_02.is";
connectAttr "decomposeMatrix2.ot" "infl_02.t";
connectAttr "decomposeMatrix2.or" "infl_02.r";
connectAttr "decomposeMatrix2.os" "infl_02.s";
connectAttr "infl_02.s" "infl_03.is";
connectAttr "decomposeMatrix3.ot" "infl_03.t";
connectAttr "decomposeMatrix3.or" "infl_03.r";
connectAttr "decomposeMatrix3.os" "infl_03.s";
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
connectAttr "infl_03.t" "arm_atts_anm_offset_parentConstraint1.tg[0].tt";
connectAttr "infl_03.rp" "arm_atts_anm_offset_parentConstraint1.tg[0].trp";
connectAttr "infl_03.rpt" "arm_atts_anm_offset_parentConstraint1.tg[0].trt";
connectAttr "infl_03.r" "arm_atts_anm_offset_parentConstraint1.tg[0].tr";
connectAttr "infl_03.ro" "arm_atts_anm_offset_parentConstraint1.tg[0].tro";
connectAttr "infl_03.s" "arm_atts_anm_offset_parentConstraint1.tg[0].ts";
connectAttr "infl_03.pm" "arm_atts_anm_offset_parentConstraint1.tg[0].tpm";
connectAttr "infl_03.jo" "arm_atts_anm_offset_parentConstraint1.tg[0].tjo";
connectAttr "infl_03.ssc" "arm_atts_anm_offset_parentConstraint1.tg[0].tsc";
connectAttr "infl_03.is" "arm_atts_anm_offset_parentConstraint1.tg[0].tis";
connectAttr "arm_atts_anm_offset_parentConstraint1.w0" "arm_atts_anm_offset_parentConstraint1.tg[0].tw"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.ctx" "arm_elbow01_anm_offset.tx"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.cty" "arm_elbow01_anm_offset.ty"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.ctz" "arm_elbow01_anm_offset.tz"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.crx" "arm_elbow01_anm_offset.rx"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.cry" "arm_elbow01_anm_offset.ry"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.crz" "arm_elbow01_anm_offset.rz"
		;
connectAttr "arm_elbow01_anm_offset.ro" "arm_elbow01_anm_offset_parentConstraint1.cro"
		;
connectAttr "arm_elbow01_anm_offset.pim" "arm_elbow01_anm_offset_parentConstraint1.cpim"
		;
connectAttr "arm_elbow01_anm_offset.rp" "arm_elbow01_anm_offset_parentConstraint1.crp"
		;
connectAttr "arm_elbow01_anm_offset.rpt" "arm_elbow01_anm_offset_parentConstraint1.crt"
		;
connectAttr "infl_02_blend_rig.t" "arm_elbow01_anm_offset_parentConstraint1.tg[0].tt"
		;
connectAttr "infl_02_blend_rig.rp" "arm_elbow01_anm_offset_parentConstraint1.tg[0].trp"
		;
connectAttr "infl_02_blend_rig.rpt" "arm_elbow01_anm_offset_parentConstraint1.tg[0].trt"
		;
connectAttr "infl_02_blend_rig.r" "arm_elbow01_anm_offset_parentConstraint1.tg[0].tr"
		;
connectAttr "infl_02_blend_rig.ro" "arm_elbow01_anm_offset_parentConstraint1.tg[0].tro"
		;
connectAttr "infl_02_blend_rig.s" "arm_elbow01_anm_offset_parentConstraint1.tg[0].ts"
		;
connectAttr "infl_02_blend_rig.pm" "arm_elbow01_anm_offset_parentConstraint1.tg[0].tpm"
		;
connectAttr "infl_02_blend_rig.jo" "arm_elbow01_anm_offset_parentConstraint1.tg[0].tjo"
		;
connectAttr "infl_02_blend_rig.ssc" "arm_elbow01_anm_offset_parentConstraint1.tg[0].tsc"
		;
connectAttr "infl_02_blend_rig.is" "arm_elbow01_anm_offset_parentConstraint1.tg[0].tis"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.w0" "arm_elbow01_anm_offset_parentConstraint1.tg[0].tw"
		;
connectAttr "arm_data_grp.fkIk" "ik:arm_ik_anm_grp.v";
connectAttr "decomposeGuide03WorldTm.ot" "ik:arm_ik_anm_offset.t";
connectAttr "getSwivelDefaultPos.o3" "ik:arm_ik_swivel_anm_offset.t";
connectAttr "makeNurbCircle1.oc" "ik:arm_ik_swivel_anmShape.cr";
connectAttr "ik:locator1_pointConstraint1.ctx" "ik:arm_ik_swivelLineLoc_anm.tx";
connectAttr "ik:locator1_pointConstraint1.cty" "ik:arm_ik_swivelLineLoc_anm.ty";
connectAttr "ik:locator1_pointConstraint1.ctz" "ik:arm_ik_swivelLineLoc_anm.tz";
connectAttr "ik:arm_ik_swivelLineLoc_anm.pim" "ik:locator1_pointConstraint1.cpim"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anm.rp" "ik:locator1_pointConstraint1.crp";
connectAttr "ik:arm_ik_swivelLineLoc_anm.rpt" "ik:locator1_pointConstraint1.crt"
		;
connectAttr "infl_02.t" "ik:locator1_pointConstraint1.tg[0].tt";
connectAttr "infl_02.rp" "ik:locator1_pointConstraint1.tg[0].trp";
connectAttr "infl_02.rpt" "ik:locator1_pointConstraint1.tg[0].trt";
connectAttr "infl_02.pm" "ik:locator1_pointConstraint1.tg[0].tpm";
connectAttr "ik:locator1_pointConstraint1.w0" "ik:locator1_pointConstraint1.tg[0].tw"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anmShape.wm" "ik:arm_ik_swivelLineAnn_anm.dom"
		 -na;
connectAttr "reverse2.ox" "arm_fk_anm_grp.v";
connectAttr "decomposeCtrlFk01DefaultLocalTm.ot" "arm_fk_infl_01_anm_offset.t";
connectAttr "decomposeCtrlFk01DefaultLocalTm.or" "arm_fk_infl_01_anm_offset.r";
connectAttr "decomposeCtrlFk01DefaultLocalTm.os" "arm_fk_infl_01_anm_offset.s";
connectAttr "makeNurbCircle2.oc" "arm_fk_infl_01_anmShape.cr";
connectAttr "decomposeCtrlFk02DefaultLocalTm.ot" "arm_fk_infl_02_anm_offset.t";
connectAttr "decomposeCtrlFk02DefaultLocalTm.or" "arm_fk_infl_02_anm_offset.r";
connectAttr "decomposeCtrlFk02DefaultLocalTm.os" "arm_fk_infl_02_anm_offset.s";
connectAttr "makeNurbCircle3.oc" "arm_fk_infl_02_anmShape.cr";
connectAttr "decomposeCtrlFk03DefaultLocalTm.ot" "arm_fk_infl_03_anm_offset.t";
connectAttr "decomposeCtrlFk03DefaultLocalTm.or" "arm_fk_infl_03_anm_offset.r";
connectAttr "decomposeCtrlFk03DefaultLocalTm.os" "arm_fk_infl_03_anm_offset.s";
connectAttr "makeNurbCircle4.oc" "arm_fk_infl_03_anmShape.cr";
connectAttr "arm_atts_anm.fkIk" "arm_data_grp.fkIk";
connectAttr "infl_01_blend_rig_parentConstraint1.ctx" "infl_01_blend_rig.tx";
connectAttr "infl_01_blend_rig_parentConstraint1.cty" "infl_01_blend_rig.ty";
connectAttr "infl_01_blend_rig_parentConstraint1.ctz" "infl_01_blend_rig.tz";
connectAttr "infl_01_blend_rig_parentConstraint1.crx" "infl_01_blend_rig.rx";
connectAttr "infl_01_blend_rig_parentConstraint1.cry" "infl_01_blend_rig.ry";
connectAttr "infl_01_blend_rig_parentConstraint1.crz" "infl_01_blend_rig.rz";
connectAttr "infl_02_blend_rig_parentConstraint1.ctx" "infl_02_blend_rig.tx";
connectAttr "infl_02_blend_rig_parentConstraint1.cty" "infl_02_blend_rig.ty";
connectAttr "infl_02_blend_rig_parentConstraint1.ctz" "infl_02_blend_rig.tz";
connectAttr "infl_02_blend_rig_parentConstraint1.crx" "infl_02_blend_rig.rx";
connectAttr "infl_02_blend_rig_parentConstraint1.cry" "infl_02_blend_rig.ry";
connectAttr "infl_02_blend_rig_parentConstraint1.crz" "infl_02_blend_rig.rz";
connectAttr "infl_01_blend_rig.s" "infl_02_blend_rig.is";
connectAttr "infl_03_blend_rig_parentConstraint1.ctx" "infl_03_blend_rig.tx";
connectAttr "infl_03_blend_rig_parentConstraint1.cty" "infl_03_blend_rig.ty";
connectAttr "infl_03_blend_rig_parentConstraint1.ctz" "infl_03_blend_rig.tz";
connectAttr "infl_03_blend_rig_parentConstraint1.crx" "infl_03_blend_rig.rx";
connectAttr "infl_03_blend_rig_parentConstraint1.cry" "infl_03_blend_rig.ry";
connectAttr "infl_03_blend_rig_parentConstraint1.crz" "infl_03_blend_rig.rz";
connectAttr "infl_02_blend_rig.s" "infl_03_blend_rig.is";
connectAttr "infl_03_blend_rig.ro" "infl_03_blend_rig_parentConstraint1.cro";
connectAttr "infl_03_blend_rig.pim" "infl_03_blend_rig_parentConstraint1.cpim";
connectAttr "infl_03_blend_rig.rp" "infl_03_blend_rig_parentConstraint1.crp";
connectAttr "infl_03_blend_rig.rpt" "infl_03_blend_rig_parentConstraint1.crt";
connectAttr "infl_03_blend_rig.jo" "infl_03_blend_rig_parentConstraint1.cjo";
connectAttr "ik:arm_ik_03_rig.t" "infl_03_blend_rig_parentConstraint1.tg[0].tt";
connectAttr "ik:arm_ik_03_rig.rp" "infl_03_blend_rig_parentConstraint1.tg[0].trp"
		;
connectAttr "ik:arm_ik_03_rig.rpt" "infl_03_blend_rig_parentConstraint1.tg[0].trt"
		;
connectAttr "ik:arm_ik_03_rig.r" "infl_03_blend_rig_parentConstraint1.tg[0].tr";
connectAttr "ik:arm_ik_03_rig.ro" "infl_03_blend_rig_parentConstraint1.tg[0].tro"
		;
connectAttr "ik:arm_ik_03_rig.s" "infl_03_blend_rig_parentConstraint1.tg[0].ts";
connectAttr "ik:arm_ik_03_rig.pm" "infl_03_blend_rig_parentConstraint1.tg[0].tpm"
		;
connectAttr "ik:arm_ik_03_rig.jo" "infl_03_blend_rig_parentConstraint1.tg[0].tjo"
		;
connectAttr "ik:arm_ik_03_rig.ssc" "infl_03_blend_rig_parentConstraint1.tg[0].tsc"
		;
connectAttr "ik:arm_ik_03_rig.is" "infl_03_blend_rig_parentConstraint1.tg[0].tis"
		;
connectAttr "infl_03_blend_rig_parentConstraint1.w0" "infl_03_blend_rig_parentConstraint1.tg[0].tw"
		;
connectAttr "arm_fk_infl_03_anm.t" "infl_03_blend_rig_parentConstraint1.tg[1].tt"
		;
connectAttr "arm_fk_infl_03_anm.rp" "infl_03_blend_rig_parentConstraint1.tg[1].trp"
		;
connectAttr "arm_fk_infl_03_anm.rpt" "infl_03_blend_rig_parentConstraint1.tg[1].trt"
		;
connectAttr "arm_fk_infl_03_anm.r" "infl_03_blend_rig_parentConstraint1.tg[1].tr"
		;
connectAttr "arm_fk_infl_03_anm.ro" "infl_03_blend_rig_parentConstraint1.tg[1].tro"
		;
connectAttr "arm_fk_infl_03_anm.s" "infl_03_blend_rig_parentConstraint1.tg[1].ts"
		;
connectAttr "arm_fk_infl_03_anm.pm" "infl_03_blend_rig_parentConstraint1.tg[1].tpm"
		;
connectAttr "infl_03_blend_rig_parentConstraint1.w1" "infl_03_blend_rig_parentConstraint1.tg[1].tw"
		;
connectAttr "arm_data_grp.fkIk" "infl_03_blend_rig_parentConstraint1.w0";
connectAttr "reverse2.ox" "infl_03_blend_rig_parentConstraint1.w1";
connectAttr "infl_02_blend_rig.ro" "infl_02_blend_rig_parentConstraint1.cro";
connectAttr "infl_02_blend_rig.pim" "infl_02_blend_rig_parentConstraint1.cpim";
connectAttr "infl_02_blend_rig.rp" "infl_02_blend_rig_parentConstraint1.crp";
connectAttr "infl_02_blend_rig.rpt" "infl_02_blend_rig_parentConstraint1.crt";
connectAttr "infl_02_blend_rig.jo" "infl_02_blend_rig_parentConstraint1.cjo";
connectAttr "ik:arm_ik_02_rig.t" "infl_02_blend_rig_parentConstraint1.tg[0].tt";
connectAttr "ik:arm_ik_02_rig.rp" "infl_02_blend_rig_parentConstraint1.tg[0].trp"
		;
connectAttr "ik:arm_ik_02_rig.rpt" "infl_02_blend_rig_parentConstraint1.tg[0].trt"
		;
connectAttr "ik:arm_ik_02_rig.r" "infl_02_blend_rig_parentConstraint1.tg[0].tr";
connectAttr "ik:arm_ik_02_rig.ro" "infl_02_blend_rig_parentConstraint1.tg[0].tro"
		;
connectAttr "ik:arm_ik_02_rig.s" "infl_02_blend_rig_parentConstraint1.tg[0].ts";
connectAttr "ik:arm_ik_02_rig.pm" "infl_02_blend_rig_parentConstraint1.tg[0].tpm"
		;
connectAttr "ik:arm_ik_02_rig.jo" "infl_02_blend_rig_parentConstraint1.tg[0].tjo"
		;
connectAttr "ik:arm_ik_02_rig.ssc" "infl_02_blend_rig_parentConstraint1.tg[0].tsc"
		;
connectAttr "ik:arm_ik_02_rig.is" "infl_02_blend_rig_parentConstraint1.tg[0].tis"
		;
connectAttr "infl_02_blend_rig_parentConstraint1.w0" "infl_02_blend_rig_parentConstraint1.tg[0].tw"
		;
connectAttr "arm_fk_infl_02_anm.t" "infl_02_blend_rig_parentConstraint1.tg[1].tt"
		;
connectAttr "arm_fk_infl_02_anm.rp" "infl_02_blend_rig_parentConstraint1.tg[1].trp"
		;
connectAttr "arm_fk_infl_02_anm.rpt" "infl_02_blend_rig_parentConstraint1.tg[1].trt"
		;
connectAttr "arm_fk_infl_02_anm.r" "infl_02_blend_rig_parentConstraint1.tg[1].tr"
		;
connectAttr "arm_fk_infl_02_anm.ro" "infl_02_blend_rig_parentConstraint1.tg[1].tro"
		;
connectAttr "arm_fk_infl_02_anm.s" "infl_02_blend_rig_parentConstraint1.tg[1].ts"
		;
connectAttr "arm_fk_infl_02_anm.pm" "infl_02_blend_rig_parentConstraint1.tg[1].tpm"
		;
connectAttr "infl_02_blend_rig_parentConstraint1.w1" "infl_02_blend_rig_parentConstraint1.tg[1].tw"
		;
connectAttr "arm_data_grp.fkIk" "infl_02_blend_rig_parentConstraint1.w0";
connectAttr "reverse2.ox" "infl_02_blend_rig_parentConstraint1.w1";
connectAttr "infl_01_blend_rig.ro" "infl_01_blend_rig_parentConstraint1.cro";
connectAttr "infl_01_blend_rig.pim" "infl_01_blend_rig_parentConstraint1.cpim";
connectAttr "infl_01_blend_rig.rp" "infl_01_blend_rig_parentConstraint1.crp";
connectAttr "infl_01_blend_rig.rpt" "infl_01_blend_rig_parentConstraint1.crt";
connectAttr "infl_01_blend_rig.jo" "infl_01_blend_rig_parentConstraint1.cjo";
connectAttr "ik:arm_ik_01_rig.t" "infl_01_blend_rig_parentConstraint1.tg[0].tt";
connectAttr "ik:arm_ik_01_rig.rp" "infl_01_blend_rig_parentConstraint1.tg[0].trp"
		;
connectAttr "ik:arm_ik_01_rig.rpt" "infl_01_blend_rig_parentConstraint1.tg[0].trt"
		;
connectAttr "ik:arm_ik_01_rig.r" "infl_01_blend_rig_parentConstraint1.tg[0].tr";
connectAttr "ik:arm_ik_01_rig.ro" "infl_01_blend_rig_parentConstraint1.tg[0].tro"
		;
connectAttr "ik:arm_ik_01_rig.s" "infl_01_blend_rig_parentConstraint1.tg[0].ts";
connectAttr "ik:arm_ik_01_rig.pm" "infl_01_blend_rig_parentConstraint1.tg[0].tpm"
		;
connectAttr "ik:arm_ik_01_rig.jo" "infl_01_blend_rig_parentConstraint1.tg[0].tjo"
		;
connectAttr "ik:arm_ik_01_rig.ssc" "infl_01_blend_rig_parentConstraint1.tg[0].tsc"
		;
connectAttr "ik:arm_ik_01_rig.is" "infl_01_blend_rig_parentConstraint1.tg[0].tis"
		;
connectAttr "infl_01_blend_rig_parentConstraint1.w0" "infl_01_blend_rig_parentConstraint1.tg[0].tw"
		;
connectAttr "arm_fk_infl_01_anm.t" "infl_01_blend_rig_parentConstraint1.tg[1].tt"
		;
connectAttr "arm_fk_infl_01_anm.rp" "infl_01_blend_rig_parentConstraint1.tg[1].trp"
		;
connectAttr "arm_fk_infl_01_anm.rpt" "infl_01_blend_rig_parentConstraint1.tg[1].trt"
		;
connectAttr "arm_fk_infl_01_anm.r" "infl_01_blend_rig_parentConstraint1.tg[1].tr"
		;
connectAttr "arm_fk_infl_01_anm.ro" "infl_01_blend_rig_parentConstraint1.tg[1].tro"
		;
connectAttr "arm_fk_infl_01_anm.s" "infl_01_blend_rig_parentConstraint1.tg[1].ts"
		;
connectAttr "arm_fk_infl_01_anm.pm" "infl_01_blend_rig_parentConstraint1.tg[1].tpm"
		;
connectAttr "infl_01_blend_rig_parentConstraint1.w1" "infl_01_blend_rig_parentConstraint1.tg[1].tw"
		;
connectAttr "arm_data_grp.fkIk" "infl_01_blend_rig_parentConstraint1.w0";
connectAttr "reverse2.ox" "infl_01_blend_rig_parentConstraint1.w1";
connectAttr "infl_01_elbow_rig_pointConstraint1.ctx" "infl_01_elbow_rig.tx";
connectAttr "infl_01_elbow_rig_pointConstraint1.cty" "infl_01_elbow_rig.ty";
connectAttr "infl_01_elbow_rig_pointConstraint1.ctz" "infl_01_elbow_rig.tz";
connectAttr "infl_01_elbow_rig_aimConstraint1.crx" "infl_01_elbow_rig.rx";
connectAttr "infl_01_elbow_rig_aimConstraint1.cry" "infl_01_elbow_rig.ry";
connectAttr "infl_01_elbow_rig_aimConstraint1.crz" "infl_01_elbow_rig.rz";
connectAttr "infl_02_elbow_rig_pointConstraint1.ctx" "infl_02_elbow_rig.tx";
connectAttr "infl_02_elbow_rig_pointConstraint1.cty" "infl_02_elbow_rig.ty";
connectAttr "infl_02_elbow_rig_pointConstraint1.ctz" "infl_02_elbow_rig.tz";
connectAttr "infl_02_elbow_rig_aimConstraint1.crx" "infl_02_elbow_rig.rx";
connectAttr "infl_02_elbow_rig_aimConstraint1.cry" "infl_02_elbow_rig.ry";
connectAttr "infl_02_elbow_rig_aimConstraint1.crz" "infl_02_elbow_rig.rz";
connectAttr "infl_01_elbow_rig.s" "infl_02_elbow_rig.is";
connectAttr "infl_02_elbow_rig.s" "infl_03_elbow_rig.is";
connectAttr "infl_03_elbow_rig_parentConstraint1.ctx" "infl_03_elbow_rig.tx";
connectAttr "infl_03_elbow_rig_parentConstraint1.cty" "infl_03_elbow_rig.ty";
connectAttr "infl_03_elbow_rig_parentConstraint1.ctz" "infl_03_elbow_rig.tz";
connectAttr "infl_03_elbow_rig_parentConstraint1.crx" "infl_03_elbow_rig.rx";
connectAttr "infl_03_elbow_rig_parentConstraint1.cry" "infl_03_elbow_rig.ry";
connectAttr "infl_03_elbow_rig_parentConstraint1.crz" "infl_03_elbow_rig.rz";
connectAttr "infl_03_elbow_rig.ro" "infl_03_elbow_rig_parentConstraint1.cro";
connectAttr "infl_03_elbow_rig.pim" "infl_03_elbow_rig_parentConstraint1.cpim";
connectAttr "infl_03_elbow_rig.rp" "infl_03_elbow_rig_parentConstraint1.crp";
connectAttr "infl_03_elbow_rig.rpt" "infl_03_elbow_rig_parentConstraint1.crt";
connectAttr "infl_03_elbow_rig.jo" "infl_03_elbow_rig_parentConstraint1.cjo";
connectAttr "infl_03_blend_rig.t" "infl_03_elbow_rig_parentConstraint1.tg[0].tt"
		;
connectAttr "infl_03_blend_rig.rp" "infl_03_elbow_rig_parentConstraint1.tg[0].trp"
		;
connectAttr "infl_03_blend_rig.rpt" "infl_03_elbow_rig_parentConstraint1.tg[0].trt"
		;
connectAttr "infl_03_blend_rig.r" "infl_03_elbow_rig_parentConstraint1.tg[0].tr"
		;
connectAttr "infl_03_blend_rig.ro" "infl_03_elbow_rig_parentConstraint1.tg[0].tro"
		;
connectAttr "infl_03_blend_rig.s" "infl_03_elbow_rig_parentConstraint1.tg[0].ts"
		;
connectAttr "infl_03_blend_rig.pm" "infl_03_elbow_rig_parentConstraint1.tg[0].tpm"
		;
connectAttr "infl_03_blend_rig.jo" "infl_03_elbow_rig_parentConstraint1.tg[0].tjo"
		;
connectAttr "infl_03_blend_rig.ssc" "infl_03_elbow_rig_parentConstraint1.tg[0].tsc"
		;
connectAttr "infl_03_blend_rig.is" "infl_03_elbow_rig_parentConstraint1.tg[0].tis"
		;
connectAttr "infl_03_elbow_rig_parentConstraint1.w0" "infl_03_elbow_rig_parentConstraint1.tg[0].tw"
		;
connectAttr "infl_02_elbow_rig.pim" "infl_02_elbow_rig_aimConstraint1.cpim";
connectAttr "infl_02_elbow_rig.t" "infl_02_elbow_rig_aimConstraint1.ct";
connectAttr "infl_02_elbow_rig.rp" "infl_02_elbow_rig_aimConstraint1.crp";
connectAttr "infl_02_elbow_rig.rpt" "infl_02_elbow_rig_aimConstraint1.crt";
connectAttr "infl_02_elbow_rig.ro" "infl_02_elbow_rig_aimConstraint1.cro";
connectAttr "infl_02_elbow_rig.jo" "infl_02_elbow_rig_aimConstraint1.cjo";
connectAttr "infl_02_elbow_rig.is" "infl_02_elbow_rig_aimConstraint1.is";
connectAttr "infl_03_blend_rig.t" "infl_02_elbow_rig_aimConstraint1.tg[0].tt";
connectAttr "infl_03_blend_rig.rp" "infl_02_elbow_rig_aimConstraint1.tg[0].trp";
connectAttr "infl_03_blend_rig.rpt" "infl_02_elbow_rig_aimConstraint1.tg[0].trt"
		;
connectAttr "infl_03_blend_rig.pm" "infl_02_elbow_rig_aimConstraint1.tg[0].tpm";
connectAttr "infl_02_elbow_rig_aimConstraint1.w0" "infl_02_elbow_rig_aimConstraint1.tg[0].tw"
		;
connectAttr "infl_02_blend_rig.wm" "infl_02_elbow_rig_aimConstraint1.wum";
connectAttr "infl_02_elbow_rig.pim" "infl_02_elbow_rig_pointConstraint1.cpim";
connectAttr "infl_02_elbow_rig.rp" "infl_02_elbow_rig_pointConstraint1.crp";
connectAttr "infl_02_elbow_rig.rpt" "infl_02_elbow_rig_pointConstraint1.crt";
connectAttr "arm_elbow01_anm.t" "infl_02_elbow_rig_pointConstraint1.tg[0].tt";
connectAttr "arm_elbow01_anm.rp" "infl_02_elbow_rig_pointConstraint1.tg[0].trp";
connectAttr "arm_elbow01_anm.rpt" "infl_02_elbow_rig_pointConstraint1.tg[0].trt"
		;
connectAttr "arm_elbow01_anm.pm" "infl_02_elbow_rig_pointConstraint1.tg[0].tpm";
connectAttr "infl_02_elbow_rig_pointConstraint1.w0" "infl_02_elbow_rig_pointConstraint1.tg[0].tw"
		;
connectAttr "infl_01_elbow_rig.pim" "infl_01_elbow_rig_pointConstraint1.cpim";
connectAttr "infl_01_elbow_rig.rp" "infl_01_elbow_rig_pointConstraint1.crp";
connectAttr "infl_01_elbow_rig.rpt" "infl_01_elbow_rig_pointConstraint1.crt";
connectAttr "infl_01_blend_rig.t" "infl_01_elbow_rig_pointConstraint1.tg[0].tt";
connectAttr "infl_01_blend_rig.rp" "infl_01_elbow_rig_pointConstraint1.tg[0].trp"
		;
connectAttr "infl_01_blend_rig.rpt" "infl_01_elbow_rig_pointConstraint1.tg[0].trt"
		;
connectAttr "infl_01_blend_rig.pm" "infl_01_elbow_rig_pointConstraint1.tg[0].tpm"
		;
connectAttr "infl_01_elbow_rig_pointConstraint1.w0" "infl_01_elbow_rig_pointConstraint1.tg[0].tw"
		;
connectAttr "infl_01_elbow_rig.pim" "infl_01_elbow_rig_aimConstraint1.cpim";
connectAttr "infl_01_elbow_rig.t" "infl_01_elbow_rig_aimConstraint1.ct";
connectAttr "infl_01_elbow_rig.rp" "infl_01_elbow_rig_aimConstraint1.crp";
connectAttr "infl_01_elbow_rig.rpt" "infl_01_elbow_rig_aimConstraint1.crt";
connectAttr "infl_01_elbow_rig.ro" "infl_01_elbow_rig_aimConstraint1.cro";
connectAttr "infl_01_elbow_rig.jo" "infl_01_elbow_rig_aimConstraint1.cjo";
connectAttr "infl_01_elbow_rig.is" "infl_01_elbow_rig_aimConstraint1.is";
connectAttr "arm_elbow01_anm.t" "infl_01_elbow_rig_aimConstraint1.tg[0].tt";
connectAttr "arm_elbow01_anm.rp" "infl_01_elbow_rig_aimConstraint1.tg[0].trp";
connectAttr "arm_elbow01_anm.rpt" "infl_01_elbow_rig_aimConstraint1.tg[0].trt";
connectAttr "arm_elbow01_anm.pm" "infl_01_elbow_rig_aimConstraint1.tg[0].tpm";
connectAttr "infl_01_elbow_rig_aimConstraint1.w0" "infl_01_elbow_rig_aimConstraint1.tg[0].tw"
		;
connectAttr "infl_01_blend_rig.wm" "infl_01_elbow_rig_aimConstraint1.wum";
connectAttr "decomposeGuide01LocalTm.ot" "ik:arm_ik_ikChain_rig.t";
connectAttr "decomposeGuide01LocalTm.or" "ik:arm_ik_ikChain_rig.r";
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
connectAttr "guide_02_translateX.o" "guide_02.tx";
connectAttr "guide_02_translateY.o" "guide_02.ty";
connectAttr "guide_02_translateZ.o" "guide_02.tz";
connectAttr "guide_02_visibility.o" "guide_02.v";
connectAttr "guide_02_rotateX.o" "guide_02.rx";
connectAttr "guide_02_rotateY.o" "guide_02.ry";
connectAttr "guide_02_rotateZ.o" "guide_02.rz";
connectAttr "guide_02_scaleX.o" "guide_02.sx";
connectAttr "guide_02_scaleY.o" "guide_02.sy";
connectAttr "guide_02_scaleZ.o" "guide_02.sz";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "ik:arm_ik_anm.softIkRatio" "multiplyDivide1.i1x";
connectAttr "ik:softik:out.outRatio" "reverse1.ix";
connectAttr "ik:softik:out.outStretch" "multiplyDivide10.i1x";
connectAttr "ik:softik:out.outStretch" "multiplyDivide10.i1y";
connectAttr "ik:softik:out.outStretch" "multiplyDivide10.i1z";
connectAttr "ik:softik:out.outStretch" "multiplyDivide11.i1x";
connectAttr "ik:softik:out.outStretch" "multiplyDivide11.i1y";
connectAttr "ik:softik:out.outStretch" "multiplyDivide11.i1z";
connectAttr "arm_data_grp.fkIk" "reverse2.ix";
connectAttr "ik:arm_ik_ikHandleTarget_rig.wm" "ik:softik:inn.inMatrixE";
connectAttr "ik:arm_ik_ikChain_rig.wm" "ik:softik:inn.inMatrixS";
connectAttr "ik:arm_ik_anm.stretch" "ik:softik:inn.inStretch";
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
connectAttr "guide_01.m" "inn.Guide01_LocalTm";
connectAttr "guide_02.m" "inn.Guide02_LocalTm";
connectAttr "guide_03.m" "inn.Guide03_LocalTm";
connectAttr "inn.Guide01_LocalTm" "decomposeGuide01LocalTm.imat";
connectAttr "inn.Guide02_LocalTm" "decomposeGuide02LocalTm.imat";
connectAttr "inn.Guide03_LocalTm" "decomposeGuide03LocalTm.imat";
connectAttr "inn.Guide01_LocalTm" "out.CtrlFk01_BaseLocalTm";
connectAttr "inn.Guide02_LocalTm" "out.CtrlFk02_BaseLocalTm";
connectAttr "inn.Guide03_LocalTm" "out.CtrlFk03_BaseLocalTm";
connectAttr "infl_01_elbow_rig.m" "out.outInf01LocalTm";
connectAttr "infl_02_elbow_rig.m" "out.outInf02LocalTm";
connectAttr "infl_03_elbow_rig.m" "out.outInf03LocalTm";
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
connectAttr "infl_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "getLimbAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "guide_02_translateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "ik:arm_ik_03_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn";
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "decomposeGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "decomposeGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "infl_02_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn";
connectAttr "ik:locator1_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn";
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn";
connectAttr "getKneeDirection.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn"
		;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn"
		;
connectAttr "infl_02_blend_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "getKneePosProjectedOnLimbDir.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn"
		;
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[22].dn"
		;
connectAttr "infl_03_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[23].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[24].dn"
		;
connectAttr "arm_fk_infl_01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn"
		;
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[26].dn"
		;
connectAttr "arm_elbow01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[27].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[28].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[29].dn"
		;
connectAttr "arm_fk_infl_02_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[30].dn"
		;
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[31].dn";
connectAttr "getKneeDirectionNormalized.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[32].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[33].dn";
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[34].dn"
		;
connectAttr "ik:arm_ik_ikHandle_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[35].dn"
		;
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[36].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[37].dn"
		;
connectAttr "getGuide02WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[38].dn"
		;
connectAttr "arm_atts_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[39].dn"
		;
connectAttr "arm_fk_infl_03_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[40].dn"
		;
connectAttr "infl_03_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[41].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[42].dn"
		;
connectAttr "infl_03_blend_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[43].dn"
		;
connectAttr "guide_02_scaleX.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[44].dn"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[45].dn"
		;
connectAttr "guide_02_translateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[46].dn"
		;
connectAttr "getKneeDirectionOffset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[47].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[48].dn"
		;
connectAttr "getLimbMiddleAim.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[49].dn"
		;
connectAttr "infl_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[50].dn";
connectAttr "infl_03_elbow_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[51].dn"
		;
connectAttr "ik:arm_ik_02_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[52].dn"
		;
connectAttr "getSwivelDefaultPos.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[53].dn"
		;
connectAttr "guide_02_rotateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[54].dn"
		;
connectAttr "ik:arm_ik_ikChain_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[55].dn"
		;
connectAttr "arm_atts_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[56].dn"
		;
connectAttr "ik:arm_ik_swivel_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[57].dn"
		;
connectAttr "infl_02_elbow_rig_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[58].dn"
		;
connectAttr "infl_02_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[59].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[60].dn"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[61].dn"
		;
connectAttr "guide_02_rotateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[62].dn"
		;
connectAttr "ik:arm_ik_03_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[0].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[1].dn"
		;
connectAttr "infl_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[2].dn";
connectAttr "arm_fk_infl_02_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[3].dn"
		;
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[4].dn";
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[5].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[6].dn";
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[7].dn"
		;
connectAttr "arm_elbow01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[8].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[9].dn";
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[10].dn";
connectAttr "infl_02_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[11].dn"
		;
connectAttr "ik:locator1_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[12].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[13].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[14].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[15].dn"
		;
connectAttr "arm_fk_infl_01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[16].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[17].dn"
		;
connectAttr "infl_03_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[18].dn"
		;
connectAttr "infl_02_blend_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[19].dn"
		;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[20].dn"
		;
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[21].dn";
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[22].dn";
connectAttr "arm_atts_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[23].dn"
		;
connectAttr "arm_fk_infl_03_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[24].dn"
		;
connectAttr "ik:arm_ik_ikHandle_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[25].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[26].dn"
		;
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[27].dn"
		;
connectAttr "infl_03_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[28].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[29].dn"
		;
connectAttr "infl_03_blend_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[30].dn"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[31].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[32].dn"
		;
connectAttr "infl_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[33].dn";
connectAttr "infl_03_elbow_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[34].dn"
		;
connectAttr "ik:arm_ik_02_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[35].dn"
		;
connectAttr "ik:arm_ik_01_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[36].dn"
		;
connectAttr "ik:arm_ik_ikChain_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[37].dn"
		;
connectAttr "arm_atts_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[38].dn"
		;
connectAttr "infl_02_elbow_rig_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[39].dn"
		;
connectAttr "infl_02_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[40].dn"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[1].ni[41].dn"
		;
connectAttr "ik:softik:metadata.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[0].dn"
		;
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[1].dn"
		;
connectAttr "ik:softik:blendTwoAttr2.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[2].dn"
		;
connectAttr "ik:softik:distanceBetween1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[3].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[4].dn"
		;
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[5].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[6].dn"
		;
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[7].dn"
		;
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[8].dn"
		;
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[9].dn";
connectAttr "ik:softik:multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[10].dn"
		;
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[11].dn"
		;
connectAttr "ik:softik:blendTwoAttr1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[12].dn"
		;
connectAttr "ik:softik:condition1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[13].dn"
		;
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[14].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[15].dn"
		;
connectAttr "ik:softik:multiplyDivide6.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[16].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[17].dn"
		;
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[18].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[2].ni[19].dn";
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[0].dn"
		;
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[1].dn"
		;
connectAttr "multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[2].dn";
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[3].dn"
		;
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[4].dn";
connectAttr "ik:softik:multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[5].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[6].dn"
		;
connectAttr "ik:arm_ik_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[7].dn";
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[8].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[9].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[10].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[11].dn";
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[12].dn";
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[13].dn"
		;
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[14].dn"
		;
connectAttr "ik:arm_ik_ikHandle_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[15].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[16].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[17].dn";
connectAttr "ik:softik:distanceBetween1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[18].dn"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[19].dn"
		;
connectAttr "reverse1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[20].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[21].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[22].dn";
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[23].dn"
		;
connectAttr "ik:arm_ik_ikChain_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[24].dn"
		;
connectAttr "ik:softik:blendTwoAttr1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[25].dn"
		;
connectAttr "ik:softik:condition1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[26].dn"
		;
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[27].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[28].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[29].dn";
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[30].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[31].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[3].ni[32].dn";
connectAttr "ik:arm_ik_02_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[0].dn"
		;
connectAttr "infl_03_blend_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[1].dn"
		;
connectAttr "arm_atts_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[2].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[3].dn";
connectAttr "infl_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[4].dn";
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[5].dn"
		;
connectAttr "ik:arm_ik_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[6].dn";
connectAttr "guide_02_rotateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[7].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[8].dn";
connectAttr "ik:softik:distanceBetween1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[9].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[10].dn"
		;
connectAttr "infl_02_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[11].dn"
		;
connectAttr "guide_02_scaleX.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[12].dn"
		;
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[13].dn"
		;
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[14].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[15].dn"
		;
connectAttr "multiplyDivide10.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[16].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[17].dn"
		;
connectAttr "ik:softik:multiplyDivide6.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[18].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[19].dn";
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[20].dn";
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[21].dn"
		;
connectAttr "infl_03_elbow_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[22].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[23].dn"
		;
connectAttr "infl_02_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[24].dn"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[25].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[26].dn"
		;
connectAttr "ik:locator1_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[27].dn"
		;
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[28].dn"
		;
connectAttr "ik:softik:metadata.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[29].dn"
		;
connectAttr "ik:softik:condition1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[30].dn"
		;
connectAttr "infl_03_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[31].dn"
		;
connectAttr "arm_elbow01_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[32].dn"
		;
connectAttr "infl_02_elbow_rig_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[33].dn"
		;
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[34].dn"
		;
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[35].dn";
connectAttr "arm_atts_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[36].dn"
		;
connectAttr "ik:arm_ik_ikHandle_rig_softIkConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[37].dn"
		;
connectAttr "ik:softik:blendTwoAttr1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[38].dn"
		;
connectAttr "infl_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[39].dn";
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[40].dn"
		;
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[41].dn"
		;
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[42].dn"
		;
connectAttr "guide_02_rotateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[43].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[44].dn";
connectAttr "arm_elbow01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[45].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[46].dn"
		;
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[47].dn"
		;
connectAttr "guide_02_translateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[48].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[49].dn"
		;
connectAttr "ik:softik:blendTwoAttr2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[50].dn"
		;
connectAttr "multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[51].dn"
		;
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[52].dn"
		;
connectAttr "infl_03_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[53].dn"
		;
connectAttr "infl_02_blend_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[54].dn"
		;
connectAttr "multiplyDivide11.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[55].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[56].dn"
		;
connectAttr "ik:arm_ik_ikHandle_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[57].dn"
		;
connectAttr "guide_02_translateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[58].dn"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[59].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[60].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[61].dn"
		;
connectAttr "reverse1.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[62].dn";
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[63].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[64].dn"
		;
connectAttr "ik:arm_ik_ikChain_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[65].dn"
		;
connectAttr "ik:softik:multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[66].dn"
		;
connectAttr "ik:arm_ik_03_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[67].dn"
		;
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[4].ni[68].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[0].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[1].dn"
		;
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[2].dn"
		;
connectAttr "guide_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[3].dn";
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[4].dn";
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[5].dn";
connectAttr "getGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[6].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[7].dn"
		;
connectAttr "decomposeCtrlFk03DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[8].dn"
		;
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[9].dn"
		;
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[10].dn"
		;
connectAttr "arm_fk_infl_02_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[11].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[12].dn";
connectAttr "arm_fk_infl_01_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[13].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[14].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[15].dn";
connectAttr "getLimbRatio.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[16].dn";
connectAttr "decomposeGuide03WorldTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[17].dn"
		;
connectAttr "multiplyDivide13.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[18].dn"
		;
connectAttr "guide_02_translateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[19].dn"
		;
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[20].dn"
		;
connectAttr "decomposeCtrlFk01DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[21].dn"
		;
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[22].dn";
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[23].dn";
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[24].dn"
		;
connectAttr "arm_fk_infl_03_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[25].dn"
		;
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[26].dn"
		;
connectAttr "decomposeCtrlFk02DefaultLocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[27].dn"
		;
connectAttr "decomposeGuide01LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[28].dn"
		;
connectAttr ":defaultRenderUtilityList1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[29].dn"
		;
connectAttr "guide_02_scaleX.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[30].dn"
		;
connectAttr "guide_02_translateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[31].dn"
		;
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[32].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[33].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[34].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[35].dn"
		;
connectAttr "guide_02_rotateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[36].dn"
		;
connectAttr "ik:arm_ik_ikChain_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[37].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[38].dn"
		;
connectAttr "getSwivelDistance.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[39].dn"
		;
connectAttr "guide_02_rotateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[40].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[5].ni[41].dn";
connectAttr "arm_atts_anm_offset.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[0].dn"
		;
connectAttr "ik:softik:multiplyDivide5.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[1].dn"
		;
connectAttr "getLimbLength.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[2].dn";
connectAttr "ik:arm_ik_01_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[3].dn"
		;
connectAttr "guide_02_scaleZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[4].dn";
connectAttr "ik:softik:multiplyDivide4.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[5].dn"
		;
connectAttr "ik:softik:multiplyDivide2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[6].dn"
		;
connectAttr "guide_02_rotateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[7].dn"
		;
connectAttr "ik:softik:plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[8].dn"
		;
connectAttr "ik:softik:plusMinusAverage4.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[9].dn"
		;
connectAttr "getLimbSegment1Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[10].dn"
		;
connectAttr "reverse2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[11].dn";
connectAttr "guide_02_rotateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[12].dn"
		;
connectAttr "inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[13].dn";
connectAttr "infl_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[14].dn";
connectAttr "infl_03_blend_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[15].dn"
		;
connectAttr "infl_01_elbow_rig_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[16].dn"
		;
connectAttr "arm_fk_infl_01_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[17].dn"
		;
connectAttr "ik:softik:distanceBetween1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[18].dn"
		;
connectAttr "decomposeGuide02LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[19].dn"
		;
connectAttr "guide_02_translateX.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[20].dn"
		;
connectAttr "ik:arm_ik_swivelLineLoc_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[21].dn"
		;
connectAttr "ik:softik:inn.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[22].dn";
connectAttr "getLimbSegment2Length.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[23].dn"
		;
connectAttr "infl_01_elbow_rig_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[24].dn"
		;
connectAttr "ik:softik:condition2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[25].dn"
		;
connectAttr "ik:arm_ik_ikChain_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[26].dn"
		;
connectAttr "ik:arm_ik_03_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[27].dn"
		;
connectAttr "guide_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[28].dn";
connectAttr "ik:softik:out.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[29].dn";
connectAttr "ik:softik:plusMinusAverage3.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[30].dn"
		;
connectAttr "infl_02_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[31].dn"
		;
connectAttr "ik:arm_ik_ikHandleTarget_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[32].dn"
		;
connectAttr "ik:arm_ik_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[33].dn";
connectAttr "infl_01_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[34].dn"
		;
connectAttr "infl_01_blend_rig_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[35].dn"
		;
connectAttr "ik:softik:multiplyDivide3.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[36].dn"
		;
connectAttr "multiplyDivide14.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[37].dn"
		;
connectAttr "ik:locator1_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[38].dn"
		;
connectAttr "guide_02_scaleY.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[39].dn"
		;
connectAttr "arm_data_grp.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[40].dn";
connectAttr "guide_02_translateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[41].dn"
		;
connectAttr "decomposeGuide03LocalTm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[42].dn"
		;
connectAttr "ik:softik:blendTwoAttr2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[43].dn"
		;
connectAttr "arm_fk_infl_03_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[44].dn"
		;
connectAttr "multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[45].dn"
		;
connectAttr "ik:softik:multiplyDivide1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[46].dn"
		;
connectAttr "infl_03_blend_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[47].dn"
		;
connectAttr "arm_atts_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[48].dn";
connectAttr "arm_elbow01_anm.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[49].dn"
		;
connectAttr "infl_02_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[50].dn"
		;
connectAttr "guide_02_scaleX.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[51].dn"
		;
connectAttr "guide_02_translateZ.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[52].dn"
		;
connectAttr "guide_02_rotateY.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[53].dn"
		;
connectAttr "ik:softik:plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[54].dn"
		;
connectAttr "ik:softik:multiplyDivide6.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[55].dn"
		;
connectAttr "infl_02_elbow_rig_pointConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[56].dn"
		;
connectAttr "infl_02_elbow_rig_aimConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[57].dn"
		;
connectAttr "ik:softik:clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[58].dn"
		;
connectAttr "infl_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[59].dn";
connectAttr "guide_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[60].dn";
connectAttr "arm_atts_anm_offset_parentConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[61].dn"
		;
connectAttr "infl_01_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[62].dn"
		;
connectAttr "infl_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[63].dn";
connectAttr "ik:arm_ik_03_rig_orientConstraint1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[64].dn"
		;
connectAttr "out.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[65].dn";
connectAttr "decomposeMatrix2.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[66].dn"
		;
connectAttr "decomposeMatrix3.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[67].dn"
		;
connectAttr "decomposeMatrix1.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[68].dn"
		;
connectAttr "infl_03_elbow_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[6].ni[69].dn"
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
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "ikRPsolver.msg" ":ikSystem.sol" -na;
// End of limb-0.0.2.ma
