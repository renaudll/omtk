//Maya ASCII 2016 scene
//Name: test_interactivefk01.ma
//Last modified: Fri, Dec 16, 2016 01:24:02 PM
//Codeset: UTF-8
requires maya "2016";
requires "stereoCamera" "10.0";
requires -nodeType "ilrOptionsNode" -nodeType "ilrUIOptionsNode" -nodeType "ilrBakeLayerManager"
		 -nodeType "ilrBakeLayer" "Turtle" "2016.0.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2016";
fileInfo "version" "2016";
fileInfo "cutIdentifier" "201603180400-990260";
fileInfo "osv" "Linux 3.10.0-327.36.3.el7.x86_64 #1 SMP Mon Oct 24 16:09:20 UTC 2016 x86_64";
createNode transform -s -n "persp";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000241";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 20.037696156177184 8.5452516660551137 -12.356276629628187 ;
	setAttr ".r" -type "double3" -18.338352729309612 -602.60000000014304 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000242";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 25.809620095136683;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000243";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000244";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000245";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0.81201162186464915 0.87887499909309152 100.10170287410062 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000246";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 17.05503611463261;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000247";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 -3.200120658396691 -0.66550630819820977 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000248";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 19.937141485198481;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "All_Grp";
	rename -uid "D220D860-0000-7E80-582E-184E000012DB";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "FX_Grp" -p "All_Grp";
	rename -uid "D220D860-0000-7E80-582E-184E000012E4";
	setAttr ".v" no;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "Model_Grp" -p "All_Grp";
	rename -uid "D220D860-0000-7E80-582E-184E000012DE";
	setAttr ".v" no;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "Proxy_Grp" -p "All_Grp";
	rename -uid "D220D860-0000-7E80-582E-184E000012E1";
	setAttr ".v" no;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "Render_Grp" -p "All_Grp";
	rename -uid "D220D860-0000-7E80-582E-184E000012D8";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode transform -n "root";
	rename -uid "CA0C18C0-0000-079D-5852-C53E000020E8";
createNode transform -n "layer1" -p "root";
	rename -uid "B5FD68C0-0000-6090-582F-2F8F00005BED";
createNode transform -n "layer1_surface" -p "layer1";
	rename -uid "CA0C18C0-0000-079D-5852-C8CC00004CB8";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsSurface -n "layer1_surfaceShape" -p "layer1_surface";
	rename -uid "CA0C18C0-0000-079D-5852-C8CC00004CB7";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
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
createNode nurbsSurface -n "layer1_surfaceShapeOrig" -p "layer1_surface";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B614";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		2 2 0 0 no 
		4 0 0 1 1
		5 0 0 0.5 1 1
		
		12
		-2.5 -2.5 5.2449534233389448e-16
		-2.5 -1.25 2.6224767116694724e-16
		-2.5 1.25 -2.6224767116694729e-16
		-2.5 2.5 -5.2449534233389448e-16
		0 -2.5 5.2449534233389448e-16
		0 -1.25 2.6224767116694724e-16
		0 1.25 -2.6224767116694734e-16
		0 2.5 -5.2449534233389448e-16
		2.5 -2.5 5.2449534233389448e-16
		2.5 -1.25 2.6224767116694724e-16
		2.5 1.25 -2.6224767116694729e-16
		2.5 2.5 -5.2449534233389448e-16
		
		;
createNode joint -n "jnt_layer1_01" -p "layer1";
	rename -uid "B5FD68C0-0000-6090-582F-2F8F00005BF2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0 2.492057365218753 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057365218753 0 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer1_02" -p "layer1";
	rename -uid "B5FD68C0-0000-6090-582F-2F8F00005BF4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 -2.4920573652187534 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.4920573652187534 0 1;
	setAttr ".radi" 4;
createNode transform -n "layer2" -p "root";
	rename -uid "B5FD68C0-0000-6090-582F-299600000C2B";
createNode transform -n "layer2_surface" -p "layer2";
	rename -uid "CA0C18C0-0000-079D-5852-C8F600004CE3";
	addAttr -ci true -sn "dr" -ln "dropoff" -dv 4 -min 0 -max 20 -at "double";
	addAttr -ci true -sn "wsm" -ln "wrapSamples" -dv 10 -min 1 -at "short";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr -k on ".dr";
	setAttr -k on ".wsm";
createNode nurbsSurface -n "layer2_surfaceShapeOrig" -p "layer2_surface";
	rename -uid "CA0C18C0-0000-079D-5852-C8F600004CE5";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		2 2 0 0 no 
		4 0 0 1 1
		5 0 0 0.5 1 1
		
		12
		-0.5 -3.061616997868383e-17 0.5
		-0.5 -1.5308084989341915e-17 0.25
		-0.5 1.5308084989341915e-17 -0.25
		-0.5 3.061616997868383e-17 -0.5
		0 -3.061616997868383e-17 0.5
		0 -1.5308084989341915e-17 0.25
		0 1.5308084989341915e-17 -0.25
		0 3.061616997868383e-17 -0.5
		0.5 -3.061616997868383e-17 0.5
		0.5 -1.5308084989341915e-17 0.25
		0.5 1.5308084989341915e-17 -0.25
		0.5 3.061616997868383e-17 -0.5
		
		;
createNode nurbsSurface -n "layer2_surfaceShapeDeformed" -p "layer2_surface";
	rename -uid "CA0C18C0-0000-079D-5852-C90300004CFD";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".mb" no;
	setAttr ".csh" no;
	setAttr ".rcsh" no;
	setAttr ".vis" no;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		2 2 0 0 no 
		4 0 0 1 1
		5 0 0 0.5 1 1
		
		12
		-2.5 -2.5 5.2449534233389448e-16
		-2.4999999999999996 -1.2499999999999998 2.6224767116694724e-16
		-2.5000000000000004 1.2500000000000002 -2.6224767116694729e-16
		-2.5 2.5 -5.2449534233389458e-16
		0 -2.5 5.2449534233389448e-16
		0 -1.25 2.6224767116694724e-16
		0 1.2500000000000004 -2.6224767116694734e-16
		0 2.5 -5.2449534233389448e-16
		2.5 -2.5 5.2449534233389448e-16
		2.4999999999999996 -1.2499999999999998 2.6224767116694724e-16
		2.5000000000000004 1.2500000000000002 -2.6224767116694729e-16
		2.5 2.5 -5.2449534233389458e-16
		
		;
createNode nurbsSurface -n "layer2_surfaceShapeDeformedDeformed" -p "layer2_surface";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B61E";
	setAttr -k off ".v";
	setAttr -s 6 ".iog[0].og";
	setAttr ".mb" no;
	setAttr ".csh" no;
	setAttr ".rcsh" no;
	setAttr ".vis" no;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
createNode transform -n "layer2_surfaceBase" -p "layer2";
	rename -uid "CA0C18C0-0000-079D-5852-F56A00013334";
	addAttr -ci true -sn "dr" -ln "dropoff" -dv 4 -min 0 -max 20 -at "double";
	addAttr -ci true -sn "wsm" -ln "wrapSamples" -dv 10 -min 1 -at "short";
	setAttr ".v" no;
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr -k on ".dr";
	setAttr -k on ".wsm";
createNode nurbsSurface -n "layer2_surfaceBaseShapeDeformedDeformed" -p "layer2_surfaceBase";
	rename -uid "CA0C18C0-0000-079D-5852-F56A00013337";
	setAttr -k off ".v";
	setAttr ".mb" no;
	setAttr ".csh" no;
	setAttr ".rcsh" no;
	setAttr ".vis" no;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		2 2 0 0 no 
		4 0 0 1 1
		5 0 0 0.5 1 1
		
		12
		-2.5 -2.5 5.2449534233389448e-16
		-2.4999999999999996 -1.2499999999999998 2.6224767116694724e-16
		-2.5000000000000004 1.2500000000000002 -2.6224767116694729e-16
		-2.5 2.5 -5.2449534233389458e-16
		0 -2.5 5.2449534233389448e-16
		0 -1.25 2.6224767116694724e-16
		0 1.2500000000000004 -2.6224767116694739e-16
		0 2.5 -5.2449534233389448e-16
		2.5 -2.5 5.2449534233389448e-16
		2.4999999999999996 -1.2499999999999998 2.6224767116694724e-16
		2.5000000000000004 1.2500000000000002 -2.6224767116694729e-16
		2.5 2.5 -5.2449534233389458e-16
		
		;
createNode joint -n "jnt_layer2_01" -p "layer2";
	rename -uid "B5FD68C0-0000-6090-582F-297A00000C07";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0 2.492057365218753 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057365218753 0 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer2_02" -p "layer2";
	rename -uid "B5FD68C0-0000-6090-582F-297A00000C08";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 1.0394179847893683e-16 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 1.0394179847893683e-16 0 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer2_03" -p "layer2";
	rename -uid "B5FD68C0-0000-6090-582F-297A00000C09";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 -2.4920573652187534 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.4920573652187534 0 1;
	setAttr ".radi" 4;
createNode transform -n "layer3" -p "root";
	rename -uid "CA0C18C0-0000-079D-5852-E5330000DB7C";
createNode transform -n "layer3_surface" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E3820000DB38";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsSurface -n "layer3_surfaceShape" -p "layer3_surface";
	rename -uid "CA0C18C0-0000-079D-5852-E3820000DB37";
	setAttr -k off ".v";
	setAttr -s 6 ".iog[0].og";
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
createNode nurbsSurface -n "layer3_surfaceShapeOrig" -p "layer3_surface";
	rename -uid "CA0C18C0-0000-079D-5852-F56A0001332C";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		6 0 0 0 2 2 2
		13 -2 -1 0 1 2 3 4 5 6 7 8
		 9 10
		
		44
		1.9590290622280593 -2.5 -1.9590290622280635
		2.7704854688859699 -2.5000000000000004 1.6299841530231401e-16
		1.9590290622280613 -2.5 1.9590290622280606
		7.9178811486417574e-16 -2.5000000000000009 2.7704854688859704
		-1.9590290622280606 -2.4999999999999991 1.9590290622280606
		-2.7704854688859704 -2.5 6.8172049100421083e-16
		-1.9590290622280606 -2.4999999999999996 -1.9590290622280602
		-1.4629149925032931e-15 -2.5 -2.7704854688859699
		1.9590290622280593 -2.5 -1.9590290622280635
		2.7704854688859699 -2.5000000000000004 1.6299841530231401e-16
		1.9590290622280613 -2.5 1.9590290622280606
		1.9590290622280593 -0.83333333333333315 -1.9590290622280626
		2.7704854688859699 -0.83333333333333315 2.6505231523126006e-16
		1.9590290622280613 -0.8333333333333337 1.9590290622280615
		7.7715611723760978e-16 -0.83333333333333359 2.7704854688859699
		-1.9590290622280606 -0.8333333333333337 1.9590290622280617
		-2.7704854688859708 -0.83333333333333359 7.8377439093315689e-16
		-1.9590290622280615 -0.83333333333333359 -1.9590290622280597
		-1.4988010832439611e-15 -0.83333333333333315 -2.7704854688859699
		1.9590290622280593 -0.83333333333333315 -1.9590290622280626
		2.7704854688859699 -0.83333333333333315 2.6505231523126006e-16
		1.9590290622280613 -0.8333333333333337 1.9590290622280615
		1.9590290622280595 0.83333333333333326 -1.9590290622280626
		2.7704854688859699 0.83333333333333315 3.6710621516020607e-16
		1.9590290622280611 0.83333333333333315 1.9590290622280611
		7.7715611723760978e-16 0.83333333333333326 2.7704854688859704
		-1.9590290622280606 0.83333333333333326 1.9590290622280617
		-2.7704854688859699 0.83333333333333315 8.8582829086210304e-16
		-1.9590290622280613 0.8333333333333337 -1.9590290622280595
		-1.5265566588595904e-15 0.8333333333333337 -2.7704854688859704
		1.9590290622280595 0.83333333333333326 -1.9590290622280626
		2.7704854688859699 0.83333333333333315 3.6710621516020607e-16
		1.9590290622280611 0.83333333333333315 1.9590290622280611
		1.9590290622280604 2.5 -1.9590290622280628
		2.7704854688859699 2.5 4.6916011508915222e-16
		1.9590290622280604 2.5 1.9590290622280615
		7.5667132056041693e-16 2.5 2.7704854688859699
		-1.9590290622280606 2.5000000000000004 1.9590290622280626
		-2.7704854688859699 2.5 9.878821907910488e-16
		-1.9590290622280615 2.5000000000000004 -1.9590290622280595
		-1.5028072818909488e-15 2.4999999999999996 -2.7704854688859699
		1.9590290622280604 2.5 -1.9590290622280628
		2.7704854688859699 2.5 4.6916011508915222e-16
		1.9590290622280604 2.5 1.9590290622280615
		
		;
