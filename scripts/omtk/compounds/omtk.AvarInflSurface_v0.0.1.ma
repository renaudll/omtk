//Maya ASCII 2020 scene
//Name: omtk.AvarInflSurface_v0.0.2.ma
//Last modified: Wed, May 06, 2020 09:02:31 PM
//Codeset: 1252
requires maya "2020";
requires -nodeType "inverseMatrix" "matrixNodes" "1.0";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "DD1B3815-4C3A-9F29-D040-5DB1EFC07D08";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "CB7E25CE-4CCE-0E35-0C8C-D28C19270EAB";
fileInfo "omtk.compound.name" "omtk.AvarInflSurface";
createNode transform -n "dag";
	rename -uid "EECFCE0B-499F-EC81-9165-1EB8C53C3ACA";
createNode arcLengthDimension -n "avarsimple_modelInfl_arcdimension_rigShape" -p
		 "dag";
	rename -uid "9EE11815-4CAD-4839-BE05-E08F073A83FF";
	setAttr -k off ".v";
	setAttr ".upv" 1;
	setAttr ".vpv" 1;
createNode multiplyDivide -n "multiplyDivide50";
	rename -uid "1BA65636-4AF0-8DED-D820-CBAC6FCBA607";
createNode multiplyDivide -n "multiplyDivide49";
	rename -uid "601C4800-49BA-7B88-2732-90AEF7692588";
createNode network -n "inputs";
	rename -uid "1C5E4217-4059-4CB6-6645-36ABBA182C70";
	addAttr -ci true -sn "globalScale" -ln "globalScale" -dv 1 -at "double";
	addAttr -ci true -sn "innAvarLr" -ln "innAvarLr" -at "double";
	addAttr -ci true -sn "innAvarUd" -ln "innAvarUd" -at "double";
	addAttr -ci true -sn "innAvarFb" -ln "innAvarFb" -at "double";
	addAttr -ci true -sn "innAvarYw" -ln "innAvarYw" -at "double";
	addAttr -ci true -sn "innAvarPt" -ln "innAvarPt" -at "double";
	addAttr -ci true -sn "innAvarRl" -ln "innAvarRl" -at "double";
	addAttr -ci true -sn "innAvarSx" -ln "innAvarSx" -at "double";
	addAttr -ci true -sn "innAvarSy" -ln "innAvarSy" -at "double";
	addAttr -ci true -sn "innAvarSz" -ln "innAvarSz" -at "double";
	addAttr -ci true -sn "multLr" -ln "multLr" -dv 0.25 -at "double";
	addAttr -ci true -sn "multUd" -ln "multUd" -dv 0.25 -at "double";
	addAttr -ci true -sn "multFb" -ln "multFb" -dv 0.1 -at "double";
	addAttr -ci true -sn "innOffset" -ln "innOffset" -dt "matrix";
	addAttr -ci true -sn "innSurface" -ln "innSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "innSurfaceTm" -ln "innSurfaceTm" -dt "matrix";
	addAttr -ci true -sn "innSurfaceMinValueU" -ln "innSurfaceMinValueU" -at "double";
	addAttr -ci true -sn "innSurfaceMinValueV" -ln "innSurfaceMinValueV" -at "double";
	addAttr -ci true -sn "innSurfaceMaxValueU" -ln "innSurfaceMaxValueU" -dv 1 -at "double";
	addAttr -ci true -sn "innSurfaceMaxValueV" -ln "innSurfaceMaxValueV" -dv 1 -at "double";
	addAttr -ci true -sn "baseU" -ln "baseU" -at "double";
	addAttr -ci true -sn "baseV" -ln "baseV" -at "double";
	addAttr -ci true -sn "blendTx" -ln "blendTx" -at "float";
	addAttr -ci true -sn "blendTy" -ln "blendTy" -at "float";
	addAttr -ci true -sn "blendTz" -ln "blendTz" -at "float";
	addAttr -ci true -sn "blendRx" -ln "blendRx" -at "float";
	addAttr -ci true -sn "blendRy" -ln "blendRy" -at "float";
	addAttr -ci true -sn "blendRz" -ln "blendRz" -at "float";
	addAttr -ci true -sn "blendSx" -ln "blendSx" -at "float";
	addAttr -ci true -sn "blendSy" -ln "blendSy" -at "float";
	addAttr -ci true -sn "blendSz" -ln "blendSz" -at "float";
	addAttr -ci true -sn "SurfaceMinU" -ln "SurfaceMinU" -at "float";
	addAttr -ci true -sn "SurfaceMaxU" -ln "SurfaceMaxU" -at "float";
	addAttr -ci true -sn "SurfaceMinV" -ln "SurfaceMinV" -at "float";
	addAttr -ci true -sn "SurfaceMaxV" -ln "SurfaceMaxV" -at "float";
	setAttr ".innAvarSx" 1;
	setAttr ".innAvarSy" 1;
	setAttr ".innAvarSz" 1;
	setAttr ".innOffset" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 5.5511151231257827e-17 0 0.50613270285737955 1;
	setAttr ".baseU" 0.5;
	setAttr ".baseV" 0.5;
	setAttr ".blendTx" 1;
	setAttr ".blendTy" 1;
	setAttr ".blendTz" 1;
	setAttr ".blendRx" 1;
	setAttr ".blendRy" 1;
	setAttr ".blendRz" 1;
	setAttr ".blendSx" 1;
	setAttr ".blendSy" 1;
	setAttr ".blendSz" 1;
	setAttr ".SurfaceMaxU" 1;
	setAttr ".SurfaceMaxV" 1;
