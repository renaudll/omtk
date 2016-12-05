//Maya ASCII 2017 scene
//Name: test_interactivefk_2layers.ma
//Last modified: Sun, Dec 04, 2016 06:38:09 PM
//Codeset: UTF-8
requires maya "2017";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201608291545-1001872";
fileInfo "osv" "Linux 4.8.10-1-ARCH #1 SMP PREEMPT Mon Nov 21 11:55:43 CET 2016 x86_64";
createNode transform -s -n "persp";
	rename -uid "60B737C0-0000-5F08-5830-A60C00000223";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 6.2885604226198542 7.2769649190405499 16.608352703812287 ;
	setAttr ".r" -type "double3" -22.538352729602543 21.40000000000002 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "60B737C0-0000-5F08-5830-A60C00000224";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 19.169377114391509;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "60B737C0-0000-5F08-5830-A60C00000225";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "60B737C0-0000-5F08-5830-A60C00000226";
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
	rename -uid "60B737C0-0000-5F08-5830-A60C00000227";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "60B737C0-0000-5F08-5830-A60C00000228";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "60B737C0-0000-5F08-5830-A60C00000229";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "60B737C0-0000-5F08-5830-A60C0000022A";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode joint -n "jnt_root";
	rename -uid "3B0637C0-0000-0C70-5831-23AF00001B55";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 4 0 0 1;
	setAttr ".radi" 0.5;
createNode joint -n "jnt_layer1_01" -p "jnt_root";
	rename -uid "60B737C0-0000-5F08-5830-A65700000268";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -4 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -4 0 0 1;
	setAttr ".radi" 0.5;
createNode joint -n "jnt_layer1_02" -p "jnt_root";
	rename -uid "60B737C0-0000-5F08-5830-A66200000271";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 4 0 0 1;
	setAttr ".radi" 0.5;
createNode joint -n "jnt_layer2_01" -p "jnt_root";
	rename -uid "60B737C0-0000-5F08-5830-A6730000028F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -4 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -4 0 0 1;
	setAttr ".radi" 0.5;
createNode joint -n "jnt_layer2_02" -p "jnt_layer2_01";
	rename -uid "60B737C0-0000-5F08-5830-A67D0000029B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr ".radi" 0.5;
createNode joint -n "jnt_layer2_03" -p "jnt_layer2_02";
	rename -uid "60B737C0-0000-5F08-5830-A67D0000029E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 4 0 0 1;
	setAttr ".radi" 0.5;
createNode transform -n "surface_layer1";
	rename -uid "60B737C0-0000-5F08-5830-A61B0000024D";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsSurface -n "surface_layerShape1" -p "surface_layer1";
	rename -uid "60B737C0-0000-5F08-5830-A61B0000024C";
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
createNode nurbsSurface -n "surface_layerShape1Orig" -p "surface_layer1";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003ED";
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
		1 1 0 0 no 
		3 0 0.5 1
		2 0 1
		
		6
		-4 -6.123233995736766e-17 1
		-4 6.123233995736766e-17 -1
		0 -6.123233995736766e-17 1
		0 6.123233995736766e-17 -1
		4 -6.123233995736766e-17 1
		4 6.123233995736766e-17 -1
		
		;
createNode transform -n "surface_layer2";
	rename -uid "60B737C0-0000-5F08-5830-A65200000260";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsSurface -n "surface_layerShape2" -p "surface_layer2";
	rename -uid "60B737C0-0000-5F08-5830-A65200000261";
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
createNode nurbsSurface -n "surface_layerShape2Orig" -p "surface_layer2";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003D6";
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
		1 1 0 0 no 
		3 0 0.5 1
		2 0 1
		
		6
		-4 -6.123233995736766e-17 1
		-4 6.123233995736766e-17 -1
		0 -6.1232339957367673e-17 1
		0 6.1232339957367673e-17 -1
		4 -6.123233995736766e-17 1
		4 6.123233995736766e-17 -1
		
		;
