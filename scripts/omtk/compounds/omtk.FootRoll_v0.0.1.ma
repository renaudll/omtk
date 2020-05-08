//Maya ASCII 2020 scene
//Name: omtk.FootRoll_v3.ma
//Last modified: Sun, May 03, 2020 04:13:51 PM
//Codeset: 1252
requires maya "2020";
requires -nodeType "inverseMatrix" "matrixNodes" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 17763)\n";
fileInfo "UUID" "098CD38D-488A-0FFF-1C17-258E31C22AD4";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "2A9383DC-4BE9-F498-D6DE-8091F79330F5";
fileInfo "omtk.compound.name" "omtk.FootRoll";
createNode network -n "inputs";
	rename -uid "BB9E5348-4286-C95C-E12B-EA8B4E90D728";
	addAttr -ci true -k true -sn "rollAuto" -ln "rollAuto" -at "double";
	addAttr -ci true -k true -sn "rollAutoThreshold" -ln "rollAutoThreshold" -nn "Roll Auto Threshold" 
		-dv 25 -at "double";
	addAttr -ci true -k true -sn "bank" -ln "bank" -at "double";
	addAttr -ci true -k true -sn "heelSpin" -ln "heelSpin" -nn "Ankle Side" -min -90 
		-max 90 -at "double";
	addAttr -ci true -k true -sn "rollBack" -ln "rollBack" -nn "Back Roll" -min -90 
		-max 0 -at "double";
	addAttr -ci true -k true -sn "rollAnkle" -ln "rollAnkle" -nn "Ankle Roll" -min 0 
		-max 90 -at "double";
	addAttr -ci true -k true -sn "rollFront" -ln "rollFront" -nn "Front Roll" -min 0 
		-max 90 -at "double";
	addAttr -ci true -k true -sn "backTwist" -ln "backTwist" -nn "Back Twist" -min -90 
		-max 90 -at "double";
	addAttr -ci true -k true -sn "footTwist" -ln "footTwist" -nn "Heel Twist" -min -90 
		-max 90 -at "double";
	addAttr -ci true -k true -sn "toesTwist" -ln "toesTwist" -nn "Toes Twist" -min -90 
		-max 90 -at "double";
	addAttr -ci true -k true -sn "frontTwist" -ln "frontTwist" -nn "Front Twist" -min 
		-90 -max 90 -at "double";
	addAttr -ci true -k true -sn "toeWiggle" -ln "toeWiggle" -nn "Toe Wiggle" -min -90 
		-max 90 -at "double";
	addAttr -ci true -sn "pivotToes" -ln "pivotToes" -dt "double3";
	addAttr -ci true -sn "pivotFoot" -ln "pivotFoot" -dt "double3";
	addAttr -ci true -sn "pivotHeel" -ln "pivotHeel" -dt "double3";
	addAttr -ci true -sn "pivotToesEnd" -ln "pivotToesEnd" -dt "double3";
	addAttr -ci true -sn "pivotBack" -ln "pivotBack" -dt "double3";
	addAttr -ci true -sn "pivotBankIn" -ln "pivotBankIn" -dt "double3";
	addAttr -ci true -sn "pivotBankOut" -ln "pivotBankOut" -dt "double3";
	addAttr -ci true -sn "bindFootTM" -ln "bindFootTM" -dt "matrix";
	addAttr -ci true -sn "bintToesTM" -ln "bintToesTM" -dt "matrix";
	addAttr -ci true -sn "footYaw" -ln "footYaw" -at "doubleAngle";
	setAttr -k on ".rollAuto";
	setAttr -k on ".rollAutoThreshold";
	setAttr -k on ".bank";
	setAttr -k on ".heelSpin";
	setAttr -k on ".rollBack";
	setAttr -k on ".rollAnkle";
	setAttr -av -k on ".rollFront";
	setAttr -k on ".backTwist";
	setAttr -k on ".footTwist";
	setAttr -k on ".toesTwist";
	setAttr -k on ".frontTwist";
	setAttr -k on ".toeWiggle";
createNode unitConversion -n "unitConversion11";
	rename -uid "3F0CF787-49BA-0FED-4F08-F494BBCD7817";
	setAttr ".cf" 0.017453292519943295;
createNode unitConversion -n "unitConversion16";
	rename -uid "DDB99187-465B-69B3-BD13-EE95F0442A31";
	setAttr ".cf" 0.017453292519943295;
