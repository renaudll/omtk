//Maya ASCII 2020 scene
//Name: omtk.InifityFollicle_v0.0.2.ma
//Last modified: Sun, Apr 26, 2020 08:47:29 PM
//Codeset: 1252
// requires maya "2020";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "C9CFED6E-4378-B530-E2A9-77A8A91ECF47";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.2";
fileInfo "omtk.compound.uid" "D01075F3-4A11-50DC-14B1-B5AFB853E1FF";
fileInfo "omtk.compound.name" "omtk.InfinityFollicle";
createNode pointOnSurfaceInfo -n "follicle:pointOnSurfaceInfo1";
	rename -uid "D4649307-4AD9-07CC-8784-13943BEA2DD2";
createNode network -n "follicleClampV:inputs";
	rename -uid "0E0D07B7-4904-BC92-1EA4-32BEAC2CE073";
	addAttr -s false -ci true -sn "is" -ln "inputSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "u" -ln "parameterU" -at "double";
	addAttr -ci true -sn "v" -ln "parameterV" -at "double";
createNode pointOnSurfaceInfo -n "follicleClampV:pointOnSurfaceInfo1";
	rename -uid "D4649307-4AD9-07CC-8784-13943BEA2DD2";
createNode clamp -n "clamp2";
	rename -uid "A316D20E-45B0-8BFA-E659-9786BBD7A651";
	setAttr ".mx" -type "float3" 1 1 0 ;
createNode network -n "inputs";
	rename -uid "F16655BE-4B10-74C1-9145-06A6666045C0";
	addAttr -ci true -sn "surfaceU" -ln "surfaceU" -at "float";
	addAttr -ci true -sn "surfaceV" -ln "surfaceV" -at "float";
	addAttr -ci true -sn "surface" -ln "surface" -dt "nurbsSurface";
	setAttr ".surfaceU" 0.5;
	setAttr ".surfaceV" 0.5;
	setAttr ".surface" -type "nurbsSurface" 
		3 3 0 0 no 
		6 0 0 0 1 1 1
		6 0 0 0 1 1 1
		
		16
		-0.5 -3.061616997868383e-17 0.5
		-0.5 -1.0205389992894611e-17 0.16666666666666669
		-0.5 1.0205389992894608e-17 -0.16666666666666663
		-0.5 3.061616997868383e-17 -0.5
		-0.16666666666666669 -3.061616997868383e-17 0.5
		-0.16666666666666669 -1.0205389992894611e-17 0.16666666666666669
		-0.16666666666666669 1.0205389992894608e-17 -0.16666666666666663
		-0.16666666666666669 3.061616997868383e-17 -0.5
		0.16666666666666663 -3.061616997868383e-17 0.5
		0.16666666666666663 -1.0205389992894611e-17 0.16666666666666669
		0.16666666666666663 1.0205389992894608e-17 -0.16666666666666663
		0.16666666666666663 3.061616997868383e-17 -0.5
		0.5 -3.061616997868383e-17 0.5
		0.5 -1.0205389992894611e-17 0.16666666666666669
		0.5 1.0205389992894608e-17 -0.16666666666666663
		0.5 3.061616997868383e-17 -0.5
		
		;
createNode network -n "follicle:inputs";
	rename -uid "0E0D07B7-4904-BC92-1EA4-32BEAC2CE073";
	addAttr -s false -ci true -sn "is" -ln "inputSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "u" -ln "parameterU" -at "double";
	addAttr -ci true -sn "v" -ln "parameterV" -at "double";
createNode clamp -n "clamp1";
	rename -uid "95A14ABB-4886-2C25-F352-92A77100B8E3";
	setAttr ".mn" -type "float3" 0.001 0.001 0 ;
	setAttr ".mx" -type "float3" 0.99900001 0.99900001 0 ;
createNode multMatrix -n "multMatrix1";
	rename -uid "A08C3CDC-4AFE-8CC2-7A44-F082EC9F6C77";
