import sys, argparse, re, csv
import os

regDict = {
      'FCC'      : '1',
      'MKK'      : '4',
      'ETSI'     : '3',
      'SD_NO_CTL': 'E',
      'NO_CTL'   : 'F',
      'None'     : '0',
    }
	
#---------- CSV file mapping ------------------------------------------------------------------------------------------------------	
PwrTableOffsets2GCsv = [54,131,208,286,363,440]
PwrTableOffsets5GCsv = [70,147,224,302,379,456]
PwrTableOffsets6GCsv = [106,183,260,338,415,492]
PwrTableOffsets5G160Csv = [100,177,254,332,409,486]

Modes = ["2G_SARLimitsCck","2G_SARLimitsHT20","2G_SARLimitsHT40","5G_SARLimitsHT20","5G_SARLimitsHT40","5G_SARLimitsHT80"]
#-----------------------------------------------------------------------------------------------------------------------------------
def setSARConfigValues(BdfFileStr, SARPwrStr):

	#--------Set SAR Version-------------------------------
	sarVer = re.findall("SARVersion,(\w+)", SARPwrStr)
	if sarVer[0] not in ['0','1','2','00','01','02']:
		print ("Invalid SARVersion value "+ sarVer[0])
		sys.exit()
	else:
		strTemp = re.findall("uint8	SAR_TABLES.SARVersion.*", BdfFileStr)
		versionStr = strTemp[0].split(' ')[0];
		op = re.sub(strTemp[0], versionStr+' '+sarVer[0], BdfFileStr)
			
	#--------Set SAR Flags-------------------------------	
	sarFlags = re.findall("SARFlags,(\w+)", SARPwrStr)
	if sarFlags[0] not in ['0','00','1','01']:
		print ("Invalid SARFlags value")
		sys.exit()
	else : 
		strTemp = re.findall("uint8	SAR_TABLES.SARFlags.*", BdfFileStr)
		flagStr = strTemp[0].split(' ')[0];
	op = re.sub(strTemp[0],flagStr+' '+sarFlags[0],op)
	
	#--------Set SAR BW_RU Map-------------------------------	
	SAR_BW_RU_Config = re.findall("SAR_BW_RU_Config_L,(\w+)", SARPwrStr)
	strTemp = re.findall("uint32	SAR_TABLES.SAR_BW_RU_Config_L.*", BdfFileStr)
	flagStr = strTemp[0].split(' ')[0];
	op = re.sub(strTemp[0],flagStr+' '+SAR_BW_RU_Config[0],op)
	
	SAR_BW_RU_Config = re.findall("SAR_BW_RU_Config_U,(\w+)", SARPwrStr)
	strTemp = re.findall("uint32	SAR_TABLES.SAR_BW_RU_Config_U.*", BdfFileStr)
	flagStr = strTemp[0].split(' ')[0];
	op = re.sub(strTemp[0],flagStr+' '+SAR_BW_RU_Config[0],op)
	
	strTemp = re.findall("uint8	SAR_TABLES.SAR_BW_RU_Mapping\[.*", BdfFileStr)
	for x in range(0,36):
		SAR_BW_RU_Config = re.findall("SAR_BW_RU_Mapping_"+str(x)+",(\w+)", SARPwrStr)
		flagStr = strTemp[x].split(' ')[0];
		mapStr = "uint8	SAR_TABLES.SAR_BW_RU_Mapping\["+str(x)+"].*"
		op = re.sub(mapStr,flagStr+' '+SAR_BW_RU_Config[0],op)

	#--------Set SAR Channels-------------------------------	
	Channels2G = re.findall("SAR2GChannels \(\w+\),(\w+),(\w+),(\w+),(\w+)", SARPwrStr)
	Channels2GBdf = [3000,3000,3000,3000]
	Channels2GBdfStr = "uint16	SAR_TABLES.SAR2GChannels.*"
	Channels2GBdfStr = re.findall(Channels2GBdfStr, op)
	Channels2GBdfStr = Channels2GBdfStr[0].split('[')[0]
	for x in range (len(Channels2G[0])):
		if Channels2G[0][x] != '0': #test this condition 
			Channels2GBdf[x] = int(Channels2G[0][x])
			op = re.sub(Channels2GBdfStr+"\["+str(x)+"].*",Channels2GBdfStr+"["+str(x)+"]	 "+str(Channels2GBdf[x]),op)

	Channels5G = re.findall("SAR5GChannels \(\w+\),(\w+),(\w+),(\w+),(\w+),(\w+),(\w+),(\w+),(\w+),(\w+),(\w+)", SARPwrStr)
	Channels5GBdf = [5930,5930,5930,5930,5930,5930,5930,5930,5930,5930]
	Channels5GBdfStr = "uint16	SAR_TABLES.SAR5GChannels.*"
	Channels5GBdfStr = re.findall(Channels5GBdfStr, op)
	Channels5GBdfStr = Channels5GBdfStr[0].split('[')[0]
	for x in range (len(Channels5G[0])):
		if Channels5G[0][x] != '0':
			Channels5GBdf[x] = int(Channels5G[0][x])
			op = re.sub(Channels5GBdfStr+"\["+str(x)+"].*",Channels5GBdfStr+"["+str(x)+"]	 "+str(Channels5GBdf[x]),op)

	Channels5G160 = re.findall("SAR5G160Channels \(\w+\),(\w+),(\w+)", SARPwrStr)
	Channels5GBdf160 = [5930,5930]
	Channels5GBdfStr160 = "uint16	SAR_TABLES.SAR5G160Channels.*"
	Channels5GBdfStr160 = re.findall(Channels5GBdfStr160, op)
	Channels5GBdfStr160 = Channels5GBdfStr160[0].split('[')[0]
	for x in range (len(Channels5G160[0])):
		if Channels5G160[0][x] != '0':
			Channels5GBdf160[x] = int(Channels5G160[0][x])
			op = re.sub(Channels5GBdfStr160+"\["+str(x)+"].*",Channels5GBdfStr160+"["+str(x)+"]	 "+str(Channels5GBdf160[x]),op)

	Channels6G = re.findall("SAR6GChannels \(\w+\),(\w+),(\w+),(\w+),(\w+),(\w+)", SARPwrStr)
	Channels6GBdf = [7115,7115,7115,7115,7115]
	Channels6GBdfStr = "uint16	SAR_TABLES_6G.SAR6GChannels.*"
	Channels6GBdfStr = re.findall(Channels6GBdfStr, op)
	Channels6GBdfStr = Channels6GBdfStr[0].split('[')[0]
	for x in range (len(Channels6G[0])):
		if Channels6G[0][x] != '0':
			Channels6GBdf[x] = int(Channels6G[0][x])
			op = re.sub(Channels6GBdfStr+"\["+str(x)+"].*",Channels6GBdfStr+"["+str(x)+"]	 "+str(Channels6GBdf[x]),op)
			
	#--------Set SAR CTL List-------------------------------
	CtlList = re.findall("SARCtlList,(\w+),(\w+),(\w+),(\w+),(\w+),(\w+)", SARPwrStr)
	ChannelsCtlBdfStr = "uint8	SAR_TABLES.SARCtlList.*"
	ChannelsCtlBdfStr = re.findall(ChannelsCtlBdfStr, op)
	ChannelsCtlBdfStr = ChannelsCtlBdfStr[0].split('[')[0]
	CtlListBdf = ['1','4','3','0','0','0']
	for x in range(len(CtlList[0])):
		CtlListBdf[x] = regDict[CtlList[0][x]] 
		op = re.sub(ChannelsCtlBdfStr+"\["+str(x)+"].*",ChannelsCtlBdfStr+"["+str(x)+"]	 "+str(CtlListBdf[x]),op)
	
	return op

