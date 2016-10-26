//Maya ASCII 2016 scene
//Name: rig_rlessard_template01.ma
//Last modified: Tue, Oct 25, 2016 08:36:55 PM
//Codeset: UTF-8
requires maya "2016";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2016";
fileInfo "version" "2016";
fileInfo "cutIdentifier" "201511301000-979500";
fileInfo "osv" "Linux 4.7.6-1-ARCH #1 SMP PREEMPT Fri Sep 30 19:28:42 CEST 2016 x86_64";
createNode transform -s -n "persp";
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007A2";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 66.599772410963638 66.394920369451597 183.30370519553543 ;
	setAttr ".r" -type "double3" -12.938352729602453 20.599999999999952 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007A3";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 194.25617749639147;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -0.012405463373085013 22.900466298296571 6.0848779807062803 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007A4";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007A5";
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
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007A6";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007A7";
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
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007A8";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007A9";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode joint -n "jnt_spine";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007B3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0 24.660126221656352 3.2722338254853867 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 -1.3019526725788757 89.999999999999986 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 0.99974183554494289 0.022721405353294168 0 -1 2.2204460492503131e-16 1.7347234759768075e-18 0
		 -5.2041704279304221e-18 -0.022721405353294168 0.99974183554494267 0 0 24.660126221656352 3.2722338254853867 1;
createNode joint -n "jnt_chest" -p "jnt_spine";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007B4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.3309289313962083 -4.1443686500635792e-15 -4.4408920985006262e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 -8.3032514824340371 0 ;
	setAttr ".bps" -type "matrix" 2.1896549702620862e-16 0.98598088545809348 0.16685830369290752 0 -1 2.2204460492503131e-16 1.7347234759768075e-18 0
		 -3.7215602618009697e-17 -0.16685830369290755 0.98598088545809315 0 6.2162510782189964e-15 33.988646238869812 3.4842456440584195 1;
createNode joint -n "jnt_neck" -p "jnt_chest";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007B5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.9883546478918177 6.6671657644728754e-16 0 ;
	setAttr ".r" -type "double3" 0 1.5902773407317584e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 -8.8297446679091465 0 ;
	setAttr ".bps" -type "matrix" 2.1065794691877385e-16 0.94868329805051377 0.31622776601683877 0 -1 2.2204460492503131e-16 1.7347234759768075e-18 0
		 -7.0385505369523665e-17 -0.31622776601683883 0.94868329805051355 0 7.0797430506427571e-15 40.87903034249338 4.6503106462100945 1;
createNode joint -n "jnt_head" -p "jnt_neck";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007B6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 6.7044023756517461 5.3481300932498026e-16 -5.3290705182007514e-15 ;
	setAttr ".r" -type "double3" 0 9.5416640443905487e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 18.43494882292206 0 ;
	setAttr ".bps" -type "matrix" 2.22105526966423e-16 1.0000000000000002 5.5511151231257827e-17 0 -1 2.2204460492503131e-16 1.7347234759768075e-18 0
		 -1.5766142109418165e-19 -5.5511151231257827e-17 1 0 7.9572656810899234e-15 47.239384899684374 6.7704288319404284 1;
createNode joint -n "jnt_shoulder_l" -p "jnt_chest";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007B7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.3592734104324649 0.0124 -1.5877576799933699 ;
	setAttr ".r" -type "double3" 3.1805546814635168e-15 -7.1562480332929135e-15 -1.9878466759146992e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -10.098083794452366 19.424574084562412 -101.19755341168045 ;
	setAttr ".bps" -type "matrix" 0.92512711464709396 -0.12508026192057944 -0.3584616434468576 0 0.13398425880981635 0.99098346020061534 0 0
		 0.35522955977216603 -0.048028217608975909 0.93354445538355468 0 -0.012399999999992552 39.537717934659113 2.8129861911369334 1;
createNode joint -n "jnt_upperarm_l" -p "jnt_shoulder_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007B8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 7.2507015329504494 0 -1.5543122344752192e-15 ;
	setAttr ".r" -type "double3" -4.3060078335626351e-08 -4.1139787951260765e-05 1.4939595395702354e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 8.5492594840313032 -15.929476023711487 -24.458139221936779 ;
	setAttr ".bps" -type "matrix" 0.85392413936539757 -0.51720551732475184 -0.057550126480321373 0 0.51806414751067431 0.85534176740297119 -1.27675647831893e-15 0
		 0.049225026897943169 -0.029814657214158082 0.99834261801352475 0 6.6954205883457121 38.630798287809725 0.21388780349286396 1;
createNode joint -n "jnt_forearm_l" -p "jnt_upperarm_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007B9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 8.7168369293212855 -7.1054273576010019e-15 -1.7763568394002505e-15 ;
	setAttr ".r" -type "double3" -2.7973206163579128e-07 8.63965891486322e-05 -3.2585333990751131e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.045924972875659706 -20.854682520336237 0.76085402846638428 ;
	setAttr ".bps" -type "matrix" 0.82186286780188289 -0.4832788958072507 0.30163377694779014 0 0.5068877694515822 0.86201205860498253 -8.6984889777208529e-14 0
		 -0.2600119530115188 0.15289447238839302 0.95342386408365642 0 14.138938305514555 34.122401986370924 -0.2877672807631364 1;
createNode joint -n "jnt_hand_l" -p "jnt_forearm_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007BA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 9.4334993362426882 1.4210854715202004e-14 -7.1054273576010019e-15 ;
	setAttr ".r" -type "double3" 0 -7.2229451968657286e-06 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -15.36658169580295 0 ;
	setAttr ".bps" -type "matrix" 0.72357977298600962 -0.42548562225762071 0.54350188350875095 0 0.5068877694515822 0.86201205860498253 -8.6984889777208529e-14 0
		 -0.46850517745902687 0.27549445742454748 0.83940794767647964 0 21.891981260569302 29.563390762897271 2.5576948042027805 1;
createNode joint -n "jnt_finger11_l" -p "jnt_hand_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007BB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -0.050600784169943402 -1.383560841903865 3.0567197902313543 ;
	setAttr ".r" -type "double3" 1.0336802714756419e-14 1.9083328088781101e-14 -3.0215269473903401e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 67.387008515058398 -3.6496452397602632 -38.405180162427605 ;
	setAttr ".bps" -type "matrix" 0.22180180627879123 -0.84962545906379261 0.478477311940812 0 -0.12085997294158772 0.46296155886062945 0.87809991570315893 0
		 -0.96757264619873584 -0.25259290237054521 -1.27675647831893e-15 0 19.72196843982864 29.234383899610418 5.0960280684396979 1;
createNode joint -n "jnt_finger12_l" -p "jnt_finger11_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.5167103276139571 -3.5527136788005009e-15 0 ;
	setAttr ".r" -type "double3" 1.6623367827336658e-14 3.3029314924495153e-14 -1.751789883149827e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.7238269992968138 3.4464000207603229 -1.9918618052693271 ;
	setAttr ".bps" -type "matrix" 0.28362549325688546 -0.84845419368057851 0.44685798728525361 0 -0.14167183312078155 0.42380555978045586 0.89460490676016957 0
		 -0.94841218427168339 -0.3170399481532481 2.6656378591287797e-16 0 20.280179336373905 27.096122732180817 6.3002168609301004 1;
createNode joint -n "jne_finger13_l" -p "jnt_finger12_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007BD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.642236987250417 -1.7763568394002505e-15 -7.1054273576010019e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -31.774757366131844 0 0 ;
	setAttr ".bps" -type "matrix" 0.28362549325688569 -0.84845419368057851 0.44685798728525322 0 0.37897739553578003 0.52723491508211118 0.76052579048397539 0
		 -0.88087042931846971 -0.046355426264874433 0.47108222340489214 0 1.719807288128784 1.9359557758266399 0.40660707280246783 1;
createNode joint -n "jnt_finger21_l" -p "jnt_hand_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007BE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.9935053449197584 0.88828087747057793 1.1015224179800516 ;
	setAttr ".r" -type "double3" -2.149048617289655e-14 1.9083328088781104e-14 9.9702934838846524e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -16.447413400142686 -3.776069358203368 -25.94261907985392 ;
	setAttr ".bps" -type "matrix" 0.39713236944024433 -0.73992307873521246 0.54295461937235789 0 0.88111041558712477 0.47291059994874751 4.7184478546569153e-16 0
		 -0.25676899479232607 0.47840297032012735 0.83976203849794107 0 23.992210935195462 29.358869427172817 5.1092972696563734 1;
createNode joint -n "jnt_finger22_l" -p "jnt_finger21_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007BF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.8091753173145353 -7.1054273576010019e-15 -7.1054273576010019e-15 ;
	setAttr ".r" -type "double3" -2.6637145457256954e-14 3.0959414643667439e-30 1.3318572728628477e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -22.49239372634711 -0.78160287188943645 -39.493117054948641 ;
	setAttr ".bps" -type "matrix" -0.25738501579708878 -0.86515660104960401 0.43041492690592081 0 0.95848298858975467 -0.28514971608622097 8.8817841970012523e-16 0
		 0.12273269420649402 0.41254538547442809 0.90263114875156547 0 25.504957754573876 26.540372698943255 7.1775066041914624 1;
createNode joint -n "jne_finger23_l" -p "jnt_finger22_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.2289780444176834 3.5527136788005009e-15 3.5527136788005009e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 47.898174153137717 47.71216193048118 113.81878459103081 ;
	setAttr ".bps" -type "matrix" 0.56913558799734232 -0.24562469229314035 -0.78469942845067764 0 0.49795535724438261 0.86239177804430911 0.091218876079428635 0
		 0.65431272696359688 -0.44266119289754258 0.61312798308019345 0 1.9700711248517355 1.8452939163227504 0.49289274456033177 1;
createNode joint -n "jnt_finger31_l" -p "jnt_hand_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.1352685685464428 0.85458473882011532 -1.2242673240078408 ;
	setAttr ".r" -type "double3" 1.3914926731402923e-15 2.4649298781342254e-14 1.7592443081845079e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -20.557234595721603 -2.2871610418975288 -34.500071828479768 ;
	setAttr ".bps" -type "matrix" 0.29027222323707375 -0.82724073481350924 0.48105592510872586 0 0.9435955930587836 0.3311002216248764 2.7755575615628914e-16 0
		 -0.15927772341745949 0.45392225094741007 0.87668990921407763 0 25.167352311607782 28.628762552857115 3.2340594546606858 1;