createNode joint -n "jnt_layer3_01" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E39A0000DB49";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 2.4920573652187534 2.492057365218753 0 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer3_02" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E5080000DB5B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.492057 2.492057365218753 0 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer3_03" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E50C0000DB5E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 2.492057365218753 -2.492 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer3_04" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E5150000DB61";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 2.492057365218753 2.492 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer3_05" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E51A0000DB6A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 -2.492057 2.492 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer3_06" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E51A0000DB6B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 -2.492057 -2.492 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer3_07" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E51A0000DB6C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.492057 -2.492057 0 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_layer3_08" -p "layer3";
	rename -uid "CA0C18C0-0000-079D-5852-E51A0000DB6D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4920573652187534 -2.492057 0 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_root";
	rename -uid "CA0C18C0-0000-079D-5852-F75B000146B9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057365218753 0 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_01" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA9D000005A2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4920573652187534 2.492057365218753 0 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-16 0 0 1 0 0
		 1.2246467991473532e-16 0 -1 0 2.4920573652187534 2.492057365218753 0 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_02" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA9D000005A3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5740186612595934 2.492057365218753 1.9260457613151178 ;
	setAttr ".r" -type "double3" 0 129.25665823369263 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824326 0 -0.77431911336924275 0 0 1 0 0
		 0.77431911336924275 0 -0.63279531498824326 0 1.5740186612595934 2.492057365218753 1.9260457613151178 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_03" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA9D000005A4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.53457986492992582 2.492057365218753 2.4367208031443206 ;
	setAttr ".r" -type "double3" 0 77.62619886091106 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.21428871510029623 0 -0.97677036532680706 0 0 1 0 0
		 0.97677036532680706 0 0.21428871510029623 0 -0.53457986492992582 2.492057365218753 2.4367208031443206 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_04" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA9D000005A5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2481967600856629 2.4920573652187548 1.0943534176986121 ;
	setAttr ".r" -type "double3" -1.0433039991593118e-14 25.955402232116771 -4.5270837327847803e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.89913499239525185 0 -0.43767141264925025 0 0 1 0 0
		 0.43767141264925025 0 0.89913499239525185 0 -2.2481967600856629 2.4920573652187548 1.0943534176986121 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_05" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA9D000005A6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2481967600856638 2.492057365218753 -1.0943534176986087 ;
	setAttr ".r" -type "double3" 0 -25.955402232116693 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.89913499239525252 0 0.43767141264924903 0 0 1 0 0
		 -0.43767141264924903 0 0.89913499239525252 0 -2.2481967600856638 2.492057365218753 -1.0943534176986087 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_06" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA9D000005A7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.53457986492992904 2.4920573652187539 -2.4367208031443202 ;
	setAttr ".r" -type "double3" 7.657390024976933e-14 -77.626198860910989 -9.5194148230941359e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.21428871510029768 0 0.97677036532680672 0 0 1 0 0
		 -0.97677036532680672 0 0.21428871510029768 0 -0.53457986492992904 2.4920573652187539 -2.4367208031443202 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_07" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA9D000005A8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5740186612595912 2.4920573652187534 -1.9260457613151192 ;
	setAttr ".r" -type "double3" -2.5444437451708134e-14 230.74334176630742 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824237 0 0.77431911336924342 0 0 1 0 0
		 -0.77431911336924342 0 -0.63279531498824237 0 1.5740186612595912 2.4920573652187534 -1.9260457613151192 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_08" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA9D000005A9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4920573652187534 2.492057365218753 -2.2204460492503131e-16 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-16 0 0 1 0 0
		 1.2246467991473532e-16 0 -1 0 2.4920573652187534 2.492057365218753 -2.2204460492503131e-16 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_09" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA0900000574";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2481967600856629 -2.4920573652187543 1.0943534176986112 ;
	setAttr ".r" -type "double3" 2.6082599978982784e-15 25.95540223211675 1.1317709331961951e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.89913499239525208 0 -0.43767141264924991 0 0 1 0 0
		 0.43767141264924991 0 0.89913499239525208 0 -2.2481967600856629 -2.4920573652187543 1.0943534176986112 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_10" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA0900000575";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.2481967600856638 -2.4920573652187534 -1.0943534176986087 ;
	setAttr ".r" -type "double3" 2.6082599978982717e-15 -25.955402232116693 -1.1317709331961951e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.89913499239525252 0 0.43767141264924903 0 0 1 0 0
		 -0.43767141264924903 0 0.89913499239525252 0 -2.2481967600856638 -2.4920573652187534 -1.0943534176986087 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_11" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA0900000576";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.53457986492992904 -2.4920573652187543 -2.436720803144321 ;
	setAttr ".r" -type "double3" -3.8286950124884665e-14 -77.626198860910989 4.7597074115470673e-14 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.21428871510029768 0 0.97677036532680672 0 0 1 0 0
		 -0.97677036532680672 0 0.21428871510029768 0 -0.53457986492992904 -2.4920573652187543 -2.436720803144321 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_12" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA0900000577";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4920573652187534 -2.4920573652187534 -3.3306690738754696e-16 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-16 0 0 1 0 0
		 1.2246467991473532e-16 0 -1 0 2.4920573652187534 -2.4920573652187534 -3.3306690738754696e-16 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_13" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA0900000578";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5740186612595912 -2.4920573652187543 -1.9260457613151187 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 230.74334176630742 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824237 0 0.77431911336924342 0 0 1 0 0
		 -0.77431911336924342 0 -0.63279531498824237 0 1.5740186612595912 -2.4920573652187543 -1.9260457613151187 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_14" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA0900000579";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.4920573652187534 -2.4920573652187534 -5.5511151231257827e-16 ;
	setAttr ".r" -type "double3" 0 180 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-16 0 0 1 0 0
		 1.2246467991473532e-16 0 -1 0 2.4920573652187534 -2.4920573652187534 -5.5511151231257827e-16 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_15" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA090000057A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.53457986492992582 -2.4920573652187539 2.4367208031443206 ;
	setAttr ".r" -type "double3" 0 77.62619886091106 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.21428871510029623 0 -0.97677036532680706 0 0 1 0 0
		 0.97677036532680706 0 0.21428871510029623 0 -0.53457986492992582 -2.4920573652187539 2.4367208031443206 1;
	setAttr ".radi" 6.5;
createNode joint -n "jnt_out_16" -p "jnt_root";
	rename -uid "D220D860-0000-7E80-582C-CA090000057B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.5740186612595934 -2.4920573652187534 1.926045761315117 ;
	setAttr ".r" -type "double3" 2.5444437451708134e-14 129.25665823369266 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.63279531498824348 0 -0.77431911336924242 0 0 1 0 0
		 0.77431911336924242 0 -0.63279531498824348 0 1.5740186612595934 -2.4920573652187534 1.926045761315117 1;
	setAttr ".radi" 6.5;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "DABEE8C0-0000-5D52-5854-311200000FF6";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "DABEE8C0-0000-5D52-5854-311200000FF7";
	setAttr -s 4 ".dli[1:3]"  1 2 3;
	setAttr -s 4 ".dli";
createNode displayLayer -n "defaultLayer";
	rename -uid "D220D860-0000-7E80-582C-AFFF0000025F";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "DABEE8C0-0000-5D52-5854-311200000FF9";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "D220D860-0000-7E80-582C-AFFF00000261";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "D220D860-0000-7E80-582C-BC2B00000491";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 1\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n"
		+ "            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 1\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n"
		+ "                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n"
		+ "                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n"
		+ "                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n"
		+ "            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n"
		+ "            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n"
		+ "            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n"
		+ "                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 1\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n"
		+ "                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n"
		+ "                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n"
		+ "            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n"
		+ "\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 1\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n"
		+ "                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n"
		+ "                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n"
		+ "                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1293\n                -height 1250\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n"
		+ "            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n"
		+ "            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n"
		+ "            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1293\n            -height 1250\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n"
		+ "                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n"
		+ "                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n"
		+ "            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n"
		+ "            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n"
		+ "                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n"
		+ "                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n"
		+ "                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n"
		+ "                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n"
		+ "                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n"
		+ "                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n"
		+ "                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n"
		+ "                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n"
		+ "                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n"
		+ "                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n"
		+ "                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n"
		+ "                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n"
		+ "                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -image \"T:/Maya_Tak/data/TK_Test_1032_Sc007_v01_DQ_retake_01.ma_TK_Tak_hairSystem_Tak__HairShape.mchp\" \n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n"
		+ "                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n"
		+ "                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -image \"T:/Maya_Tak/data/TK_Test_1032_Sc007_v01_DQ_retake_01.ma_TK_Tak_hairSystem_Tak__HairShape.mchp\" \n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\tif ($useSceneConfig) {\n\t\tscriptedPanel -e -to $panelName;\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"profilerPanel\" -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"Stereo\" -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels `;\n"
		+ "string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -editorChanged \"updateModelPanelBar\" \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n"
		+ "                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererOverrideName \"stereoOverrideVP2\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n"
		+ "                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n"
		+ "                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -editorChanged \"updateModelPanelBar\" \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n"
		+ "                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererOverrideName \"stereoOverrideVP2\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n"
		+ "                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n"
		+ "                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 1\n"
		+ "                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n"
		+ "                -defaultPinnedState 0\n                -additiveGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n"
		+ "\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 35 100 -ps 2 65 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Outliner\")) \n\t\t\t\t\t\"outlinerPanel\"\n\t\t\t\t\t\"$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 0\\n    -showReferenceMembers 0\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    $editorName\"\n"
		+ "\t\t\t\t\t\"outlinerPanel -edit -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 0\\n    -showReferenceMembers 0\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1293\\n    -height 1250\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1293\\n    -height 1250\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "D220D860-0000-7E80-582C-BC2B00000492";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode displayLayer -n "layer_anm";
	rename -uid "D220D860-0000-7E80-582D-E40F00000C0C";
	setAttr ".c" 17;
	setAttr ".do" 1;