createNode setRange -n "setRange1";
	rename -uid "D69DAB9A-4A85-4052-D50D-B980AAE87646";
	setAttr ".m" -type "float3" 1 1 0 ;
createNode condition -n "infinityFol:condition5";
	rename -uid "0D5AB27A-4F84-FF11-E641-BF87522DC536";
	setAttr ".st" 1;
createNode plusMinusAverage -n "infinityFol:plusMinusAverage3";
	rename -uid "AB7690EC-4C92-E7E6-8F0F-FC93E0510B77";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[1]"  1;
createNode condition -n "infinityFol:condition6";
	rename -uid "4C11A5DC-4B14-AE17-B1B7-7CBC933A9084";
	setAttr ".st" 1;
createNode decomposeMatrix -n "infinityFol:decomposeMatrix6";
	rename -uid "7D177FFA-4E87-A54F-90AA-859B0CA09AED";
createNode network -n "infinityFol:inputs";
	rename -uid "CA1D6489-41DC-9FEA-3AC1-D8A2D2129D63";
	addAttr -ci true -sn "surfaceU" -ln "surfaceU" -at "float";
	addAttr -ci true -sn "surfaceV" -ln "surfaceV" -at "float";
	addAttr -ci true -sn "surface" -ln "surface" -dt "nurbsSurface";
createNode decomposeMatrix -n "infinityFol:decomposeMatrix5";
	rename -uid "930F8296-4964-5B48-0CC1-E9884862FBFD";
createNode network -n "infinityFol:follicleClampU:inputs";
	rename -uid "DA97D738-4CA0-109E-DF8A-1087AB6CE66B";
	addAttr -s false -ci true -sn "is" -ln "inputSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "u" -ln "parameterU" -at "double";
	addAttr -ci true -sn "v" -ln "parameterV" -at "double";
createNode pointOnSurfaceInfo -n "infinityFol:follicleClampU:pointOnSurfaceInfo1";
	rename -uid "7C744147-4B75-BFAA-F90F-BEAAB94CF802";
createNode multiplyDivide -n "infinityFol:multiplyDivide3";
	rename -uid "844C5343-403F-6D56-7975-8A9F4F016FD3";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode network -n "infinityFol:follicleClampV:inputs";
	rename -uid "CE221FC5-49DE-BEA8-1D16-029A75810939";
	addAttr -s false -ci true -sn "is" -ln "inputSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "u" -ln "parameterU" -at "double";
	addAttr -ci true -sn "v" -ln "parameterV" -at "double";
createNode fourByFourMatrix -n "infinityFol:follicleClampU:fourByFourMatrix1";
	rename -uid "EADECB13-43B3-97E7-0F95-1B9919D9F2CD";
createNode fourByFourMatrix -n "infinityFol:follicleClampV:fourByFourMatrix1";
	rename -uid "A1289804-4FB4-F9CE-4A8A-5295B654C59E";
createNode pointOnSurfaceInfo -n "infinityFol:follicleClampV:pointOnSurfaceInfo1";
	rename -uid "5418B3F1-4BF4-99ED-7242-E79AAC35BE76";
createNode multiplyDivide -n "infinityFol:multiplyDivide4";
	rename -uid "C2BB795E-4C5C-B77C-BBC3-D5B4A9BAC00C";
	setAttr ".i2" -type "float3" -1 1 1 ;
createNode condition -n "infinityFol:condition2";
	rename -uid "6D10ECDC-4A0A-26E7-422A-119282CA7D02";
	setAttr ".op" 2;
	setAttr ".st" 1;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode pointOnSurfaceInfo -n "infinityFol:follicle:pointOnSurfaceInfo1";
	rename -uid "8F4D05CB-4B4B-D13E-51FE-4BAF519E132C";
createNode network -n "infinityFol:follicleClampV:outputs";
	rename -uid "9E7C5334-475A-818A-33B5-FC98B4B3B593";
	addAttr -s false -ci true -sn "o" -ln "output" -dt "matrix";
createNode addDoubleLinear -n "addDoubleLinear1";
	rename -uid "A22A8A4F-4865-AD15-A22A-E9B8ECB4B964";
createNode clamp -n "infinityFol:clamp1";
	rename -uid "7906E1BD-4FD7-E4BD-0C84-C780AF660D53";
	setAttr ".mn" -type "float3" 0.001 0.001 0 ;
	setAttr ".mx" -type "float3" 0.99900001 0.99900001 0 ;
createNode network -n "infinityFol:follicle:inputs";
	rename -uid "74AF0693-4E91-EE00-AAE3-148010756CDE";
	addAttr -s false -ci true -sn "is" -ln "inputSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "u" -ln "parameterU" -at "double";
	addAttr -ci true -sn "v" -ln "parameterV" -at "double";