createNode joint -n "jnt_finger32_l" -p "jnt_finger31_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.0694332995969607 0 -1.7763568394002505e-15 ;
	setAttr ".r" -type "double3" -1.2324649390671124e-14 4.7708320221952744e-15 1.192708005548818e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -19.717476097987067 -4.0861774257148777 -39.175141443507037 ;
	setAttr ".bps" -type "matrix" -0.3814447613800997 -0.81593924574169852 0.43444567125723238 0 0.90589654887028925 -0.42349904692324825 5.5511151231257827e-16 0
		 0.18398732771736809 0.39356283426356342 0.90069803970356932 0 26.348595762796776 25.262361559823962 5.1916844552665546 1;
createNode joint -n "jne_finger33_l" -p "jnt_finger32_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 4.295824279279433 -1.7763568394002505e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 23.603073342575488 -10.602097130109492 112.83444044218663 ;
	setAttr ".bps" -type "matrix" 1 5.0098813986210189e-15 7.716050021144838e-15 0 -5.1209037010835345e-15 1.0000000000000002 7.382983113757291e-15 0
		 -7.9658502016854966e-15 -7.3274719625260332e-15 1 0 1.9937399895170815 1.7546153283734247 0.33646248954541069 1;
createNode joint -n "jnt_finger41_l" -p "jnt_hand_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 1.9671059115781639 -0.33460465562706787 -2.9927571406343381 ;
	setAttr ".r" -type "double3" -1.9083328088781094e-14 1.590277340731759e-14 2.8426207465580184e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -20.318986087148993 3.3191106588546693 -36.034071617857101 ;
	setAttr ".bps" -type "matrix" 0.31359406143913732 -0.86569143207986698 0.39017574124183585 0 0.94021227767493998 0.34058900879109649 3.8857805861880479e-16 0
		 -0.1328895689638887 0.36684802236649439 0.92074040366782195 0 24.547854517234217 27.613494227384393 1.1146764428927405 1;
createNode joint -n "jnt_finger42_l" -p "jnt_finger41_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.5498778095362522 7.1054273576010019e-15 -4.4408920985006262e-15 ;
	setAttr ".r" -type "double3" -7.9016905367609244e-15 2.3854160110976376e-15 6.8332229484567742e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -15.022784131185174 -5.562964436274993 -37.568617682057869 ;
	setAttr ".bps" -type "matrix" -0.33604881460098074 -0.85405668253584932 0.39706218306599739 0 0.93055610909792641 -0.3661493244845993 3.8857805861880479e-16 0
		 0.14538405010799477 0.3694886401438231 0.91779170990964187 0 25.661075117139362 24.540395422738413 2.4997526485464885 1;
createNode joint -n "jne_finger43_l" -p "jnt_finger42_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 3.5659211796855423 3.5527136788005009e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 21.928947484350523 -8.3595193068847475 109.85601310020324 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 1.9706458687096529e-15 4.7739590058881731e-15 0 -2.005340338229189e-15 1 2.9976021664879227e-15 0
		 -4.8849813083506888e-15 -2.9420910152566648e-15 1 0 1.9738025246855753 1.7334594148477831 0.083047842683514297 1;
createNode joint -n "jnt_shoulder_r" -p "jnt_chest";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.3593267173401813 0.0124 -1.5877667041099706 ;
	setAttr ".r" -type "double3" -1.1131941385122306e-14 1.5902773407317592e-15 1.2722218725854064e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 169.90191620554768 -19.424574084562405 -78.802446588319668 ;
	setAttr ".bps" -type "matrix" 0.92512711464709441 0.12508026192057828 0.35846164344685749 0 0.1339842588098159 -0.99098346020061556 -9.4368957093138306e-16 0
		 0.35522955977216591 0.048028217608976534 -0.93354445538355502 0 -0.012399999999992552 39.537771999999975 2.8129861882306537 1;
createNode joint -n "jnt_upperarm_r" -p "jnt_shoulder_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -7.2507001384745955 1.6659686700393198e-05 -3.7681972542280562e-07 ;
	setAttr ".r" -type "double3" 1.7095481412866394e-14 -2.7829853462805787e-15 1.4014319065198616e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 8.5492594840313849 -15.929476023711512 -24.458139221936801 ;
	setAttr ".bps" -type "matrix" 0.85392413936539791 0.51720551732475128 0.057550126480321095 0 0.5180641475106742 -0.85534176740297152 -9.4368957093138306e-16 0
		 0.049225026897941955 0.029814657214159927 -0.99834261801352508 0 -6.7202172000000013 38.630836000000023 0.21388865223065737 1;
createNode joint -n "jnt_forearm_r" -p "jnt_upperarm_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007C9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -8.716869354248054 -2.4962742820378025e-05 -2.5771794294193739e-06 ;
	setAttr ".r" -type "double3" 1.6648216604333457e-15 3.1706814146407725e-06 2.5065504639758321e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.045924972864049098 -20.854682520336215 0.76085402846643713 ;
	setAttr ".bps" -type "matrix" 0.8218628349988234 0.48327887651811169 -0.30163389723154249 0 0.50688776945152858 -0.86201205860501429 -1.0849079880997925e-13 0
		 -0.26001205669766753 -0.15289453335857886 -0.95342382602959508 0 -14.163775746197114 34.122444153724857 -0.2877657306643685 1;
createNode joint -n "jnt_hand_r" -p "jnt_forearm_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007CA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -9.4334917068481374 0.00011736123267525045 -8.4560241631059796e-07 ;
	setAttr ".r" -type "double3" 0 -3.1805546814635168e-15 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -15.366581695802966 0 ;
	setAttr ".bps" -type "matrix" 0.72357977298598275 0.42548562225766717 -0.54350188350875084 0 0.50688776945152858 -0.86201205860501429 -1.0849079880997925e-13 0
		 -0.4685051774591269 -0.2754944574243765 -0.8394079476764803 0 -21.916752001157722 29.563336003796728 2.5576958429099803 1;
createNode joint -n "jnt_finger11_r" -p "jnt_hand_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007CB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.050606310861213366 1.3835242906529643 -3.0567234350985202 ;
	setAttr ".r" -type "double3" -3.9756933518293952e-15 -1.2722218725854064e-14 4.7708320221952752e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 67.38700851504953 -3.6496452397672901 -38.405180162423946 ;
	setAttr ".bps" -type "matrix" 0.22180180627879165 0.84962545906379294 -0.47847731194081194 0 -0.12085997294158796 -0.46296155886062879 -0.87809991570315937 0
		 -0.96757264619873595 0.25259290237054588 1.7208456881689926e-15 0 -19.746752001157713 29.234364003796717 5.0960291629099812 1;
createNode joint -n "jnt_finger12_r" -p "jnt_finger11_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007CC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.516714170440645 2.0854070985620865e-06 3.7205543936380536e-05 ;
	setAttr ".r" -type "double3" -1.5157330903849568e-14 4.2925064158033009e-15 1.141148232392281e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.7238269992974316 3.4464000207603251 -1.9918618052693255 ;
	setAttr ".bps" -type "matrix" 0.28362549325688591 0.84845419368057851 -0.4468579872852535 0 -0.14167183312079196 -0.42380555978045181 -0.89460490676017024 0
		 -0.94841218427168195 0.31703994815325331 9.8077063999293157e-15 0 -20.305000001157723 27.096108003796736 6.3002179629099739 1;
createNode joint -n "jne_finger13_r" -p "jnt_finger12_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007CD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.6421832366865257 -2.6078026168718793e-05 3.3400545788708769e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -31.774757366132441 0 0 ;
	setAttr ".bps" -type "matrix" 0.28362549325688552 0.84845419368057839 -0.4468579872852535 0 0.37897739553577936 -0.5272349150821114 -0.76052579048397595 0
		 -0.88087042931846971 0.046355426264874794 -0.4710822234048917 0 -1.7198099999999996 1.9359600000000003 0.40660699999999994 1;
createNode joint -n "jnt_finger21_r" -p "jnt_hand_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007CE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -2.993545001639911 -0.88836168713722685 -1.1014953763539546 ;
	setAttr ".r" -type "double3" 7.8582063907252973e-16 -1.6697912077683464e-14 -5.7468958001737028e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -16.447413400152968 -3.776069358208296 -25.942619079850093 ;
	setAttr ".bps" -type "matrix" 0.39713236944024538 0.73992307873521213 -0.54295461937235756 0 0.88111041558712477 -0.47291059994874785 1.1934897514720433e-15 0
		 -0.25676899479232451 -0.47840297032012746 -0.83976203849794173 0 -24.017064001157721 29.358860003796721 5.1092971629099804 1;
createNode joint -n "jnt_finger22_r" -p "jnt_finger21_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007CF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.8091639045568666 7.340515885800869e-05 -6.2661494144578e-06 ;
	setAttr ".r" -type "double3" 1.3517357396219949e-14 -1.5902773407317584e-14 -9.9392333795734887e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -22.492393726347025 -0.78160287188937827 -39.493117054948648 ;
	setAttr ".bps" -type "matrix" -0.25738501579708811 0.86515660104960446 -0.43041492690592065 0 0.95848298858975467 0.28514971608621997 -4.9960036108132044e-16 0
		 0.12273269420649408 -0.41254538547442771 -0.90263114875156591 0 -25.52974000115773 26.540340003796736 7.1775055629099835 1;
createNode joint -n "jne_finger23_r" -p "jnt_finger22_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.2289931086499521 -7.9172758944423549e-06 1.0632750893080356e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 47.898174153137781 47.712161930481173 113.81878459103073 ;
	setAttr ".bps" -type "matrix" 0.56913558799734232 0.24562469229314049 0.78469942845067697 0 0.49795535724438406 -0.86239177804430844 -0.091218876079429689 0
		 0.65431272696359577 0.44266119289754369 -0.61312798308019367 0 -1.97007 1.8452900000000003 0.49289299999999991 1;