createNode network -n "follicleClampU:outputs";
	rename -uid "695429D5-4D56-E2C1-D9AA-BC9DC22A2982";
	addAttr -s false -ci true -sn "o" -ln "output" -dt "matrix";
createNode multiplyDivide -n "multiplyDivide5";
	rename -uid "40FB6F97-4A25-D219-66EA-949005CDCB7B";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 0.001 1 1 ;
createNode fourByFourMatrix -n "follicleClampV:fourByFourMatrix1";
	rename -uid "E31D94CB-46DE-3E29-78AA-0BA2E324483A";
createNode condition -n "condition1";
	rename -uid "8F6E94D5-44A5-0F1C-DACA-778CFB51E737";
	setAttr ".op" 4;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode decomposeMatrix -n "decomposeMatrix4";
	rename -uid "ED04AD0D-4DBF-6FF6-3822-F58EFEB3B573";
createNode plusMinusAverage -n "plusMinusAverage1";
	rename -uid "B262993C-4669-BDAA-0515-E69FB736C51D";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode condition -n "condition4";
	rename -uid "6F6758D9-484D-9B00-141B-5D8C085EB4C6";
	setAttr ".op" 2;
	setAttr ".st" 1;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode multiplyDivide -n "multiplyDivide4";
	rename -uid "FFC263F4-480C-5413-17B9-0894A91F58F2";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode fourByFourMatrix -n "follicleClampU:fourByFourMatrix1";
	rename -uid "E31D94CB-46DE-3E29-78AA-0BA2E324483A";
createNode network -n "follicle:outputs";
	rename -uid "695429D5-4D56-E2C1-D9AA-BC9DC22A2982";
	addAttr -s false -ci true -sn "o" -ln "output" -dt "matrix";
createNode condition -n "condition6";
	rename -uid "07D4066C-4D9C-A0F4-92A7-25A08CAAAED8";
	setAttr ".st" 1;
createNode condition -n "condition3";
	rename -uid "21FB03E7-4865-9A82-2B09-0980E1A6E324";
	setAttr ".op" 4;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode network -n "follicleClampV:outputs";
	rename -uid "695429D5-4D56-E2C1-D9AA-BC9DC22A2982";
	addAttr -s false -ci true -sn "o" -ln "output" -dt "matrix";
createNode pointOnSurfaceInfo -n "follicleClampU:pointOnSurfaceInfo1";
	rename -uid "D4649307-4AD9-07CC-8784-13943BEA2DD2";
createNode fourByFourMatrix -n "follicle:fourByFourMatrix1";
	rename -uid "E31D94CB-46DE-3E29-78AA-0BA2E324483A";
createNode decomposeMatrix -n "decomposeMatrix6";
	rename -uid "451C2F74-4D0F-B3FA-1447-7C8FAFDB161E";
createNode decomposeMatrix -n "decomposeMatrix5";
	rename -uid "9CB323FB-4B62-DF9E-B189-53BE87CDAD79";
createNode multiplyDivide -n "multiplyDivide6";
	rename -uid "140FE797-4593-E577-6AEE-3A97E9849A71";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 0.001 1 1 ;
createNode condition -n "condition5";
	rename -uid "0DDBB495-4D46-5307-07A4-97B149CB28F4";
	setAttr ".st" 1;
createNode plusMinusAverage -n "plusMinusAverage2";
	rename -uid "582E8B6D-40B5-539D-0E83-7AB43D76B35D";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode network -n "follicleClampU:inputs";
	rename -uid "0E0D07B7-4904-BC92-1EA4-32BEAC2CE073";
	addAttr -s false -ci true -sn "is" -ln "inputSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "u" -ln "parameterU" -at "double";
	addAttr -ci true -sn "v" -ln "parameterV" -at "double";
createNode plusMinusAverage -n "plusMinusAverage4";
	rename -uid "70166841-476E-091A-1E7F-108624AE62AE";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[1]"  1;