createNode displayLayer -n "layer_rig";
	rename -uid "D220D860-0000-7E80-582D-E40F00000C0D";
	setAttr ".dt" 2;
	setAttr ".c" 13;
	setAttr ".do" 2;
createNode displayLayer -n "layer_geo";
	rename -uid "D220D860-0000-7E80-582D-E40F00000C0E";
	setAttr ".dt" 2;
	setAttr ".c" 12;
	setAttr ".do" 3;
createNode makeNurbCircle -n "makeNurbCircle2";
	rename -uid "D220D860-0000-7E80-582D-E40F00000C60";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle3";
	rename -uid "D220D860-0000-7E80-582D-E41000000CDE";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle4";
	rename -uid "D220D860-0000-7E80-582D-E41000000D5C";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle5";
	rename -uid "D220D860-0000-7E80-582D-E41000000DDA";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle6";
	rename -uid "D220D860-0000-7E80-582D-E41000000E58";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle7";
	rename -uid "D220D860-0000-7E80-582D-E41000000ED6";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle8";
	rename -uid "D220D860-0000-7E80-582D-E41000000F54";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle10";
	rename -uid "D220D860-0000-7E80-582E-184E0000132C";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle11";
	rename -uid "D220D860-0000-7E80-582E-184E000013AA";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle12";
	rename -uid "D220D860-0000-7E80-582E-184F00001428";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle13";
	rename -uid "D220D860-0000-7E80-582E-184F000014A6";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle14";
	rename -uid "D220D860-0000-7E80-582E-184F00001524";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle15";
	rename -uid "D220D860-0000-7E80-582E-184F000015A2";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle16";
	rename -uid "D220D860-0000-7E80-582E-184F00001620";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle17";
	rename -uid "D220D860-0000-7E80-582E-184F000016AC";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle18";
	rename -uid "D220D860-0000-7E80-582E-18500000172A";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle19";
	rename -uid "D220D860-0000-7E80-582E-1850000017A8";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle20";
	rename -uid "D220D860-0000-7E80-582E-185000001826";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle21";
	rename -uid "D220D860-0000-7E80-582E-1850000018A4";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle22";
	rename -uid "D220D860-0000-7E80-582E-185000001922";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle23";
	rename -uid "D220D860-0000-7E80-582E-1851000019A0";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle24";
	rename -uid "D220D860-0000-7E80-582E-185100001A2C";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle25";
	rename -uid "D220D860-0000-7E80-582E-185100001AAA";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle26";
	rename -uid "D220D860-0000-7E80-582E-185100001B28";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle27";
	rename -uid "D220D860-0000-7E80-582E-185100001BA6";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle28";
	rename -uid "D220D860-0000-7E80-582E-185200001C24";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle29";
	rename -uid "D220D860-0000-7E80-582E-185200001CA2";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle30";
	rename -uid "D220D860-0000-7E80-582E-185200001D20";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle31";
	rename -uid "D220D860-0000-7E80-582E-185200001DAC";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle32";
	rename -uid "D220D860-0000-7E80-582E-185200001E2A";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle33";
	rename -uid "D220D860-0000-7E80-582E-185200001EA8";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle34";
	rename -uid "D220D860-0000-7E80-582E-185300001F26";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle35";
	rename -uid "D220D860-0000-7E80-582E-185300001FA4";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle36";
	rename -uid "D220D860-0000-7E80-582E-185300002022";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle37";
	rename -uid "D220D860-0000-7E80-582E-1853000020A0";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle38";
	rename -uid "D220D860-0000-7E80-582E-18530000212C";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle39";
	rename -uid "D220D860-0000-7E80-582E-1854000021AA";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle40";
	rename -uid "D220D860-0000-7E80-582E-185400002228";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle41";
	rename -uid "D220D860-0000-7E80-582E-1854000022A6";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle42";
	rename -uid "D220D860-0000-7E80-582E-185400002324";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle43";
	rename -uid "D220D860-0000-7E80-582E-1854000023A2";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle44";
	rename -uid "D220D860-0000-7E80-582E-185500002420";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle45";
	rename -uid "D220D860-0000-7E80-582E-1855000024AC";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle46";
	rename -uid "D220D860-0000-7E80-582E-18550000252A";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle47";
	rename -uid "D220D860-0000-7E80-582E-1855000025A8";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle48";
	rename -uid "D220D860-0000-7E80-582E-185500002626";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle49";
	rename -uid "D220D860-0000-7E80-582E-1856000026A4";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle50";
	rename -uid "D220D860-0000-7E80-582E-185600002722";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle51";
	rename -uid "D220D860-0000-7E80-582E-1856000027A0";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle52";
	rename -uid "D220D860-0000-7E80-582E-18560000282C";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle53";
	rename -uid "D220D860-0000-7E80-582E-1856000028AA";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle54";
	rename -uid "D220D860-0000-7E80-582E-185700002928";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle55";
	rename -uid "D220D860-0000-7E80-582E-1857000029A6";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle56";
	rename -uid "D220D860-0000-7E80-582E-185700002A24";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle57";
	rename -uid "D220D860-0000-7E80-582E-185700002AA2";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle58";
	rename -uid "D220D860-0000-7E80-582E-185700002B20";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle59";
	rename -uid "D220D860-0000-7E80-582E-194A00002C19";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle60";
	rename -uid "D220D860-0000-7E80-582E-194A00002C97";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle61";
	rename -uid "D220D860-0000-7E80-582E-194A00002D15";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle62";
	rename -uid "D220D860-0000-7E80-582E-194B00002D93";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle63";
	rename -uid "D220D860-0000-7E80-582E-194B00002E11";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle64";
	rename -uid "D220D860-0000-7E80-582E-194B00002E8F";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle65";
	rename -uid "D220D860-0000-7E80-582E-194B00002F0D";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle66";
	rename -uid "D220D860-0000-7E80-582E-194C00002F99";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle67";
	rename -uid "D220D860-0000-7E80-582E-194C00003017";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle68";
	rename -uid "D220D860-0000-7E80-582E-194C00003095";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle69";
	rename -uid "D220D860-0000-7E80-582E-194C00003113";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle70";
	rename -uid "D220D860-0000-7E80-582E-194C00003191";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle71";
	rename -uid "D220D860-0000-7E80-582E-194D0000320F";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle72";
	rename -uid "D220D860-0000-7E80-582E-194D0000328D";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle73";
	rename -uid "D220D860-0000-7E80-582E-194D00003319";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle74";
	rename -uid "D220D860-0000-7E80-582E-194D00003397";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle75";
	rename -uid "D220D860-0000-7E80-582E-194D00003415";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle76";
	rename -uid "D220D860-0000-7E80-582E-194E00003493";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle77";
	rename -uid "D220D860-0000-7E80-582E-194E00003511";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle78";
	rename -uid "D220D860-0000-7E80-582E-194E0000358F";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle79";
	rename -uid "D220D860-0000-7E80-582E-194E0000360D";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle80";
	rename -uid "D220D860-0000-7E80-582E-194E00003699";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle81";
	rename -uid "D220D860-0000-7E80-582E-194F00003717";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle82";
	rename -uid "D220D860-0000-7E80-582E-194F00003795";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle83";
	rename -uid "D220D860-0000-7E80-582E-194F00003813";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle84";
	rename -uid "D220D860-0000-7E80-582E-194F00003891";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle85";
	rename -uid "D220D860-0000-7E80-582E-19500000390F";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle86";
	rename -uid "D220D860-0000-7E80-582E-19500000398D";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle87";
	rename -uid "D220D860-0000-7E80-582E-195000003A19";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle88";
	rename -uid "D220D860-0000-7E80-582E-195000003A97";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle89";
	rename -uid "D220D860-0000-7E80-582E-195100003B15";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle90";
	rename -uid "D220D860-0000-7E80-582E-195100003B93";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle91";
	rename -uid "D220D860-0000-7E80-582E-195100003C11";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle92";
	rename -uid "D220D860-0000-7E80-582E-195200003C8F";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle93";
	rename -uid "D220D860-0000-7E80-582E-195200003D0D";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle94";
	rename -uid "D220D860-0000-7E80-582E-195200003D99";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle95";
	rename -uid "D220D860-0000-7E80-582E-195200003E17";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle96";
	rename -uid "D220D860-0000-7E80-582E-195300003E95";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle97";
	rename -uid "D220D860-0000-7E80-582E-195300003F13";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle98";
	rename -uid "D220D860-0000-7E80-582E-195300003F91";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle99";
	rename -uid "D220D860-0000-7E80-582E-19530000400F";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle100";
	rename -uid "D220D860-0000-7E80-582E-19540000408D";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle101";
	rename -uid "D220D860-0000-7E80-582E-195400004119";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle102";
	rename -uid "D220D860-0000-7E80-582E-195400004197";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle103";
	rename -uid "D220D860-0000-7E80-582E-195400004215";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle104";
	rename -uid "D220D860-0000-7E80-582E-195500004293";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle105";
	rename -uid "D220D860-0000-7E80-582E-195500004311";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle106";
	rename -uid "D220D860-0000-7E80-582E-19550000438F";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle107";
	rename -uid "D220D860-0000-7E80-582E-19560000440D";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle108";
	rename -uid "D220D860-0000-7E80-582E-1A6C00004504";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle109";
	rename -uid "D220D860-0000-7E80-582E-1A6C00004582";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle110";
	rename -uid "D220D860-0000-7E80-582E-1A6C00004600";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle111";
	rename -uid "D220D860-0000-7E80-582E-1A6C0000467E";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle112";
	rename -uid "D220D860-0000-7E80-582E-1A6C000046FC";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle113";
	rename -uid "D220D860-0000-7E80-582E-1A6D0000477A";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle114";
	rename -uid "D220D860-0000-7E80-582E-1A6D000047F8";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle115";
	rename -uid "D220D860-0000-7E80-582E-1A6D00004884";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle116";
	rename -uid "D220D860-0000-7E80-582E-1A6D00004902";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle117";
	rename -uid "D220D860-0000-7E80-582E-1A6D00004980";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle118";
	rename -uid "D220D860-0000-7E80-582E-1A6E000049FE";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle119";
	rename -uid "D220D860-0000-7E80-582E-1A6E00004A7C";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle120";
	rename -uid "D220D860-0000-7E80-582E-1A6E00004AFA";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle121";
	rename -uid "D220D860-0000-7E80-582E-1A6E00004B78";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle122";
	rename -uid "D220D860-0000-7E80-582E-1A6E00004C04";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle123";
	rename -uid "D220D860-0000-7E80-582E-1A6F00004C82";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle124";
	rename -uid "D220D860-0000-7E80-582E-1A6F00004D00";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle125";
	rename -uid "D220D860-0000-7E80-582E-1A6F00004D7E";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle126";
	rename -uid "D220D860-0000-7E80-582E-1A6F00004DFC";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle127";
	rename -uid "D220D860-0000-7E80-582E-1A6F00004E7A";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle128";
	rename -uid "D220D860-0000-7E80-582E-1A7000004EF8";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle129";
	rename -uid "D220D860-0000-7E80-582E-1A7000004F84";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle130";
	rename -uid "D220D860-0000-7E80-582E-1A7000005002";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle131";
	rename -uid "D220D860-0000-7E80-582E-1A7000005080";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle132";
	rename -uid "D220D860-0000-7E80-582E-1A70000050FE";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle133";
	rename -uid "D220D860-0000-7E80-582E-1A710000517C";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle134";
	rename -uid "D220D860-0000-7E80-582E-1A71000051FA";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle135";
	rename -uid "D220D860-0000-7E80-582E-1A7100005278";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle136";
	rename -uid "D220D860-0000-7E80-582E-1A7100005304";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle137";
	rename -uid "D220D860-0000-7E80-582E-1A7100005382";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle138";
	rename -uid "D220D860-0000-7E80-582E-1A7100005400";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle139";
	rename -uid "D220D860-0000-7E80-582E-1A720000547E";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle140";
	rename -uid "D220D860-0000-7E80-582E-1A72000054FC";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle141";
	rename -uid "D220D860-0000-7E80-582E-1A720000557A";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle142";
	rename -uid "D220D860-0000-7E80-582E-1A72000055F8";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle143";
	rename -uid "D220D860-0000-7E80-582E-1A7200005684";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle144";
	rename -uid "D220D860-0000-7E80-582E-1A7300005702";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle145";
	rename -uid "D220D860-0000-7E80-582E-1A7300005780";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle146";
	rename -uid "D220D860-0000-7E80-582E-1A73000057FE";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle147";
	rename -uid "D220D860-0000-7E80-582E-1A730000587C";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle148";
	rename -uid "D220D860-0000-7E80-582E-1A73000058FA";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle149";
	rename -uid "D220D860-0000-7E80-582E-1A7400005978";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle150";
	rename -uid "D220D860-0000-7E80-582E-1A7400005A04";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle151";
	rename -uid "D220D860-0000-7E80-582E-1A7400005A82";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle152";
	rename -uid "D220D860-0000-7E80-582E-1A7400005B00";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle153";
	rename -uid "D220D860-0000-7E80-582E-1A7400005B7E";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle154";
	rename -uid "D220D860-0000-7E80-582E-1A7500005BFC";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle155";
	rename -uid "D220D860-0000-7E80-582E-1A7500005C7A";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode makeNurbCircle -n "makeNurbCircle156";
	rename -uid "D220D860-0000-7E80-582E-1A7500005CF8";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode ilrOptionsNode -s -n "TurtleRenderOptions";
	rename -uid "B5FD68C0-0000-6090-582F-285200000B67";