def setSARPwrValues(op, SARPwrStr):
	print ("Generating BDF ...")
	for ctl in range(0,6):
		for sarSet in range(0,6):
			PwrStr2G = "int8	SAR_TABLES.SARPwrLimits2G\["+str(ctl)+"]\["+str(sarSet)+"].*"
			#PwrStr2G = "int8\tSAR_TABLES.SARPwrLimits2G\[.*"
			PwrArr2G = re.findall(PwrStr2G, op)
			for values in range(len(PwrArr2G)):					
				bdfPower = listVal[PwrTableOffsets2GCsv[ctl]+(values/4)][(sarSet*6)+2+(values%4)]
				bdfPower = float(bdfPower)*4.0
				newstr = PwrArr2G[values].split(" ")[0]+" "+str(int(bdfPower))
				op = op.replace(PwrArr2G[values], newstr)		
				
			PwrStr5G = "int8	SAR_TABLES.SARPwrLimits5G\["+str(ctl)+"]\["+str(sarSet)+"].*"
			PwrArr5G = re.findall(PwrStr5G, op)
			for values in range(len(PwrArr5G)):			
				bdfPower = listVal[PwrTableOffsets5GCsv[ctl]+(values/4)][(sarSet*6)+2+(values%4)]
				bdfPower = float(bdfPower)*4.0
				newstr = PwrArr5G[values].split(" ")[0]+" "+str(int(bdfPower))
				op = op.replace(PwrArr5G[values], newstr)

			PwrStr5G160 = "int8	SAR_TABLES.SARPwrLimits5G160\["+str(ctl)+"]\["+str(sarSet)+"].*"
			PwrArr5G160 = re.findall(PwrStr5G160, op)
			for values in range(len(PwrArr5G160)):		
				bdfPower = listVal[PwrTableOffsets5G160Csv[ctl]+(values/4)][(sarSet*6)+2+(values%4)]
				bdfPower = float(bdfPower)*4.0
				newstr = PwrArr5G160[values].split(" ")[0]+" "+str(int(bdfPower))
				op = op.replace(PwrArr5G160[values], newstr)
			
			PwrStr6G = "int8	SAR_TABLES_6G.SARPwrLimits6G\["+str(ctl)+"]\["+str(sarSet)+"].*"
			PwrArr6G = re.findall(PwrStr6G, op)
			for values in range(len(PwrArr6G)):			
				bdfPower = listVal[PwrTableOffsets6GCsv[ctl]+(values/4)][(sarSet*6)+2+(values%4)]
				bdfPower = float(bdfPower)*4.0
				newstr = PwrArr6G[values].split(" ")[0]+" "+str(int(bdfPower))
				op = op.replace(PwrArr6G[values], newstr)

	return op
	