createNode plusMinusAverage -n "infinityFol:plusMinusAverage4";
	rename -uid "8D3A4DEE-405E-D2C6-3AC8-F1B0673D968A";
	setAttr ".op" 2;
	setAttr -s 2 ".i1[1]"  1;
createNode condition -n "infinityFol:condition4";
	rename -uid "04104904-48E1-4DEA-23CA-CCBD810EDCA9";
	setAttr ".op" 2;
	setAttr ".st" 1;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode decomposeMatrix -n "infinityFol:decomposeMatrix4";
	rename -uid "076C3E8C-4E4B-F7DA-71AA-02BF6B97D6BB";
createNode addDoubleLinear -n "addDoubleLinear2";
	rename -uid "ACD11AE6-40AC-C45D-F240-24A985B39517";
createNode network -n "bindFol:inputs";
	rename -uid "A04B120A-459A-E421-4468-25B825D17689";
	addAttr -s false -ci true -sn "is" -ln "inputSurface" -dt "nurbsSurface";
	addAttr -ci true -sn "u" -ln "parameterU" -at "double";
	addAttr -ci true -sn "v" -ln "parameterV" -at "double";
createNode network -n "infinityFol:follicle:outputs";
	rename -uid "E8CDDA27-411A-B15E-9CC1-F59C44158C0B";
	addAttr -s false -ci true -sn "o" -ln "output" -dt "matrix";
createNode network -n "infinityFol:follicleClampU:outputs";
	rename -uid "3909BA66-435C-304A-E233-7CBE7632B4AE";
	addAttr -s false -ci true -sn "o" -ln "output" -dt "matrix";
createNode clamp -n "infinityFol:clamp2";
	rename -uid "964C0840-4354-50D4-B50E-0C978AB6A0A8";
	setAttr ".mx" -type "float3" 1 1 0 ;
createNode fourByFourMatrix -n "infinityFol:follicle:fourByFourMatrix1";
	rename -uid "80B1490E-4622-C55D-0195-488C28E00C02";
createNode pointOnSurfaceInfo -n "bindFol:pointOnSurfaceInfo1";
	rename -uid "EB6BAAAE-4CA6-F8E0-F1F2-B8B810E3EEDD";
createNode condition -n "infinityFol:condition1";
	rename -uid "5D7A7F68-4370-9104-88AB-A0B24035BA50";
	setAttr ".op" 4;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode addDoubleLinear -n "infinityFol:addDoubleLinear3";
	rename -uid "C55DCE4A-4CEF-3CBD-3E5D-2F9D56F1A8FD";
createNode multiplyDivide -n "infinityFol:multiplyDivide6";
	rename -uid "72E704F7-4A4B-ABC4-57FB-9E85F04245CD";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 0.001 1 1 ;
createNode plusMinusAverage -n "infinityFol:plusMinusAverage1";
	rename -uid "7DED9030-430F-6A0F-DFCB-A6A21E123C0B";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode network -n "bindFol:outputs";
	rename -uid "C412A048-485D-01B8-0F0C-7CA56BAC2F22";
	addAttr -s false -ci true -sn "o" -ln "output" -dt "matrix";
createNode addDoubleLinear -n "infinityFol:addDoubleLinear4";
	rename -uid "EC0981F6-4CCB-C64D-9AAE-8FA42FBE2FCA";
createNode condition -n "infinityFol:condition3";
	rename -uid "E518D915-4E06-A2EC-128F-D79E6FDC3FEF";
	setAttr ".op" 4;
	setAttr ".ct" -type "float3" 1 0 0 ;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode multiplyDivide -n "infinityFol:multiplyDivide5";
	rename -uid "19C14457-4EDB-F07C-5DB9-9E852DA87016";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 0.001 1 1 ;
createNode multiplyDivide -n "infinityFol:multiplyDivide7";
	rename -uid "DDC3E01E-449B-0B63-24FD-CB811A49FA49";
createNode plusMinusAverage -n "infinityFol:plusMinusAverage2";
	rename -uid "AAF2A4FC-4158-52E1-8E5F-EDB202782E64";
	setAttr ".op" 2;
	setAttr -s 2 ".i3";
	setAttr -s 2 ".i3";
createNode fourByFourMatrix -n "bindFol:fourByFourMatrix1";
	rename -uid "053246BB-40EA-B637-97BD-AE9FF0A4EC50";
createNode multMatrix -n "infinityFol:multMatrix3";
	rename -uid "3C1A3BFC-4FB4-FA0A-1E37-0F86D665097A";
createNode multMatrix -n "infinityFol:multMatrix1";
	rename -uid "681BE250-4838-9E68-F1F0-2BAA36770E5A";
createNode multiplyDivide -n "infinityFol:multiplyDivide8";
	rename -uid "5D53C07A-421F-CD1D-E90C-09953A29C97A";
createNode decomposeMatrix -n "decomposeMatrix164";
	rename -uid "06C784E0-4FA2-E9CE-6FB5-019772A67A71";
createNode unitConversion -n "unitConversion62";
	rename -uid "EDDEA27D-4A5A-5D11-17D2-4890EBF7E041";
	setAttr ".cf" 57.295779513082323;
createNode unitConversion -n "unitConversion58";
	rename -uid "41B1F798-4344-FB4B-DF48-D0B8E3D73793";
	setAttr ".cf" 0.017453292519943295;