createNode joint -n "jnt_finger31_r" -p "jnt_hand_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.1353162505394385 -0.85466448750021584 1.2242972566659054 ;
	setAttr ".r" -type "double3" -6.559894030518502e-15 -1.3517357396219944e-14 4.1744780194208652e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -20.557234595730989 -2.287161041903925 -34.500071828476287 ;
	setAttr ".bps" -type "matrix" 0.29027222323707447 0.82724073481350924 -0.48105592510872536 0 0.94359559305878371 -0.33110022162487679 6.106226635438361e-16 0
		 -0.15927772341745844 -0.45392225094740962 -0.8766899092140783 0 -25.19221200115771 28.628748003796712 3.2340612829099795 1;
createNode joint -n "jnt_finger32_r" -p "jnt_finger31_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.0693854308160109 2.1324520389498502e-06 -2.2250689363900733e-05 ;
	setAttr ".r" -type "double3" -3.379339349054986e-15 -2.3854160110976368e-15 6.361109362927032e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -19.717476097987067 -4.0861774257148475 -39.175141443507073 ;
	setAttr ".bps" -type "matrix" -0.38144476138009942 0.81593924574169907 -0.4344456712572321 0 0.90589654887028948 0.42349904692324775 3.3306690738754696e-16 0
		 0.1839873277173687 -0.39356283426356253 -0.90069803970356987 0 -26.373436001157742 25.262396003796745 5.1916827629099824 1;
createNode joint -n "jne_finger33_r" -p "jnt_finger32_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -4.2958190591571608 4.6541408737610368e-05 8.8237688800063552e-07 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 23.603073342575517 -10.602097130109502 112.8344404421866 ;
	setAttr ".bps" -type "matrix" 1.0000000000000004 -4.8711035205428743e-15 -8.0491169285323849e-15 0 -4.496403249731884e-15 -1.0000000000000004 -7.8825834748386114e-15 0
		 -8.354428260304303e-15 8.1046280797636427e-15 -1 0 -1.9937400000000003 1.7546199999999996 0.33646200000000004 1;
createNode joint -n "jnt_finger41_r" -p "jnt_hand_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D4";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -1.9671655620574049 0.33456570047268741 2.992799478615304 ;
	setAttr ".r" -type "double3" -2.5046868116525194e-14 -8.7465253740246766e-15 -2.8624992133171654e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -20.318986087158173 3.3191106588480181 -36.034071617854501 ;
	setAttr ".bps" -type "matrix" 0.31359406143913826 0.86569143207986676 -0.39017574124183574 0 0.94021227767493987 -0.34058900879109738 -1.1102230246251563e-16 0
		 -0.13288956896388837 -0.36684802236649405 -0.92074040366782239 0 -24.572708001157721 27.613436003796711 1.1146743629099811 1;
createNode joint -n "jnt_finger42_r" -p "jnt_finger41_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.5498506323752679 6.5941734533225826e-05 -1.5637648921540404e-05 ;
	setAttr ".r" -type "double3" 1.2945851476894474e-14 -8.7465253740246751e-15 1.1243757760642511e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -15.022784131185146 -5.5629644362749699 -37.568617682057805 ;
	setAttr ".bps" -type "matrix" -0.33604881460097924 0.85405668253584988 -0.39706218306599739 0 0.93055610909792708 0.36614932448459758 -3.0531133177191805e-16 0
		 0.14538405010799443 -0.36948864014382338 -0.91779170990964221 0 -25.685856001157727 24.540344003796719 2.4997543629099814 1;
createNode joint -n "jne_finger43_r" -p "jnt_finger42_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" -3.5658747534714905 3.308679361069266e-05 -1.9073877540520812e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 21.928947484350537 -8.359519306884728 109.8560131002032 ;
	setAttr ".bps" -type "matrix" 0.99999999999999989 -1.915134717478395e-15 -5.1902926401226068e-15 0 -1.6167622796103842e-15 -1.0000000000000004 -2.886579864025407e-15 0
		 -5.2458037913538647e-15 3.1086244689504383e-15 -1.0000000000000002 0 -1.9738 1.73346 0.083047799999999949 1;
createNode joint -n "jnt_hips" -p "jnt_spine";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 2.1316282072803009e-14 2.5448757812034989e-17 0 ;
	setAttr ".r" -type "double3" 0 4.2241741863187335e-16 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -1.103483979833826e-32 0.20990694580978311 -179.99999999999997 ;
	setAttr ".bps" -type "matrix" 3.4452603867391094e-16 -0.99965188521009973 -0.026383866204443329 0 1 3.4436302076355502e-16 1.1138177107854707e-17 0
		 -3.9420053669764686e-18 -0.026383866204443329 0.9996518852100994 0 -2.544875781202947e-17 24.660126221656373 3.2722338254853875 1;
createNode joint -n "jne_hips" -p "jnt_hips";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 5.9204869265686568 5.8936955648038863e-16 1.6875389974302379e-13 ;
	setAttr ".r" -type "double3" 0 -1.987846675914698e-16 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -2.7587099495845651e-33 0.20990694580815089 180 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 0.99974183554494267 0.022721405353294175 0 -0.99999999999999989 2.2204460492503131e-16 -1.7347234759768075e-18 0
		 -5.2041704279304221e-18 -0.022721405353294175 0.99974183554494267 0 0 1.98871985658519 0.031159739778607365 1;
createNode joint -n "jnt_thigh_l" -p "jnt_hips";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007D9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.88237774749891074 3.5875245700067184 -0.3744042385550217 ;
	setAttr ".r" -type "double3" -3.3793393490549844e-15 -5.0193128566846126e-15 -2.539474128481026e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.32654655883898681 -12.847080088880078 12.226393936134848 ;
	setAttr ".bps" -type "matrix" 0.20647366249584431 -0.95838795015602973 0.19713235069687624 0 0.97757093724454924 0.21060641646163905 -5.2041704279304213e-18 0
		 -0.04151733794892818 0.19271085683196656 0.98037688482987173 0 3.5875245700067171 23.787933874238057 2.8746793861514202 1;
createNode joint -n "jnt_calf_l" -p "jnt_thigh_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007DA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" 11.322528743743906 -8.8817841970012523e-15 0 ;
	setAttr ".r" -type "double3" 0 -2.901791022518843e-06 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 27.722328051074136 0 ;
	setAttr ".bps" -type "matrix" 0.20208637930910744 -0.93802351582932531 -0.28155457561355235 0 0.97757093724454924 0.21060641646163905 -5.2041704279304213e-18 0
		 0.059297200208347854 -0.27523957036803182 0.95954521568869922 0 5.9253285484419838 12.936558760938606 5.1067160932386049 1;
createNode joint -n "jnt_foot_l" -p "jnt_calf_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007DB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 9.5312850713729826 -1.7763568394002505e-15 -1.9984014443252814e-15 ;
	setAttr ".r" -type "double3" -4.8446684488792746 -19.053546684224585 2.5745237664734377 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.59091778135313844 -38.093740956083501 1.9494499084004999 ;
	setAttr ".bps" -type "matrix" 0.22170541056684831 -0.72409416941007887 0.65309596902117961 0 0.97109441616414083 0.22470252537946048 -0.080525834257831233 0
		 -0.08844402648122697 0.65207086188114682 0.75298157033579938 0 7.8514714386786943 3.9959892279177591 2.423139169916396 1;
createNode joint -n "jnt_toes_l" -p "jnt_foot_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007DC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 3.6651260312005687 0 5.3290705182007514e-15 ;
	setAttr ".r" -type "double3" -1.987846675914698e-16 -6.3611093629270335e-15 9.9392333795734887e-17 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 1.3053021610053457 -36.122006918795542 1.8749295500070076 ;
	setAttr ".bps" -type "matrix" 0.15251568619890118 -0.19424509873638968 0.96902415195915947 0 0.95804105896680924 0.26982702529010683 -0.096699047341981023 0
		 -0.24268558835875056 0.94311304626751036 0.22724763400965192 0 8.6640497102052585 1.3420928385723283 4.8168182068480867 1;
createNode joint -n "jne_toes_l" -p "jnt_toes_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007DD";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 4.1369675478651162 0 1.1657341758564144e-15 ;
	setAttr ".r" -type "double3" 7.9513867036587919e-16 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -4.5172613679282128 -6.9835097691796237 0.55034912683864468 ;
createNode joint -n "jnt_thigh_r" -p "jnt_hips";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007DE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".t" -type "double3" 0.88238018351800906 -3.5875183999999969 -0.37440417298135659 ;
	setAttr ".r" -type "double3" -7.951386703658789e-16 -7.9513867036587919e-15 -4.7708320221952752e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 179.67345344116194 12.847080088880078 167.77360606386512 ;
	setAttr ".bps" -type "matrix" 0.20647366249584445 0.95838795015602996 -0.19713235069687635 0 0.97757093724454869 -0.21060641646164241 -1.593516985032295e-14 0
		 -0.041517337948944126 -0.19271085683196329 -0.98037688482987195 0 -3.5875183999999973 23.787931437336887 2.8746793874306555 1;
createNode joint -n "jnt_calf_r" -p "jnt_thigh_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007DF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".t" -type "double3" -11.322519874572755 -7.4449822022870657e-06 -3.6480890672763167e-06 ;
	setAttr ".r" -type "double3" 0 7.6308131172183726e-06 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0 27.722328051074136 0 ;
	setAttr ".bps" -type "matrix" 0.20208636840858904 0.93802346523239744 0.28155475200542135 0 0.97757093724454869 -0.21060641646164241 -1.593516985032295e-14 0
		 0.059297237357593242 0.27523974280359959 -0.95954516393089373 0 -5.9253276737243059 12.936567095131586 5.1067179226194801 1;
createNode joint -n "jnt_foot_r" -p "jnt_calf_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007E0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -9.5312895059585472 2.1178298634794146e-06 9.2764192927141664e-07 ;
	setAttr ".r" -type "double3" -4.8446565247949742 -19.053550531221536 2.5744890062772137 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -0.59091778135764261 -38.093740956083487 1.9494499084007011 ;
	setAttr ".bps" -type "matrix" 0.22170487383426599 0.72409440439690964 -0.65309589069233764 0 0.97109454009461615 -0.22470212856326577 0.08052544701871428 0
		 -0.088444011196679398 -0.65207073768129153 -0.75298167968631136 0 -7.851469230898835 3.9959936939145311 2.4231371793631191 1;