lockNode -l 1 ;
createNode ilrUIOptionsNode -s -n "TurtleUIOptions";
	rename -uid "B5FD68C0-0000-6090-582F-285200000B68";
lockNode -l 1 ;
createNode ilrBakeLayerManager -s -n "TurtleBakeLayerManager";
	rename -uid "B5FD68C0-0000-6090-582F-285200000B69";
lockNode -l 1 ;
createNode ilrBakeLayer -s -n "TurtleDefaultBakeLayer";
	rename -uid "B5FD68C0-0000-6090-582F-285200000B6A";
lockNode -l 1 ;
createNode dagPose -n "bindPose10";
	rename -uid "B5FD68C0-0000-6090-582F-300300005C7C";
	setAttr -s 17 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr -s 27 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 2.492057365218753 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 3.1415926535897931 0 0 2.4920573652187534
		 2.492057365218753 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 2.2559542663029748 0 0 1.5740186612595934
		 2.492057365218753 1.9260457613151178 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 1.3548327559307698 0 0 -0.53457986492992582
		 2.492057365218753 2.4367208031443206 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 -1.8209089884554144e-16 0.45300722762992318 -7.9012516650569582e-16 0 -2.2481967600856629
		 2.4920573652187548 1.0943534176986121 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 -0.45300722762992179 0 0 -2.2481967600856638
		 2.492057365218753 -1.0943534176986087 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 1.3364666804521832e-15 -1.3548327559307685 -1.6614513152614622e-15 0 -0.53457986492992904
		 2.4920573652187539 -2.4367208031443202 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 -4.4408920985006262e-16 4.0272310408766128 0 0 1.5740186612595912
		 2.4920573652187534 -1.9260457613151192 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 3.1415926535897931 0 0 2.4920573652187534
		 2.492057365218753 -2.2204460492503131e-16 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 1.0394179847893683e-16 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 3.872457909892546e-12 3.1416316015452961 0 0 2.4824748536971244
		 -8.3266726846886741e-17 -9.6687325880195907e-05 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 -4.4408920985006262e-16 2.2543011779493387 0 0 1.5690809847449598
		 -3.959417827617268e-16 1.9264945274258813 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 1.2146700620416774e-15 1.3560179025403669 1.5082069463050992e-15 0 -0.53180997025957988
		 -6.9813769278087004e-16 2.4378951878414155 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[14]" -type "matrix" "xform" 1 1 1 0 0.4527294822074498 0 0 -2.249879435471354
		 1.0394179847893683e-16 1.0943996382581656 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[15]" -type "matrix" "xform" 1 1 1 -6.0042269159070203e-17 -0.45285714898312412 2.6062357385716595e-16 0 -2.2494731430612114
		 -4.8232393136138834e-16 -1.0945571625572645 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[16]" -type "matrix" "xform" 1 1 1 4.4270870184486047e-16 -1.3556749820376923 -5.4988655882257853e-16 0 -0.53256374439824605
		 3.9679144323975552e-16 -2.4373364840343346 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[17]" -type "matrix" "xform" 1 1 1 0 4.0284516583014724 0 0 1.5702973590724276
		 1.8862462612253975e-16 -1.9262860437164639 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[18]" -type "matrix" "xform" 1 1 1 3.872457909892546e-12 3.1416316015452961 0 0 2.4824748536971244
		 -8.3266726846886765e-17 -9.6687325880417951e-05 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[19]" -type "matrix" "xform" 1 1 1 4.5522724711385341e-17 0.45300722762992279 1.9753129162642395e-16 0 -2.2481967600856629
		 -2.4920573652187543 1.0943534176986112 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[20]" -type "matrix" "xform" 1 1 1 4.5522724711385224e-17 -0.45300722762992179 -1.9753129162642395e-16 0 -2.2481967600856638
		 -2.4920573652187534 -1.0943534176986087 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[21]" -type "matrix" "xform" 1 1 1 -6.6823334022609158e-16 -1.3548327559307685 8.307256576307308e-16 0 -0.53457986492992904
		 -2.4920573652187543 -2.436720803144321 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[22]" -type "matrix" "xform" 1 1 1 0 3.1415926535897931 0 0 2.4920573652187534
		 -2.4920573652187534 -3.3306690738754696e-16 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[23]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 4.0272310408766128 0 0 1.5740186612595912
		 -2.4920573652187543 -1.9260457613151187 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[24]" -type "matrix" "xform" 1 1 1 0 3.1415926535897931 0 0 2.4920573652187534
		 -2.4920573652187534 -5.5511151231257827e-16 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[25]" -type "matrix" "xform" 1 1 1 0 1.3548327559307698 0 0 -0.53457986492992582
		 -2.4920573652187539 2.4367208031443206 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[26]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 2.2559542663029752 0 0 1.5740186612595934
		 -2.4920573652187534 1.926045761315117 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr -s 17 ".m";
	setAttr -s 27 ".p";
	setAttr -s 27 ".g[0:26]" yes no no no no no no no no no no no no no 
		no no no no no no no no no no no no no;
	setAttr ".bp" yes;
createNode skinCluster -n "skinCluster1";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B613";
	setAttr -s 12 ".wl";
	setAttr -s 2 ".wl[0].w[0:1]"  0.03865081162476184 0.9613491883752382;
	setAttr -s 2 ".wl[1].w[0:1]"  0.12895515676534691 0.87104484323465303;
	setAttr -s 2 ".wl[2].w[0:1]"  0.87104484323465314 0.12895515676534688;
	setAttr -s 2 ".wl[3].w[0:1]"  0.9613491883752382 0.038650811624761805;
	setAttr ".wl[4].w[1]"  1;
	setAttr -s 2 ".wl[5].w[0:1]"  0.011991828008663786 0.98800817199133617;
	setAttr -s 2 ".wl[6].w[0:1]"  0.98800817199133628 0.011991828008663762;
	setAttr ".wl[7].w[0]"  1;
	setAttr -s 2 ".wl[8].w[0:1]"  0.03865081162476184 0.9613491883752382;
	setAttr -s 2 ".wl[9].w[0:1]"  0.12895515676534691 0.87104484323465303;
	setAttr -s 2 ".wl[10].w[0:1]"  0.87104484323465314 0.12895515676534688;
	setAttr -s 2 ".wl[11].w[0:1]"  0.9613491883752382 0.038650811624761805;
	setAttr -s 2 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.492057365218753 0 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.4920573652187534 0 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr -s 2 ".ma";
	setAttr -s 2 ".dpf[0:1]"  4 4;
	setAttr -s 2 ".lw";
	setAttr -s 2 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 5;
	setAttr ".ucm" yes;
	setAttr -s 2 ".ifcl";
	setAttr -s 2 ".ifcl";
createNode tweak -n "tweak5";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B615";
createNode objectSet -n "skinCluster1Set";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B616";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster1GroupId";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B617";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster1GroupParts";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B618";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode objectSet -n "tweakSet5";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B619";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId10";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B61A";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts10";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B61B";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode dagPose -n "bindPose17";
	rename -uid "CA0C18C0-0000-079D-5852-DF810000B61C";
	setAttr -s 4 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr ".wm[2]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057365218753 0 1;
	setAttr ".wm[3]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.4920573652187534 0 1;
	setAttr -s 4 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 2.492057365218753 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 -2.4920573652187534 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr -s 4 ".m";
	setAttr -s 4 ".p";
	setAttr -s 4 ".g[0:3]" yes yes no no;
	setAttr ".bp" yes;
createNode blendShape -n "blendShape5";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B61D";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".tc" no;
	setAttr ".w[0]"  1;
	setAttr ".aal" -type "attributeAlias" {"layer1_surface","weight[0]"} ;