createNode inverseMatrix -n "inverseMatrix3";
	rename -uid "FA90D0AC-4E7F-8A47-C04A-179805E5CA14";
	setAttr ".omat" -type "matrix" 0 0.30263467000093991 0 0 -6.123233995736766e-17 0 0.30263467000093991 0
		 1 0 1.8531028996383326e-17 0 6.1629758220391547e-33 0 1.1420628366221694e-49 1;
createNode condition -n "infinityFol:condition8";
	rename -uid "A2B60B49-40DB-0A26-946B-1A84BD699948";
	setAttr ".st" 1;
	setAttr ".cf" -type "float3" 0 0 0 ;
createNode unitConversion -n "unitConversion60";
	rename -uid "7B6092F4-4021-54EF-9523-20B7166BDD8A";
	setAttr ".cf" 57.295779513082323;
createNode network -n "infinityFol:outputs";
	rename -uid "F50067E5-4E4F-258E-EADE-C6BA2BDAF25F";
	addAttr -ci true -sn "outputTM" -ln "outputTM" -dt "matrix";
createNode composeMatrix -n "composeMatrix21";
	rename -uid "07747677-462E-8707-6E3A-B8B76CE0B50B";
createNode inverseMatrix -n "inverseMatrix2";
	rename -uid "F8E31FE1-4963-9DA3-8968-B29C60DD1D37";
	setAttr ".omat" -type "matrix" 0 0.30263467000093991 0 0 -6.123233995736766e-17 0 0.30263467000093991 0
		 1 0 1.8531028996383326e-17 0 0 0 0 1;
createNode unitConversion -n "unitConversion57";
	rename -uid "A1CB4CD5-41C8-9966-18F7-C3A8E19D64D8";
	setAttr ".cf" 0.017453292519943295;
createNode composeMatrix -n "getAvarFbTM";
	rename -uid "57101548-45FF-5404-139E-81B17BDF947C";
createNode multMatrix -n "multMatrix31";
	rename -uid "FA53B6B3-461E-C598-55A6-14A493FAF876";
	setAttr -s 2 ".i";
createNode decomposeMatrix -n "infinityFol:decomposeMatrix3";
	rename -uid "0E3A5582-4E6B-EE55-CE31-6881E06FF692";
createNode multMatrix -n "multMatrix32";
	rename -uid "16B99620-4E42-8009-817A-33AE7184CDF0";
	setAttr -s 2 ".i";
createNode composeMatrix -n "getFollicleRotTM";
	rename -uid "ED78FEB5-4204-7616-61BD-7CA949B700AD";
createNode condition -n "infinityFol:condition7";
	rename -uid "6711D49D-4B56-5DC4-2AD7-CB8AE8C2E763";
	setAttr ".st" 1;
	setAttr ".cf" -type "float3" 0 0 0 ;
createNode composeMatrix -n "infinityFol:composeMatrix22";
	rename -uid "836D46D8-4DBC-2714-46E4-DFA16ED18A76";
createNode multiplyDivide -n "multiplyDivide52";
	rename -uid "A1C37C58-48A7-A746-99B2-96B45427534E";
createNode unitConversion -n "unitConversion59";
	rename -uid "D6E6D561-4640-4E86-9F16-EEB5082DE899";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "multiplyDivide51";
	rename -uid "3819B027-4C1C-D169-2B36-4987F9AEBB2B";
createNode multMatrix -n "multMatrix33";
	rename -uid "CDCDA55D-41CD-427D-3DF0-419719DF6103";
	setAttr -s 3 ".i";
createNode decomposeMatrix -n "decomposeMatrix163";
	rename -uid "D99F51FF-4FE1-33DD-606E-29891B423965";
createNode inverseMatrix -n "inverseMatrix1";
	rename -uid "AA6E4D91-4CEB-8570-43D8-08BFD8519E41";
	setAttr ".omat" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 6.1629758220391547e-33 1;
createNode composeMatrix -n "composeMatrix19";
	rename -uid "5F1F7FCB-4487-06F4-95C3-DDBB39E28D08";
createNode multMatrix -n "multMatrix35";
	rename -uid "68779E8D-4DA6-985B-EFA1-D4AE8E342CD7";
	setAttr -s 4 ".i";
createNode decomposeMatrix -n "decomposeMatrix165";
	rename -uid "50E754A2-43AC-C77C-81C0-8AAF1380FC01";
createNode plusMinusAverage -n "infinityFol:plusMinusAverage5";
	rename -uid "500AFC0D-4FBE-9FA0-A847-D897A27181A9";
	setAttr -s 3 ".i3";
	setAttr -s 3 ".i3";
createNode composeMatrix -n "getRotTM";
	rename -uid "E3428E82-49E6-50A7-3B6D-7D846F0C4C5A";
createNode unitConversion -n "unitConversion63";
	rename -uid "190AEED7-42B8-2596-4C1B-56907F5F399A";
	setAttr ".cf" 0.017453292519943295;
createNode multiplyDivide -n "multiplyDivide55";
	rename -uid "0F35D1A3-4191-29C7-3E13-678704611C29";