createNode joint -n "jnt_toes_r" -p "jnt_foot_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007E1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -3.665133407918213 -6.6584807800751378e-06 1.7224165911322586e-06 ;
	setAttr ".r" -type "double3" 1.8503774362149631e-05 -1.8313037854952169e-14 2.1866283863920485e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 1.3053021610092232 -36.122006918795691 1.8749295500044563 ;
	setAttr ".bps" -type "matrix" 0.15251526516359232 0.19424537215237936 -0.96902416341877839 0 0.9580411294099318 -0.26982694209851904 0.096698581565114877 0
		 -0.24268557487214151 -0.94311301375558787 -0.22724778334195472 0 -8.6640537890388583 1.3420914749101245 4.8168189137884276 1;
createNode joint -n "jne_toes_r" -p "jnt_toes_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007E2";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -4.1369651531707508 2.6819344949302604e-06 -1.6476318880354055e-06 ;
	setAttr ".r" -type "double3" -1.8636062586700294e-17 1.0871036508908505e-17 -2.981770013872047e-16 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -4.5172613679276132 -6.9835097691795758 0.55034912683857939 ;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "EC7EB7C0-0000-2F37-580F-FAA300000981";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "EC7EB7C0-0000-2F37-580F-FAA300000982";
	setAttr -s 4 ".dli[1:3]"  3 4 1;
	setAttr -s 4 ".dli";
createNode displayLayer -n "defaultLayer";
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007AC";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "EC7EB7C0-0000-2F37-580F-FAA300000984";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "EC7EB7C0-0000-2F37-580F-F37F000007AE";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007E7";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode shadingEngine -n "___Default";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007E8";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo1";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007E9";
createNode dagPose -n "bindPose1";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007EA";
	setAttr -s 37 ".wm";
	setAttr -s 37 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 -3.4694469519536142e-18 0 0 0
		 24.660126221656352 3.2722338254853867 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.0080337484255059901 -0.0080337484255059918 0.70706114225449801 0.70706114225449823 1
		 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 -8.3266726846886741e-17 0 0 9.3309289313962083
		 -4.1443686500635816e-15 -4.4408920985006262e-16 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 -0.072396148395920887 0 0.99737595604537999 1
		 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 -8.3266726846886728e-17 -4.1633363423443352e-17 2.2204460492503126e-16 0 5.3593267173401884
		 0.0124 -1.5877667041099719 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.74926534078878082 -0.63469433345451531 0.074790229960738835 0.17369793802984709 1
		 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 5.0653925498522767e-16 -1.8041124150158806e-16 4.5276282722994665e-16 0 -7.2507001384745902
		 1.6659686728814904e-05 -3.768197222031589e-07 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.042874116424811134 -0.15067892218656087 -0.19910001901848295 0.96737627373030388 1
		 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 1.2037062152420219e-33 1.3877787807814457e-16 1.7347234759768068e-17 0 5.3592734104324649
		 0.0124 -1.5877576799933699 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.074790229960738613 0.17369793802984743 -0.74926534078878115 0.6346943334545152 1
		 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 1.4710455076283326e-15 2.4286128663674954e-17 4.7184478546569163e-16 0 7.2507015329504449
		 0 -3.5527136788005009e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.042874116424810517 -0.15067892218656051 -0.19910001901848293 0.96737627373030399 1
		 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 -3.4694469519536142e-18 0 0 2.1316282072803009e-14
		 2.5448757812034203e-17 4.4408920985006262e-16 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.0018317826391891206 5.1890178971811187e-19 -0.99999832228477403 2.8327646962435537e-16 1
		 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 -1.3877787807814452e-17 -1.3877787807814457e-16 -8.3266726846886741e-17 0 0.88238018351800906
		 -3.5875183999999978 -0.37440417298135609 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.10550710741281298 0.98810111938114653 -0.0090984428946303854 0.1115421288123874 1
		 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 1.331828134998326e-07 0 0 -11.322519874572755
		 -7.4449822022870657e-06 -3.6480890672763167e-06 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0.23957002054685281 0 0.97087908889582164 1
		 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 -0.084555207485898606 -0.33254719096493041 0.044933309715934344 0 -9.5312895059585472
		 2.1178298634794146e-06 9.2764192927141664e-07 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.00067775002946285096 -0.3263728801801663 0.014397183101266389 0.94513121039173653 1
		 1 1 yes;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 3.2295178666562468e-07 -3.1962280661127511e-16 3.8163864860112018e-17 0 -3.665133407918213
		 -6.6584807800751378e-06 1.7224165911322586e-06 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.015900060256136796 -0.30979062955615655 0.019084914089267033 0.95048025754207888 1
		 1 1 yes;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 -8.6736173798840281e-17 -2.2204460492503126e-16 -4.1243050641348579e-16 0 0.88237774749891429
		 3.5875245700067167 -0.37440423855502031 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.0090984428946222964 -0.1115421288123882 0.10550710741281163 0.98810111938114675 1
		 1 1 yes;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 0 -5.0645807547766728e-08 0 0 11.322528743743906
		 -8.8817841970012523e-15 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0.23957002054685281 0 0.97087908889582164 1
		 1 1 yes;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 -0.084555415600429937 -0.33254712382216733 0.044933916395807093 0 9.5312850713729826
		 -1.7763568394002505e-15 -1.9984014443252814e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.00067775002949943455 -0.32637288018016603 0.014397183101277569 0.94513121039173653 1
		 1 1 yes;
	setAttr ".xm[14]" -type "matrix" "xform" 1 1 1 -5.2041704279304213e-18 -2.2204460492503136e-16 3.469446951953615e-18 0 3.6651260312005687
		 -1.7763568394002505e-15 7.1054273576010019e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.015900060256111539 -0.30979062955615588 0.019084914089277732 0.95048025754207932 1
		 1 1 yes;
	setAttr ".xm[15]" -type "matrix" "xform" 1 1 1 0 -5.5511151231257827e-17 0 0 6.9883546478918248
		 6.6671657644728952e-16 -8.8817841970012523e-16 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 -0.076977831713692671 0 0.99703280458802268 1
		 1 1 yes;
	setAttr ".xm[16]" -type "matrix" "xform" 1 1 1 0 1.1102230246251563e-16 0 0 6.704402375651739
		 5.3481300932497878e-16 -1.7763568394002505e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 0.16018224300696762 0 0.98708745763749661 1
		 1 1 yes;
	setAttr ".xm[17]" -type "matrix" "xform" 1 1 1 -1.3010426069826051e-18 -5.0821976835258065e-21 -6.9388939039072284e-18 0 -8.7168697357177756
		 -2.4962743253809094e-05 -2.5771793860096537e-06 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.00080755735450235345 -0.18098709309522301 0.0064574688485070936 0.98346393989822045 1
		 1 1 yes;
	setAttr ".xm[18]" -type "matrix" "xform" 1 1 1 0 0 0 0 -9.4334913730621448
		 0.00011736123448713442 -8.4560240343201087e-07 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 -0.13369717957236801 0 0.99102223192741445 1
		 1 1 yes;
	setAttr ".xm[19]" -type "matrix" "xform" 1 1 1 -8.673622782801485e-19 1.2615979044395354e-07 -8.5651972173486233e-18 0 8.716837215423574
		 0 -1.3322676295501878e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.00080755735440262474 -0.1809870930952239 0.0064574688484882996 0.98346393989822067 1
		 1 1 yes;
	setAttr ".xm[20]" -type "matrix" "xform" 1 1 1 0 -1.2615979078089986e-07 0 0 9.4334995031356961
		 1.4210854715202004e-14 -5.3290705182007514e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0 -0.13369717957236787 0 0.99102223192741445 1
		 1 1 yes;
	setAttr ".xm[21]" -type "matrix" "xform" 1 1 1 -4.3715031594615539e-16 -1.5265566588595912e-16 -4.9960036108132054e-16 0 -1.9671655620574049
		 0.33456570047268741 2.992799478615304 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.15885215635100344 0.08164289402849445 -0.29946456217508155 0.93724138101055665 1
		 1 1 yes;
	setAttr ".xm[22]" -type "matrix" "xform" 1 1 1 2.2594773274597917e-16 -1.526556658859591e-16 1.9624059321987633e-16 0 -3.5498506323752679
		 6.5941734533225826e-05 -1.5637648921540404e-05 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.13910676258442584 -0.0035038957465071477 -0.32487287811004462 0.93546493487803939 1
		 1 1 yes;
	setAttr ".xm[23]" -type "matrix" "xform" 1 1 1 -3.3306690738754686e-16 2.7755575615628923e-16 4.9613091412936693e-16 0 1.9671059115781639
		 -0.33460465562706787 -2.9927571406343381 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.15885215635090855 0.081642894028528326 -0.29946456217509909 0.9372413810105642 1
		 1 1 yes;
	setAttr ".xm[24]" -type "matrix" "xform" 1 1 1 -1.3791051634015616e-16 4.163336342344337e-17 1.1926223897340549e-17 0 3.5498778095362522
		 7.1054273576010019e-15 -4.4408920985006262e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.13910676258442614 -0.0035038957465071616 -0.32487287811004489 0.93546493487803906 1
		 1 1 yes;
	setAttr ".xm[25]" -type "matrix" "xform" 1 1 1 -1.1449174941446924e-16 -2.3592239273284572e-16 7.2858385991025886e-17 0 -3.1353162505394385
		 -0.85466448750021584 1.2242972566659054 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.17619841141502712 0.034148644738717537 -0.29512606675143627 0.93845010235022963 1
		 1 1 yes;
	setAttr ".xm[26]" -type "matrix" "xform" 1 1 1 -5.8980598183211429e-17 -4.1633363423443364e-17 1.1102230246251563e-16 0 -4.0693854308160109
		 2.1324520389498502e-06 -2.2250689363900733e-05 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.17298405707830825 0.024272457794404199 -0.33583751205493878 0.92558118460030081 1
		 1 1 yes;
	setAttr ".xm[27]" -type "matrix" "xform" 1 1 1 2.4286128663675367e-17 4.3021142204224816e-16 3.0704605524789491e-16 0 3.1352685685464428
		 0.85458473882011532 -1.2242673240078408 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.17619841141493311 0.034148644738751191 -0.29512606675145836 0.93845010235023918 1
		 1 1 yes;
	setAttr ".xm[28]" -type "matrix" "xform" 1 1 1 -2.1510571102112398e-16 8.3266726846886728e-17 2.0816681711721673e-17 0 4.0694332995969607
		 0 -1.7763568394002505e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.17298405707830847 0.02427245779440397 -0.33583751205493867 0.92558118460030081 1
		 1 1 yes;
	setAttr ".xm[29]" -type "matrix" "xform" 1 1 1 1.3715157481941645e-17 -2.9143354396410359e-16 -1.0030225348206523e-16 0 -2.993545001639911
		 -0.88836168713722685 -1.1014953763539546 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.14663202848861581 0.00031381580561846978 -0.22662674538457331 0.96288071328558122 1
		 1 1 yes;
	setAttr ".xm[30]" -type "matrix" "xform" 1 1 1 2.3592239273284581e-16 -2.7755575615628914e-16 -1.7347234759768068e-16 0 -3.8091639045568666
		 7.340515885800869e-05 -6.2661494144578e-06 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.18581294733858161 0.059593357146885233 -0.33261695394457891 0.92265277452243277 1
		 1 1 yes;
	setAttr ".xm[31]" -type "matrix" "xform" 1 1 1 -3.7507974157136016e-16 3.3306690738754701e-16 1.7401444868392339e-16 0 2.9935053449197584
		 0.88828087747057793 1.1015224179800516 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.14663202848851997 0.00031381580564451839 -0.22662674538459959 0.96288071328558955 1
		 1 1 yes;
	setAttr ".xm[32]" -type "matrix" "xform" 1 1 1 -4.649058915617843e-16 5.4034372002214386e-32 2.3245294578089215e-16 0 3.8091753173145353
		 -7.1054273576010019e-15 -7.1054273576010019e-15 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 -0.18581294733858245 0.059593357146884969 -0.3326169539445788 0.92265277452243277 1
		 1 1 yes;
	setAttr ".xm[33]" -type "matrix" "xform" 1 1 1 -6.9388939039072271e-17 -2.2204460492503126e-16 8.3266726846886741e-17 0 0.050606310861213366
		 1.3835242906529643 -3.0567234350985202 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.5149046474820671 -0.20739040271746431 -0.25683691683102888 0.79113666519431858 1
		 1 1 yes;
	setAttr ".xm[34]" -type "matrix" "xform" 1 1 1 -2.6454533008646303e-16 7.4918370118748356e-17 1.9916793908558712e-16 0 -2.516714170440645
		 2.0854070985620865e-06 3.7205543936380536e-05 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.015556203358375783 0.02980169105800835 -0.017823851058125739 0.99927582482546518 1
		 1 1 yes;
	setAttr ".xm[35]" -type "matrix" "xform" 1 1 1 1.8041124150158777e-16 3.3306690738754696e-16 -5.2735593669694926e-16 0 -0.050600784169943402
		 -1.383560841903865 3.0567197902313543 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.51490464748213949 -0.20739040271745279 -0.25683691683107079 0.79113666519426085 1
		 1 1 yes;
	setAttr ".xm[36]" -type "matrix" "xform" 1 1 1 2.9013250135712094e-16 5.7647029511054271e-16 -3.0574501264091215e-16 0 2.5167103276139571
		 -3.5527136788005009e-15 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 1 0.015556203358370416 0.02980169105800844 -0.017823851058125593 0.99927582482546518 1
		 1 1 yes;
	setAttr -s 37 ".m";
	setAttr -s 37 ".p";
	setAttr ".bp" yes;