createNode transform -n "surface_final";
	rename -uid "60B737C0-0000-5F08-5830-A6CE000002BA";
createNode nurbsSurface -n "surface_finalShape" -p "surface_final";
	rename -uid "60B737C0-0000-5F08-5830-A6CE000002BB";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr -av ".iog[0].og[0].gid";
	setAttr -av ".iog[0].og[1].gid";
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
createNode nurbsSurface -n "surface_finalShapeOrig" -p "surface_final";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003DF";
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
		1 1 0 0 no 
		3 0 0.5 1
		2 0 1
		
		6
		-4 -6.123233995736766e-17 1
		-4 6.123233995736766e-17 -1
		0 -6.123233995736766e-17 1
		0 6.123233995736766e-17 -1
		4 -6.123233995736766e-17 1
		4 6.123233995736766e-17 -1
		
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "304226C0-0000-07B7-5844-A7C600005099";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "304226C0-0000-07B7-5844-A7C60000509A";
createNode displayLayer -n "defaultLayer";
	rename -uid "60B737C0-0000-5F08-5830-A60C00000241";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "304226C0-0000-07B7-5844-A7C60000509C";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "60B737C0-0000-5F08-5830-A60C00000243";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "60B737C0-0000-5F08-5830-A6EF000002C6";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 660\n                -height 550\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n"
		+ "                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n"
		+ "            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n"
		+ "            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 660\n            -height 550\n            -sceneRenderFilter 0\n            $editorName;\n"
		+ "        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 660\\n    -height 550\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 660\\n    -height 550\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "60B737C0-0000-5F08-5830-A6EF000002C7";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode blendShape -n "blendShape1";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003D5";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".w[0]"  1;
	setAttr ".mlid" 0;
	setAttr ".mlpr" 0;
	setAttr ".pndr[0]"  0;
	setAttr ".tgdt[0].cid" -type "Int32Array" 1 0 ;
	setAttr ".aal" -type "attributeAlias" {"surface_layer1","weight[0]"} ;
createNode tweak -n "tweak1";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003D7";
createNode objectSet -n "blendShape1Set";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003D8";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "blendShape1GroupId";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003D9";
	setAttr ".ihi" 0;
createNode groupParts -n "blendShape1GroupParts";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003DA";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode objectSet -n "tweakSet1";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003DB";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId2";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003DC";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	rename -uid "3B0637C0-0000-0C70-5831-0A94000003DD";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode blendShape -n "blendShape2";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003DE";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".w[0]"  1;
	setAttr ".mlid" 1;
	setAttr ".mlpr" 0;
	setAttr ".pndr[0]"  0;
	setAttr ".tgdt[0].cid" -type "Int32Array" 1 0 ;
	setAttr ".aal" -type "attributeAlias" {"surface_layer2","weight[0]"} ;
createNode tweak -n "tweak2";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003E0";
createNode objectSet -n "blendShape2Set";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003E1";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "blendShape2GroupId";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003E2";
	setAttr ".ihi" 0;
createNode groupParts -n "blendShape2GroupParts";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003E3";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode objectSet -n "tweakSet2";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003E4";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId4";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003E5";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts4";
	rename -uid "3B0637C0-0000-0C70-5831-0A9A000003E6";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode skinCluster -n "skinCluster1";
	rename -uid "3B0637C0-0000-0C70-5831-0AA0000003E7";
	setAttr -s 6 ".wl";
	setAttr -s 3 ".wl[0].w[0:2]"  0.99631672268283589 0.0034474627082451068 0.00023581460891901451;
	setAttr -s 3 ".wl[1].w[0:2]"  0.99631672268283589 0.0034474627082451068 0.00023581460891901451;
	setAttr -s 3 ".wl[2].w[0:2]"  0.0034364261168384879 0.99312714776632305 0.0034364261168384879;
	setAttr -s 3 ".wl[3].w[0:2]"  0.0034364261168384879 0.99312714776632305 0.0034364261168384879;
	setAttr -s 3 ".wl[4].w[0:2]"  0.00023581460891901451 0.0034474627082451068 0.99631672268283589;
	setAttr -s 3 ".wl[5].w[0:2]"  0.00023581460891901451 0.0034474627082451068 0.99631672268283589;
	setAttr -s 3 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 4 0 0 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr ".pm[2]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -4 0 0 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr -s 3 ".ma";
	setAttr -s 3 ".dpf[0:2]"  4 4 4;
	setAttr -s 3 ".lw";
	setAttr -s 3 ".lw";
	setAttr ".mi" 5;
	setAttr ".ucm" yes;
	setAttr -s 3 ".ifcl";
	setAttr -s 3 ".ifcl";
