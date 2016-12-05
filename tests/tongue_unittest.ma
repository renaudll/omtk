//Maya ASCII 2017 scene
//Name: tongue_unittest.ma
//Last modified: Sun, Dec 04, 2016 01:28:52 PM
//Codeset: UTF-8
requires maya "2017";
requires -nodeType "ilrOptionsNode" -nodeType "ilrUIOptionsNode" -nodeType "ilrBakeLayerManager"
		 -nodeType "ilrBakeLayer" "Turtle" "2017.0.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201608291545-1001872";
fileInfo "osv" "Linux 4.8.10-1-ARCH #1 SMP PREEMPT Mon Nov 21 11:55:43 CET 2016 x86_64";
createNode transform -s -n "persp";
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000241";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 3.1615942874789988 14.246265974419391 41.385488854158645 ;
	setAttr ".r" -type "double3" -18.938352729617069 4.5999999999990528 -9.9713523173432193e-17 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000242";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 43.895356615971806;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -0.16820308349579527 0 1.7763568394002505e-15 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000243";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000244";
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
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000245";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000246";
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
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000247";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000248";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "surface";
	rename -uid "1DFA5860-0000-26CE-5813-5CC000000262";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr ".s" -type "double3" 33.802639176263305 11.857236690500219 11.857236690500219 ;
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsSurface -n "surfaceShape" -p "surface";
	rename -uid "1DFA5860-0000-26CE-5813-5CC000000263";
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
createNode nurbsSurface -n "surfaceShape1Orig" -p "surface";
	rename -uid "1DFA5860-0000-26CE-5813-5CC000000264";
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
		6 0 0 0.33333333333333331 0.66666666666666663 1 1
		4 0 0 1 1
		
		15
		-0.5 2.4452395332311091e-18 0.49999999999999989
		-0.50000000000000022 2.9516652221886997e-17 -5.351758062717843e-17
		-0.5 -1.4251900421985907e-17 -0.49999999999999978
		-0.33333333333333348 2.5653075481454494e-18 0.49999999999999989
		-0.33333333333333337 3.0966001371954062e-17 -5.6145441653305599e-17
		-0.33333333333333348 -1.4951708096927071e-17 -0.49999999999999989
		3.5379636002739961e-17 -3.6909351297667407e-18 0.5
		7.0759272005479921e-17 -4.4553528240610811e-17 8.0781418635074658e-17
		3.5379636002739961e-17 2.1512346426011067e-17 -0.5
		0.33333333333333326 2.6910595635425749e-18 0.50000000000000033
		0.33333333333333326 3.2483962477291531e-17 -5.8897705197054643e-17
		0.33333333333333326 -1.5684644554459186e-17 -0.49999999999999989
		0.49999999999999978 -3.1976183389912009e-18 0.5
		0.50000000000000022 -3.8598667806427429e-17 6.9984471846722727e-17
		0.49999999999999978 1.8637085461562171e-17 -0.49999999999999989
		
		;
createNode joint -n "jnt_root";
	rename -uid "304226C0-0000-07B7-5844-605700001526";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 0 0 -3.8629913759875992e-17 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 180 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-16 0 0 1 0 0
		 1.2246467991473532e-16 0 -1 0 16.883372589744553 0 -3.8629913759875992e-17 1;
	setAttr ".radi" 0.88497247732329609;
createNode joint -n "jnt_tongue_01" -p "jnt_root";
	rename -uid "91A25860-0000-4EB9-5818-ADE9000005A1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -16.883372589744553 0 2.0676168200842827e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-16 0 0 1 0 0
		 1.2246467991473532e-16 0 -1 0 16.883372589744553 0 -3.8629913759875992e-17 1;
	setAttr ".radi" 0.88497247732329609;
createNode joint -n "jnt_tongue_02" -p "jnt_tongue_01";
	rename -uid "91A25860-0000-4EB9-5818-ADEA000005A2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 22.805469476184495 0 7.378682121104886e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-16 0 0 1 0 0
		 1.2246467991473532e-16 0 -1 0 -5.9220968864399417 0 -7.6618315644514935e-14 1;
	setAttr ".radi" 0.72254798618683869;