#-----------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	cmdParser = argparse.ArgumentParser(description="CSV to BDF text conversion tool for SAR powers")
	cmdParser.add_argument('-csv', action="store", dest="CsvFilePath", default="sarBDFTool.csv", help="CSV file name")
	cmdParser.add_argument('-bdf', action="store", dest="BdfFilePath", default="bdwlan.txt", help="BDF txt file name")
	args = cmdParser.parse_args()
	SARPwrFile = open(args.CsvFilePath,'r')
	if SARPwrFile == None:
		print ("No input file %s found" % (args.CsvFilePath))
	else:
		SARPwrStr = SARPwrFile.read()
	
	newBDFFilePath = open(args.BdfFilePath,'r') #handle errono 2
	if newBDFFilePath == None:
		print ("No input file %s found" % (args.BdfFilePath))
	else:
		BdfFileStr = newBDFFilePath.read()
	
	if os.path.exists("getSarPwr_helium_temp.csv"):
		os.remove("getSarPwr_helium_temp.csv")
	temp_file = open("getSarPwr_helium_temp.csv",'wb')
	writeCsv = csv.writer(temp_file)

	with open (args.CsvFilePath,"rb") as f:
		readCsv = csv.reader(f)
		listVal = list(readCsv)
		copy_listVal = listVal
	
	for x in range(len(listVal)):
		for y in range(len(listVal[x])):
			listVal[x][y] = listVal[x][y].strip()
		writeCsv.writerow(listVal[x])
	temp_file.close()
	
	temp_file = open("getSarPwr_helium_temp.csv",'r')
	
	SARPwrStr = temp_file.read()	
	
	op = setSARConfigValues(BdfFileStr, SARPwrStr)
	
	op = setSARPwrValues(op, copy_listVal)

	i = 0
	while os.path.exists("setSarPwr_helium_op%s.txt" % i):
		i += 1
	output = open("setSarPwr_helium_op%s.txt" % i,'w+')
	output.write(op)
	
	temp_file.close()
	if os.path.exists("getSarPwr_helium_temp.csv"):
		os.remove("getSarPwr_helium_temp.csv")



	