createNode objectSet -n "skinCluster1Set";
	rename -uid "3B0637C0-0000-0C70-5831-0AA0000003E8";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster1GroupId";
	rename -uid "3B0637C0-0000-0C70-5831-0AA0000003E9";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster1GroupParts";
	rename -uid "3B0637C0-0000-0C70-5831-0AA0000003EA";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode dagPose -n "bindPose5";
	rename -uid "3B0637C0-0000-0C70-5831-0AA0000003EB";
	setAttr -s 4 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 4
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr -s 4 ".m";
	setAttr -s 4 ".p";
	setAttr -s 4 ".g[0:3]" yes no no no;
	setAttr ".bp" yes;
createNode skinCluster -n "skinCluster2";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003EC";
	setAttr -s 6 ".wl";
	setAttr -s 2 ".wl[0].w[0:1]"  0.99976336961665879 0.00023663038334122111;
	setAttr -s 2 ".wl[1].w[0:1]"  0.99976336961665879 0.00023663038334122111;
	setAttr -s 2 ".wl[2].w[0:1]"  0.5 0.5;
	setAttr -s 2 ".wl[3].w[0:1]"  0.5 0.5;
	setAttr -s 2 ".wl[4].w[0:1]"  0.00023663038334122111 0.99976336961665879;
	setAttr -s 2 ".wl[5].w[0:1]"  0.00023663038334122111 0.99976336961665879;
	setAttr -s 2 ".pm";
	setAttr ".pm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 4 0 0 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 -4 0 0 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr -s 2 ".ma";
	setAttr -s 2 ".dpf[0:1]"  4 4;
	setAttr -s 2 ".lw";
	setAttr -s 2 ".lw";
	setAttr ".mi" 5;
	setAttr ".ucm" yes;
	setAttr -s 2 ".ifcl";
	setAttr -s 2 ".ifcl";