createNode joint -n "jnt_tongue_03" -p "jnt_tongue_02";
	rename -uid "91A25860-0000-4EB9-5818-ADEC000005A3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 10.689902312645504 0 6.0570943598104596e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -1 0 -1.2246467991473532e-16 0 0 1 0 0
		 1.2246467991473532e-16 0 -1 0 -16.611999199085446 0 -8.3984545469363323e-14 1;
	setAttr ".radi" 0.72254798618683869;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "304226C0-0000-07B7-5844-605300001504";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "304226C0-0000-07B7-5844-605300001505";
	setAttr -s 4 ".dli[1:3]"  1 2 3;
	setAttr -s 4 ".dli";
createNode displayLayer -n "defaultLayer";
	rename -uid "1DFA5860-0000-26CE-5813-5CBE0000025F";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "304226C0-0000-07B7-5844-605300001507";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "1DFA5860-0000-26CE-5813-5CBE00000261";
	setAttr ".g" yes;
createNode network -n "Rig";
	rename -uid "1DFA5860-0000-26CE-5813-5CCE00000291";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".name" -type "string" "untitled";
	setAttr "._class_namespace" -type "string" "Rig";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Rig";
createNode displayLayer -n "layer_anm";
	rename -uid "1DFA5860-0000-26CE-5813-62910000029E";
	setAttr ".c" 17;
	setAttr ".do" 1;
createNode displayLayer -n "layer_rig";
	rename -uid "1DFA5860-0000-26CE-5813-62910000029F";
	setAttr ".dt" 2;
	setAttr ".c" 13;
	setAttr ".do" 2;
createNode displayLayer -n "layer_geo";
	rename -uid "1DFA5860-0000-26CE-5813-6291000002A0";
	setAttr ".dt" 2;
	setAttr ".c" 12;
	setAttr ".do" 3;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "1DFA5860-0000-26CE-5813-6CAC000005A7";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 1\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1237\n                -height 757\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n"
		+ "                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n"
		+ "            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n"
		+ "            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1237\n            -height 757\n            -sceneRenderFilter 0\n            $editorName;\n"
		+ "        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1237\\n    -height 757\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1237\\n    -height 757\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "1DFA5860-0000-26CE-5813-6CAC000005A8";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode ilrOptionsNode -s -n "TurtleRenderOptions";
	rename -uid "91A25860-0000-4EB9-5818-AC9400000599";
lockNode -l 1 ;
createNode ilrUIOptionsNode -s -n "TurtleUIOptions";
	rename -uid "91A25860-0000-4EB9-5818-AC940000059A";
lockNode -l 1 ;
createNode ilrBakeLayerManager -s -n "TurtleBakeLayerManager";
	rename -uid "91A25860-0000-4EB9-5818-AC940000059B";
lockNode -l 1 ;
createNode ilrBakeLayer -s -n "TurtleDefaultBakeLayer";
	rename -uid "91A25860-0000-4EB9-5818-AC940000059C";
lockNode -l 1 ;
createNode skinCluster -n "skinCluster1";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000611";
	setAttr -s 15 ".wl";
	setAttr ".wl[0].w[2]"  1;
	setAttr ".wl[1].w[2]"  1;
	setAttr ".wl[2].w[2]"  1;
	setAttr ".wl[3].w[1]"  1;
	setAttr ".wl[4].w[1]"  1;
	setAttr ".wl[5].w[1]"  1;
	setAttr ".wl[6].w[1]"  1;
	setAttr ".wl[7].w[1]"  1;
	setAttr ".wl[8].w[1]"  1;
	setAttr ".wl[9].w[0]"  1;
	setAttr ".wl[10].w[0]"  1;
	setAttr ".wl[11].w[0]"  1;
	setAttr ".wl[12].w[0]"  1;
	setAttr ".wl[13].w[0]"  1;
	setAttr ".wl[14].w[0]"  1;
	setAttr -s 3 ".pm";
	setAttr ".pm[0]" -type "matrix" -1 0 1.2246467991473532e-16 0 0 1 0 0
		 -1.2246467991473532e-16 0 -1 0 16.883372589744553 0 -2.1062467338441587e-15 1;
	setAttr ".pm[1]" -type "matrix" -1 0 1.2246467991473532e-16 0 0 1 0 0
		 -1.2246467991473532e-16 0 -1 0 -5.9220968864399417 0 -7.5893067944893013e-14 1;
	setAttr ".pm[2]" -type "matrix" -1 0 1.2246467991473532e-16 0 0 1 0 0
		 -1.2246467991473532e-16 0 -1 0 -16.611999199085446 0 -8.1950162304703472e-14 1;
	setAttr ".gm" -type "matrix" 33.802639176263305 0 0 0 0 11.857236690500219 0 0
		 0 0 11.857236690500219 0 0 0 0 1;
	setAttr -s 3 ".ma";
	setAttr -s 3 ".dpf[0:2]"  0.1 0.1 0.1;
	setAttr -s 3 ".lw";
	setAttr -s 3 ".lw";
	setAttr ".mmi" yes;
	setAttr ".mi" 1;
	setAttr ".ucm" yes;
	setAttr -s 3 ".ifcl";
	setAttr -s 3 ".ifcl";