createNode multiplyDivide -n "multiplyDivide1";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007EB";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 18.150337 1 1 ;
createNode condition -n "condition1";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007EC";
	setAttr ".op" 2;
	setAttr ".st" 1;
createNode multiplyDivide -n "multiplyDivide2";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007ED";
	setAttr ".i1" -type "float3" 8.7168369 0 -1.3322676e-15 ;
createNode multiplyDivide -n "multiplyDivide3";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007EE";
	setAttr ".i1" -type "float3" 9.4334993 1.4210855e-14 -5.3290705e-15 ;
createNode multiplyDivide -n "multiplyDivide4";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007EF";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 18.150362 1 1 ;
createNode condition -n "condition2";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F0";
	setAttr ".op" 2;
	setAttr ".st" 1;
createNode multiplyDivide -n "multiplyDivide5";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F1";
	setAttr ".i1" -type "float3" -8.7168694 -2.4962743e-05 -2.5771794e-06 ;
createNode multiplyDivide -n "multiplyDivide6";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F2";
	setAttr ".i1" -type "float3" -9.4334917 0.00011736123 -8.4560241e-07 ;
createNode multiplyDivide -n "multiplyDivide7";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F3";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 20.853813 1 1 ;
createNode condition -n "condition3";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F4";
	setAttr ".op" 2;
	setAttr ".st" 1;
createNode multiplyDivide -n "multiplyDivide8";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F5";
	setAttr ".i1" -type "float3" 11.322529 -8.8817842e-15 0 ;
createNode multiplyDivide -n "multiplyDivide9";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F6";
	setAttr ".i1" -type "float3" 9.5312853 -1.7763568e-15 -1.9984014e-15 ;
createNode multiplyDivide -n "multiplyDivide10";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F7";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 20.853809 1 1 ;
createNode condition -n "condition7";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F8";
	setAttr ".op" 2;
	setAttr ".st" 1;
createNode multiplyDivide -n "multiplyDivide11";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007F9";
	setAttr ".i1" -type "float3" -11.32252 -7.4449822e-06 -3.648089e-06 ;
createNode multiplyDivide -n "multiplyDivide12";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007FA";
	setAttr ".i1" -type "float3" -9.5312891 2.1178298e-06 9.2764191e-07 ;
createNode multiplyDivide -n "multiplyDivide13";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007FB";
createNode plusMinusAverage -n "plusMinusAverage1";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007FC";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  18.15033722 0;
createNode plusMinusAverage -n "plusMinusAverage2";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007FD";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  17.8506794 18.15033722;
createNode multiplyDivide -n "multiplyDivide14";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007FE";
	setAttr ".op" 2;
createNode condition -n "condition8";
	rename -uid "EC7EB7C0-0000-2F37-580F-F385000007FF";
createNode multiplyDivide -n "multiplyDivide15";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000800";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "multiplyDivide16";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000801";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 2.7182817 0 0 ;
createNode plusMinusAverage -n "plusMinusAverage3";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000802";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  1 1;
createNode multiplyDivide -n "multiplyDivide17";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000803";
createNode plusMinusAverage -n "plusMinusAverage4";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000804";
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode condition -n "condition9";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000805";
	setAttr ".op" 2;
createNode blendTwoAttr -n "blendTwoAttr1";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000806";
createNode multiplyDivide -n "multiplyDivide18";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000807";
	setAttr ".op" 2;
createNode condition -n "condition10";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000808";
	setAttr ".op" 2;
createNode blendTwoAttr -n "blendTwoAttr2";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000809";
	setAttr -s 2 ".i[0:1]"  1 1;
createNode multiplyDivide -n "multiplyDivide19";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000080A";
	setAttr ".op" 2;
createNode multiplyDivide -n "multiplyDivide20";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000080B";
	setAttr ".i2" -type "float3" 8.7168369 0 -1.3322676e-15 ;
createNode multiplyDivide -n "multiplyDivide21";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000080C";
	setAttr ".i2" -type "float3" 9.4334993 1.4210855e-14 -5.3290705e-15 ;
createNode multiplyDivide -n "multiplyDivide22";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000080D";
createNode plusMinusAverage -n "plusMinusAverage5";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000080E";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  18.15036201 0;
createNode plusMinusAverage -n "plusMinusAverage6";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000080F";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  17.85070419 18.15036201;
createNode multiplyDivide -n "multiplyDivide23";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000810";
	setAttr ".op" 2;
createNode condition -n "condition11";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000811";
createNode multiplyDivide -n "multiplyDivide24";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000812";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode multiplyDivide -n "multiplyDivide25";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000813";
	setAttr ".op" 3;
	setAttr ".i1" -type "float3" 2.7182817 0 0 ;
createNode plusMinusAverage -n "plusMinusAverage7";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000814";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[0:1]"  1 1;
createNode multiplyDivide -n "multiplyDivide26";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000815";
createNode plusMinusAverage -n "plusMinusAverage8";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000816";
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode condition -n "condition12";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000817";
	setAttr ".op" 2;
createNode blendTwoAttr -n "blendTwoAttr3";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000818";
createNode multiplyDivide -n "multiplyDivide27";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000819";
	setAttr ".op" 2;
createNode condition -n "condition13";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000081A";
	setAttr ".op" 2;
createNode blendTwoAttr -n "blendTwoAttr4";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000081B";
	setAttr -s 2 ".i[0:1]"  1 1;
createNode multiplyDivide -n "multiplyDivide28";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000081C";
	setAttr ".op" 2;
createNode multiplyDivide -n "multiplyDivide29";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000081D";
	setAttr ".i2" -type "float3" -8.7168694 -2.4962743e-05 -2.5771794e-06 ;
createNode multiplyDivide -n "multiplyDivide30";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000081E";
	setAttr ".i2" -type "float3" -9.4334917 0.00011736123 -8.4560241e-07 ;
createNode displayLayer -n "layer_anm";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000081F";
	setAttr ".c" 17;
	setAttr ".do" 1;
createNode displayLayer -n "layer_rig";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000820";
	setAttr ".dt" 2;
	setAttr ".c" 13;
	setAttr ".do" 2;
createNode displayLayer -n "layer_geo";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000821";
	setAttr ".dt" 2;
	setAttr ".c" 12;
	setAttr ".do" 3;