createNode multMatrix -n "multMatrix36";
	rename -uid "A520E7DB-4ABB-1280-AB3D-17806576887D";
	setAttr -s 2 ".i";
createNode unitConversion -n "unitConversion61";
	rename -uid "76354277-4E97-4128-8627-04BFD01034EB";
	setAttr ".cf" 57.295779513082323;
createNode multiplyDivide -n "multiplyDivide54";
	rename -uid "D9156092-4475-94D8-879E-8785CF03CDB8";
createNode network -n "outputs";
	rename -uid "5FD7C27F-42D5-0B24-3A37-62B5E2E04F88";
	addAttr -ci true -sn "output" -ln "output" -dt "matrix";
createNode composeMatrix -n "composeMatrix20";
	rename -uid "3DD323C2-4960-2140-E72C-73B0F0876054";
createNode multiplyDivide -n "multiplyDivide53";
	rename -uid "CB637D21-4738-0162-4C57-419CDDAB949F";
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
	setAttr -s 4 ".u";
select -ne :defaultRenderingList1;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".dss" -type "string" "lambert1";
connectAttr "inputs.innSurface" "avarsimple_modelInfl_arcdimension_rigShape.ng";
connectAttr "inputs.innAvarUd" "multiplyDivide50.i1x";
connectAttr "inputs.multUd" "multiplyDivide50.i2x";
connectAttr "inputs.innAvarLr" "multiplyDivide49.i1x";
connectAttr "inputs.multLr" "multiplyDivide49.i2x";
connectAttr "inputs.SurfaceMaxU" "setRange1.omx";
connectAttr "inputs.SurfaceMaxV" "setRange1.omy";
connectAttr "inputs.SurfaceMinU" "setRange1.onx";
connectAttr "inputs.SurfaceMinV" "setRange1.ony";
connectAttr "inputs.baseV" "setRange1.vy";
connectAttr "inputs.baseU" "setRange1.vx";
connectAttr "infinityFol:plusMinusAverage3.o1" "infinityFol:condition5.ctr";
connectAttr "infinityFol:multiplyDivide3.ox" "infinityFol:condition5.cfr";
connectAttr "infinityFol:condition2.ocr" "infinityFol:condition5.ft";
connectAttr "infinityFol:inputs.surfaceU" "infinityFol:plusMinusAverage3.i1[0]";
connectAttr "infinityFol:plusMinusAverage4.o1" "infinityFol:condition6.ctr";
connectAttr "infinityFol:multiplyDivide4.ox" "infinityFol:condition6.cfr";
connectAttr "infinityFol:condition4.ocr" "infinityFol:condition6.ft";
connectAttr "infinityFol:follicleClampU:outputs.o" "infinityFol:decomposeMatrix6.imat"
		;
connectAttr "inputs.innSurface" "infinityFol:inputs.surface";
connectAttr "addDoubleLinear1.o" "infinityFol:inputs.surfaceU";
connectAttr "addDoubleLinear2.o" "infinityFol:inputs.surfaceV";
connectAttr "infinityFol:follicleClampV:outputs.o" "infinityFol:decomposeMatrix5.imat"
		;
connectAttr "infinityFol:inputs.surface" "infinityFol:follicleClampU:inputs.is";
connectAttr "infinityFol:clamp1.opr" "infinityFol:follicleClampU:inputs.u";
connectAttr "infinityFol:clamp2.opg" "infinityFol:follicleClampU:inputs.v";
connectAttr "infinityFol:follicleClampU:inputs.is" "infinityFol:follicleClampU:pointOnSurfaceInfo1.is"
		;
connectAttr "infinityFol:follicleClampU:inputs.u" "infinityFol:follicleClampU:pointOnSurfaceInfo1.u"
		;
connectAttr "infinityFol:follicleClampU:inputs.v" "infinityFol:follicleClampU:pointOnSurfaceInfo1.v"
		;
connectAttr "infinityFol:inputs.surfaceU" "infinityFol:multiplyDivide3.i1x";
connectAttr "infinityFol:inputs.surface" "infinityFol:follicleClampV:inputs.is";
connectAttr "infinityFol:clamp2.opr" "infinityFol:follicleClampV:inputs.u";
connectAttr "infinityFol:clamp1.opg" "infinityFol:follicleClampV:inputs.v";
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.px" "infinityFol:follicleClampU:fourByFourMatrix1.i30"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.py" "infinityFol:follicleClampU:fourByFourMatrix1.i31"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.pz" "infinityFol:follicleClampU:fourByFourMatrix1.i32"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.nx" "infinityFol:follicleClampU:fourByFourMatrix1.i00"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.ny" "infinityFol:follicleClampU:fourByFourMatrix1.i01"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.nz" "infinityFol:follicleClampU:fourByFourMatrix1.i02"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.tux" "infinityFol:follicleClampU:fourByFourMatrix1.i10"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.tuy" "infinityFol:follicleClampU:fourByFourMatrix1.i11"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.tuz" "infinityFol:follicleClampU:fourByFourMatrix1.i12"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.tvx" "infinityFol:follicleClampU:fourByFourMatrix1.i20"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.tvy" "infinityFol:follicleClampU:fourByFourMatrix1.i21"
		;
