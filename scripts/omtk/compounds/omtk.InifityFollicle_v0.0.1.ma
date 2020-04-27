//Maya ASCII 2020 scene
//Name: omtk.InifityFollicle_v0.0.1.ma
//Last modified: Sun, Apr 26, 2020 08:31:28 PM
//Codeset: 1252
requires maya "2020";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "860EB50E-44E3-05AC-B1A8-2DA154529E1C";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "D01075F3-4A11-50DC-14B1-B5AFB853E1FF";
fileInfo "omtk.compound.name" "omtk.InfinityFollicle";
createNode transform -n "dag";
	rename -uid "5008A3A5-4B09-5C0F-E789-3DA5B322FC7C";
createNode transform -n "l_cheek_jnt_cheek_avarModel_influenceClampedU_rig" -p "dag";
	rename -uid "5234987B-48D0-2D31-5ED8-4F92D0F3E0A2";
createNode follicle -n "l_cheek_jnt_cheek_avarModel_influenceClampedU_rigShape" 
		-p "l_cheek_jnt_cheek_avarModel_influenceClampedU_rig";
	rename -uid "EBE95CEE-4889-A637-8D56-5F813EF8AC02";
	setAttr -k off ".v";
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "l_cheek_jnt_cheek_avarModel_influenceClampedV_rig" -p "dag";
	rename -uid "78BDA903-40B8-9E66-737E-B382BC162512";
createNode follicle -n "l_cheek_jnt_cheek_avarModel_influenceClampedV_rigShape" 
		-p "l_cheek_jnt_cheek_avarModel_influenceClampedV_rig";
	rename -uid "8667D158-4736-3A54-5290-5E81A86391B4";
	setAttr -k off ".v";
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -n "l_cheek_jnt_cheek_avarModel_influenceFollicle_rig" -p "dag";
	rename -uid "48850093-469B-C0FF-E240-ABAFEC0CEA31";