createNode tweak -n "tweak6";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B61F";
createNode objectSet -n "blendShape5Set";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B620";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "blendShape5GroupId";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B621";
	setAttr ".ihi" 0;
createNode groupParts -n "blendShape5GroupParts";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B622";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode objectSet -n "tweakSet6";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B623";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId12";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B624";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts12";
	rename -uid "CA0C18C0-0000-079D-5852-DF830000B625";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode skinCluster -n "skinCluster2";
	rename -uid "CA0C18C0-0000-079D-5852-DF870000B626";
	setAttr -s 12 ".wl";
	setAttr -s 3 ".wl[0].w[0:2]"  0.031161411114955604 0.19377084710449174 0.77506774178055271;
	setAttr -s 3 ".wl[1].w[0:2]"  0.069084227581287155 0.4642771230390102 0.46663864937970267;
	setAttr -s 3 ".wl[2].w[0:2]"  0.46663864937970295 0.46427712303900998 0.069084227581287086;
	setAttr -s 3 ".wl[3].w[0:2]"  0.77506774178055271 0.19377084710449174 0.03116141111495558;
	setAttr -s 2 ".wl[4].w[1:2]"  1.0188220560912443e-10 0.99999999989811783;
	setAttr -s 3 ".wl[5].w[0:2]"  0.0061085095307383255 0.49061064532237414 0.50328084514688753;
	setAttr -s 3 ".wl[6].w[0:2]"  0.50328084514688876 0.49061064532237297 0.0061085095307383142;
	setAttr -s 2 ".wl[7].w[0:1]"  0.99999999989811783 1.0188220560914719e-10;
	setAttr -s 3 ".wl[8].w[0:2]"  0.031161411114955604 0.19377084710449174 0.77506774178055271;
	setAttr -s 3 ".wl[9].w[0:2]"  0.069084227581287155 0.4642771230390102 0.46663864937970267;
	setAttr -s 3 ".wl[10].w[0:2]"  0.46663864937970295 0.46427712303900998 0.069084227581287086;
	setAttr -s 3 ".wl[11].w[0:2]"  0.77506774178055271 0.19377084710449174 0.03116141111495558;
	setAttr -s 3 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.492057365218753 0 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -1.0394179847893683e-16 0 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.4920573652187534 0 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr -s 3 ".ma";
	setAttr -s 3 ".dpf[0:2]"  4 4 4;
	setAttr -s 3 ".lw";
	setAttr -s 3 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 5;
	setAttr ".ucm" yes;
	setAttr -s 3 ".ifcl";
	setAttr -s 3 ".ifcl";
createNode objectSet -n "skinCluster2Set";
	rename -uid "CA0C18C0-0000-079D-5852-DF870000B627";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster2GroupId";
	rename -uid "CA0C18C0-0000-079D-5852-DF870000B628";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster2GroupParts";
	rename -uid "CA0C18C0-0000-079D-5852-DF870000B629";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode dagPose -n "bindPose18";
	rename -uid "CA0C18C0-0000-079D-5852-DF870000B62A";
	setAttr -s 5 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr ".wm[2]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057365218753 0 1;
	setAttr ".wm[3]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 1.0394179847893683e-16 0 1;
	setAttr ".wm[4]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.4920573652187534 0 1;
	setAttr -s 5 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 2.492057365218753 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 1.0394179847893683e-16 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 -2.4920573652187534 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr -s 5 ".m";
	setAttr -s 5 ".p";
	setAttr -s 5 ".g[0:4]" yes yes no no no;
	setAttr ".bp" yes;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "CA0C18C0-0000-079D-5852-E5660000DBE5";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -559.54886551852894 -674.61369574652656 ;
	setAttr ".tgi[0].vh" -type "double2" 1042.1317618244473 132.94930681202541 ;
	setAttr -s 6 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 301.42855834960938;
	setAttr ".tgi[0].ni[0].y" -261.42855834960938;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 1.4285714626312256;
	setAttr ".tgi[0].ni[1].y" -261.42855834960938;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 562.85711669921875;
	setAttr ".tgi[0].ni[2].y" -261.42855834960938;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 427.14285278320312;
	setAttr ".tgi[0].ni[3].y" -127.14286041259766;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 37.142856597900391;
	setAttr ".tgi[0].ni[4].y" -64.285713195800781;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 427.14285278320312;
	setAttr ".tgi[0].ni[5].y" -1.4285714626312256;
	setAttr ".tgi[0].ni[5].nvs" 18304;
createNode network -n "Rig2";
	rename -uid "CA0C18C0-0000-079D-5852-E57C0000DBF5";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -s false -ci true -m -sn "modules" -ln "modules" -nn "modules" -at "message";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".name" -type "string" "untitled";
	setAttr "._class_namespace" -type "string" "Rig";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Rig";
createNode network -n "net_InteractiveFK_interactivefk";
	rename -uid "CA0C18C0-0000-079D-5852-E57C0000DBF6";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "locked" -ln "locked" -nn "locked" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "interactivefk";
	setAttr "._class_namespace" -type "string" "Module.InteractiveFK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 32 ".input";
	setAttr "._class" -type "string" "InteractiveFK";
createNode wrap -n "wrap1";
	rename -uid "CA0C18C0-0000-079D-5852-F56A0001332B";
	setAttr ".md" 1;
	setAttr ".awt" yes;
createNode tweak -n "tweak7";
	rename -uid "CA0C18C0-0000-079D-5852-F56A0001332D";
createNode objectSet -n "wrap1Set";
	rename -uid "CA0C18C0-0000-079D-5852-F56A0001332E";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "wrap1GroupId";
	rename -uid "CA0C18C0-0000-079D-5852-F56A0001332F";
	setAttr ".ihi" 0;