createNode plusMinusAverage -n "plusMinusAverage5";
	rename -uid "38377C6C-4574-442D-E540-1AB522E82609";
	setAttr ".op" 2;
	setAttr -s 2 ".i1";
	setAttr -s 2 ".i1";
createNode composeMatrix -n "getPivotToesTM";
	rename -uid "B6FD57FF-46E5-A795-47FC-DDA6DBDC635A";
	setAttr ".oq" -type "double4" 0 -0.11839147176395705 0 0.99296699814926581 ;
createNode unitConversion -n "unitConversion8";
	rename -uid "E2C6C6C5-48D4-72E5-FB98-02821F1E085D";
	setAttr ".cf" 0.017453292519943295;
createNode composeMatrix -n "getPivotBackTM";
	rename -uid "224D8822-40B4-E770-6C07-B0985A577D97";
	setAttr ".oq" -type "double4" 0 -0.11839147176395705 0 0.99296699814926581 ;
createNode inverseMatrix -n "getPivotToesInvTM";
	rename -uid "57810908-498C-4C0D-75A8-B1A5402B6540";
	setAttr ".omat" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.82899355419008913 -0.29713815287223522 -1.3790788474221514 1;
createNode composeMatrix -n "getToesDryTM";
	rename -uid "93413B0F-4FA6-A477-1AD3-06B6FAD4834B";
createNode composeMatrix -n "getToesWiggleTMDry";
	rename -uid "506499C2-4FBD-477F-E153-C5BD42427425";
createNode network -n "outputs";
	rename -uid "8FB320A7-442C-8DA1-3AF1-6D814CA30203";
	addAttr -ci true -sn "outFoot" -ln "outFoot" -dt "matrix";
	addAttr -ci true -sn "outToes" -ln "outToes" -dt "matrix";
createNode composeMatrix -n "getPivotBackRawTM";
	rename -uid "0E0D69E9-4E3A-48C6-F025-309401E5261C";
createNode composeMatrix -n "composeMatrix8";
	rename -uid "0451F3F1-4E21-7FE8-2912-A5A84041D9A1";
createNode multMatrix -n "getToesOutTM";
	rename -uid "740A96A9-402C-3D9D-72E1-5E90232BC600";
	setAttr -s 3 ".i";
createNode multMatrix -n "applyBackPivot";
	rename -uid "772A1ABF-4DA9-C408-AEE9-13B66B8D294F";
	setAttr -s 3 ".i";
createNode condition -n "condition8";
	rename -uid "2F2C0B46-4AB1-FABF-5BCC-CEA449D740F6";
	setAttr ".op" 2;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode unitConversion -n "unitConversion5";
	rename -uid "A0FF4FF5-4B9D-0F48-35B3-3CA90AA67440";
	setAttr ".cf" 0.017453292519943295;
createNode multMatrix -n "applyToesPivot";
	rename -uid "3E2CB33C-4C1B-F745-CA0B-1A97F385D606";
	setAttr -s 3 ".i";
createNode inverseMatrix -n "inverseMatrix5";
	rename -uid "2516CAF2-4946-F186-7C63-4D88A56C133F";
	setAttr ".omat" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.78352837516254892 -2.816787425530265e-08 0.025401165290903471 1;
createNode unitConversion -n "unitConversion3";
	rename -uid "199D88E8-46CB-0DAC-D316-AC9B0DB781E2";
	setAttr ".cf" 0.017453292519943295;
createNode condition -n "condition11";
	rename -uid "AAFF6780-4311-B49E-C9E0-0CB96B30FDCD";
	setAttr ".op" 2;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode addDoubleLinear -n "addDoubleLinear1";
	rename -uid "D23284FA-4904-0D2E-3650-349FFEC32A88";
createNode unitConversion -n "unitConversion1";
	rename -uid "DE65295E-4965-9012-F200-59BF718A23C5";
	setAttr ".cf" 0.017453292519943295;
createNode condition -n "condition12";
	rename -uid "F9324709-4DEC-4A24-AC9B-79908012D5C7";
	setAttr ".op" 4;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode condition -n "condition9";
	rename -uid "9621A8A7-4AC2-C503-0DFB-B98CC29217B4";
	setAttr ".op" 2;
	setAttr ".cf" -type "float3" 0 1 1 ;