createNode follicle -n "l_cheek_jnt_cheek_avarModel_influenceFollicle_rigShape" 
		-p "l_cheek_jnt_cheek_avarModel_influenceFollicle_rig";
	rename -uid "409D26A9-4F3E-69CB-B32E-E0B09D750B50";
	setAttr -k off ".v";
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode transform -s -n "persp";
	rename -uid "CF05ECAA-483D-813D-5ED2-16B7CAEDC1A2";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 28 21 28 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "71D95C91-48FD-1A9B-17D4-76B1C349AFB6";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "9CE831CB-468E-2BAC-ABDB-748EFB93F4B8";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "4A77CC83-434F-381A-ADBD-1A8C17B2D1A2";
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
	rename -uid "9FD720DA-4A76-2B5B-F332-628945CFCFA3";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "1FF289A7-482E-3738-9FB0-15BCE943DB54";
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
	rename -uid "F62C547F-41A4-7DF2-648A-1F824D00E944";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "83266765-4B7E-642A-A2BD-5B9EAEE3C03B";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode network -n "inputs";
	rename -uid "F16655BE-4B10-74C1-9145-06A6666045C0";
	addAttr -ci true -sn "surfaceU" -ln "surfaceU" -at "float";
	addAttr -ci true -sn "surfaceV" -ln "surfaceV" -at "float";
	addAttr -ci true -sn "surface" -ln "surface" -dt "nurbsSurface";
	setAttr ".surfaceU" 0.5;
	setAttr ".surfaceV" 0.49959063529968262;
	setAttr ".surface" -type "nurbsSurface" 
		3 3 0 0 no 
		9 0 0 0 0.25 0.5 0.75 1 1 1
		9 0 0 0 0.25 0.5 0.75 1 1 1
		
		49
		-0.22479334701803727 15.788134910348834 1.6920539488665616
		-0.22479334701803724 15.806867689267005 1.6920539488665616
		-0.22479334701803724 15.844333247103345 1.6920539488665616
		-0.22479334701803727 15.900531583857854 1.6920539488665616
		-0.22479334701803727 15.956450699014367 1.6823677083853823
		-0.22479334701803727 15.992906212358237 1.6652665814652383
		-0.22479334701803727 16.010704467559862 1.6535974562374345
		-0.18732778918169773 15.788134910348834 1.6920539488665616
		-0.18732778918169773 15.806867689267005 1.6920539488665616
		-0.18732778918169773 15.844333247103345 1.6920539488665616
		-0.18732778918169773 15.900531583857854 1.6920539488665616
		-0.18732778918169773 15.956450699014367 1.6823677083853823
		-0.18732778918169773 15.992906212358237 1.6652665814652383
		-0.18732778918169773 16.010704467559862 1.6535974562374345
		-0.11239667350901865 15.788134910348834 1.6920539488665616
		-0.11239667350901865 15.806867689267005 1.6920539488665616
		-0.11239667350901865 15.844333247103345 1.6920539488665616
		-0.11239667350901865 15.900531583857854 1.6920539488665616
		-0.11239667350901865 15.956450699014367 1.6823677083853823
		-0.11239667350901865 15.992906212358237 1.6652665814652383
		-0.11239667350901865 16.010704467559862 1.6535974562374345
		-3.3994844356677086e-17 15.788134910348834 1.6920539488665616
		-3.399484435667708e-17 15.806867689267005 1.6920539488665616
		-3.399484435667708e-17 15.844333247103345 1.6920539488665616
		-3.3994844356677086e-17 15.900531583857854 1.6920539488665616
		-3.3926454789429544e-17 15.956450699014367 1.6823677083853823
		-3.3679065238489595e-17 15.992906212358237 1.6652665814652383
		-3.3450172942850987e-17 16.010704467559862 1.6535974562374345
		0.11239667350901859 15.788134910348834 1.6920539488665616
		0.11239667350901859 15.806867689267005 1.6920539488665616
		0.11239667350901859 15.844333247103345 1.6920539488665616
		0.11239667350901859 15.900531583857854 1.6920539488665616
		0.11239667350901859 15.956450699014367 1.6823677083853823
		0.11239667350901859 15.992906212358237 1.6652665814652383
		0.11239667350901859 16.010704467559862 1.6535974562374345
		0.18732778918169765 15.788134910348834 1.6920539488665616
		0.18732778918169765 15.806867689267005 1.6920539488665616
		0.18732778918169765 15.844333247103345 1.6920539488665616
		0.18732778918169765 15.900531583857854 1.6920539488665616
		0.18732778918169765 15.956450699014367 1.6823677083853823
		0.18732778918169765 15.992906212358237 1.6652665814652383
		0.18732778918169765 16.010704467559862 1.6535974562374345
		0.22479334701803722 15.788134910348834 1.6920539488665616
		0.22479334701803722 15.806867689267005 1.6920539488665616
		0.22479334701803722 15.844333247103345 1.6920539488665616
		0.22479334701803722 15.900531583857854 1.6920539488665616
		0.22479334701803719 15.956450699014367 1.6823677083853823
		0.22479334701803719 15.992906212358237 1.6652665814652383
		0.22479334701803722 16.010704467559862 1.6535974562374345
		
		;
createNode clamp -n "clamp1";
	rename -uid "95A14ABB-4886-2C25-F352-92A77100B8E3";
	setAttr ".mn" -type "float3" 0.001 0.001 0 ;
	setAttr ".mx" -type "float3" 0.99900001 0.99900001 0 ;
createNode multiplyDivide -n "multiplyDivide8";
	rename -uid "5767BD07-4D78-4F6C-0583-F8A21FD8553E";
createNode multMatrix -n "multMatrix1";
	rename -uid "A08C3CDC-4AFE-8CC2-7A44-F082EC9F6C77";
createNode condition -n "condition8";
	rename -uid "A4B65477-49D7-07E1-5D3F-E690C941B539";
	setAttr ".st" 1;
	setAttr ".cf" -type "float3" 0 0 0 ;
createNode condition -n "condition7";
	rename -uid "A2CDF280-4C72-6FF9-5D98-369E5294DA8F";
	setAttr ".st" 1;
	setAttr ".cf" -type "float3" 0 0 0 ;
createNode plusMinusAverage -n "plusMinusAverage2";
	rename -uid "582E8B6D-40B5-539D-0E83-7AB43D76B35D";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode multiplyDivide -n "multiplyDivide7";
	rename -uid "DF10E41C-4C48-2C81-B93F-DB8DAD6A8AA4";