createNode tweak -n "tweak1";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000612";
createNode objectSet -n "skinCluster1Set";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000613";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster1GroupId";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000614";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster1GroupParts";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000615";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode objectSet -n "tweakSet1";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000616";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId2";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000617";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000618";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode dagPose -n "bindPose1";
	rename -uid "91A25860-0000-4EB9-5818-AE6900000619";
	setAttr -s 3 ".wm";
	setAttr -s 3 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 16.883372589744553
		 0 -3.8629913759875992e-17 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 1 0 6.123233995736766e-17 1
		 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 22.805469476184495
		 0 7.378682121104886e-14 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 10.689902312645504
		 0 6.0570943598104596e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0 0 1 1
		 1 1 yes;
	setAttr -s 3 ".m";
	setAttr -s 3 ".p";
	setAttr ".bp" yes;
createNode network -n "Rig2";
	rename -uid "91A25860-0000-4EB9-5818-AF0600000630";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".name" -type "string" "untitled";
	setAttr "._class_namespace" -type "string" "Rig";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Rig";
createNode makeNurbCircle -n "makeNurbCircle2";
	rename -uid "496CE860-0000-06CE-581A-5D410000038F";
	setAttr ".nr" -type "double3" 1 0 0 ;
createNode network -n "Rig4";
	rename -uid "B5FD68C0-0000-6090-582F-313200005F40";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".name" -type "string" "untitled";
	setAttr "._class_namespace" -type "string" "Rig";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Rig";
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "B5FD68C0-0000-6090-582F-315000005F59";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -318.00593782421095 -1089.565669466743 ;
	setAttr ".tgi[0].vh" -type "double2" 1450.3551729201129 463.69237605935314 ;
	setAttr -s 6 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 541.4285888671875;
	setAttr ".tgi[0].ni[0].y" -1.4285714626312256;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 541.4285888671875;
	setAttr ".tgi[0].ni[1].y" -127.14286041259766;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 262.85714721679688;
	setAttr ".tgi[0].ni[2].y" -194.28572082519531;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 1.4285714626312256;
	setAttr ".tgi[0].ni[3].y" -194.28572082519531;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 541.4285888671875;
	setAttr ".tgi[0].ni[4].y" -397.14285278320312;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 820;
	setAttr ".tgi[0].ni[5].y" -127.14286041259766;
	setAttr ".tgi[0].ni[5].nvs" 18304;
createNode network -n "Rig5";
	rename -uid "B5FD68C0-0000-6090-582F-316400005F63";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".name" -type "string" "untitled";
	setAttr "._class_namespace" -type "string" "Rig";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Rig";
createNode network -n "Rig6";
	rename -uid "4CD098C0-0000-7087-582F-31A00000028A";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".name" -type "string" "untitled";
	setAttr "._class_namespace" -type "string" "Rig";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Rig";