createNode network -n "Rig";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000822";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -s false -ci true -m -sn "modules" -ln "modules" -nn "modules" -at "message";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	setAttr ".name" -type "string" "untitled";
	setAttr -s 12 ".modules";
	setAttr "._class_namespace" -type "string" "Rig";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "Rig";
createNode network -n "net_FK_jnt_spine";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000823";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "spine";
	setAttr "._class_namespace" -type "string" "Module.FK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 2 ".input";
	setAttr "._class" -type "string" "FK";
createNode network -n "net_FK_jnt_neck";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000824";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "neck";
	setAttr "._class_namespace" -type "string" "Module.FK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "FK";
createNode network -n "net_FK_jnt_head";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000825";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "head";
	setAttr "._class_namespace" -type "string" "Module.FK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "FK";
createNode network -n "net_FK_jnt_shoulder_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000826";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "shoulder_l";
	setAttr "._class_namespace" -type "string" "Module.FK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "FK";
createNode network -n "net_Arm_jnt_hand_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000827";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "arm_l";
	setAttr "._class_namespace" -type "string" "Module.Limb.Arm";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 3 ".input";
	setAttr "._class" -type "string" "Arm";
createNode network -n "net_Hand_jne_finger13_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000828";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "hand_l";
	setAttr "._class_namespace" -type "string" "Module.Hand";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 12 ".input";
	setAttr "._class" -type "string" "Hand";
createNode network -n "net_FK_jnt_shoulder_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F38500000829";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "shoulder_r";
	setAttr "._class_namespace" -type "string" "Module.FK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "FK";
createNode network -n "net_Arm_jnt_hand_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000082A";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "arm_r";
	setAttr "._class_namespace" -type "string" "Module.Limb.Arm";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 3 ".input";
	setAttr "._class" -type "string" "Arm";
createNode network -n "net_Hand_jne_finger13_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000082B";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "hand_r";
	setAttr "._class_namespace" -type "string" "Module.Hand";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 12 ".input";
	setAttr "._class" -type "string" "Hand";
createNode network -n "net_Leg_jne_toes_l";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000082C";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "leg_l";
	setAttr "._class_namespace" -type "string" "Module.Limb.Leg";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 5 ".input";
	setAttr "._class" -type "string" "Leg";
createNode network -n "net_Leg_jne_toes_r";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000082D";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "leg_r";
	setAttr "._class_namespace" -type "string" "Module.Limb.Leg";
	setAttr "._class_module" -type "string" "omtk";
	setAttr -s 5 ".input";
	setAttr "._class" -type "string" "Leg";