createNode multMatrix -n "multMatrix3";
	rename -uid "8EDA987B-4C90-F1FC-9BA0-5A8BEAE0D592";
createNode decomposeMatrix -n "decomposeMatrix3";
	rename -uid "FEBBF7F4-45BC-5CCA-F502-6489A510F384";
createNode plusMinusAverage -n "plusMinusAverage1";
	rename -uid "B262993C-4669-BDAA-0515-E69FB736C51D";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode plusMinusAverage -n "plusMinusAverage5";
	rename -uid "65AE5C41-4B0E-E4B3-AF74-97BBE5A4DC80";
	setAttr -s 3 ".i3";
	setAttr -s 3 ".i3";
createNode network -n "outputs";
	rename -uid "4DA83365-4E4D-49DB-AADE-19A1BABCC994";
	addAttr -ci true -sn "outputTM" -ln "outputTM" -dt "matrix";
createNode composeMatrix -n "composeMatrix20";
	rename -uid "8EBAD256-4B6B-8E3F-1269-8783FCD9AEFD";
createNode multiplyDivide -n "multiplyDivide6";
	rename -uid "140FE797-4593-E577-6AEE-3A97E9849A71";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 0.001 1 1 ;
createNode condition -n "condition6";
	rename -uid "07D4066C-4D9C-A0F4-92A7-25A08CAAAED8";
	setAttr ".st" 1;
createNode plusMinusAverage -n "plusMinusAverage4";
	rename -uid "70166841-476E-091A-1E7F-108624AE62AE";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[1]"  1;
createNode multiplyDivide -n "multiplyDivide4";
	rename -uid "FFC263F4-480C-5413-17B9-0894A91F58F2";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode condition -n "condition4";
	rename -uid "6F6758D9-484D-9B00-141B-5D8C085EB4C6";
	setAttr ".op" 2;
	setAttr ".st" 1;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode addDoubleLinear -n "addDoubleLinear4";
	rename -uid "6111E4B7-4283-A5E7-D951-40BCF6D86101";
createNode condition -n "condition3";
	rename -uid "21FB03E7-4865-9A82-2B09-0980E1A6E324";
	setAttr ".op" 4;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode addDoubleLinear -n "addDoubleLinear3";
	rename -uid "E14B0FB6-4708-62B5-9262-8380E8C7A147";
createNode condition -n "condition2";
	rename -uid "06EA4634-457C-D53E-E6B5-06938A1D51CA";
	setAttr ".op" 2;
	setAttr ".st" 1;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode condition -n "condition1";
	rename -uid "8F6E94D5-44A5-0F1C-DACA-778CFB51E737";
	setAttr ".op" 4;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode multiplyDivide -n "multiplyDivide5";
	rename -uid "40FB6F97-4A25-D219-66EA-949005CDCB7B";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 0.001 1 1 ;
createNode condition -n "condition5";
	rename -uid "0DDBB495-4D46-5307-07A4-97B149CB28F4";
	setAttr ".st" 1;
createNode plusMinusAverage -n "plusMinusAverage3";
	rename -uid "6DB3C3F8-410D-FC86-002D-48A0665C0183";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[1]"  1;
createNode multiplyDivide -n "multiplyDivide3";
	rename -uid "17873DE4-4CB0-1596-65D4-4BA63E1265E7";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "D2EAC68B-456D-F5E1-C8F4-5DA4C0DDE9D5";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "10FDECB0-42C3-18DC-5926-50B0BB02A419";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "801AB9C1-46A4-040C-2A57-A8A0EAA0B754";
createNode displayLayerManager -n "layerManager";
	rename -uid "5E6FCD29-44AB-20C3-C597-A5B0AE0F66A3";