createNode network -n "Rig7";
	rename -uid "4CD098C0-0000-7087-582F-31E60000028C";
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
createNode network -n "net_Tongue_tongue";
	rename -uid "4CD098C0-0000-7087-582F-31E60000028D";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "locked" -ln "locked" -nn "locked" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -m -sn "layer4_joints_count" -ln "layer4_joints_count" -nn "layer4_joints_count" 
		-at "long";
	addAttr -ci true -sn "layer2_joints_count" -ln "layer2_joints_count" -nn "layer2_joints_count" 
		-at "long";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -ci true -m -sn "layer3_joints_count" -ln "layer3_joints_count" -nn "layer3_joints_count" 
		-at "long";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "tongue";
	setAttr "._class_namespace" -type "string" "Module.Tongue";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 2 ".layer4_joints_count[0:1]"  7 5;
	setAttr ".layer2_joints_count" 4;
	setAttr -s 4 ".input";
	setAttr "._class" -type "string" "Tongue";
	setAttr -s 2 ".layer3_joints_count[0:1]"  5 3;
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "304226C0-0000-07B7-5844-605400001524";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "304226C0-0000-07B7-5844-605400001525";
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
connectAttr "skinCluster1.og[0]" "surfaceShape.cr";
connectAttr "skinCluster1GroupId.id" "surfaceShape.iog.og[12].gid";
connectAttr "skinCluster1Set.mwc" "surfaceShape.iog.og[12].gco";
connectAttr "groupId2.id" "surfaceShape.iog.og[13].gid";
connectAttr "tweakSet1.mwc" "surfaceShape.iog.og[13].gco";
connectAttr "tweak1.pl[0].cp[0]" "surfaceShape.twl";
connectAttr "jnt_root.s" "jnt_tongue_01.is";
connectAttr "jnt_tongue_01.s" "jnt_tongue_02.is";
connectAttr "jnt_tongue_02.s" "jnt_tongue_03.is";
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
connectAttr "skinCluster1GroupParts.og" "skinCluster1.ip[0].ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1.ip[0].gi";
connectAttr "bindPose1.msg" "skinCluster1.bp";
connectAttr "jnt_tongue_01.wm" "skinCluster1.ma[0]";
connectAttr "jnt_tongue_02.wm" "skinCluster1.ma[1]";
connectAttr "jnt_tongue_03.wm" "skinCluster1.ma[2]";
connectAttr "jnt_tongue_01.liw" "skinCluster1.lw[0]";
connectAttr "jnt_tongue_02.liw" "skinCluster1.lw[1]";
connectAttr "jnt_tongue_03.liw" "skinCluster1.lw[2]";
connectAttr "jnt_tongue_01.obcc" "skinCluster1.ifcl[0]";
connectAttr "jnt_tongue_02.obcc" "skinCluster1.ifcl[1]";
connectAttr "jnt_tongue_03.obcc" "skinCluster1.ifcl[2]";
connectAttr "jnt_tongue_01.msg" "skinCluster1.ptt";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "skinCluster1GroupId.msg" "skinCluster1Set.gn" -na;
connectAttr "surfaceShape.iog.og[12]" "skinCluster1Set.dsm" -na;
connectAttr "skinCluster1.msg" "skinCluster1Set.ub[0]";
connectAttr "tweak1.og[0]" "skinCluster1GroupParts.ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1GroupParts.gi";
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "surfaceShape.iog.og[13]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "surfaceShape1Orig.ws" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "jnt_tongue_01.msg" "bindPose1.m[0]";
connectAttr "jnt_tongue_02.msg" "bindPose1.m[1]";
connectAttr "jnt_tongue_03.msg" "bindPose1.m[2]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[1]" "bindPose1.p[2]";
connectAttr "jnt_tongue_01.bps" "bindPose1.wm[0]";
connectAttr "jnt_tongue_02.bps" "bindPose1.wm[1]";
connectAttr "jnt_tongue_03.bps" "bindPose1.wm[2]";
connectAttr "jnt_tongue_03.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "skinCluster1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn";
connectAttr "jnt_tongue_02.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "jnt_tongue_01.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "bindPose1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn";
connectAttr "surfaceShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn";
connectAttr "net_Tongue_tongue.msg" "Rig7.modules[0]";
connectAttr "Rig7.msg" "net_Tongue_tongue.rig";
connectAttr "jnt_tongue_03.msg" "net_Tongue_tongue.input[0]";
connectAttr "jnt_tongue_02.msg" "net_Tongue_tongue.input[1]";
connectAttr "jnt_tongue_01.msg" "net_Tongue_tongue.input[2]";
connectAttr "surface.msg" "net_Tongue_tongue.input[3]";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "surfaceShape.iog" ":initialShadingGroup.dsm" -na;
// End of tongue_unittest.ma