createNode plusMinusAverage -n "plusMinusAverage5";
	rename -uid "65AE5C41-4B0E-E4B3-AF74-97BBE5A4DC80";
	setAttr -s 3 ".i3";
	setAttr -s 3 ".i3";
createNode addDoubleLinear -n "addDoubleLinear3";
	rename -uid "E14B0FB6-4708-62B5-9262-8380E8C7A147";
createNode addDoubleLinear -n "addDoubleLinear4";
	rename -uid "6111E4B7-4283-A5E7-D951-40BCF6D86101";
createNode multiplyDivide -n "multiplyDivide3";
	rename -uid "17873DE4-4CB0-1596-65D4-4BA63E1265E7";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode plusMinusAverage -n "plusMinusAverage3";
	rename -uid "6DB3C3F8-410D-FC86-002D-48A0665C0183";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[1]"  1;
createNode multMatrix -n "multMatrix3";
	rename -uid "8EDA987B-4C90-F1FC-9BA0-5A8BEAE0D592";
createNode condition -n "condition7";
	rename -uid "A2CDF280-4C72-6FF9-5D98-369E5294DA8F";
	setAttr ".st" 1;
	setAttr ".cf" -type "float3" 0 0 0 ;
createNode multiplyDivide -n "multiplyDivide7";
	rename -uid "DF10E41C-4C48-2C81-B93F-DB8DAD6A8AA4";
createNode multiplyDivide -n "multiplyDivide8";
	rename -uid "5767BD07-4D78-4F6C-0583-F8A21FD8553E";
createNode decomposeMatrix -n "decomposeMatrix3";
	rename -uid "FEBBF7F4-45BC-5CCA-F502-6489A510F384";
createNode condition -n "condition8";
	rename -uid "A4B65477-49D7-07E1-5D3F-E690C941B539";
	setAttr ".st" 1;
	setAttr ".cf" -type "float3" 0 0 0 ;
createNode composeMatrix -n "composeMatrix20";
	rename -uid "8EBAD256-4B6B-8E3F-1269-8783FCD9AEFD";
createNode network -n "outputs";
	rename -uid "4DA83365-4E4D-49DB-AADE-19A1BABCC994";
	addAttr -ci true -sn "outputTM" -ln "outputTM" -dt "matrix";
createNode condition -n "condition2";
	rename -uid "06EA4634-457C-D53E-E6B5-06938A1D51CA";
	setAttr ".op" 2;
	setAttr ".st" 1;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 0;
	setAttr -av ".unw";
	setAttr -k on ".etw";
	setAttr -k on ".tps";
	setAttr -k on ".tms";
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultRenderingList1;
connectAttr "follicle:inputs.is" "follicle:pointOnSurfaceInfo1.is";
connectAttr "follicle:inputs.u" "follicle:pointOnSurfaceInfo1.u";
connectAttr "follicle:inputs.v" "follicle:pointOnSurfaceInfo1.v";
connectAttr "inputs.surface" "follicleClampV:inputs.is";
connectAttr "clamp2.opr" "follicleClampV:inputs.u";
connectAttr "clamp1.opg" "follicleClampV:inputs.v";
connectAttr "follicleClampV:inputs.is" "follicleClampV:pointOnSurfaceInfo1.is";
connectAttr "follicleClampV:inputs.u" "follicleClampV:pointOnSurfaceInfo1.u";
connectAttr "follicleClampV:inputs.v" "follicleClampV:pointOnSurfaceInfo1.v";
connectAttr "inputs.surfaceU" "clamp2.ipr";
connectAttr "inputs.surfaceV" "clamp2.ipg";
connectAttr "inputs.surface" "follicle:inputs.is";
connectAttr "clamp2.opr" "follicle:inputs.u";
connectAttr "clamp2.opg" "follicle:inputs.v";
connectAttr "inputs.surfaceU" "clamp1.ipr";
connectAttr "inputs.surfaceV" "clamp1.ipg";
connectAttr "follicle:outputs.o" "multMatrix1.i[0]";
connectAttr "follicleClampU:fourByFourMatrix1.o" "follicleClampU:outputs.o";
connectAttr "condition5.ocr" "multiplyDivide5.i1x";
connectAttr "follicleClampV:pointOnSurfaceInfo1.px" "follicleClampV:fourByFourMatrix1.i30"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.py" "follicleClampV:fourByFourMatrix1.i31"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.pz" "follicleClampV:fourByFourMatrix1.i32"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.nx" "follicleClampV:fourByFourMatrix1.i00"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.ny" "follicleClampV:fourByFourMatrix1.i01"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.nz" "follicleClampV:fourByFourMatrix1.i02"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.tux" "follicleClampV:fourByFourMatrix1.i10"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.tuy" "follicleClampV:fourByFourMatrix1.i11"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.tuz" "follicleClampV:fourByFourMatrix1.i12"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.tvx" "follicleClampV:fourByFourMatrix1.i20"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.tvy" "follicleClampV:fourByFourMatrix1.i21"
		;