createNode tweak -n "tweak3";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003EE";
createNode objectSet -n "skinCluster2Set";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003EF";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster2GroupId";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003F0";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster2GroupParts";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003F1";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode objectSet -n "tweakSet3";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003F2";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId6";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003F3";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts6";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003F4";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode dagPose -n "bindPose6";
	rename -uid "3B0637C0-0000-0C70-5831-0AA3000003F5";
	setAttr -s 3 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
	setAttr -s 3 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 -4
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 4
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr -s 3 ".m";
	setAttr -s 3 ".p";
	setAttr -s 3 ".g[0:2]" yes no no;
	setAttr ".bp" yes;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "3B0637C0-0000-0C70-5831-2B9B0000295F";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" 1450.916487728158 -1044.5621513137771 ;
	setAttr ".tgi[0].vh" -type "double2" 3080.7022107381908 -409.88598033390866 ;
	setAttr -s 26 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 1.4285714626312256;
	setAttr ".tgi[0].ni[0].y" -567.14288330078125;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 820;
	setAttr ".tgi[0].ni[1].y" -504.28570556640625;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 820;
	setAttr ".tgi[0].ni[2].y" -127.14286041259766;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 524.28570556640625;
	setAttr ".tgi[0].ni[3].y" -252.85714721679688;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 2160;
	setAttr ".tgi[0].ni[4].y" -782.85711669921875;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 2420;
	setAttr ".tgi[0].ni[5].y" -782.85711669921875;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 2835.71435546875;
	setAttr ".tgi[0].ni[6].y" -778.5714111328125;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" 262.85714721679688;
	setAttr ".tgi[0].ni[7].y" -190;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" 262.85714721679688;
	setAttr ".tgi[0].ni[8].y" -504.28570556640625;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" 1.4285714626312256;
	setAttr ".tgi[0].ni[9].y" -692.85711669921875;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" 262.85714721679688;
	setAttr ".tgi[0].ni[10].y" -755.71429443359375;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" 820;
	setAttr ".tgi[0].ni[11].y" -378.57144165039062;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" 820;
	setAttr ".tgi[0].ni[12].y" -1.4285714626312256;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" 524.28570556640625;
	setAttr ".tgi[0].ni[13].y" -630;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" 1727.142822265625;
	setAttr ".tgi[0].ni[14].y" -782.85711669921875;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" 820;
	setAttr ".tgi[0].ni[15].y" -755.71429443359375;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" 262.85714721679688;
	setAttr ".tgi[0].ni[16].y" -630;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" 820;
	setAttr ".tgi[0].ni[17].y" -630;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" 1081.4285888671875;
	setAttr ".tgi[0].ni[18].y" -127.14286041259766;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" 1467.142822265625;
	setAttr ".tgi[0].ni[19].y" -782.85711669921875;
	setAttr ".tgi[0].ni[19].nvs" 18304;
	setAttr ".tgi[0].ni[20].x" 1.4285714626312256;
	setAttr ".tgi[0].ni[20].y" -190;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" 1.4285714626312256;
	setAttr ".tgi[0].ni[21].y" -315.71429443359375;
	setAttr ".tgi[0].ni[21].nvs" 18304;
	setAttr ".tgi[0].ni[22].x" 820;
	setAttr ".tgi[0].ni[22].y" -252.85714721679688;
	setAttr ".tgi[0].ni[22].nvs" 18304;
	setAttr ".tgi[0].ni[23].x" 2835.71435546875;
	setAttr ".tgi[0].ni[23].y" -690;
	setAttr ".tgi[0].ni[23].nvs" 18304;
	setAttr ".tgi[0].ni[24].x" 262.85714721679688;
	setAttr ".tgi[0].ni[24].y" -315.71429443359375;
	setAttr ".tgi[0].ni[24].nvs" 18304;
	setAttr ".tgi[0].ni[25].x" 1.4285714626312256;
	setAttr ".tgi[0].ni[25].y" -441.42855834960938;
	setAttr ".tgi[0].ni[25].nvs" 18304;
createNode network -n "Rig";
	rename -uid "3B0637C0-0000-0C70-5831-2C4100002BE4";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -s false -ci true -m -sn "modules" -ln "modules" -nn "modules" -at "message";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".name" -type "string" "untitled";
	setAttr -s 2 ".modules";
	setAttr "._class_namespace" -type "string" "Rig";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Rig";
createNode network -n "net_InteractiveFK_surface_layer1";
	rename -uid "3B0637C0-0000-0C70-5831-2C4100002BE5";
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
	setAttr ".name" -type "string" "layer1";
	setAttr "._class_namespace" -type "string" "Module.InteractiveFK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 3 ".input";
	setAttr "._class" -type "string" "InteractiveFK";