connectAttr "infinityFol:follicleClampU:pointOnSurfaceInfo1.tvz" "infinityFol:follicleClampU:fourByFourMatrix1.i22"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.px" "infinityFol:follicleClampV:fourByFourMatrix1.i30"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.py" "infinityFol:follicleClampV:fourByFourMatrix1.i31"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.pz" "infinityFol:follicleClampV:fourByFourMatrix1.i32"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.nx" "infinityFol:follicleClampV:fourByFourMatrix1.i00"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.ny" "infinityFol:follicleClampV:fourByFourMatrix1.i01"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.nz" "infinityFol:follicleClampV:fourByFourMatrix1.i02"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.tux" "infinityFol:follicleClampV:fourByFourMatrix1.i10"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.tuy" "infinityFol:follicleClampV:fourByFourMatrix1.i11"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.tuz" "infinityFol:follicleClampV:fourByFourMatrix1.i12"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.tvx" "infinityFol:follicleClampV:fourByFourMatrix1.i20"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.tvy" "infinityFol:follicleClampV:fourByFourMatrix1.i21"
		;
connectAttr "infinityFol:follicleClampV:pointOnSurfaceInfo1.tvz" "infinityFol:follicleClampV:fourByFourMatrix1.i22"
		;
connectAttr "infinityFol:follicleClampV:inputs.is" "infinityFol:follicleClampV:pointOnSurfaceInfo1.is"
		;
connectAttr "infinityFol:follicleClampV:inputs.u" "infinityFol:follicleClampV:pointOnSurfaceInfo1.u"
		;
connectAttr "infinityFol:follicleClampV:inputs.v" "infinityFol:follicleClampV:pointOnSurfaceInfo1.v"
		;
connectAttr "infinityFol:inputs.surfaceV" "infinityFol:multiplyDivide4.i1x";
connectAttr "infinityFol:inputs.surfaceU" "infinityFol:condition2.ft";
connectAttr "infinityFol:follicle:inputs.is" "infinityFol:follicle:pointOnSurfaceInfo1.is"
		;
connectAttr "infinityFol:follicle:inputs.u" "infinityFol:follicle:pointOnSurfaceInfo1.u"
		;
connectAttr "infinityFol:follicle:inputs.v" "infinityFol:follicle:pointOnSurfaceInfo1.v"
		;
connectAttr "infinityFol:follicleClampV:fourByFourMatrix1.o" "infinityFol:follicleClampV:outputs.o"
		;
connectAttr "multiplyDivide49.ox" "addDoubleLinear1.i2";
connectAttr "setRange1.ox" "addDoubleLinear1.i1";
connectAttr "infinityFol:inputs.surfaceU" "infinityFol:clamp1.ipr";
connectAttr "infinityFol:inputs.surfaceV" "infinityFol:clamp1.ipg";
connectAttr "infinityFol:inputs.surface" "infinityFol:follicle:inputs.is";
connectAttr "infinityFol:clamp2.opr" "infinityFol:follicle:inputs.u";
connectAttr "infinityFol:clamp2.opg" "infinityFol:follicle:inputs.v";
connectAttr "infinityFol:inputs.surfaceV" "infinityFol:plusMinusAverage4.i1[0]";
connectAttr "infinityFol:inputs.surfaceV" "infinityFol:condition4.ft";
connectAttr "infinityFol:follicle:outputs.o" "infinityFol:decomposeMatrix4.imat"
		;
connectAttr "multiplyDivide50.ox" "addDoubleLinear2.i2";
connectAttr "setRange1.oy" "addDoubleLinear2.i1";
connectAttr "inputs.innSurface" "bindFol:inputs.is";
connectAttr "setRange1.ox" "bindFol:inputs.u";
connectAttr "setRange1.oy" "bindFol:inputs.v";
connectAttr "infinityFol:follicle:fourByFourMatrix1.o" "infinityFol:follicle:outputs.o"
		;
connectAttr "infinityFol:follicleClampU:fourByFourMatrix1.o" "infinityFol:follicleClampU:outputs.o"
		;
connectAttr "infinityFol:inputs.surfaceU" "infinityFol:clamp2.ipr";
connectAttr "infinityFol:inputs.surfaceV" "infinityFol:clamp2.ipg";
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.px" "infinityFol:follicle:fourByFourMatrix1.i30"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.py" "infinityFol:follicle:fourByFourMatrix1.i31"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.pz" "infinityFol:follicle:fourByFourMatrix1.i32"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.nx" "infinityFol:follicle:fourByFourMatrix1.i00"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.ny" "infinityFol:follicle:fourByFourMatrix1.i01"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.nz" "infinityFol:follicle:fourByFourMatrix1.i02"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.tux" "infinityFol:follicle:fourByFourMatrix1.i10"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.tuy" "infinityFol:follicle:fourByFourMatrix1.i11"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.tuz" "infinityFol:follicle:fourByFourMatrix1.i12"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.tvx" "infinityFol:follicle:fourByFourMatrix1.i20"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.tvy" "infinityFol:follicle:fourByFourMatrix1.i21"
		;
connectAttr "infinityFol:follicle:pointOnSurfaceInfo1.tvz" "infinityFol:follicle:fourByFourMatrix1.i22"
		;