createNode groupParts -n "wrap1GroupParts";
	rename -uid "CA0C18C0-0000-079D-5852-F56A00013330";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode objectSet -n "tweakSet7";
	rename -uid "CA0C18C0-0000-079D-5852-F56A00013331";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId14";
	rename -uid "CA0C18C0-0000-079D-5852-F56A00013332";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts14";
	rename -uid "CA0C18C0-0000-079D-5852-F56A00013333";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode skinCluster -n "skinCluster3";
	rename -uid "CA0C18C0-0000-079D-5852-F6CB00013FD0";
	setAttr -s 32 ".wl";
	setAttr -s 5 ".wl[0].w";
	setAttr ".wl[0].w[2]" 0.0096802404448129951;
	setAttr ".wl[0].w[4]" 0.014598534312702803;
	setAttr ".wl[0].w[5]" 0.48056878806779918;
	setAttr ".wl[0].w[6]" 0.014597907884866776;
	setAttr ".wl[0].w[7]" 0.48055452928981834;
	setAttr -s 5 ".wl[1].w";
	setAttr ".wl[1].w[0]" 9.6318149894088347e-06;
	setAttr ".wl[1].w[4]" 3.1216741892286632e-05;
	setAttr ".wl[1].w[5]" 3.1216741892286632e-05;
	setAttr ".wl[1].w[6]" 7.8476522291170825e-06;
	setAttr ".wl[1].w[7]" 0.99992008704899693;
	setAttr -s 5 ".wl[2].w[3:7]"  0.0096802404448129847 0.48056878806779646 0.014598534312702804 0.014597907884866769 0.48055452928982106;
	setAttr -s 5 ".wl[3].w[3:7]"  9.6397235977672917e-06 0.99992002347792075 7.85445623881394e-06 3.1241175216679051e-05 3.1241167025976581e-05;
	setAttr -s 5 ".wl[4].w[3:7]"  0.0096802396048732246 0.48056874636957336 0.014598533046010158 0.48055457837495058 0.014597902604592716;
	setAttr -s 5 ".wl[5].w";
	setAttr ".wl[5].w[1]" 9.6318653245228328e-06;
	setAttr ".wl[5].w[4]" 3.1216905536480416e-05;
	setAttr ".wl[5].w[5]" 3.1216905536480375e-05;
	setAttr ".wl[5].w[6]" 0.99992008663241294;
	setAttr ".wl[5].w[7]" 7.8476911895224173e-06;
	setAttr -s 5 ".wl[6].w";
	setAttr ".wl[6].w[2]" 0.0096802396048732264;
	setAttr ".wl[6].w[4]" 0.01459853304601017;
	setAttr ".wl[6].w[5]" 0.48056874636957281;
	setAttr ".wl[6].w[6]" 0.48055457837495108;
	setAttr ".wl[6].w[7]" 0.014597902604592719;
	setAttr -s 5 ".wl[7].w";
	setAttr ".wl[7].w[2]" 9.6397235977672291e-06;
	setAttr ".wl[7].w[4]" 7.8544562388138841e-06;
	setAttr ".wl[7].w[5]" 0.99992002347792075;
	setAttr ".wl[7].w[6]" 3.1241175216678882e-05;
	setAttr ".wl[7].w[7]" 3.124116702597631e-05;
	setAttr -s 5 ".wl[11].w";
	setAttr ".wl[11].w[0]" 0.082738337938716294;
	setAttr ".wl[11].w[2]" 0.082739004544782099;
	setAttr ".wl[11].w[4]" 0.027354161186446478;
	setAttr ".wl[11].w[5]" 0.40358783885380028;
	setAttr ".wl[11].w[7]" 0.40358065747625477;
	setAttr -s 5 ".wl[12].w";
	setAttr ".wl[12].w[0]" 0.05684760026451547;
	setAttr ".wl[12].w[2]" 0.011329814957955615;
	setAttr ".wl[12].w[4]" 0.025468288509860392;
	setAttr ".wl[12].w[5]" 0.025468288509860371;
	setAttr ".wl[12].w[7]" 0.88088600775780823;
	setAttr -s 5 ".wl[13].w";
	setAttr ".wl[13].w[0]" 0.082738337938716322;
	setAttr ".wl[13].w[3]" 0.082739004544781974;
	setAttr ".wl[13].w[4]" 0.40358783885379929;
	setAttr ".wl[13].w[5]" 0.027354161186446489;
	setAttr ".wl[13].w[7]" 0.40358065747625593;
	setAttr -s 5 ".wl[14].w";
	setAttr ".wl[14].w[1]" 0.011329808694584866;
	setAttr ".wl[14].w[3]" 0.056848537556655448;
	setAttr ".wl[14].w[4]" 0.88088568976427317;
	setAttr ".wl[14].w[6]" 0.025467984778702376;
	setAttr ".wl[14].w[7]" 0.025467979205784148;
	setAttr -s 5 ".wl[15].w";
	setAttr ".wl[15].w[1]" 0.082738338048743476;
	setAttr ".wl[15].w[3]" 0.082739000410591276;
	setAttr ".wl[15].w[4]" 0.40358781868786836;
	setAttr ".wl[15].w[5]" 0.02735415981965077;
	setAttr ".wl[15].w[6]" 0.40358068303314604;
	setAttr -s 5 ".wl[16].w";
	setAttr ".wl[16].w[1]" 0.056847605506286578;
	setAttr ".wl[16].w[3]" 0.011329816416486369;
	setAttr ".wl[16].w[4]" 0.025468291788491349;
	setAttr ".wl[16].w[5]" 0.025468291788491328;
	setAttr ".wl[16].w[6]" 0.88088599450024441;
	setAttr -s 5 ".wl[17].w";
	setAttr ".wl[17].w[1]" 0.082738338048743559;
	setAttr ".wl[17].w[2]" 0.082739000410591179;
	setAttr ".wl[17].w[4]" 0.02735415981965077;
	setAttr ".wl[17].w[5]" 0.40358781868786736;
	setAttr ".wl[17].w[6]" 0.40358068303314709;
	setAttr -s 5 ".wl[18].w";
	setAttr ".wl[18].w[1]" 0.011329808694584883;
	setAttr ".wl[18].w[2]" 0.056848537556655497;
	setAttr ".wl[18].w[5]" 0.88088568976427306;
	setAttr ".wl[18].w[6]" 0.025467984778702414;
	setAttr ".wl[18].w[7]" 0.025467979205784124;
	setAttr -s 5 ".wl[22].w";
	setAttr ".wl[22].w[0]" 0.40358060968111625;
	setAttr ".wl[22].w[2]" 0.4035877910565453;
	setAttr ".wl[22].w[3]" 0.027354165080029538;
	setAttr ".wl[22].w[5]" 0.082739050394425404;
	setAttr ".wl[22].w[7]" 0.082738383787883535;
	setAttr -s 5 ".wl[23].w";
	setAttr ".wl[23].w[0]" 0.88088590062532279;
	setAttr ".wl[23].w[2]" 0.025468303518778698;
	setAttr ".wl[23].w[3]" 0.025468303518778698;
	setAttr ".wl[23].w[4]" 0.011329825491567438;
	setAttr ".wl[23].w[7]" 0.056847666845552251;
	setAttr -s 5 ".wl[24].w";
	setAttr ".wl[24].w[0]" 0.40358060968111714;
	setAttr ".wl[24].w[2]" 0.027354165080029563;
	setAttr ".wl[24].w[3]" 0.4035877910565443;
	setAttr ".wl[24].w[4]" 0.082739050394425306;
	setAttr ".wl[24].w[7]" 0.082738383787883632;
	setAttr -s 5 ".wl[25].w";
	setAttr ".wl[25].w[0]" 0.025467994214346507;
	setAttr ".wl[25].w[1]" 0.025467999787267645;
	setAttr ".wl[25].w[3]" 0.88088558263213679;
	setAttr ".wl[25].w[4]" 0.056848604138188971;
	setAttr ".wl[25].w[6]" 0.01132981922806014;
	setAttr -s 5 ".wl[26].w";
	setAttr ".wl[26].w[1]" 0.40358063523800047;
	setAttr ".wl[26].w[2]" 0.027354163713233914;
	setAttr ".wl[26].w[3]" 0.40358777089062003;
	setAttr ".wl[26].w[4]" 0.082739046260233234;
	setAttr ".wl[26].w[6]" 0.082738383897912507;
	setAttr -s 5 ".wl[27].w";
	setAttr ".wl[27].w[1]" 0.88088588736775608;
	setAttr ".wl[27].w[2]" 0.025468306797409909;
	setAttr ".wl[27].w[3]" 0.025468306797409929;
	setAttr ".wl[27].w[4]" 0.011329826950098813;
	setAttr ".wl[27].w[6]" 0.056847672087325378;
	setAttr -s 5 ".wl[28].w";
	setAttr ".wl[28].w[1]" 0.40358063523800136;
	setAttr ".wl[28].w[2]" 0.40358777089061909;
	setAttr ".wl[28].w[3]" 0.027354163713233948;
	setAttr ".wl[28].w[5]" 0.082739046260233096;
	setAttr ".wl[28].w[6]" 0.082738383897912535;
	setAttr -s 5 ".wl[29].w";
	setAttr ".wl[29].w[0]" 0.025467994214346475;
	setAttr ".wl[29].w[1]" 0.025467999787267659;
	setAttr ".wl[29].w[2]" 0.88088558263213679;
	setAttr ".wl[29].w[5]" 0.056848604138188936;
	setAttr ".wl[29].w[6]" 0.011329819228060142;
	setAttr -s 5 ".wl[33].w";
	setAttr ".wl[33].w[0]" 0.48055452816739652;
	setAttr ".wl[33].w[1]" 0.014597907816839444;
	setAttr ".wl[33].w[2]" 0.48056878694536215;
	setAttr ".wl[33].w[3]" 0.014598534244672711;
	setAttr ".wl[33].w[5]" 0.0096802428257292215;
	setAttr -s 5 ".wl[34].w";
	setAttr ".wl[34].w[0]" 0.99992008705808255;
	setAttr ".wl[34].w[1]" 7.8476510588012139e-06;
	setAttr ".wl[34].w[2]" 3.1216737249958586e-05;
	setAttr ".wl[34].w[3]" 3.1216737249958599e-05;
	setAttr ".wl[34].w[7]" 9.631816358898453e-06;
	setAttr -s 5 ".wl[35].w[0:4]"  0.48055452816739713 0.014597907816839438 0.014598534244672706 0.48056878694536159 0.009680242825729218;
	setAttr -s 5 ".wl[36].w[0:4]"  3.1241162381938673e-05 3.124117057263993e-05 7.8544550679669411e-06 0.99992002348700848 9.6397249689711455e-06;
	setAttr -s 5 ".wl[37].w[0:4]"  0.014597902536565434 0.48055457725252704 0.014598532977980088 0.48056874524713811 0.0096802419857892619;
	setAttr -s 5 ".wl[38].w";
	setAttr ".wl[38].w[0]" 7.8476900192036756e-06;
	setAttr ".wl[38].w[1]" 0.99992008664149845;
	setAttr ".wl[38].w[2]" 3.1216900894139644e-05;
	setAttr ".wl[38].w[3]" 3.1216900894139664e-05;
	setAttr ".wl[38].w[6]" 9.6318666940231729e-06;
	setAttr -s 5 ".wl[39].w";
	setAttr ".wl[39].w[0]" 0.014597902536565403;
	setAttr ".wl[39].w[1]" 0.48055457725252965;
	setAttr ".wl[39].w[2]" 0.48056874524713572;
	setAttr ".wl[39].w[3]" 0.014598532977980083;
	setAttr ".wl[39].w[5]" 0.0096802419857892411;
	setAttr -s 5 ".wl[40].w";
	setAttr ".wl[40].w[0]" 3.1241162381938612e-05;
	setAttr ".wl[40].w[1]" 3.1241170572639978e-05;
	setAttr ".wl[40].w[2]" 0.99992002348700848;
	setAttr ".wl[40].w[3]" 7.8544550679669411e-06;
	setAttr ".wl[40].w[5]" 9.6397249689711522e-06;
	setAttr -s 8 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -2.4920573652187534 -2.492057365218753 0 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 2.492057 -2.492057365218753 0 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.492057365218753 2.492 1;
	setAttr ".pm[3]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.492057365218753 -2.492 1;
	setAttr ".pm[4]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057 -2.492 1;
	setAttr ".pm[5]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057 2.492 1;
	setAttr ".pm[6]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 2.492057 2.492057 0 1;
	setAttr ".pm[7]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -2.4920573652187534 2.492057 0 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr -s 8 ".ma";
	setAttr -s 8 ".dpf[0:7]"  4 4 4 4 4 4 4 4;
	setAttr -s 8 ".lw";
	setAttr -s 8 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 5;
	setAttr ".ucm" yes;
	setAttr -s 8 ".ifcl";
	setAttr -s 8 ".ifcl";
createNode objectSet -n "skinCluster3Set";
	rename -uid "CA0C18C0-0000-079D-5852-F6CB00013FD1";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster3GroupId";
	rename -uid "CA0C18C0-0000-079D-5852-F6CB00013FD2";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster3GroupParts";
	rename -uid "CA0C18C0-0000-079D-5852-F6CB00013FD3";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode dagPose -n "bindPose20";
	rename -uid "CA0C18C0-0000-079D-5852-F6CB00013FD4";
	setAttr -s 10 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr ".wm[2]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 2.4920573652187534 2.492057365218753 0 1;
	setAttr ".wm[3]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -2.492057 2.492057365218753 0 1;
	setAttr ".wm[4]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057365218753 -2.492 1;
	setAttr ".wm[5]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 2.492057365218753 2.492 1;
	setAttr ".wm[6]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.492057 2.492 1;
	setAttr ".wm[7]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 -2.492057 -2.492 1;
	setAttr ".wm[8]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -2.492057 -2.492057 0 1;
	setAttr ".wm[9]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 2.4920573652187534 -2.492057 0 1;
	setAttr -s 10 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 0 0 0 2.4920573652187534
		 2.492057365218753 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 0 0 0 -2.492057
		 2.492057365218753 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 0 0 0 0
		 2.492057365218753 -2.492 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 0 0 0 0
		 2.492057365218753 2.492 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 0 0 0 0
		 -2.492057 2.492 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 0 0 0 0
		 -2.492057 -2.492 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 0 0 0 -2.492057
		 -2.492057 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 4.4408920985006262e-16 0 0 0 2.4920573652187534
		 -2.492057 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 no;
	setAttr -s 10 ".m";
	setAttr -s 10 ".p";
	setAttr -s 10 ".g[0:9]" yes yes no no no no no no no no;
	setAttr ".bp" yes;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 118;
	setAttr -av ".unw" 118;
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
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -k on ".an";
	setAttr -k on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".dsm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
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
connectAttr "layer_geo.di" "Render_Grp.do";
connectAttr "skinCluster1GroupId.id" "layer1_surfaceShape.iog.og[4].gid";
connectAttr "skinCluster1Set.mwc" "layer1_surfaceShape.iog.og[4].gco";
connectAttr "groupId10.id" "layer1_surfaceShape.iog.og[5].gid";
connectAttr "tweakSet5.mwc" "layer1_surfaceShape.iog.og[5].gco";
connectAttr "skinCluster1.og[0]" "layer1_surfaceShape.cr";
connectAttr "tweak5.pl[0].cp[0]" "layer1_surfaceShape.twl";
connectAttr "blendShape5GroupId.id" "layer2_surfaceShapeDeformedDeformed.iog.og[0].gid"
		;
connectAttr "blendShape5Set.mwc" "layer2_surfaceShapeDeformedDeformed.iog.og[0].gco"
		;
connectAttr "groupId12.id" "layer2_surfaceShapeDeformedDeformed.iog.og[1].gid";
connectAttr "tweakSet6.mwc" "layer2_surfaceShapeDeformedDeformed.iog.og[1].gco";
connectAttr "skinCluster2GroupId.id" "layer2_surfaceShapeDeformedDeformed.iog.og[2].gid"
		;
connectAttr "skinCluster2Set.mwc" "layer2_surfaceShapeDeformedDeformed.iog.og[2].gco"
		;