createNode displayLayer -n "defaultLayer";
	rename -uid "E5B70E5A-4B04-D957-73DF-379F08585E13";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "BA37CCCA-40F4-179C-0536-BDA88B148D00";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "E92F9398-4CCE-8353-7B09-2CB26EF90E7E";
	setAttr ".g" yes;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "DA416B95-461D-4F18-D767-A382E205AF13";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1932.5044369789359 -820.90516171615138 ;
	setAttr ".tgi[0].vh" -type "double2" 1166.8811657234808 665.80165921204002 ;
	setAttr -s 20 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -582.85711669921875;
	setAttr ".tgi[0].ni[0].y" 164.28572082519531;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" -582.85711669921875;
	setAttr ".tgi[0].ni[1].y" 62.857143402099609;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 821.4285888671875;
	setAttr ".tgi[0].ni[2].y" 17.142856597900391;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 207.14285278320313;
	setAttr ".tgi[0].ni[3].y" -95.714286804199219;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" -100;
	setAttr ".tgi[0].ni[4].y" 115.71428680419922;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" -1080;
	setAttr ".tgi[0].ni[5].y" 97.142860412597656;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 514.28570556640625;
	setAttr ".tgi[0].ni[6].y" 8.5714282989501953;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" 1128.5714111328125;
	setAttr ".tgi[0].ni[7].y" -15.714285850524902;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" -582.85711669921875;
	setAttr ".tgi[0].ni[8].y" -38.571430206298828;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" 207.14285278320313;
	setAttr ".tgi[0].ni[9].y" 108.57142639160156;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" -1387.142822265625;
	setAttr ".tgi[0].ni[10].y" 160;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" 1435.7142333984375;
	setAttr ".tgi[0].ni[11].y" -5.7142858505249023;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" -100;
	setAttr ".tgi[0].ni[12].y" -87.142860412597656;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" 514.28570556640625;
	setAttr ".tgi[0].ni[13].y" -92.857139587402344;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" -1729.9381103515625;
	setAttr ".tgi[0].ni[14].y" 125.44939422607422;
	setAttr ".tgi[0].ni[14].nvs" 18306;
	setAttr ".tgi[0].ni[15].x" -100;
	setAttr ".tgi[0].ni[15].y" 14.285714149475098;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" -1080;
	setAttr ".tgi[0].ni[16].y" 198.57142639160156;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" 514.28570556640625;
	setAttr ".tgi[0].ni[17].y" 110;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" 207.14285278320313;
	setAttr ".tgi[0].ni[18].y" 5.7142858505249023;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" -1127.53662109375;
	setAttr ".tgi[0].ni[19].y" 1391.1038818359375;
	setAttr ".tgi[0].ni[19].nvs" 18306;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedU_rigShape.ot" "l_cheek_jnt_cheek_avarModel_influenceClampedU_rig.t"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedU_rigShape.or" "l_cheek_jnt_cheek_avarModel_influenceClampedU_rig.r"
		;
connectAttr "inputs.surface" "l_cheek_jnt_cheek_avarModel_influenceClampedU_rigShape.is"
		;
connectAttr "inputs.surfaceV" "l_cheek_jnt_cheek_avarModel_influenceClampedU_rigShape.pv"
		;
connectAttr "clamp1.opr" "l_cheek_jnt_cheek_avarModel_influenceClampedU_rigShape.pu"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedV_rigShape.ot" "l_cheek_jnt_cheek_avarModel_influenceClampedV_rig.t"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedV_rigShape.or" "l_cheek_jnt_cheek_avarModel_influenceClampedV_rig.r"
		;
connectAttr "inputs.surface" "l_cheek_jnt_cheek_avarModel_influenceClampedV_rigShape.is"
		;
connectAttr "clamp1.opg" "l_cheek_jnt_cheek_avarModel_influenceClampedV_rigShape.pv"
		;
connectAttr "inputs.surfaceU" "l_cheek_jnt_cheek_avarModel_influenceClampedV_rigShape.pu"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceFollicle_rigShape.ot" "l_cheek_jnt_cheek_avarModel_influenceFollicle_rig.t"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceFollicle_rigShape.or" "l_cheek_jnt_cheek_avarModel_influenceFollicle_rig.r"
		;
connectAttr "inputs.surface" "l_cheek_jnt_cheek_avarModel_influenceFollicle_rigShape.is"
		;
connectAttr "inputs.surfaceV" "l_cheek_jnt_cheek_avarModel_influenceFollicle_rigShape.pv"
		;
connectAttr "inputs.surfaceU" "l_cheek_jnt_cheek_avarModel_influenceFollicle_rigShape.pu"
		;