createNode network -n "net_InteractiveFK_surface_layer2";
	rename -uid "3B0637C0-0000-0C70-5831-2C4100002BE6";
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
	setAttr ".name" -type "string" "layer2";
	setAttr "._class_namespace" -type "string" "Module.InteractiveFK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 4 ".input";
	setAttr "._class" -type "string" "InteractiveFK";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "304226C0-0000-07B7-5844-A7C6000050C2";
	setAttr ".bsdt[0].bscd" -type "Int32Array" 2 0 1 ;
	setAttr -s 2 ".bspr";
	setAttr -s 2 ".obsv";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "304226C0-0000-07B7-5844-A7C6000050C3";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -k on ".ihi";
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
	setAttr -s 3 ".dsm";
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
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
	setAttr ".ovt" no;
	setAttr ".povt" no;
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
connectAttr "jnt_root.s" "jnt_layer1_01.is";
connectAttr "jnt_root.s" "jnt_layer1_02.is";
connectAttr "jnt_root.s" "jnt_layer2_01.is";
connectAttr "jnt_layer2_01.s" "jnt_layer2_02.is";
connectAttr "jnt_layer2_02.s" "jnt_layer2_03.is";
connectAttr "skinCluster2GroupId.id" "surface_layerShape1.iog.og[6].gid";
connectAttr "skinCluster2Set.mwc" "surface_layerShape1.iog.og[6].gco";
connectAttr "groupId6.id" "surface_layerShape1.iog.og[7].gid";
connectAttr "tweakSet3.mwc" "surface_layerShape1.iog.og[7].gco";
connectAttr "skinCluster2.og[0]" "surface_layerShape1.cr";
connectAttr "tweak3.pl[0].cp[0]" "surface_layerShape1.twl";
connectAttr "blendShape1GroupId.id" "surface_layerShape2.iog.og[5].gid";
connectAttr "blendShape1Set.mwc" "surface_layerShape2.iog.og[5].gco";
connectAttr "groupId2.id" "surface_layerShape2.iog.og[6].gid";
connectAttr "tweakSet1.mwc" "surface_layerShape2.iog.og[6].gco";
connectAttr "skinCluster1GroupId.id" "surface_layerShape2.iog.og[7].gid";
connectAttr "skinCluster1Set.mwc" "surface_layerShape2.iog.og[7].gco";
connectAttr "skinCluster1.og[0]" "surface_layerShape2.cr";
connectAttr "tweak1.pl[0].cp[0]" "surface_layerShape2.twl";
connectAttr "blendShape2GroupId.id" "surface_finalShape.iog.og[5].gid";
connectAttr "blendShape2Set.mwc" "surface_finalShape.iog.og[5].gco";
connectAttr "groupId4.id" "surface_finalShape.iog.og[6].gid";
connectAttr "tweakSet2.mwc" "surface_finalShape.iog.og[6].gco";
connectAttr "blendShape2.og[0]" "surface_finalShape.cr";
connectAttr "tweak2.pl[0].cp[0]" "surface_finalShape.twl";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "blendShape1GroupParts.og" "blendShape1.ip[0].ig";
connectAttr "blendShape1GroupId.id" "blendShape1.ip[0].gi";
connectAttr "surface_layerShape1.ws" "blendShape1.it[0].itg[0].iti[6000].igt";
connectAttr "shapeEditorManager.obsv[0]" "blendShape1.tgdt[0].dpvs";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "blendShape1GroupId.msg" "blendShape1Set.gn" -na;
connectAttr "surface_layerShape2.iog.og[5]" "blendShape1Set.dsm" -na;
connectAttr "blendShape1.msg" "blendShape1Set.ub[0]";
connectAttr "tweak1.og[0]" "blendShape1GroupParts.ig";
connectAttr "blendShape1GroupId.id" "blendShape1GroupParts.gi";
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "surface_layerShape2.iog.og[6]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "surface_layerShape2Orig.ws" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "blendShape2GroupParts.og" "blendShape2.ip[0].ig";
connectAttr "blendShape2GroupId.id" "blendShape2.ip[0].gi";
connectAttr "surface_layerShape2.ws" "blendShape2.it[0].itg[0].iti[6000].igt";
connectAttr "shapeEditorManager.obsv[1]" "blendShape2.tgdt[0].dpvs";
connectAttr "groupParts4.og" "tweak2.ip[0].ig";
connectAttr "groupId4.id" "tweak2.ip[0].gi";
connectAttr "blendShape2GroupId.msg" "blendShape2Set.gn" -na;
connectAttr "surface_finalShape.iog.og[5]" "blendShape2Set.dsm" -na;
connectAttr "blendShape2.msg" "blendShape2Set.ub[0]";
connectAttr "tweak2.og[0]" "blendShape2GroupParts.ig";
connectAttr "blendShape2GroupId.id" "blendShape2GroupParts.gi";
connectAttr "groupId4.msg" "tweakSet2.gn" -na;
connectAttr "surface_finalShape.iog.og[6]" "tweakSet2.dsm" -na;
connectAttr "tweak2.msg" "tweakSet2.ub[0]";
connectAttr "surface_finalShapeOrig.ws" "groupParts4.ig";
connectAttr "groupId4.id" "groupParts4.gi";
connectAttr "skinCluster1GroupParts.og" "skinCluster1.ip[0].ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1.ip[0].gi";
connectAttr "bindPose5.msg" "skinCluster1.bp";
connectAttr "jnt_layer2_01.wm" "skinCluster1.ma[0]";
connectAttr "jnt_layer2_02.wm" "skinCluster1.ma[1]";
connectAttr "jnt_layer2_03.wm" "skinCluster1.ma[2]";
connectAttr "jnt_layer2_01.liw" "skinCluster1.lw[0]";
connectAttr "jnt_layer2_02.liw" "skinCluster1.lw[1]";
connectAttr "jnt_layer2_03.liw" "skinCluster1.lw[2]";
connectAttr "jnt_layer2_01.obcc" "skinCluster1.ifcl[0]";
connectAttr "jnt_layer2_02.obcc" "skinCluster1.ifcl[1]";
connectAttr "jnt_layer2_03.obcc" "skinCluster1.ifcl[2]";
connectAttr "skinCluster1GroupId.msg" "skinCluster1Set.gn" -na;
connectAttr "surface_layerShape2.iog.og[7]" "skinCluster1Set.dsm" -na;
connectAttr "skinCluster1.msg" "skinCluster1Set.ub[0]";
connectAttr "blendShape1.og[0]" "skinCluster1GroupParts.ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1GroupParts.gi";
connectAttr "jnt_layer2_01.msg" "bindPose5.m[1]";
connectAttr "jnt_layer2_02.msg" "bindPose5.m[2]";
connectAttr "jnt_layer2_03.msg" "bindPose5.m[3]";
connectAttr "bindPose5.w" "bindPose5.p[0]";
connectAttr "bindPose5.m[0]" "bindPose5.p[1]";
connectAttr "bindPose5.m[0]" "bindPose5.p[2]";
connectAttr "bindPose5.m[0]" "bindPose5.p[3]";
connectAttr "jnt_layer2_01.bps" "bindPose5.wm[1]";
connectAttr "jnt_layer2_02.bps" "bindPose5.wm[2]";
connectAttr "jnt_layer2_03.bps" "bindPose5.wm[3]";
connectAttr "skinCluster2GroupParts.og" "skinCluster2.ip[0].ig";
connectAttr "skinCluster2GroupId.id" "skinCluster2.ip[0].gi";
connectAttr "bindPose6.msg" "skinCluster2.bp";
connectAttr "jnt_layer1_01.wm" "skinCluster2.ma[0]";
connectAttr "jnt_layer1_02.wm" "skinCluster2.ma[1]";
connectAttr "jnt_layer1_01.liw" "skinCluster2.lw[0]";
connectAttr "jnt_layer1_02.liw" "skinCluster2.lw[1]";
connectAttr "jnt_layer1_01.obcc" "skinCluster2.ifcl[0]";
connectAttr "jnt_layer1_02.obcc" "skinCluster2.ifcl[1]";
connectAttr "groupParts6.og" "tweak3.ip[0].ig";
connectAttr "groupId6.id" "tweak3.ip[0].gi";
connectAttr "skinCluster2GroupId.msg" "skinCluster2Set.gn" -na;
connectAttr "surface_layerShape1.iog.og[6]" "skinCluster2Set.dsm" -na;
connectAttr "skinCluster2.msg" "skinCluster2Set.ub[0]";
connectAttr "tweak3.og[0]" "skinCluster2GroupParts.ig";
connectAttr "skinCluster2GroupId.id" "skinCluster2GroupParts.gi";
connectAttr "groupId6.msg" "tweakSet3.gn" -na;
connectAttr "surface_layerShape1.iog.og[7]" "tweakSet3.dsm" -na;
connectAttr "tweak3.msg" "tweakSet3.ub[0]";
connectAttr "surface_layerShape1Orig.ws" "groupParts6.ig";
connectAttr "groupId6.id" "groupParts6.gi";
connectAttr "jnt_layer1_01.msg" "bindPose6.m[1]";
connectAttr "jnt_layer1_02.msg" "bindPose6.m[2]";
connectAttr "bindPose6.w" "bindPose6.p[0]";
connectAttr "bindPose6.m[0]" "bindPose6.p[1]";
connectAttr "bindPose6.m[0]" "bindPose6.p[2]";
connectAttr "jnt_layer1_01.bps" "bindPose6.wm[1]";
connectAttr "jnt_layer1_02.bps" "bindPose6.wm[2]";
connectAttr "jnt_layer1_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr ":initialShadingGroup.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "blendShape2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "surface_layerShape2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "surface_layer2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn";
connectAttr "surface_layerShape1Orig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "tweak1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn";
connectAttr "skinCluster2Set.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn";
connectAttr "jnt_layer1_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn";
connectAttr "tweak3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn";
connectAttr "skinCluster1Set.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "blendShape1Set.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn";
connectAttr "surface_layerShape1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "tweakSet3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn";
connectAttr "skinCluster2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn";
connectAttr "blendShape1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn";
connectAttr "surface_finalShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn"
		;