connectAttr "follicleClampV:pointOnSurfaceInfo1.tvz" "follicleClampV:fourByFourMatrix1.i22"
		;
connectAttr "inputs.surfaceU" "condition1.ft";
connectAttr "follicle:outputs.o" "decomposeMatrix4.imat";
connectAttr "decomposeMatrix4.ot" "plusMinusAverage1.i3[0]";
connectAttr "decomposeMatrix6.ot" "plusMinusAverage1.i3[1]";
connectAttr "inputs.surfaceV" "condition4.ft";
connectAttr "inputs.surfaceV" "multiplyDivide4.i1x";
connectAttr "follicleClampU:pointOnSurfaceInfo1.px" "follicleClampU:fourByFourMatrix1.i30"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.py" "follicleClampU:fourByFourMatrix1.i31"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.pz" "follicleClampU:fourByFourMatrix1.i32"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.nx" "follicleClampU:fourByFourMatrix1.i00"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.ny" "follicleClampU:fourByFourMatrix1.i01"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.nz" "follicleClampU:fourByFourMatrix1.i02"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.tux" "follicleClampU:fourByFourMatrix1.i10"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.tuy" "follicleClampU:fourByFourMatrix1.i11"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.tuz" "follicleClampU:fourByFourMatrix1.i12"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.tvx" "follicleClampU:fourByFourMatrix1.i20"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.tvy" "follicleClampU:fourByFourMatrix1.i21"
		;
connectAttr "follicleClampU:pointOnSurfaceInfo1.tvz" "follicleClampU:fourByFourMatrix1.i22"
		;