connectAttr "skinCluster2.og[0]" "layer2_surfaceShapeDeformedDeformed.cr";
connectAttr "tweak6.pl[0].cp[0]" "layer2_surfaceShapeDeformedDeformed.twl";
connectAttr "wrap1GroupId.id" "layer3_surfaceShape.iog.og[3].gid";
connectAttr "wrap1Set.mwc" "layer3_surfaceShape.iog.og[3].gco";
connectAttr "groupId14.id" "layer3_surfaceShape.iog.og[4].gid";
connectAttr "tweakSet7.mwc" "layer3_surfaceShape.iog.og[4].gco";
connectAttr "skinCluster3GroupId.id" "layer3_surfaceShape.iog.og[5].gid";
connectAttr "skinCluster3Set.mwc" "layer3_surfaceShape.iog.og[5].gco";
connectAttr "skinCluster3.og[0]" "layer3_surfaceShape.cr";
connectAttr "tweak7.pl[0].cp[0]" "layer3_surfaceShape.twl";
connectAttr "jnt_root.s" "jnt_out_01.is";
connectAttr "jnt_root.s" "jnt_out_02.is";
connectAttr "jnt_root.s" "jnt_out_03.is";
connectAttr "jnt_root.s" "jnt_out_04.is";
connectAttr "jnt_root.s" "jnt_out_05.is";
connectAttr "jnt_root.s" "jnt_out_06.is";
connectAttr "jnt_root.s" "jnt_out_07.is";
connectAttr "jnt_root.s" "jnt_out_08.is";
connectAttr "jnt_root.s" "jnt_out_09.is";
connectAttr "jnt_root.s" "jnt_out_10.is";
connectAttr "jnt_root.s" "jnt_out_11.is";
connectAttr "jnt_root.s" "jnt_out_12.is";
connectAttr "jnt_root.s" "jnt_out_13.is";
connectAttr "jnt_root.s" "jnt_out_14.is";
connectAttr "jnt_root.s" "jnt_out_15.is";
connectAttr "jnt_root.s" "jnt_out_16.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "layerManager.dli[1]" "layer_anm.id";
connectAttr "layerManager.dli[2]" "layer_rig.id";
connectAttr "layerManager.dli[3]" "layer_geo.id";
connectAttr ":TurtleDefaultBakeLayer.idx" ":TurtleBakeLayerManager.bli[0]";
connectAttr ":TurtleRenderOptions.msg" ":TurtleDefaultBakeLayer.rset";
connectAttr "jnt_out_01.msg" "bindPose10.m[2]";
connectAttr "jnt_out_02.msg" "bindPose10.m[3]";
connectAttr "jnt_out_03.msg" "bindPose10.m[4]";
connectAttr "jnt_out_04.msg" "bindPose10.m[5]";
connectAttr "jnt_out_05.msg" "bindPose10.m[6]";
connectAttr "jnt_out_06.msg" "bindPose10.m[7]";
connectAttr "jnt_out_07.msg" "bindPose10.m[8]";
connectAttr "jnt_out_08.msg" "bindPose10.m[9]";
connectAttr "jnt_out_09.msg" "bindPose10.m[19]";
connectAttr "jnt_out_10.msg" "bindPose10.m[20]";
connectAttr "jnt_out_11.msg" "bindPose10.m[21]";
connectAttr "jnt_out_12.msg" "bindPose10.m[22]";
connectAttr "jnt_out_13.msg" "bindPose10.m[23]";
connectAttr "jnt_out_14.msg" "bindPose10.m[24]";
connectAttr "jnt_out_15.msg" "bindPose10.m[25]";
connectAttr "jnt_out_16.msg" "bindPose10.m[26]";
connectAttr "bindPose10.w" "bindPose10.p[0]";
connectAttr "bindPose10.m[0]" "bindPose10.p[1]";
connectAttr "bindPose10.m[0]" "bindPose10.p[2]";
connectAttr "bindPose10.m[0]" "bindPose10.p[3]";
connectAttr "bindPose10.m[0]" "bindPose10.p[4]";
connectAttr "bindPose10.m[0]" "bindPose10.p[5]";
connectAttr "bindPose10.m[0]" "bindPose10.p[6]";
connectAttr "bindPose10.m[0]" "bindPose10.p[7]";
connectAttr "bindPose10.m[0]" "bindPose10.p[8]";
connectAttr "bindPose10.m[0]" "bindPose10.p[9]";
connectAttr "bindPose10.m[0]" "bindPose10.p[10]";
connectAttr "bindPose10.m[0]" "bindPose10.p[11]";
connectAttr "bindPose10.m[0]" "bindPose10.p[12]";
connectAttr "bindPose10.m[0]" "bindPose10.p[13]";
connectAttr "bindPose10.m[0]" "bindPose10.p[14]";
connectAttr "bindPose10.m[0]" "bindPose10.p[15]";
connectAttr "bindPose10.m[0]" "bindPose10.p[16]";
connectAttr "bindPose10.m[0]" "bindPose10.p[17]";
connectAttr "bindPose10.m[0]" "bindPose10.p[18]";
connectAttr "bindPose10.m[0]" "bindPose10.p[19]";
connectAttr "bindPose10.m[0]" "bindPose10.p[20]";
connectAttr "bindPose10.m[0]" "bindPose10.p[21]";
connectAttr "bindPose10.m[0]" "bindPose10.p[22]";
connectAttr "bindPose10.m[0]" "bindPose10.p[23]";
connectAttr "bindPose10.m[0]" "bindPose10.p[24]";
connectAttr "bindPose10.m[0]" "bindPose10.p[25]";
connectAttr "bindPose10.m[0]" "bindPose10.p[26]";
connectAttr "jnt_out_01.bps" "bindPose10.wm[2]";
connectAttr "jnt_out_02.bps" "bindPose10.wm[3]";
connectAttr "jnt_out_03.bps" "bindPose10.wm[4]";
connectAttr "jnt_out_04.bps" "bindPose10.wm[5]";
connectAttr "jnt_out_05.bps" "bindPose10.wm[6]";
connectAttr "jnt_out_06.bps" "bindPose10.wm[7]";
connectAttr "jnt_out_07.bps" "bindPose10.wm[8]";
connectAttr "jnt_out_08.bps" "bindPose10.wm[9]";
connectAttr "jnt_out_09.bps" "bindPose10.wm[19]";
connectAttr "jnt_out_10.bps" "bindPose10.wm[20]";
connectAttr "jnt_out_11.bps" "bindPose10.wm[21]";
connectAttr "jnt_out_12.bps" "bindPose10.wm[22]";
connectAttr "jnt_out_13.bps" "bindPose10.wm[23]";
connectAttr "jnt_out_14.bps" "bindPose10.wm[24]";
connectAttr "jnt_out_15.bps" "bindPose10.wm[25]";
connectAttr "jnt_out_16.bps" "bindPose10.wm[26]";
connectAttr "skinCluster1GroupParts.og" "skinCluster1.ip[0].ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1.ip[0].gi";
connectAttr "bindPose17.msg" "skinCluster1.bp";
connectAttr "jnt_layer1_01.wm" "skinCluster1.ma[0]";
connectAttr "jnt_layer1_02.wm" "skinCluster1.ma[1]";
connectAttr "jnt_layer1_01.liw" "skinCluster1.lw[0]";
connectAttr "jnt_layer1_02.liw" "skinCluster1.lw[1]";
connectAttr "jnt_layer1_01.obcc" "skinCluster1.ifcl[0]";
connectAttr "jnt_layer1_02.obcc" "skinCluster1.ifcl[1]";
connectAttr "groupParts10.og" "tweak5.ip[0].ig";
connectAttr "groupId10.id" "tweak5.ip[0].gi";
connectAttr "skinCluster1GroupId.msg" "skinCluster1Set.gn" -na;
connectAttr "layer1_surfaceShape.iog.og[4]" "skinCluster1Set.dsm" -na;
connectAttr "skinCluster1.msg" "skinCluster1Set.ub[0]";
connectAttr "tweak5.og[0]" "skinCluster1GroupParts.ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1GroupParts.gi";
connectAttr "groupId10.msg" "tweakSet5.gn" -na;
connectAttr "layer1_surfaceShape.iog.og[5]" "tweakSet5.dsm" -na;
connectAttr "tweak5.msg" "tweakSet5.ub[0]";
connectAttr "layer1_surfaceShapeOrig.ws" "groupParts10.ig";
connectAttr "groupId10.id" "groupParts10.gi";
connectAttr "root.msg" "bindPose17.m[0]";
connectAttr "layer1.msg" "bindPose17.m[1]";
connectAttr "jnt_layer1_01.msg" "bindPose17.m[2]";
connectAttr "jnt_layer1_02.msg" "bindPose17.m[3]";
connectAttr "bindPose17.w" "bindPose17.p[0]";
connectAttr "bindPose17.m[0]" "bindPose17.p[1]";
connectAttr "bindPose17.m[1]" "bindPose17.p[2]";
connectAttr "bindPose17.m[1]" "bindPose17.p[3]";
connectAttr "blendShape5GroupParts.og" "blendShape5.ip[0].ig";
connectAttr "blendShape5GroupId.id" "blendShape5.ip[0].gi";
connectAttr "layer1_surfaceShape.ws" "blendShape5.it[0].itg[0].iti[6000].igt";
connectAttr "groupParts12.og" "tweak6.ip[0].ig";
connectAttr "groupId12.id" "tweak6.ip[0].gi";
connectAttr "blendShape5GroupId.msg" "blendShape5Set.gn" -na;
connectAttr "layer2_surfaceShapeDeformedDeformed.iog.og[0]" "blendShape5Set.dsm"
		 -na;
connectAttr "blendShape5.msg" "blendShape5Set.ub[0]";
connectAttr "tweak6.og[0]" "blendShape5GroupParts.ig";
connectAttr "blendShape5GroupId.id" "blendShape5GroupParts.gi";
connectAttr "groupId12.msg" "tweakSet6.gn" -na;
connectAttr "layer2_surfaceShapeDeformedDeformed.iog.og[1]" "tweakSet6.dsm" -na;
connectAttr "tweak6.msg" "tweakSet6.ub[0]";
connectAttr "layer2_surfaceShapeDeformed.ws" "groupParts12.ig";
connectAttr "groupId12.id" "groupParts12.gi";
connectAttr "skinCluster2GroupParts.og" "skinCluster2.ip[0].ig";
connectAttr "skinCluster2GroupId.id" "skinCluster2.ip[0].gi";
connectAttr "bindPose18.msg" "skinCluster2.bp";
connectAttr "jnt_layer2_01.wm" "skinCluster2.ma[0]";
connectAttr "jnt_layer2_02.wm" "skinCluster2.ma[1]";
connectAttr "jnt_layer2_03.wm" "skinCluster2.ma[2]";
connectAttr "jnt_layer2_01.liw" "skinCluster2.lw[0]";
connectAttr "jnt_layer2_02.liw" "skinCluster2.lw[1]";
connectAttr "jnt_layer2_03.liw" "skinCluster2.lw[2]";
connectAttr "jnt_layer2_01.obcc" "skinCluster2.ifcl[0]";
connectAttr "jnt_layer2_02.obcc" "skinCluster2.ifcl[1]";
connectAttr "jnt_layer2_03.obcc" "skinCluster2.ifcl[2]";
connectAttr "skinCluster2GroupId.msg" "skinCluster2Set.gn" -na;
connectAttr "layer2_surfaceShapeDeformedDeformed.iog.og[2]" "skinCluster2Set.dsm"
		 -na;