connectAttr "inputs.surfaceU" "clamp1.ipr";
connectAttr "inputs.surfaceV" "clamp1.ipg";
connectAttr "multiplyDivide6.ox" "multiplyDivide8.i1x";
connectAttr "multiplyDivide6.ox" "multiplyDivide8.i1y";
connectAttr "multiplyDivide6.ox" "multiplyDivide8.i1z";
connectAttr "plusMinusAverage2.o3" "multiplyDivide8.i2";
connectAttr "l_cheek_jnt_cheek_avarModel_influenceFollicle_rig.m" "multMatrix1.i[0]"
		;
connectAttr "addDoubleLinear4.o" "condition8.ft";
connectAttr "multiplyDivide8.o" "condition8.ct";
connectAttr "addDoubleLinear3.o" "condition7.ft";
connectAttr "multiplyDivide7.o" "condition7.ct";
connectAttr "l_cheek_jnt_cheek_avarModel_influenceFollicle_rig.t" "plusMinusAverage2.i3[0]"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedV_rig.t" "plusMinusAverage2.i3[1]"
		;
connectAttr "multiplyDivide5.ox" "multiplyDivide7.i1x";
connectAttr "multiplyDivide5.ox" "multiplyDivide7.i1y";
connectAttr "multiplyDivide5.ox" "multiplyDivide7.i1z";
connectAttr "plusMinusAverage1.o3" "multiplyDivide7.i2";
connectAttr "multMatrix1.o" "multMatrix3.i[1]";
connectAttr "multMatrix3.o" "decomposeMatrix3.imat";
connectAttr "l_cheek_jnt_cheek_avarModel_influenceFollicle_rig.t" "plusMinusAverage1.i3[0]"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedU_rig.t" "plusMinusAverage1.i3[1]"
		;
connectAttr "condition7.oc" "plusMinusAverage5.i3[0]";
connectAttr "condition8.oc" "plusMinusAverage5.i3[1]";
connectAttr "decomposeMatrix3.ot" "plusMinusAverage5.i3[2]";
connectAttr "composeMatrix20.omat" "outputs.outputTM";
connectAttr "plusMinusAverage5.o3" "composeMatrix20.it";
connectAttr "decomposeMatrix3.or" "composeMatrix20.ir";
connectAttr "condition6.ocr" "multiplyDivide6.i1x";
connectAttr "plusMinusAverage4.o1" "condition6.ctr";
connectAttr "multiplyDivide4.ox" "condition6.cfr";
connectAttr "condition4.ocr" "condition6.ft";
connectAttr "inputs.surfaceV" "plusMinusAverage4.i1[0]";
connectAttr "inputs.surfaceV" "multiplyDivide4.i1x";
connectAttr "inputs.surfaceV" "condition4.ft";
connectAttr "condition4.ocr" "addDoubleLinear4.i2";
connectAttr "condition3.ocr" "addDoubleLinear4.i1";
connectAttr "inputs.surfaceV" "condition3.ft";
connectAttr "condition2.ocr" "addDoubleLinear3.i2";
connectAttr "condition1.ocr" "addDoubleLinear3.i1";
connectAttr "inputs.surfaceU" "condition2.ft";
connectAttr "inputs.surfaceU" "condition1.ft";
connectAttr "condition5.ocr" "multiplyDivide5.i1x";
connectAttr "plusMinusAverage3.o1" "condition5.ctr";
connectAttr "multiplyDivide3.ox" "condition5.cfr";
connectAttr "condition2.ocr" "condition5.ft";
connectAttr "inputs.surfaceU" "plusMinusAverage3.i1[0]";
connectAttr "inputs.surfaceU" "multiplyDivide3.i1x";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedU_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedV_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "plusMinusAverage5.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "multMatrix3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "plusMinusAverage1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedV_rigShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "condition8.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn";
connectAttr "composeMatrix20.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn";
connectAttr "l_cheek_jnt_cheek_avarModel_influenceFollicle_rig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "multiplyDivide7.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn";
connectAttr "clamp1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn";
connectAttr "outputs.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn";
connectAttr "multMatrix1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn";
connectAttr "decomposeMatrix3.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "inputs.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn";
connectAttr "plusMinusAverage2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceClampedU_rigShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "condition7.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn";
connectAttr "multiplyDivide8.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn"
		;
connectAttr "l_cheek_jnt_cheek_avarModel_influenceFollicle_rigShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn"
		;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of omtk.InifityFollicle_v0.0.1.ma