createNode network -n "net_FK_jnt_hips";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000082E";
	addAttr -ci true -sn "_uid" -ln "_uid" -nn "_uid" -at "long";
	addAttr -ci true -sn "iCtrlIndex" -ln "iCtrlIndex" -nn "iCtrlIndex" -at "long";
	addAttr -ci true -sn "canPinTo" -ln "canPinTo" -nn "canPinTo" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "name" -ln "name" -nn "name" -dt "string";
	addAttr -ci true -sn "_class_namespace" -ln "_class_namespace" -nn "_class_namespace" 
		-dt "string";
	addAttr -ci true -sn "_class_module" -ln "_class_module" -nn "_class_module" -dt "string";
	addAttr -s false -ci true -m -sn "input" -ln "input" -nn "input" -at "message";
	addAttr -ci true -sn "_class" -ln "_class" -nn "_class" -dt "string";
	addAttr -s false -ci true -sn "rig" -ln "rig" -nn "rig" -at "message";
	setAttr ".iCtrlIndex" 2;
	setAttr ".canPinTo" yes;
	setAttr ".name" -type "string" "hips";
	setAttr "._class_namespace" -type "string" "Module.FK";
	setAttr "._class_module" -type "string" "omtk";
	setAttr "._class" -type "string" "FK";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "EC7EB7C0-0000-2F37-580F-F3850000082F";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n"
		+ "                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n"
		+ "            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n"
		+ "            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n"
		+ "        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n"
		+ "                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n"
		+ "                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n"
		+ "            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n"
		+ "            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n"
		+ "            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n"
		+ "                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n"
		+ "                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n"
		+ "                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n"
		+ "            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n"
		+ "                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n"
		+ "                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n"
		+ "                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 603\n                -height 553\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n"
		+ "            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 603\n            -height 553\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n"
		+ "            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showReferenceNodes 1\n                -showReferenceMembers 1\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n"
		+ "                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n"
		+ "                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n"
		+ "            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n"
		+ "            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n"
		+ "                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n"
		+ "                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n"
		+ "                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n"
		+ "                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n"
		+ "                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n"
		+ "                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n"
		+ "                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n"
		+ "                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n"
		+ "                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n"
		+ "                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n"
		+ "                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n"
		+ "                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n"
		+ "                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n"
		+ "                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n"
		+ "\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" == $panelName) {\n"
		+ "\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n"
		+ "\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"profilerPanel\" -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"Stereo\" -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels `;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n"
		+ "                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n"
		+ "                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n"
		+ "                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n"
		+ "                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n"
		+ "                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n"
		+ "                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n"
		+ "                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n"
		+ "                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 32 100 -ps 2 68 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Outliner\")) \n\t\t\t\t\t\"outlinerPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    $editorName\"\n"
		+ "\t\t\t\t\t\"outlinerPanel -edit -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 603\\n    -height 553\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 603\\n    -height 553\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
select -ne :renderPartition;
	setAttr -s 3 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 52 ".u";
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
connectAttr "jnt_spine.s" "jnt_chest.is";
connectAttr "jnt_chest.s" "jnt_neck.is";
connectAttr "jnt_neck.s" "jnt_head.is";
connectAttr "jnt_chest.s" "jnt_shoulder_l.is";
connectAttr "jnt_shoulder_l.s" "jnt_upperarm_l.is";
connectAttr "jnt_upperarm_l.s" "jnt_forearm_l.is";
connectAttr "jnt_hand_l.s" "jnt_finger11_l.is";
connectAttr "jnt_finger11_l.s" "jnt_finger12_l.is";
connectAttr "jnt_finger12_l.s" "jne_finger13_l.is";
connectAttr "jnt_hand_l.s" "jnt_finger21_l.is";
connectAttr "jnt_finger21_l.s" "jnt_finger22_l.is";
connectAttr "jnt_finger22_l.s" "jne_finger23_l.is";
connectAttr "jnt_hand_l.s" "jnt_finger31_l.is";
connectAttr "jnt_finger31_l.s" "jnt_finger32_l.is";
connectAttr "jnt_finger32_l.s" "jne_finger33_l.is";
connectAttr "jnt_hand_l.s" "jnt_finger41_l.is";
connectAttr "jnt_finger41_l.s" "jnt_finger42_l.is";
connectAttr "jnt_finger42_l.s" "jne_finger43_l.is";
connectAttr "jnt_chest.s" "jnt_shoulder_r.is";
connectAttr "jnt_shoulder_r.s" "jnt_upperarm_r.is";
connectAttr "jnt_upperarm_r.s" "jnt_forearm_r.is";
connectAttr "jnt_hand_r.s" "jnt_finger11_r.is";
connectAttr "jnt_finger11_r.s" "jnt_finger12_r.is";
connectAttr "jnt_finger12_r.s" "jne_finger13_r.is";
connectAttr "jnt_hand_r.s" "jnt_finger21_r.is";
connectAttr "jnt_finger21_r.s" "jnt_finger22_r.is";
connectAttr "jnt_finger22_r.s" "jne_finger23_r.is";
connectAttr "jnt_hand_r.s" "jnt_finger31_r.is";
connectAttr "jnt_finger31_r.s" "jnt_finger32_r.is";
connectAttr "jnt_finger32_r.s" "jne_finger33_r.is";
connectAttr "jnt_hand_r.s" "jnt_finger41_r.is";
connectAttr "jnt_finger41_r.s" "jnt_finger42_r.is";
connectAttr "jnt_finger42_r.s" "jne_finger43_r.is";
connectAttr "jnt_spine.s" "jnt_hips.is";
connectAttr "jnt_hips.s" "jne_hips.is";
connectAttr "jnt_thigh_l.s" "jnt_calf_l.is";
connectAttr "jnt_calf_l.s" "jnt_foot_l.is";
connectAttr "jnt_foot_l.s" "jnt_toes_l.is";
connectAttr "jnt_toes_l.s" "jne_toes_l.is";
connectAttr "jnt_thigh_r.s" "jnt_calf_r.is";
connectAttr "jnt_calf_r.s" "jnt_foot_r.is";
connectAttr "jnt_foot_r.s" "jnt_toes_r.is";
connectAttr "jnt_toes_r.s" "jne_toes_r.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "___Default.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "___Default.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "___Default.msg" "materialInfo1.sg";
connectAttr "jnt_spine.msg" "bindPose1.m[0]";
connectAttr "jnt_chest.msg" "bindPose1.m[1]";
connectAttr "jnt_shoulder_r.msg" "bindPose1.m[2]";
connectAttr "jnt_upperarm_r.msg" "bindPose1.m[3]";
connectAttr "jnt_shoulder_l.msg" "bindPose1.m[4]";
connectAttr "jnt_upperarm_l.msg" "bindPose1.m[5]";
connectAttr "jnt_hips.msg" "bindPose1.m[6]";
connectAttr "jnt_thigh_r.msg" "bindPose1.m[7]";
connectAttr "jnt_calf_r.msg" "bindPose1.m[8]";
connectAttr "jnt_foot_r.msg" "bindPose1.m[9]";
connectAttr "jnt_toes_r.msg" "bindPose1.m[10]";
connectAttr "jnt_thigh_l.msg" "bindPose1.m[11]";
connectAttr "jnt_calf_l.msg" "bindPose1.m[12]";
connectAttr "jnt_foot_l.msg" "bindPose1.m[13]";
connectAttr "jnt_toes_l.msg" "bindPose1.m[14]";
connectAttr "jnt_neck.msg" "bindPose1.m[15]";
connectAttr "jnt_head.msg" "bindPose1.m[16]";
connectAttr "jnt_forearm_r.msg" "bindPose1.m[17]";
connectAttr "jnt_hand_r.msg" "bindPose1.m[18]";
connectAttr "jnt_forearm_l.msg" "bindPose1.m[19]";
connectAttr "jnt_hand_l.msg" "bindPose1.m[20]";
connectAttr "jnt_finger41_r.msg" "bindPose1.m[21]";
connectAttr "jnt_finger42_r.msg" "bindPose1.m[22]";
connectAttr "jnt_finger41_l.msg" "bindPose1.m[23]";
connectAttr "jnt_finger42_l.msg" "bindPose1.m[24]";
connectAttr "jnt_finger31_r.msg" "bindPose1.m[25]";
connectAttr "jnt_finger32_r.msg" "bindPose1.m[26]";
connectAttr "jnt_finger31_l.msg" "bindPose1.m[27]";
connectAttr "jnt_finger32_l.msg" "bindPose1.m[28]";
connectAttr "jnt_finger21_r.msg" "bindPose1.m[29]";
connectAttr "jnt_finger22_r.msg" "bindPose1.m[30]";
connectAttr "jnt_finger21_l.msg" "bindPose1.m[31]";
connectAttr "jnt_finger22_l.msg" "bindPose1.m[32]";
connectAttr "jnt_finger11_r.msg" "bindPose1.m[33]";
connectAttr "jnt_finger12_r.msg" "bindPose1.m[34]";
connectAttr "jnt_finger11_l.msg" "bindPose1.m[35]";
connectAttr "jnt_finger12_l.msg" "bindPose1.m[36]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[1]" "bindPose1.p[2]";
connectAttr "bindPose1.m[2]" "bindPose1.p[3]";
connectAttr "bindPose1.m[1]" "bindPose1.p[4]";
connectAttr "bindPose1.m[4]" "bindPose1.p[5]";
connectAttr "bindPose1.m[0]" "bindPose1.p[6]";
connectAttr "bindPose1.m[6]" "bindPose1.p[7]";
connectAttr "bindPose1.m[7]" "bindPose1.p[8]";
connectAttr "bindPose1.m[8]" "bindPose1.p[9]";
connectAttr "bindPose1.m[9]" "bindPose1.p[10]";
connectAttr "bindPose1.m[6]" "bindPose1.p[11]";
connectAttr "bindPose1.m[11]" "bindPose1.p[12]";
connectAttr "bindPose1.m[12]" "bindPose1.p[13]";
connectAttr "bindPose1.m[13]" "bindPose1.p[14]";
connectAttr "bindPose1.m[1]" "bindPose1.p[15]";
connectAttr "bindPose1.m[15]" "bindPose1.p[16]";
connectAttr "bindPose1.m[3]" "bindPose1.p[17]";
connectAttr "bindPose1.m[17]" "bindPose1.p[18]";
connectAttr "bindPose1.m[5]" "bindPose1.p[19]";
connectAttr "bindPose1.m[19]" "bindPose1.p[20]";
connectAttr "bindPose1.m[18]" "bindPose1.p[21]";
connectAttr "bindPose1.m[21]" "bindPose1.p[22]";
connectAttr "bindPose1.m[20]" "bindPose1.p[23]";
connectAttr "bindPose1.m[23]" "bindPose1.p[24]";
connectAttr "bindPose1.m[18]" "bindPose1.p[25]";
connectAttr "bindPose1.m[25]" "bindPose1.p[26]";
connectAttr "bindPose1.m[20]" "bindPose1.p[27]";
connectAttr "bindPose1.m[27]" "bindPose1.p[28]";
connectAttr "bindPose1.m[18]" "bindPose1.p[29]";
connectAttr "bindPose1.m[29]" "bindPose1.p[30]";
connectAttr "bindPose1.m[20]" "bindPose1.p[31]";
connectAttr "bindPose1.m[31]" "bindPose1.p[32]";
connectAttr "bindPose1.m[18]" "bindPose1.p[33]";
connectAttr "bindPose1.m[33]" "bindPose1.p[34]";
connectAttr "bindPose1.m[20]" "bindPose1.p[35]";
connectAttr "bindPose1.m[35]" "bindPose1.p[36]";
connectAttr "jnt_spine.bps" "bindPose1.wm[0]";
connectAttr "jnt_chest.bps" "bindPose1.wm[1]";
connectAttr "jnt_shoulder_r.bps" "bindPose1.wm[2]";
connectAttr "jnt_upperarm_r.bps" "bindPose1.wm[3]";
connectAttr "jnt_shoulder_l.bps" "bindPose1.wm[4]";
connectAttr "jnt_upperarm_l.bps" "bindPose1.wm[5]";
connectAttr "jnt_hips.bps" "bindPose1.wm[6]";
connectAttr "jnt_thigh_r.bps" "bindPose1.wm[7]";
connectAttr "jnt_calf_r.bps" "bindPose1.wm[8]";
connectAttr "jnt_foot_r.bps" "bindPose1.wm[9]";
connectAttr "jnt_toes_r.bps" "bindPose1.wm[10]";
connectAttr "jnt_thigh_l.bps" "bindPose1.wm[11]";
connectAttr "jnt_calf_l.bps" "bindPose1.wm[12]";
connectAttr "jnt_foot_l.bps" "bindPose1.wm[13]";
connectAttr "jnt_toes_l.bps" "bindPose1.wm[14]";
connectAttr "jnt_neck.bps" "bindPose1.wm[15]";
connectAttr "jnt_head.bps" "bindPose1.wm[16]";
connectAttr "jnt_forearm_r.bps" "bindPose1.wm[17]";
connectAttr "jnt_hand_r.bps" "bindPose1.wm[18]";
connectAttr "jnt_forearm_l.bps" "bindPose1.wm[19]";
connectAttr "jnt_hand_l.bps" "bindPose1.wm[20]";
connectAttr "jnt_finger41_r.bps" "bindPose1.wm[21]";
connectAttr "jnt_finger42_r.bps" "bindPose1.wm[22]";
connectAttr "jnt_finger41_l.bps" "bindPose1.wm[23]";
connectAttr "jnt_finger42_l.bps" "bindPose1.wm[24]";
connectAttr "jnt_finger31_r.bps" "bindPose1.wm[25]";
connectAttr "jnt_finger32_r.bps" "bindPose1.wm[26]";
connectAttr "jnt_finger31_l.bps" "bindPose1.wm[27]";
connectAttr "jnt_finger32_l.bps" "bindPose1.wm[28]";
connectAttr "jnt_finger21_r.bps" "bindPose1.wm[29]";
connectAttr "jnt_finger22_r.bps" "bindPose1.wm[30]";
connectAttr "jnt_finger21_l.bps" "bindPose1.wm[31]";
connectAttr "jnt_finger22_l.bps" "bindPose1.wm[32]";
connectAttr "jnt_finger11_r.bps" "bindPose1.wm[33]";
connectAttr "jnt_finger12_r.bps" "bindPose1.wm[34]";
connectAttr "jnt_finger11_l.bps" "bindPose1.wm[35]";
connectAttr "jnt_finger12_l.bps" "bindPose1.wm[36]";
connectAttr "multiplyDivide1.ox" "condition1.ctr";
connectAttr "multiplyDivide1.ox" "condition1.ft";
connectAttr "condition1.ocr" "multiplyDivide2.i2y";
connectAttr "condition1.ocr" "multiplyDivide2.i2x";
connectAttr "condition1.ocr" "multiplyDivide2.i2z";
connectAttr "condition1.ocr" "multiplyDivide3.i2y";
connectAttr "condition1.ocr" "multiplyDivide3.i2x";
connectAttr "condition1.ocr" "multiplyDivide3.i2z";
connectAttr "multiplyDivide4.ox" "condition2.ctr";
connectAttr "multiplyDivide4.ox" "condition2.ft";
connectAttr "condition2.ocr" "multiplyDivide5.i2y";
connectAttr "condition2.ocr" "multiplyDivide5.i2x";
connectAttr "condition2.ocr" "multiplyDivide5.i2z";
connectAttr "condition2.ocr" "multiplyDivide6.i2y";
connectAttr "condition2.ocr" "multiplyDivide6.i2x";
connectAttr "condition2.ocr" "multiplyDivide6.i2z";
connectAttr "multiplyDivide7.ox" "condition3.ctr";
connectAttr "multiplyDivide7.ox" "condition3.ft";
connectAttr "condition3.ocr" "multiplyDivide8.i2y";
connectAttr "condition3.ocr" "multiplyDivide8.i2x";
connectAttr "condition3.ocr" "multiplyDivide8.i2z";
connectAttr "condition3.ocr" "multiplyDivide9.i2y";
connectAttr "condition3.ocr" "multiplyDivide9.i2x";
connectAttr "condition3.ocr" "multiplyDivide9.i2z";
connectAttr "multiplyDivide10.ox" "condition7.ctr";
connectAttr "multiplyDivide10.ox" "condition7.ft";
connectAttr "condition7.ocr" "multiplyDivide11.i2y";
connectAttr "condition7.ocr" "multiplyDivide11.i2x";
connectAttr "condition7.ocr" "multiplyDivide11.i2z";
connectAttr "condition7.ocr" "multiplyDivide12.i2y";
connectAttr "condition7.ocr" "multiplyDivide12.i2x";
connectAttr "condition7.ocr" "multiplyDivide12.i2z";
connectAttr "multiplyDivide13.ox" "plusMinusAverage1.i1[1]";
connectAttr "plusMinusAverage1.o1" "plusMinusAverage2.i1[1]";
connectAttr "plusMinusAverage2.o1" "multiplyDivide14.i1x";
connectAttr "multiplyDivide13.ox" "multiplyDivide14.i2x";
connectAttr "multiplyDivide14.ox" "condition8.cfr";
connectAttr "multiplyDivide13.ox" "condition8.ft";
connectAttr "condition8.ocr" "multiplyDivide15.i1x";
connectAttr "multiplyDivide15.ox" "multiplyDivide16.i2x";
connectAttr "multiplyDivide16.ox" "plusMinusAverage3.i1[1]";
connectAttr "multiplyDivide13.ox" "multiplyDivide17.i1x";
connectAttr "plusMinusAverage3.o1" "multiplyDivide17.i2x";
connectAttr "multiplyDivide17.ox" "plusMinusAverage4.i1[0]";
connectAttr "plusMinusAverage1.o1" "plusMinusAverage4.i1[1]";
connectAttr "plusMinusAverage4.o1" "condition9.ctr";
connectAttr "condition8.ocr" "condition9.ft";
connectAttr "condition9.ocr" "blendTwoAttr1.i[0]";
connectAttr "plusMinusAverage4.o1" "multiplyDivide18.i2x";
connectAttr "plusMinusAverage1.o1" "condition10.st";
connectAttr "multiplyDivide18.ox" "condition10.ctr";
connectAttr "condition10.ocr" "blendTwoAttr2.i[1]";
connectAttr "blendTwoAttr1.o" "multiplyDivide19.i1x";
connectAttr "multiplyDivide22.ox" "plusMinusAverage5.i1[1]";
connectAttr "plusMinusAverage5.o1" "plusMinusAverage6.i1[1]";
connectAttr "plusMinusAverage6.o1" "multiplyDivide23.i1x";
connectAttr "multiplyDivide22.ox" "multiplyDivide23.i2x";
connectAttr "multiplyDivide23.ox" "condition11.cfr";
connectAttr "multiplyDivide22.ox" "condition11.ft";
connectAttr "condition11.ocr" "multiplyDivide24.i1x";
connectAttr "multiplyDivide24.ox" "multiplyDivide25.i2x";
connectAttr "multiplyDivide25.ox" "plusMinusAverage7.i1[1]";
connectAttr "multiplyDivide22.ox" "multiplyDivide26.i1x";
connectAttr "plusMinusAverage7.o1" "multiplyDivide26.i2x";
connectAttr "multiplyDivide26.ox" "plusMinusAverage8.i1[0]";
connectAttr "plusMinusAverage5.o1" "plusMinusAverage8.i1[1]";
connectAttr "plusMinusAverage8.o1" "condition12.ctr";
connectAttr "condition11.ocr" "condition12.ft";
connectAttr "condition12.ocr" "blendTwoAttr3.i[0]";
connectAttr "plusMinusAverage8.o1" "multiplyDivide27.i2x";
connectAttr "plusMinusAverage5.o1" "condition13.st";
connectAttr "multiplyDivide27.ox" "condition13.ctr";
connectAttr "condition13.ocr" "blendTwoAttr4.i[1]";
connectAttr "blendTwoAttr3.o" "multiplyDivide28.i1x";
connectAttr "layerManager.dli[1]" "layer_anm.id";
connectAttr "layerManager.dli[2]" "layer_rig.id";
connectAttr "layerManager.dli[3]" "layer_geo.id";
connectAttr "net_FK_jnt_spine.msg" "Rig.modules[0]";
connectAttr "net_FK_jnt_neck.msg" "Rig.modules[1]";
connectAttr "net_FK_jnt_head.msg" "Rig.modules[2]";
connectAttr "net_FK_jnt_shoulder_l.msg" "Rig.modules[3]";
connectAttr "net_Arm_jnt_hand_l.msg" "Rig.modules[4]";
connectAttr "net_Hand_jne_finger13_l.msg" "Rig.modules[5]";
connectAttr "net_FK_jnt_shoulder_r.msg" "Rig.modules[6]";
connectAttr "net_Arm_jnt_hand_r.msg" "Rig.modules[7]";
connectAttr "net_Hand_jne_finger13_r.msg" "Rig.modules[8]";
connectAttr "net_Leg_jne_toes_l.msg" "Rig.modules[9]";
connectAttr "net_Leg_jne_toes_r.msg" "Rig.modules[10]";
connectAttr "net_FK_jnt_hips.msg" "Rig.modules[11]";
connectAttr "jnt_spine.msg" "net_FK_jnt_spine.input[0]";
connectAttr "jnt_chest.msg" "net_FK_jnt_spine.input[1]";
connectAttr "Rig.msg" "net_FK_jnt_spine.rig";
connectAttr "jnt_neck.msg" "net_FK_jnt_neck.input[0]";
connectAttr "Rig.msg" "net_FK_jnt_neck.rig";
connectAttr "jnt_head.msg" "net_FK_jnt_head.input[0]";
connectAttr "Rig.msg" "net_FK_jnt_head.rig";
connectAttr "jnt_shoulder_l.msg" "net_FK_jnt_shoulder_l.input[0]";
connectAttr "Rig.msg" "net_FK_jnt_shoulder_l.rig";
connectAttr "jnt_hand_l.msg" "net_Arm_jnt_hand_l.input[0]";
connectAttr "jnt_upperarm_l.msg" "net_Arm_jnt_hand_l.input[1]";
connectAttr "jnt_forearm_l.msg" "net_Arm_jnt_hand_l.input[2]";
connectAttr "Rig.msg" "net_Arm_jnt_hand_l.rig";
connectAttr "jne_finger13_l.msg" "net_Hand_jne_finger13_l.input[0]";
connectAttr "jnt_finger12_l.msg" "net_Hand_jne_finger13_l.input[1]";
connectAttr "jne_finger23_l.msg" "net_Hand_jne_finger13_l.input[2]";
connectAttr "jnt_finger22_l.msg" "net_Hand_jne_finger13_l.input[3]";
connectAttr "jne_finger33_l.msg" "net_Hand_jne_finger13_l.input[4]";
connectAttr "jnt_finger32_l.msg" "net_Hand_jne_finger13_l.input[5]";
connectAttr "jne_finger43_l.msg" "net_Hand_jne_finger13_l.input[6]";
connectAttr "jnt_finger11_l.msg" "net_Hand_jne_finger13_l.input[7]";
connectAttr "jnt_finger21_l.msg" "net_Hand_jne_finger13_l.input[8]";
connectAttr "jnt_finger31_l.msg" "net_Hand_jne_finger13_l.input[9]";
connectAttr "jnt_finger41_l.msg" "net_Hand_jne_finger13_l.input[10]";
connectAttr "jnt_finger42_l.msg" "net_Hand_jne_finger13_l.input[11]";
connectAttr "Rig.msg" "net_Hand_jne_finger13_l.rig";
connectAttr "jnt_shoulder_r.msg" "net_FK_jnt_shoulder_r.input[0]";
connectAttr "Rig.msg" "net_FK_jnt_shoulder_r.rig";
connectAttr "jnt_hand_r.msg" "net_Arm_jnt_hand_r.input[0]";
connectAttr "jnt_upperarm_r.msg" "net_Arm_jnt_hand_r.input[1]";
connectAttr "jnt_forearm_r.msg" "net_Arm_jnt_hand_r.input[2]";
connectAttr "Rig.msg" "net_Arm_jnt_hand_r.rig";
connectAttr "jne_finger13_r.msg" "net_Hand_jne_finger13_r.input[0]";
connectAttr "jnt_finger12_r.msg" "net_Hand_jne_finger13_r.input[1]";
connectAttr "jne_finger23_r.msg" "net_Hand_jne_finger13_r.input[2]";
connectAttr "jnt_finger22_r.msg" "net_Hand_jne_finger13_r.input[3]";
connectAttr "jne_finger33_r.msg" "net_Hand_jne_finger13_r.input[4]";
connectAttr "jnt_finger32_r.msg" "net_Hand_jne_finger13_r.input[5]";
connectAttr "jne_finger43_r.msg" "net_Hand_jne_finger13_r.input[6]";
connectAttr "jnt_finger11_r.msg" "net_Hand_jne_finger13_r.input[7]";
connectAttr "jnt_finger21_r.msg" "net_Hand_jne_finger13_r.input[8]";
connectAttr "jnt_finger31_r.msg" "net_Hand_jne_finger13_r.input[9]";
connectAttr "jnt_finger41_r.msg" "net_Hand_jne_finger13_r.input[10]";
connectAttr "jnt_finger42_r.msg" "net_Hand_jne_finger13_r.input[11]";
connectAttr "Rig.msg" "net_Hand_jne_finger13_r.rig";
connectAttr "jne_toes_l.msg" "net_Leg_jne_toes_l.input[0]";
connectAttr "jnt_thigh_l.msg" "net_Leg_jne_toes_l.input[1]";
connectAttr "jnt_calf_l.msg" "net_Leg_jne_toes_l.input[2]";
connectAttr "jnt_foot_l.msg" "net_Leg_jne_toes_l.input[3]";
connectAttr "jnt_toes_l.msg" "net_Leg_jne_toes_l.input[4]";
connectAttr "Rig.msg" "net_Leg_jne_toes_l.rig";
connectAttr "jne_toes_r.msg" "net_Leg_jne_toes_r.input[0]";
connectAttr "jnt_thigh_r.msg" "net_Leg_jne_toes_r.input[1]";
connectAttr "jnt_calf_r.msg" "net_Leg_jne_toes_r.input[2]";
connectAttr "jnt_foot_r.msg" "net_Leg_jne_toes_r.input[3]";
connectAttr "jnt_toes_r.msg" "net_Leg_jne_toes_r.input[4]";
connectAttr "Rig.msg" "net_Leg_jne_toes_r.rig";
connectAttr "jnt_hips.msg" "net_FK_jnt_hips.input[0]";
connectAttr "Rig.msg" "net_FK_jnt_hips.rig";
connectAttr "___Default.pa" ":renderPartition.st" -na;
connectAttr "multiplyDivide1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide4.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide5.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide6.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide7.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide8.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide9.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide10.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition7.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide11.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide12.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide13.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "plusMinusAverage1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "plusMinusAverage2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide14.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition8.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide15.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide16.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "plusMinusAverage3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide17.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "plusMinusAverage4.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition9.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "blendTwoAttr1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide18.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition10.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "blendTwoAttr2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide19.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide20.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide21.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide22.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "plusMinusAverage5.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "plusMinusAverage6.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide23.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition11.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide24.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide25.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "plusMinusAverage7.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide26.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "plusMinusAverage8.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition12.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "blendTwoAttr3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide27.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "condition13.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "blendTwoAttr4.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide28.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide29.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multiplyDivide30.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of rig_rlessard_template01.ma