createNode inverseMatrix -n "getPivotHeelInvTM";
	rename -uid "BD6F2E0D-42A1-CFB0-3E32-CB942F490D67";
	setAttr ".omat" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.79765678953632768 -2.816787425530265e-08 -0.40690870036073234 1;
createNode addDoubleLinear -n "addDoubleLinear3";
	rename -uid "F4A1F01C-4A2E-8BC1-F240-D8851B894B1E";
createNode multMatrix -n "applyPivotToesFK";
	rename -uid "44637C82-4EBF-92E8-00B8-F9B8D2253A72";
	setAttr -s 3 ".i";
createNode multMatrix -n "getFootOutTM";
	rename -uid "73C55E0B-451B-6ADC-842A-0EA4102CADA6";
	setAttr -s 3 ".i";
createNode composeMatrix -n "getPivotBankOutDry";
	rename -uid "F62E8674-431F-150F-5318-E19FE94D63C6";
createNode condition -n "condition10";
	rename -uid "8438F832-4C90-45CC-CC18-50A098FE3DE7";
	setAttr ".op" 2;
createNode unitConversion -n "unitConversion4";
	rename -uid "88474D93-42D2-8EEC-72DD-57A9B08FB28B";
	setAttr ".cf" 0.017453292519943295;
createNode unitConversion -n "unitConversion17";
	rename -uid "AD0DC318-4BB6-EDCA-4038-3CAE6D64AEE0";
	setAttr ".cf" 0.017453292519943295;
createNode composeMatrix -n "getPivotHeelTM";
	rename -uid "AEA76B6F-4AF0-6C70-E938-EAB5076B11A0";
	setAttr ".oq" -type "double4" 0 -0.11839147176395705 0 0.99296699814926581 ;
createNode multMatrix -n "applyHeelPivot1";
	rename -uid "A3CE3714-4D7D-78F2-14C6-F98F2DDF92BB";
	setAttr -s 3 ".i";
createNode unitConversion -n "unitConversion6";
	rename -uid "B8786534-4F83-3770-90D3-9C8395E340E3";
	setAttr ".cf" 0.017453292519943295;
createNode composeMatrix -n "getFootHeelDryTM";
	rename -uid "AB44EA60-4E18-7A8B-113A-EEA703F8D6E8";
createNode composeMatrix -n "getPivotBankInTM";
	rename -uid "02FBD480-4D7C-C43F-58C9-C0B8F9772D54";
	setAttr ".oq" -type "double4" 0 -0.11839147176395705 0 0.99296699814926581 ;
createNode multMatrix -n "applyFrontPivot";
	rename -uid "9A257EED-410B-94F4-4746-2EBE150057AA";
	setAttr -s 3 ".i";
createNode addDoubleLinear -n "addDoubleLinear2";
	rename -uid "993B6357-4241-01C7-DD31-7FAE3D4EAC5D";
createNode unitConversion -n "unitConversion2";
	rename -uid "263E5145-4F52-E43A-236F-40B819063F6B";
	setAttr ".cf" 0.017453292519943295;
createNode composeMatrix -n "getToesEndDryTM";
	rename -uid "47A3C2CE-4CC3-C23B-327D-9FA203628BFD";
createNode inverseMatrix -n "getPivotBankInInvTM";
	rename -uid "9A68AE18-4CA7-6D74-2F3C-75ADD12FAE38";
	setAttr ".omat" -type "matrix" 1 0 0 0 0 1 0 0 5.5511151231257827e-17 0 1 0 -0.45487936708192633 -2.816787425530265e-08 -1.3913053333407088 1;
createNode multMatrix -n "applyBankInPivot";
	rename -uid "FE139A68-4329-3E19-1347-A0893BE7680B";
	setAttr -s 3 ".i";
createNode multMatrix -n "applyHeelBackOutInnFront";
	rename -uid "6D447188-4758-7DF1-5D72-3C8926673BEB";
	setAttr -s 5 ".i";
createNode multMatrix -n "applyBankOutPivot";
	rename -uid "5925F249-4097-3D71-CDED-E493A4CFB00F";
	setAttr -s 3 ".i";
createNode unitConversion -n "unitConversion7";
	rename -uid "81385D46-46D8-5F56-27D6-5DA1D97ABBE3";
	setAttr ".cf" 0.017453292519943295;
createNode composeMatrix -n "getPivotBankOutTM";
	rename -uid "389F59C4-456E-D935-0E08-21ACC49234F9";
	setAttr ".oq" -type "double4" 0 -0.11839147176395705 0 0.99296699814926581 ;