connectAttr "bindFol:inputs.is" "bindFol:pointOnSurfaceInfo1.is";
connectAttr "bindFol:inputs.u" "bindFol:pointOnSurfaceInfo1.u";
connectAttr "bindFol:inputs.v" "bindFol:pointOnSurfaceInfo1.v";
connectAttr "infinityFol:inputs.surfaceU" "infinityFol:condition1.ft";
connectAttr "infinityFol:condition2.ocr" "infinityFol:addDoubleLinear3.i2";
connectAttr "infinityFol:condition1.ocr" "infinityFol:addDoubleLinear3.i1";
connectAttr "infinityFol:condition6.ocr" "infinityFol:multiplyDivide6.i1x";
connectAttr "infinityFol:decomposeMatrix4.ot" "infinityFol:plusMinusAverage1.i3[0]"
		;
connectAttr "infinityFol:decomposeMatrix6.ot" "infinityFol:plusMinusAverage1.i3[1]"
		;
connectAttr "bindFol:fourByFourMatrix1.o" "bindFol:outputs.o";
connectAttr "infinityFol:condition4.ocr" "infinityFol:addDoubleLinear4.i2";
connectAttr "infinityFol:condition3.ocr" "infinityFol:addDoubleLinear4.i1";
connectAttr "infinityFol:inputs.surfaceV" "infinityFol:condition3.ft";
connectAttr "infinityFol:condition5.ocr" "infinityFol:multiplyDivide5.i1x";
connectAttr "infinityFol:multiplyDivide5.ox" "infinityFol:multiplyDivide7.i1x";
connectAttr "infinityFol:multiplyDivide5.ox" "infinityFol:multiplyDivide7.i1y";
connectAttr "infinityFol:multiplyDivide5.ox" "infinityFol:multiplyDivide7.i1z";
connectAttr "infinityFol:plusMinusAverage1.o3" "infinityFol:multiplyDivide7.i2";
connectAttr "infinityFol:decomposeMatrix4.ot" "infinityFol:plusMinusAverage2.i3[0]"
		;
connectAttr "infinityFol:decomposeMatrix5.ot" "infinityFol:plusMinusAverage2.i3[1]"
		;
connectAttr "bindFol:pointOnSurfaceInfo1.px" "bindFol:fourByFourMatrix1.i30";
connectAttr "bindFol:pointOnSurfaceInfo1.py" "bindFol:fourByFourMatrix1.i31";
connectAttr "bindFol:pointOnSurfaceInfo1.pz" "bindFol:fourByFourMatrix1.i32";
connectAttr "bindFol:pointOnSurfaceInfo1.nx" "bindFol:fourByFourMatrix1.i00";
connectAttr "bindFol:pointOnSurfaceInfo1.ny" "bindFol:fourByFourMatrix1.i01";
connectAttr "bindFol:pointOnSurfaceInfo1.nz" "bindFol:fourByFourMatrix1.i02";
connectAttr "bindFol:pointOnSurfaceInfo1.tux" "bindFol:fourByFourMatrix1.i10";
connectAttr "bindFol:pointOnSurfaceInfo1.tuy" "bindFol:fourByFourMatrix1.i11";
connectAttr "bindFol:pointOnSurfaceInfo1.tuz" "bindFol:fourByFourMatrix1.i12";
connectAttr "bindFol:pointOnSurfaceInfo1.tvx" "bindFol:fourByFourMatrix1.i20";
connectAttr "bindFol:pointOnSurfaceInfo1.tvy" "bindFol:fourByFourMatrix1.i21";
connectAttr "bindFol:pointOnSurfaceInfo1.tvz" "bindFol:fourByFourMatrix1.i22";
connectAttr "infinityFol:multMatrix1.o" "infinityFol:multMatrix3.i[1]";
connectAttr "infinityFol:follicle:outputs.o" "infinityFol:multMatrix1.i[0]";
connectAttr "infinityFol:multiplyDivide6.ox" "infinityFol:multiplyDivide8.i1x";
connectAttr "infinityFol:multiplyDivide6.ox" "infinityFol:multiplyDivide8.i1y";
connectAttr "infinityFol:multiplyDivide6.ox" "infinityFol:multiplyDivide8.i1z";
connectAttr "infinityFol:plusMinusAverage2.o3" "infinityFol:multiplyDivide8.i2";
connectAttr "multMatrix33.o" "decomposeMatrix164.imat";
connectAttr "decomposeMatrix165.orz" "unitConversion62.i";
connectAttr "inputs.innAvarPt" "unitConversion58.i";
connectAttr "bindFol:outputs.o" "inverseMatrix3.imat";
connectAttr "infinityFol:addDoubleLinear4.o" "infinityFol:condition8.ft";
connectAttr "infinityFol:multiplyDivide8.o" "infinityFol:condition8.ct";
connectAttr "decomposeMatrix165.orx" "unitConversion60.i";
connectAttr "infinityFol:composeMatrix22.omat" "infinityFol:outputs.outputTM";
connectAttr "decomposeMatrix164.ot" "composeMatrix21.it";
connectAttr "multMatrix32.o" "inverseMatrix2.imat";
connectAttr "inputs.innAvarYw" "unitConversion57.i";
connectAttr "multiplyDivide52.ox" "getAvarFbTM.itz";
connectAttr "infinityFol:outputs.outputTM" "multMatrix31.i[0]";
connectAttr "inverseMatrix3.omat" "multMatrix31.i[1]";
connectAttr "infinityFol:multMatrix3.o" "infinityFol:decomposeMatrix3.imat";
connectAttr "bindFol:outputs.o" "multMatrix32.i[0]";
connectAttr "inverseMatrix1.omat" "multMatrix32.i[1]";
connectAttr "decomposeMatrix164.or" "getFollicleRotTM.ir";
connectAttr "infinityFol:addDoubleLinear3.o" "infinityFol:condition7.ft";
connectAttr "infinityFol:multiplyDivide7.o" "infinityFol:condition7.ct";
connectAttr "infinityFol:plusMinusAverage5.o3" "infinityFol:composeMatrix22.it";
connectAttr "infinityFol:decomposeMatrix3.or" "infinityFol:composeMatrix22.ir";
connectAttr "multiplyDivide51.ox" "multiplyDivide52.i1x";
connectAttr "inputs.multFb" "multiplyDivide52.i2x";
connectAttr "inputs.innAvarRl" "unitConversion59.i";
connectAttr "inputs.innAvarFb" "multiplyDivide51.i1x";
connectAttr "avarsimple_modelInfl_arcdimension_rigShape.al" "multiplyDivide51.i2x"
		;