connectAttr "skinCluster2.msg" "skinCluster2Set.ub[0]";
connectAttr "blendShape5.og[0]" "skinCluster2GroupParts.ig";
connectAttr "skinCluster2GroupId.id" "skinCluster2GroupParts.gi";
connectAttr "root.msg" "bindPose18.m[0]";
connectAttr "layer2.msg" "bindPose18.m[1]";
connectAttr "jnt_layer2_01.msg" "bindPose18.m[2]";
connectAttr "jnt_layer2_02.msg" "bindPose18.m[3]";
connectAttr "jnt_layer2_03.msg" "bindPose18.m[4]";
connectAttr "bindPose18.w" "bindPose18.p[0]";
connectAttr "bindPose18.m[0]" "bindPose18.p[1]";
connectAttr "bindPose18.m[1]" "bindPose18.p[2]";
connectAttr "bindPose18.m[1]" "bindPose18.p[3]";
connectAttr "bindPose18.m[1]" "bindPose18.p[4]";
connectAttr "layer3_surfaceShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr ":initialShadingGroup.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "net_InteractiveFK_interactivefk.msg" "Rig2.modules[0]";
connectAttr "Rig2.msg" "net_InteractiveFK_interactivefk.rig";
connectAttr "jnt_layer1_01.msg" "net_InteractiveFK_interactivefk.input[0]";
connectAttr "jnt_layer1_02.msg" "net_InteractiveFK_interactivefk.input[1]";
connectAttr "jnt_layer2_01.msg" "net_InteractiveFK_interactivefk.input[2]";
connectAttr "jnt_layer2_02.msg" "net_InteractiveFK_interactivefk.input[3]";
connectAttr "jnt_layer2_03.msg" "net_InteractiveFK_interactivefk.input[4]";
connectAttr "jnt_layer3_01.msg" "net_InteractiveFK_interactivefk.input[5]";
connectAttr "jnt_layer3_02.msg" "net_InteractiveFK_interactivefk.input[6]";
connectAttr "jnt_layer3_03.msg" "net_InteractiveFK_interactivefk.input[7]";
connectAttr "jnt_layer3_04.msg" "net_InteractiveFK_interactivefk.input[8]";
connectAttr "jnt_layer3_05.msg" "net_InteractiveFK_interactivefk.input[9]";
connectAttr "jnt_layer3_06.msg" "net_InteractiveFK_interactivefk.input[10]";
connectAttr "jnt_layer3_07.msg" "net_InteractiveFK_interactivefk.input[11]";
connectAttr "jnt_layer3_08.msg" "net_InteractiveFK_interactivefk.input[12]";
connectAttr "jnt_out_01.msg" "net_InteractiveFK_interactivefk.input[13]";
connectAttr "jnt_out_02.msg" "net_InteractiveFK_interactivefk.input[14]";
connectAttr "jnt_out_03.msg" "net_InteractiveFK_interactivefk.input[15]";
connectAttr "jnt_out_04.msg" "net_InteractiveFK_interactivefk.input[16]";
connectAttr "jnt_out_05.msg" "net_InteractiveFK_interactivefk.input[17]";
connectAttr "jnt_out_06.msg" "net_InteractiveFK_interactivefk.input[18]";
connectAttr "jnt_out_07.msg" "net_InteractiveFK_interactivefk.input[19]";
connectAttr "jnt_out_08.msg" "net_InteractiveFK_interactivefk.input[20]";
connectAttr "jnt_out_09.msg" "net_InteractiveFK_interactivefk.input[21]";
connectAttr "jnt_out_10.msg" "net_InteractiveFK_interactivefk.input[22]";
connectAttr "jnt_out_11.msg" "net_InteractiveFK_interactivefk.input[23]";
connectAttr "jnt_out_12.msg" "net_InteractiveFK_interactivefk.input[24]";
connectAttr "jnt_out_13.msg" "net_InteractiveFK_interactivefk.input[25]";
connectAttr "jnt_out_14.msg" "net_InteractiveFK_interactivefk.input[26]";
connectAttr "jnt_out_15.msg" "net_InteractiveFK_interactivefk.input[27]";
connectAttr "jnt_out_16.msg" "net_InteractiveFK_interactivefk.input[28]";
connectAttr "layer1_surface.msg" "net_InteractiveFK_interactivefk.input[29]";
connectAttr "layer2_surface.msg" "net_InteractiveFK_interactivefk.input[30]";
connectAttr "layer3_surface.msg" "net_InteractiveFK_interactivefk.input[31]";
connectAttr "wrap1GroupParts.og" "wrap1.ip[0].ig";
connectAttr "wrap1GroupId.id" "wrap1.ip[0].gi";
connectAttr "layer3_surfaceShape.wm" "wrap1.gm";
connectAttr "layer2_surfaceShapeDeformedDeformed.ws" "wrap1.dp[0]";
connectAttr "layer2_surfaceBaseShapeDeformedDeformed.ws" "wrap1.bp[0]";
connectAttr "layer2_surface.wsm" "wrap1.ns[0]";
connectAttr "layer2_surface.dr" "wrap1.dr[0]";
connectAttr "groupParts14.og" "tweak7.ip[0].ig";
connectAttr "groupId14.id" "tweak7.ip[0].gi";
connectAttr "wrap1GroupId.msg" "wrap1Set.gn" -na;
connectAttr "layer3_surfaceShape.iog.og[3]" "wrap1Set.dsm" -na;
connectAttr "wrap1.msg" "wrap1Set.ub[0]";
connectAttr "tweak7.og[0]" "wrap1GroupParts.ig";
connectAttr "wrap1GroupId.id" "wrap1GroupParts.gi";
connectAttr "groupId14.msg" "tweakSet7.gn" -na;
connectAttr "layer3_surfaceShape.iog.og[4]" "tweakSet7.dsm" -na;
connectAttr "tweak7.msg" "tweakSet7.ub[0]";
connectAttr "layer3_surfaceShapeOrig.ws" "groupParts14.ig";
connectAttr "groupId14.id" "groupParts14.gi";
connectAttr "skinCluster3GroupParts.og" "skinCluster3.ip[0].ig";
connectAttr "skinCluster3GroupId.id" "skinCluster3.ip[0].gi";
connectAttr "bindPose20.msg" "skinCluster3.bp";
connectAttr "jnt_layer3_01.wm" "skinCluster3.ma[0]";
connectAttr "jnt_layer3_02.wm" "skinCluster3.ma[1]";
connectAttr "jnt_layer3_03.wm" "skinCluster3.ma[2]";
connectAttr "jnt_layer3_04.wm" "skinCluster3.ma[3]";
connectAttr "jnt_layer3_05.wm" "skinCluster3.ma[4]";
connectAttr "jnt_layer3_06.wm" "skinCluster3.ma[5]";
connectAttr "jnt_layer3_07.wm" "skinCluster3.ma[6]";
connectAttr "jnt_layer3_08.wm" "skinCluster3.ma[7]";
connectAttr "jnt_layer3_01.liw" "skinCluster3.lw[0]";
connectAttr "jnt_layer3_02.liw" "skinCluster3.lw[1]";
connectAttr "jnt_layer3_03.liw" "skinCluster3.lw[2]";
connectAttr "jnt_layer3_04.liw" "skinCluster3.lw[3]";
connectAttr "jnt_layer3_05.liw" "skinCluster3.lw[4]";
connectAttr "jnt_layer3_06.liw" "skinCluster3.lw[5]";
connectAttr "jnt_layer3_07.liw" "skinCluster3.lw[6]";
connectAttr "jnt_layer3_08.liw" "skinCluster3.lw[7]";
connectAttr "jnt_layer3_01.obcc" "skinCluster3.ifcl[0]";
connectAttr "jnt_layer3_02.obcc" "skinCluster3.ifcl[1]";
connectAttr "jnt_layer3_03.obcc" "skinCluster3.ifcl[2]";
connectAttr "jnt_layer3_04.obcc" "skinCluster3.ifcl[3]";
connectAttr "jnt_layer3_05.obcc" "skinCluster3.ifcl[4]";
connectAttr "jnt_layer3_06.obcc" "skinCluster3.ifcl[5]";
connectAttr "jnt_layer3_07.obcc" "skinCluster3.ifcl[6]";
connectAttr "jnt_layer3_08.obcc" "skinCluster3.ifcl[7]";
connectAttr "skinCluster3GroupId.msg" "skinCluster3Set.gn" -na;
connectAttr "layer3_surfaceShape.iog.og[5]" "skinCluster3Set.dsm" -na;
connectAttr "skinCluster3.msg" "skinCluster3Set.ub[0]";
connectAttr "wrap1.og[0]" "skinCluster3GroupParts.ig";
connectAttr "skinCluster3GroupId.id" "skinCluster3GroupParts.gi";
connectAttr "root.msg" "bindPose20.m[0]";
connectAttr "layer3.msg" "bindPose20.m[1]";
connectAttr "jnt_layer3_01.msg" "bindPose20.m[2]";
connectAttr "jnt_layer3_02.msg" "bindPose20.m[3]";
connectAttr "jnt_layer3_03.msg" "bindPose20.m[4]";
connectAttr "jnt_layer3_04.msg" "bindPose20.m[5]";
connectAttr "jnt_layer3_05.msg" "bindPose20.m[6]";
connectAttr "jnt_layer3_06.msg" "bindPose20.m[7]";
connectAttr "jnt_layer3_07.msg" "bindPose20.m[8]";
connectAttr "jnt_layer3_08.msg" "bindPose20.m[9]";
connectAttr "bindPose20.w" "bindPose20.p[0]";
connectAttr "bindPose20.m[0]" "bindPose20.p[1]";
connectAttr "bindPose20.m[1]" "bindPose20.p[2]";
connectAttr "bindPose20.m[1]" "bindPose20.p[3]";
connectAttr "bindPose20.m[1]" "bindPose20.p[4]";
connectAttr "bindPose20.m[1]" "bindPose20.p[5]";
connectAttr "bindPose20.m[1]" "bindPose20.p[6]";
connectAttr "bindPose20.m[1]" "bindPose20.p[7]";
connectAttr "bindPose20.m[1]" "bindPose20.p[8]";
connectAttr "bindPose20.m[1]" "bindPose20.p[9]";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "layer1_surfaceShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "layer2_surfaceShapeDeformed.iog" ":initialShadingGroup.dsm" -na;
connectAttr "layer2_surfaceShapeDeformedDeformed.iog" ":initialShadingGroup.dsm"
		 -na;
connectAttr "layer3_surfaceShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "layer2_surfaceBaseShapeDeformedDeformed.iog" ":initialShadingGroup.dsm"
		 -na;
// End of test_interactivefk01.ma