connectAttr "follicle:fourByFourMatrix1.o" "follicle:outputs.o";
connectAttr "plusMinusAverage4.o1" "condition6.ctr";
connectAttr "multiplyDivide4.ox" "condition6.cfr";
connectAttr "condition4.ocr" "condition6.ft";
connectAttr "inputs.surfaceV" "condition3.ft";
connectAttr "follicleClampV:fourByFourMatrix1.o" "follicleClampV:outputs.o";
connectAttr "follicleClampU:inputs.is" "follicleClampU:pointOnSurfaceInfo1.is";
connectAttr "follicleClampU:inputs.u" "follicleClampU:pointOnSurfaceInfo1.u";
connectAttr "follicleClampU:inputs.v" "follicleClampU:pointOnSurfaceInfo1.v";
connectAttr "follicle:pointOnSurfaceInfo1.px" "follicle:fourByFourMatrix1.i30";
connectAttr "follicle:pointOnSurfaceInfo1.py" "follicle:fourByFourMatrix1.i31";
connectAttr "follicle:pointOnSurfaceInfo1.pz" "follicle:fourByFourMatrix1.i32";
connectAttr "follicle:pointOnSurfaceInfo1.nx" "follicle:fourByFourMatrix1.i00";
connectAttr "follicle:pointOnSurfaceInfo1.ny" "follicle:fourByFourMatrix1.i01";
connectAttr "follicle:pointOnSurfaceInfo1.nz" "follicle:fourByFourMatrix1.i02";
connectAttr "follicle:pointOnSurfaceInfo1.tux" "follicle:fourByFourMatrix1.i10";
connectAttr "follicle:pointOnSurfaceInfo1.tuy" "follicle:fourByFourMatrix1.i11";
connectAttr "follicle:pointOnSurfaceInfo1.tuz" "follicle:fourByFourMatrix1.i12";
connectAttr "follicle:pointOnSurfaceInfo1.tvx" "follicle:fourByFourMatrix1.i20";
connectAttr "follicle:pointOnSurfaceInfo1.tvy" "follicle:fourByFourMatrix1.i21";
connectAttr "follicle:pointOnSurfaceInfo1.tvz" "follicle:fourByFourMatrix1.i22";
connectAttr "follicleClampU:outputs.o" "decomposeMatrix6.imat";
connectAttr "follicleClampV:outputs.o" "decomposeMatrix5.imat";
connectAttr "condition6.ocr" "multiplyDivide6.i1x";
connectAttr "plusMinusAverage3.o1" "condition5.ctr";
connectAttr "multiplyDivide3.ox" "condition5.cfr";
connectAttr "condition2.ocr" "condition5.ft";
connectAttr "decomposeMatrix4.ot" "plusMinusAverage2.i3[0]";
connectAttr "decomposeMatrix5.ot" "plusMinusAverage2.i3[1]";
connectAttr "inputs.surface" "follicleClampU:inputs.is";
connectAttr "clamp1.opr" "follicleClampU:inputs.u";
connectAttr "clamp2.opg" "follicleClampU:inputs.v";
connectAttr "inputs.surfaceV" "plusMinusAverage4.i1[0]";
connectAttr "condition7.oc" "plusMinusAverage5.i3[0]";
connectAttr "condition8.oc" "plusMinusAverage5.i3[1]";
connectAttr "decomposeMatrix3.ot" "plusMinusAverage5.i3[2]";
connectAttr "condition2.ocr" "addDoubleLinear3.i2";
connectAttr "condition1.ocr" "addDoubleLinear3.i1";
connectAttr "condition4.ocr" "addDoubleLinear4.i2";
connectAttr "condition3.ocr" "addDoubleLinear4.i1";
connectAttr "inputs.surfaceU" "multiplyDivide3.i1x";
connectAttr "inputs.surfaceU" "plusMinusAverage3.i1[0]";
connectAttr "multMatrix1.o" "multMatrix3.i[1]";
connectAttr "addDoubleLinear3.o" "condition7.ft";
connectAttr "multiplyDivide7.o" "condition7.ct";
connectAttr "multiplyDivide5.ox" "multiplyDivide7.i1x";
connectAttr "multiplyDivide5.ox" "multiplyDivide7.i1y";
connectAttr "multiplyDivide5.ox" "multiplyDivide7.i1z";
connectAttr "plusMinusAverage1.o3" "multiplyDivide7.i2";
connectAttr "multiplyDivide6.ox" "multiplyDivide8.i1x";
connectAttr "multiplyDivide6.ox" "multiplyDivide8.i1y";
connectAttr "multiplyDivide6.ox" "multiplyDivide8.i1z";
connectAttr "plusMinusAverage2.o3" "multiplyDivide8.i2";
connectAttr "multMatrix3.o" "decomposeMatrix3.imat";
connectAttr "addDoubleLinear4.o" "condition8.ft";
connectAttr "multiplyDivide8.o" "condition8.ct";
connectAttr "plusMinusAverage5.o3" "composeMatrix20.it";
connectAttr "decomposeMatrix3.or" "composeMatrix20.ir";
connectAttr "composeMatrix20.omat" "outputs.outputTM";
connectAttr "inputs.surfaceU" "condition2.ft";
connectAttr "clamp2.msg" ":defaultRenderUtilityList1.u" -na;
// End of omtk.InifityFollicle_v0.0.2.ma