connectAttr "surface_layer1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn";
connectAttr "jnt_layer2_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn";
connectAttr "jnt_layer2_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn";
connectAttr "tweakSet1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[22].dn";
connectAttr "surface_layerShape2Orig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[23].dn"
		;
connectAttr "skinCluster1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[24].dn";
connectAttr "jnt_layer2_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn";
connectAttr "net_InteractiveFK_surface_layer1.msg" "Rig.modules[0]";
connectAttr "net_InteractiveFK_surface_layer2.msg" "Rig.modules[1]";
connectAttr "Rig.msg" "net_InteractiveFK_surface_layer1.rig";
connectAttr "jnt_layer1_01.msg" "net_InteractiveFK_surface_layer1.input[0]";
connectAttr "jnt_layer1_02.msg" "net_InteractiveFK_surface_layer1.input[1]";
connectAttr "surface_layer1.msg" "net_InteractiveFK_surface_layer1.input[2]";
connectAttr "Rig.msg" "net_InteractiveFK_surface_layer2.rig";
connectAttr "jnt_layer2_01.msg" "net_InteractiveFK_surface_layer2.input[0]";
connectAttr "jnt_layer2_02.msg" "net_InteractiveFK_surface_layer2.input[1]";
connectAttr "jnt_layer2_03.msg" "net_InteractiveFK_surface_layer2.input[2]";
connectAttr "surface_layer2.msg" "net_InteractiveFK_surface_layer2.input[3]";
connectAttr "blendShape1.mlpr" "shapeEditorManager.bspr[0]";
connectAttr "blendShape2.mlpr" "shapeEditorManager.bspr[1]";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "surface_layerShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "surface_layerShape2.iog" ":initialShadingGroup.dsm" -na;
connectAttr "surface_finalShape.iog" ":initialShadingGroup.dsm" -na;
// End of test_interactivefk_2layers.ma