createNode inverseMatrix -n "getPivotBankOutInvTM";
	rename -uid "B315A68E-4FE4-5FC1-A11E-B4A9531EEA21";
	setAttr ".omat" -type "matrix" 1 3.3087224502121107e-24 0 0 0 1 0 0 0 0 1 0 -1.2096162322242836 -2.8167874255302653e-08 -1.3666396510351597 1;
createNode composeMatrix -n "getPivotToesEndTM";
	rename -uid "6288B087-496B-FEE6-0676-52AF5B824A65";
	setAttr ".oq" -type "double4" 0 -0.11839147176395705 0 0.99296699814926581 ;
createNode inverseMatrix -n "getPivotToesEndInvTM";
	rename -uid "E4352E9D-4FAE-3D1B-C936-2F9EA8B2DA9E";
	setAttr ".omat" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -0.86180174431862067 -2.816787425530265e-08 -2.3696553286436663 1;
connectAttr "inputs.toeWiggle" "unitConversion11.i";
connectAttr "inputs.toesTwist" "unitConversion16.i";
connectAttr "inputs.rollAuto" "plusMinusAverage5.i1[0]";
connectAttr "inputs.rollAutoThreshold" "plusMinusAverage5.i1[1]";
connectAttr "inputs.pivotToes" "getPivotToesTM.it";
connectAttr "inputs.backTwist" "unitConversion8.i";
connectAttr "inputs.pivotBack" "getPivotBackTM.it";
connectAttr "inputs.footYaw" "getPivotBackTM.iry";
connectAttr "getPivotToesTM.omat" "getPivotToesInvTM.imat";
connectAttr "unitConversion1.o" "getToesDryTM.irx";
connectAttr "unitConversion16.o" "getToesDryTM.iry";
connectAttr "unitConversion11.o" "getToesWiggleTMDry.irx";
connectAttr "getFootOutTM.o" "outputs.outFoot";
connectAttr "getToesOutTM.o" "outputs.outToes";
connectAttr "unitConversion3.o" "getPivotBackRawTM.irx";
connectAttr "unitConversion8.o" "getPivotBackRawTM.iry";
connectAttr "unitConversion4.o" "composeMatrix8.irz";
connectAttr "inputs.bintToesTM" "getToesOutTM.i[0]";
connectAttr "applyPivotToesFK.o" "getToesOutTM.i[1]";
connectAttr "applyHeelBackOutInnFront.o" "getToesOutTM.i[4]";
connectAttr "inverseMatrix5.omat" "applyBackPivot.i[0]";
connectAttr "getPivotBackRawTM.omat" "applyBackPivot.i[1]";
connectAttr "getPivotBackTM.omat" "applyBackPivot.i[2]";
connectAttr "inputs.rollAuto" "condition8.ctr";
connectAttr "inputs.rollAuto" "condition8.ft";
connectAttr "condition12.ocr" "unitConversion5.i";
connectAttr "getPivotToesInvTM.omat" "applyToesPivot.i[0]";
connectAttr "getToesDryTM.omat" "applyToesPivot.i[1]";
connectAttr "getPivotToesTM.omat" "applyToesPivot.i[2]";
connectAttr "getPivotBackTM.omat" "inverseMatrix5.imat";
connectAttr "addDoubleLinear3.o" "unitConversion3.i";
connectAttr "inputs.bank" "condition11.ctr";
connectAttr "inputs.bank" "condition11.ft";
connectAttr "inputs.rollAnkle" "addDoubleLinear1.i2";
connectAttr "condition8.ocr" "addDoubleLinear1.i1";
connectAttr "addDoubleLinear1.o" "unitConversion1.i";
connectAttr "inputs.bank" "condition12.ctr";
connectAttr "inputs.bank" "condition12.ft";
connectAttr "inputs.rollAutoThreshold" "condition9.st";
connectAttr "plusMinusAverage5.o1" "condition9.ctr";
connectAttr "inputs.rollAuto" "condition9.ft";
connectAttr "getPivotHeelTM.omat" "getPivotHeelInvTM.imat";
connectAttr "inputs.rollBack" "addDoubleLinear3.i2";
connectAttr "condition10.ocr" "addDoubleLinear3.i1";
connectAttr "getPivotToesInvTM.omat" "applyPivotToesFK.i[0]";
connectAttr "getToesWiggleTMDry.omat" "applyPivotToesFK.i[1]";
connectAttr "getPivotToesTM.omat" "applyPivotToesFK.i[2]";
connectAttr "inputs.bindFootTM" "getFootOutTM.i[0]";
connectAttr "applyToesPivot.o" "getFootOutTM.i[4]";
connectAttr "applyHeelBackOutInnFront.o" "getFootOutTM.i[10]";
connectAttr "unitConversion5.o" "getPivotBankOutDry.irz";
connectAttr "inputs.rollAuto" "condition10.cfr";
connectAttr "inputs.rollAuto" "condition10.ft";
connectAttr "condition11.ocr" "unitConversion4.i";
connectAttr "inputs.heelSpin" "unitConversion17.i";
connectAttr "inputs.pivotHeel" "getPivotHeelTM.it";
connectAttr "getPivotHeelInvTM.omat" "applyHeelPivot1.i[1]";
connectAttr "getFootHeelDryTM.omat" "applyHeelPivot1.i[2]";
connectAttr "getPivotHeelTM.omat" "applyHeelPivot1.i[3]";
connectAttr "inputs.footTwist" "unitConversion6.i";
connectAttr "unitConversion6.o" "getFootHeelDryTM.iry";
connectAttr "unitConversion17.o" "getFootHeelDryTM.irz";
connectAttr "inputs.pivotBankIn" "getPivotBankInTM.it";
connectAttr "inputs.footYaw" "getPivotBankInTM.iry";
connectAttr "getPivotToesEndInvTM.omat" "applyFrontPivot.i[0]";
connectAttr "getToesEndDryTM.omat" "applyFrontPivot.i[1]";
connectAttr "getPivotToesEndTM.omat" "applyFrontPivot.i[2]";
connectAttr "inputs.rollFront" "addDoubleLinear2.i2";
connectAttr "condition9.ocr" "addDoubleLinear2.i1";
connectAttr "addDoubleLinear2.o" "unitConversion2.i";
connectAttr "unitConversion2.o" "getToesEndDryTM.irx";
connectAttr "unitConversion7.o" "getToesEndDryTM.iry";
connectAttr "getPivotBankInTM.omat" "getPivotBankInInvTM.imat";
connectAttr "getPivotBankInInvTM.omat" "applyBankInPivot.i[0]";
connectAttr "composeMatrix8.omat" "applyBankInPivot.i[1]";
connectAttr "getPivotBankInTM.omat" "applyBankInPivot.i[2]";
connectAttr "applyHeelPivot1.o" "applyHeelBackOutInnFront.i[0]";
connectAttr "applyBackPivot.o" "applyHeelBackOutInnFront.i[3]";
connectAttr "applyBankOutPivot.o" "applyHeelBackOutInnFront.i[6]";
connectAttr "applyBankInPivot.o" "applyHeelBackOutInnFront.i[9]";
connectAttr "applyFrontPivot.o" "applyHeelBackOutInnFront.i[13]";
connectAttr "getPivotBankOutInvTM.omat" "applyBankOutPivot.i[0]";
connectAttr "getPivotBankOutDry.omat" "applyBankOutPivot.i[1]";
connectAttr "getPivotBankOutTM.omat" "applyBankOutPivot.i[2]";
connectAttr "inputs.frontTwist" "unitConversion7.i";
connectAttr "inputs.pivotBankOut" "getPivotBankOutTM.it";
connectAttr "inputs.footYaw" "getPivotBankOutTM.iry";
connectAttr "getPivotBankOutTM.omat" "getPivotBankOutInvTM.imat";
connectAttr "inputs.pivotToesEnd" "getPivotToesEndTM.it";
connectAttr "inputs.footYaw" "getPivotToesEndTM.iry";
connectAttr "getPivotToesEndTM.omat" "getPivotToesEndInvTM.imat";
connectAttr "getFootOutTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getPivotToesInvTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getPivotToesEndInvTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "inverseMatrix5.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getPivotBankInInvTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getPivotBankOutInvTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyHeelBackOutInnFront.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getToesOutTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyToesPivot.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyFrontPivot.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyHeelPivot1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyBackPivot.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyBankOutPivot.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyBankInPivot.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "getPivotHeelInvTM.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "applyPivotToesFK.msg" ":defaultRenderUtilityList1.u" -na;
// End of omtk.FootRoll_v3.ma