connectAttr "inverseMatrix2.omat" "multMatrix33.i[0]";
connectAttr "multMatrix31.o" "multMatrix33.i[1]";
connectAttr "multMatrix32.o" "multMatrix33.i[2]";
connectAttr "bindFol:outputs.o" "decomposeMatrix163.imat";
connectAttr "composeMatrix19.omat" "inverseMatrix1.imat";
connectAttr "decomposeMatrix163.ot" "composeMatrix19.it";
connectAttr "getRotTM.omat" "multMatrix35.i[0]";
connectAttr "getFollicleRotTM.omat" "multMatrix35.i[1]";
connectAttr "getAvarFbTM.omat" "multMatrix35.i[2]";
connectAttr "composeMatrix21.omat" "multMatrix35.i[3]";
connectAttr "multMatrix35.o" "decomposeMatrix165.imat";
connectAttr "infinityFol:condition7.oc" "infinityFol:plusMinusAverage5.i3[0]";
connectAttr "infinityFol:condition8.oc" "infinityFol:plusMinusAverage5.i3[1]";
connectAttr "infinityFol:decomposeMatrix3.ot" "infinityFol:plusMinusAverage5.i3[2]"
		;
connectAttr "inputs.innAvarSx" "getRotTM.isx";
connectAttr "inputs.innAvarSy" "getRotTM.isy";
connectAttr "inputs.innAvarSz" "getRotTM.isz";
connectAttr "unitConversion58.o" "getRotTM.irx";
connectAttr "unitConversion57.o" "getRotTM.iry";
connectAttr "unitConversion59.o" "getRotTM.irz";
connectAttr "multiplyDivide54.o" "unitConversion63.i";
connectAttr "inputs.blendSy" "multiplyDivide55.i2y";
connectAttr "inputs.blendSx" "multiplyDivide55.i2x";
connectAttr "inputs.blendSz" "multiplyDivide55.i2z";
connectAttr "decomposeMatrix165.osx" "multiplyDivide55.i1x";
connectAttr "decomposeMatrix165.osy" "multiplyDivide55.i1y";
connectAttr "decomposeMatrix165.osz" "multiplyDivide55.i1z";
connectAttr "composeMatrix20.omat" "multMatrix36.i[0]";
connectAttr "inputs.innOffset" "multMatrix36.i[1]";
connectAttr "decomposeMatrix165.ory" "unitConversion61.i";
connectAttr "inputs.blendRy" "multiplyDivide54.i2y";
connectAttr "inputs.blendRx" "multiplyDivide54.i2x";
connectAttr "inputs.blendRz" "multiplyDivide54.i2z";
connectAttr "unitConversion60.o" "multiplyDivide54.i1x";
connectAttr "unitConversion61.o" "multiplyDivide54.i1y";
connectAttr "unitConversion62.o" "multiplyDivide54.i1z";
connectAttr "multMatrix36.o" "outputs.output";
connectAttr "multiplyDivide53.o" "composeMatrix20.it";
connectAttr "multiplyDivide55.o" "composeMatrix20.is";
connectAttr "unitConversion63.o" "composeMatrix20.ir";
connectAttr "inputs.blendTy" "multiplyDivide53.i2y";
connectAttr "inputs.blendTx" "multiplyDivide53.i2x";
connectAttr "inputs.blendTz" "multiplyDivide53.i2z";
connectAttr "decomposeMatrix165.otx" "multiplyDivide53.i1x";
connectAttr "decomposeMatrix165.oty" "multiplyDivide53.i1y";
connectAttr "decomposeMatrix165.otz" "multiplyDivide53.i1z";
connectAttr "infinityFol:clamp2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multMatrix35.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "inverseMatrix3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "multMatrix36.msg" ":defaultRenderUtilityList1.u" -na;
// End of omtk.AvarInflSurface_v0.0.2.ma
